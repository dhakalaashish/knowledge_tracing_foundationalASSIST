''' HFUT SPY @2025
Standard / cold / zeroshot splits, adapted for FoundationalASSIST from MACA-CD/SLP/data/data_preprocess.py.
Run from this directory after `python concept_main.py --stage preprocess`:
    python data_preprocess.py
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

os.makedirs("preprocessed", exist_ok=True)
standard_spilt = {
    "train": train_set,
    "test": test_set,
    "Q_matrix": new_Q_matrix
}
with open("preprocessed/standard_spilt.pkl", "wb") as f:
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
    "train_users": train_students_cold,
    "cold_users": test_students_cold
}
with open("preprocessed/cold_spilt.pkl", "wb") as f:
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
    "test": test_set_newc,
    "zeroshot_concepts": sorted(selected_numbers)
}
with open("preprocessed/zeroshot_spilt.pkl", "wb") as f:
    pickle.dump(newc_spilt, f)

# counts for model/train.py
parameter["student_num"] = len(user_ids)
parameter["exercise_num"] = len(question_ids)
parameter["concept_num"] = len(conceptname2id)
with open(PARAMETER_FILE, "w") as f:
    json.dump(parameter, f, indent=4)
print("Wrote student_num={}, exercise_num={}, concept_num={} to {}".format(
    parameter["student_num"], parameter["exercise_num"], parameter["concept_num"], PARAMETER_FILE))
