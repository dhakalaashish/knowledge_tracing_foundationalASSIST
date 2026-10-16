''' HFUT SPY @2025
Standard / cold / zeroshot splits, adapted for FoundationalASSIST from MACA-CD/SLP/data/data_preprocess.py.
Run from this directory after `python concept_main.py --stage preprocess`:
    python data_preprocess.py [--practice_q practice_probabilities|practice_one_hot|practice_per_concept]
Practice version: each split also stores Q_practice (exercise -> six practice values), from the column
chosen by practice_q (default: "practice_q" in ../parameter.json):
    practice_probabilities: the zero-shot scores in mathematical_practice
    practice_one_hot:       the 0/1 marks in practice_multi_hot (Code/add_practice_multi_hot.py)
    practice_per_concept:   Q_joint (exercise -> {concept id: six weights that sum to 1}) instead of
                            the outer product of the concept Q-matrix and Q_practice. One-skill
                            problems use mathematical_practice, multi-skill problems the per-skill
                            scores in concept_practice (Code/augment_practice_per_concept.py); each
                            vector is divided by its sum.
The splits are written to preprocessed/<practice_q>/; they are the same for every setting, only
Q_practice (and Q_joint) differs.
Problems can have several skills, so Q_matrix maps each exercise to a list of concept ids.
The student, exercise and concept counts are written into ../parameter.json.
'''
import json,os,pickle
import argparse
import pandas as pd
from tqdm import tqdm
import random
from collections import defaultdict
import numpy as np
from sklearn.model_selection import train_test_split

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DATA_DIR)
PARAMETER_FILE = "../parameter.json"
with open(PARAMETER_FILE, "r") as f:
    parameter = json.load(f)
random.seed(parameter.get("seed", 2025))

# Practice version: which Problems.csv column fills Q_practice
PRACTICE_Q_COLUMNS = {"practice_probabilities": "mathematical_practice", "practice_one_hot": "practice_multi_hot",
                      "practice_per_concept": "mathematical_practice"}
arg_parser = argparse.ArgumentParser(description="Standard / cold / zeroshot splits")
arg_parser.add_argument("--practice_q", default=parameter.get("practice_q", "practice_probabilities"),
                        choices=sorted(PRACTICE_Q_COLUMNS), help="source of Q_practice")
practice_q = arg_parser.parse_args().practice_q
PRACTICE_COLUMN = PRACTICE_Q_COLUMNS[practice_q]
PREPROCESSED_DIR = os.path.join("preprocessed", practice_q)
print("practice_q: {} (Problems.csv column {}), splits written to {}".format(practice_q, PRACTICE_COLUMN, PREPROCESSED_DIR))

filename = "./cleaned_data.csv"
all_data = pd.read_csv(filename, dtype={"concept_codes": str})


CONCEPT_DATA_FILE = "./graph/concept_data.json"
with open(CONCEPT_DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)
    conceptname2id = data["concept_dict"]
    code2id = data["code2id"]

qid2cid = dict()
concept_ids = set()
for qid, codes in zip(all_data['question_id'], all_data['concept_codes']):
    if qid in qid2cid:
        continue
    cids = sorted(code2id[code] for code in codes.split("|"))
    qid2cid[qid] = cids
    concept_ids.update(cids)

user_ids = all_data['student_id'].unique()
user_mapping = {id: i for i, id in enumerate(user_ids)}
all_data['new_Sid'] = all_data['student_id'].map(user_mapping)

question_ids = all_data['question_id'].unique()
q_mapping = {id: i for i, id in enumerate(question_ids)}
all_data['new_Qid'] = all_data['question_id'].map(q_mapping)

print("exercise number is: ")
print(len(question_ids))
print("student number is: ")
print(len(user_ids))
print("concept number is: ")
print(len(concept_ids))
assert concept_ids == set(range(1, len(conceptname2id) + 1)), "concept ids must be 1..N"

# Practice version: Q_practice maps each exercise to its six practice values from PRACTICE_COLUMN
# of Data/Problems.csv: the zero-shot scores (mathematical_practice, written by
# Code/augment_mathematical_practice.py) or their 0/1 marks (practice_multi_hot), both in the order
# of PRACTICE_NAMES there.
PRACTICE_NAMES = ["Representing", "Abstracting and Generalizing", "Justifying and Proving",
                  "Mathematical Modeling", "Collaborative Mathematics", "Procedural Fluency"]
problems = pd.read_csv("../../../Data/Problems.csv", dtype=str, keep_default_na=False)
if PRACTICE_COLUMN not in problems.columns:
    raise RuntimeError("Data/Problems.csv has no {} column; run Code/augment_mathematical_practice.py "
                       "(it also writes practice_multi_hot) or Code/add_practice_multi_hot.py first".format(PRACTICE_COLUMN))
