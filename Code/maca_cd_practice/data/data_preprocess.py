''' HFUT SPY @2025
Standard / cold / zeroshot / colditem splits, adapted for FoundationalASSIST from MACA-CD/SLP/data/data_preprocess.py.
Run from this directory after `python concept_main.py --stage preprocess`:
    python data_preprocess.py
Practice version: each split also stores Q_joint, the joint Q-matrix (exercise -> {concept id: six
practice weights that sum to 1}). A one-skill problem's concept gets the problem's zero-shot scores
(mathematical_practice); each skill of a multi-skill problem gets its own scores (concept_practice,
Code/augment_practice_per_concept.py). Scores below practice_cutoff (../parameter.json) are set to 0, then each
vector is divided by its sum.
The splits are written to preprocessed/ and are the same as maca_cd's.
Problems can have several skills, so Q_matrix maps each exercise to a list of concept ids.
The student, exercise and concept counts are written into ../parameter.json.
'''
import json,os,pickle
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
PREPROCESSED_DIR = "preprocessed"

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

# Practice version: the joint Q-matrix Q_joint maps each exercise to {concept id: six practice weights},
# in the order of PRACTICE_NAMES in Code/augment_mathematical_practice.py. A one-skill problem's concept
# gets the problem's zero-shot scores (mathematical_practice); each skill of a multi-skill problem gets its
# own scores (concept_practice, written by Code/augment_practice_per_concept.py). Scores below
# practice_cutoff (../parameter.json) are set to 0 first, so incidental practices drop out; when no score
# reaches the cutoff, the highest-scored practice(s) are kept. Every vector is then divided by its sum, so
# each involved concept's weights sum to 1 and summing over practices gives back the concept Q-matrix.
# An all-zero vector falls back to the problem's scores, then to a one-hot of predicted_practice.
PRACTICE_NAMES = ["Representing", "Abstracting and Generalizing", "Justifying and Proving",
                  "Mathematical Modeling", "Collaborative Mathematics", "Procedural Fluency"]
problems = pd.read_csv("../../../Data/Problems.csv", dtype=str, keep_default_na=False)
for column in ("mathematical_practice", "concept_practice", "predicted_practice"):
    if column not in problems.columns:
        raise RuntimeError("Data/Problems.csv has no {} column; run Code/augment_mathematical_practice.py and "
                           "Code/augment_practice_per_concept.py first".format(column))
problems["problem_id"] = problems["problem_id"].str.strip()
problems = problems.drop_duplicates("problem_id")
practice_scores = dict()
for problem_id, scores in zip(problems["problem_id"], problems["mathematical_practice"]):
    if scores.strip():
        scores = [float(score) for score in json.loads(scores)]
        assert len(scores) == len(PRACTICE_NAMES), "problem {} has {} practice scores".format(problem_id, len(scores))
        practice_scores[problem_id] = scores
missing = sorted({str(problem_id).strip() for problem_id in all_data['problem_id']} - set(practice_scores))
if missing:
    raise RuntimeError("{} problems have no mathematical_practice scores in Data/Problems.csv; run "
                       "augment_mathematical_practice.py first. Examples: {}".format(len(missing), missing[:5]))
concept_scores = dict(zip(problems["problem_id"], problems["concept_practice"]))
predicted = dict(zip(problems["problem_id"], problems["predicted_practice"]))


PRACTICE_CUTOFF = parameter.get("practice_cutoff", 0.0)


def practice_weights(scores):
    """Scores below PRACTICE_CUTOFF set to 0 (when none reaches it, the highest-scored practice(s) are kept),
    then divided by their sum. None for an all-zero vector."""
    kept = [score if score >= PRACTICE_CUTOFF else 0.0 for score in scores]
    if sum(kept) == 0 and max(scores) > 0:
        top = max(scores)
        kept = [score if score == top else 0.0 for score in scores]
        counts["kept only the highest score (none reaches the cutoff)"] += 1
    total = sum(kept)
    return [score / total for score in kept] if total > 0 else None


Q_joint = dict()
counts = {"one skill": 0, "several skills": 0, "fallback to problem scores": 0, "fallback to predicted_practice": 0,
          "kept only the highest score (none reaches the cutoff)": 0}
missing_skills = set()
for qid, problem_id, codes in zip(all_data['question_id'], all_data['problem_id'], all_data['concept_codes']):
    exercise = q_mapping[qid]
    if exercise in Q_joint:
        continue
    problem_id = str(problem_id).strip()
    codes = codes.split("|")

    item_weights = practice_weights(practice_scores[problem_id])
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
            weights = practice_weights([float(score) for score in per_skill[code.strip()]])
            if weights is None:
                weights = item_weights
                counts["fallback to problem scores"] += 1
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
print("Q_joint for {} exercises (practice_cutoff {}): {}".format(
    len(Q_joint), PRACTICE_CUTOFF, ", ".join("{} {}".format(n, name) for name, n in counts.items())))

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
    "practice_names": PRACTICE_NAMES,
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
    "practice_names": PRACTICE_NAMES,
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
    "practice_names": PRACTICE_NAMES,
    "Q_joint": Q_joint,
    "test": test_set_newc,
    "zeroshot_concepts": sorted(selected_numbers)
}
with open(os.path.join(PREPROCESSED_DIR, "zeroshot_spilt.pkl"), "wb") as f:
    pickle.dump(newc_spilt, f)

# split 4: cold-start items. 20% of the exercises are held out: all their responses are test responses,
# so the model has never seen these items in training. (After the other splits, which stay unchanged.)
train_set_colditem, test_set_colditem = [], []
exercise_ids = sorted(new_Q_matrix)
held_out_items = set(random.sample(exercise_ids, int(0.2 * len(exercise_ids))))
for record in all_sets:
    if record[1] in held_out_items:
        test_set_colditem.append(record)
    else:
        train_set_colditem.append(record)

print("training length whole: " + str(len(train_set_colditem)))
print("testing length whole: " + str(len(test_set_colditem)))

colditem_spilt = {
    "train": train_set_colditem,
    "Q_matrix": new_Q_matrix,
    "practice_names": PRACTICE_NAMES,
    "Q_joint": Q_joint,
    "test": test_set_colditem,
    "colditem_exercises": sorted(held_out_items)
}
with open(os.path.join(PREPROCESSED_DIR, "colditem_spilt.pkl"), "wb") as f:
    pickle.dump(colditem_spilt, f)

# counts for model/train.py
parameter["student_num"] = len(user_ids)
parameter["exercise_num"] = len(question_ids)
parameter["concept_num"] = len(conceptname2id)
with open(PARAMETER_FILE, "w") as f:
    json.dump(parameter, f, indent=4)
print("Wrote student_num={}, exercise_num={}, concept_num={} to {}".format(
    parameter["student_num"], parameter["exercise_num"], parameter["concept_num"], PARAMETER_FILE))