problems["problem_id"] = problems["problem_id"].str.strip()
problems = problems.drop_duplicates("problem_id")
practice_scores = dict()
for problem_id, scores in zip(problems["problem_id"], problems[PRACTICE_COLUMN]):
    if scores.strip():
        scores = [float(score) for score in json.loads(scores)]
        assert len(scores) == len(PRACTICE_NAMES), "problem {} has {} practice scores".format(problem_id, len(scores))
        practice_scores[problem_id] = scores

Q_practice = dict()
missing = set()
for qid, problem_id in zip(all_data['question_id'], all_data['problem_id']):
    problem_id = str(problem_id).strip()
    if problem_id not in practice_scores:
        missing.add(problem_id)
        continue
    Q_practice[q_mapping[qid]] = practice_scores[problem_id]
if missing:
    raise RuntimeError("{} problems have no {} in Data/Problems.csv; run augment_mathematical_practice.py "
                       "first. Examples: {}".format(len(missing), PRACTICE_COLUMN, sorted(missing)[:5]))
print("{} for {} exercises".format(PRACTICE_COLUMN, len(Q_practice)))

# practice_per_concept: Q_joint maps each exercise to {concept id: six practice weights}. A one-skill
# problem's concept gets the item-level scores (mathematical_practice); each skill of a multi-skill
# problem gets its own scores (concept_practice, written by Code/augment_practice_per_concept.py).
# Every vector is divided by its sum, so each involved concept's weights sum to 1 and summing over
# practices gives back the concept Q-matrix. An all-zero vector falls back to the item-level scores,
# then to a one-hot of predicted_practice.
Q_joint = None
if practice_q == "practice_per_concept":
    for column in ("concept_practice", "predicted_practice"):
        if column not in problems.columns:
            raise RuntimeError("Data/Problems.csv has no {} column; run Code/augment_practice_per_concept.py "
                               "(and Code/augment_mathematical_practice.py) first".format(column))
    concept_scores = dict(zip(problems["problem_id"], problems["concept_practice"]))
    predicted = dict(zip(problems["problem_id"], problems["predicted_practice"]))

    def divide_by_sum(scores):
        total = sum(scores)
        return [score / total for score in scores] if total > 0 else None

    Q_joint = dict()
    counts = {"one skill": 0, "several skills": 0, "fallback to item scores": 0, "fallback to predicted_practice": 0}
    missing_skills = set()
    for qid, problem_id, codes in zip(all_data['question_id'], all_data['problem_id'], all_data['concept_codes']):
        exercise = q_mapping[qid]
        if exercise in Q_joint:
            continue
        problem_id = str(problem_id).strip()
        codes = codes.split("|")

        item_weights = divide_by_sum(practice_scores[problem_id])
        if item_weights is None:
            item_weights = [1.0 if name == predicted.get(problem_id, "").strip() else 0.0 for name in PRACTICE_NAMES]
            assert sum(item_weights) == 1, "problem {} has all-zero scores and no predicted_practice".format(problem_id)
            counts["fallback to predicted_practice"] += 1

        joint = dict()
        if len(codes) == 1:
            joint[code2id[codes[0]]] = item_weights
            counts["one skill"] += 1
        else:
            cell = concept_scores.get(problem_id, "")
            per_skill = {code.strip(): scores for code, scores in json.loads(cell).items()} if cell.strip() else {}
            for code in codes:
                if code.strip() not in per_skill:
                    missing_skills.add("{}:{}".format(problem_id, code))
                    continue
                weights = divide_by_sum([float(score) for score in per_skill[code.strip()]])
                if weights is None:
                    weights = item_weights
                    counts["fallback to item scores"] += 1
                joint[code2id[code]] = weights
            counts["several skills"] += 1
        Q_joint[exercise] = joint

        if not missing_skills:
            # Summing over practices must give back the concept Q-matrix (1 per involved concept)
            assert sorted(joint) == qid2cid[qid], "exercise {}: Q_joint concepts differ from Q_matrix".format(exercise)
            assert all(abs(sum(weights) - 1) < 1e-6 for weights in joint.values()), \
                "exercise {}: practice weights do not sum to 1".format(exercise)
    if missing_skills:
        raise RuntimeError("{} skills of multi-skill problems have no concept_practice scores; run "
                           "Code/augment_practice_per_concept.py first. Examples: {}".format(
                               len(missing_skills), sorted(missing_skills)[:5]))
    print("Q_joint for {} exercises: {}".format(len(Q_joint), ", ".join("{} {}".format(n, name) for name, n in counts.items())))


# split 1: standard
all_sets = []
all_set_dict = defaultdict(list)
all_stu_concepts = defaultdict(set)
new_Q_matrix = dict()
for row in tqdm(all_data.itertuples(index=False), total=len(all_data)):
    student = int(row.new_Sid)
    exercise = int(row.new_Qid)
    concepts = qid2cid[row.question_id]
    y = int(row.score) / int(row.full_score)
    if y == int(y):
        y = int(y)
        new_Q_matrix[exercise] = concepts
        # 4th field: first concept (the model reads all concepts from Q_matrix)
        all_sets.append([student, exercise, y, concepts[0]])
        all_set_dict[student].append([student, exercise, y, concepts[0]])
        all_stu_concepts[student].update(concepts)

random.shuffle(all_sets)
cut = int(0.8*len(all_sets))
train_set = all_sets[:cut]
test_set = all_sets[cut:]

print("training length whole: " + str(len(train_set)))
print("testing length whole: " + str(len(test_set)))

os.makedirs(PREPROCESSED_DIR, exist_ok=True)
standard_spilt = {
    "train": train_set,
    "test": test_set,
    "Q_matrix": new_Q_matrix,
    "Q_practice": Q_practice,
    "practice_names": PRACTICE_NAMES,
    "practice_q": practice_q,
    "Q_joint": Q_joint
}
with open(os.path.join(PREPROCESSED_DIR, "standard_spilt.pkl"), "wb") as f:
    pickle.dump(standard_spilt, f)

test_ratio = 0.8
# split 3: cold-start students
student_ids = list(all_set_dict.keys())
train_students_cold, test_students_cold = train_test_split(student_ids, test_size=0.5, random_state=43)
train_set_cold, test_set_cold = [], []

for student in train_students_cold:
    records = all_set_dict[student]
    train_set_cold.extend(records)

for student in test_students_cold:

    records = all_set_dict[student]
    random.shuffle(records)
    if len(records) > 5:
        train_set_cold.extend(records[:2])
        test_set_cold.extend(records[2:])
    else:
        train_set_cold.extend(records)

print("training length whole: " + str(len(train_set_cold)))
print("testing length whole: " + str(len(test_set_cold)))

cold_spilt = {
    "train": train_set_cold,
    "test": test_set_cold,
    "Q_matrix": new_Q_matrix,
    "Q_practice": Q_practice,
    "practice_names": PRACTICE_NAMES,
    "practice_q": practice_q,
    "Q_joint": Q_joint,
    "train_users": train_students_cold,
    "cold_users": test_students_cold
}
with open(os.path.join(PREPROCESSED_DIR, "cold_spilt.pkl"), "wb") as f:
    pickle.dump(cold_spilt, f)

# split 3: zero-shot concepts for the whole dataset
# A record is a test record when any concept of its exercise is held out, so no held-out
# concept is seen in training.
train_set_newc, test_set_newc = [], []
numbers = list(range(1, len(concept_ids)+1))
selected_count = int(0.2*len(numbers))
selected_numbers = set(random.sample(numbers, selected_count))

for student, her_concepts in all_stu_concepts.items():
    her_concepts = list(her_concepts)
    records = all_set_dict[student]
    for record in records:
        if any(concept in selected_numbers for concept in new_Q_matrix[record[1]]):
            test_set_newc.append(record)
        else:
            train_set_newc.append(record)

print("training length whole: " + str(len(train_set_newc)))
print("testing length whole: " + str(len(test_set_newc)))
train_concepts = {concept for record in train_set_newc for concept in new_Q_matrix[record[1]]}
assert not (train_concepts & selected_numbers), "a held-out concept appears in training"

newc_spilt = {
    "train": train_set_newc,
    "Q_matrix": new_Q_matrix,
    "Q_practice": Q_practice,
    "practice_names": PRACTICE_NAMES,
    "practice_q": practice_q,
    "Q_joint": Q_joint,
    "test": test_set_newc,
    "zeroshot_concepts": sorted(selected_numbers)
}
with open(os.path.join(PREPROCESSED_DIR, "zeroshot_spilt.pkl"), "wb") as f:
    pickle.dump(newc_spilt, f)

# counts for model/train.py
parameter["student_num"] = len(user_ids)
parameter["exercise_num"] = len(question_ids)
parameter["concept_num"] = len(conceptname2id)
with open(PARAMETER_FILE, "w") as f:
    json.dump(parameter, f, indent=4)
print("Wrote student_num={}, exercise_num={}, concept_num={} to {}".format(
    parameter["student_num"], parameter["exercise_num"], parameter["concept_num"], PARAMETER_FILE))
