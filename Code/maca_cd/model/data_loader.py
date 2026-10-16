import json
import torch
import math
import random
import pickle
import time
import pdb
import copy
import numpy as np
import networkx as nx
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data
from collections import defaultdict
from torch.autograd import Variable

def concept_list(concept_id):
    """Q_matrix values: a list of concept ids (FoundationalASSIST) or one id (MACA-CD datasets)."""
    return concept_id if isinstance(concept_id, (list, tuple)) else [concept_id]

def load_LLM_generation():
    DAG_path = '../data/graph/DAG_edges.json'
    ConceptEmbedding_path = '../data/concept_preknowledge/concept_meta_emb.json'

    CONCEPT_DATA_FILE = "../data/graph/concept_data.json"
    with open(CONCEPT_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        concept2id = data["concept_dict"]


    with open(DAG_path, 'r', encoding='utf-8') as f:
        DAG_edges = json.load(f)

    with open(ConceptEmbedding_path, 'r', encoding='utf-8') as f:
        concept_emb = json.load(f)

    concept_number = 0
    concept_emb_matrix = dict()
    for concept_name, emb in concept_emb.items():
        concept_name = concept_name.lower()
        concept_id = concept2id[concept_name]
        concept_emb_matrix[concept_id] = emb
        concept_number += 1

    missing = [name for name, concept_id in concept2id.items() if concept_id not in concept_emb_matrix]
    if missing:
        raise ValueError("{} concepts have no embedding (run data/concept_main.py --stage embed): {}".format(len(missing), missing[:5]))

    concept_embs = []
    for i in range(concept_number):
        concept_embs.append(concept_emb_matrix[i+1])

    concept_embs = np.array(concept_embs) * 10

    return DAG_edges["DAG"], concept_embs


def load_response_logs(split, student_n, exercise_n, knowledge_n, encoder_style = True):
    data_file = '../data/preprocessed/' + split + '_spilt.pkl'
    with open(data_file, "rb") as f:
        loaded_data = pickle.load(f)

    if split == "standard":
        train_set = loaded_data["train"]
        train_data = EduData(train_set)
        test_set = loaded_data["test"]
        test_data = EduData(test_set)

        all_set = train_set + test_set
        Q_dict = loaded_data["Q_matrix"]
        Q_matrix = np.zeros((exercise_n, knowledge_n))
        for i_id, concept_id in Q_dict.items():
            for c_id in concept_list(concept_id):  # multi-skill exercises: multi-hot row
                Q_matrix[i_id, c_id - 1] = 1

        response_matrix = np.zeros((student_n, exercise_n))
        concept_num_matrix = np.zeros(knowledge_n)
        for idx in range(len(train_set)):
            u_id = train_set[idx][0]
            i_id = train_set[idx][1]
            for c_id in concept_list(Q_dict[i_id]):
                concept_num_matrix[c_id - 1] += 1
            y_label = train_set[idx][2]
            if y_label == 1:
                response_matrix[u_id, i_id] = y_label
            else:
                response_matrix[u_id, i_id] = -1

        output = {"train": train_data, "test":test_data, "Q": Q_matrix, "R":response_matrix, "DOA_set": np.array(all_set), "train_set": train_set, "concept_num_matrix": concept_num_matrix}
        return output

    elif split == "cold":
        train_set = loaded_data["train"]
        train_data = EduData(train_set)
        test_set = loaded_data["test"]
        test_data = EduData(test_set)
        all_set = train_set + test_set
        train_users = loaded_data["train_users"]
        cold_users = loaded_data["cold_users"]

        Q_dict = loaded_data["Q_matrix"]
        Q_matrix = np.zeros((exercise_n, knowledge_n))
        for i_id, concept_id in Q_dict.items():
            for c_id in concept_list(concept_id):  # multi-skill exercises: multi-hot row
                Q_matrix[i_id, c_id - 1] = 1

        response_matrix = np.zeros((student_n, exercise_n))
        concept_num_matrix = np.zeros(knowledge_n)
        for idx in range(len(train_set)):
            u_id = train_set[idx][0]
            i_id = train_set[idx][1]
            for c_id in concept_list(Q_dict[i_id]):
                concept_num_matrix[c_id - 1] += 1
            y_label = train_set[idx][2]
            if y_label == 1:
                response_matrix[u_id, i_id] = y_label
            else:
                response_matrix[u_id, i_id] = -1
        output = {"train": train_data, "test": test_data, "Q": Q_matrix, "R": response_matrix, "DOA_set": np.array(all_set), "train_set": train_set, "concept_num_matrix": concept_num_matrix}
        return output

    elif split in ("zeroshot", "colditem"):
        train_set = loaded_data["train"]
        train_data = EduData(train_set)
        test_set = loaded_data["test"]
        test_data = EduData(test_set)
        all_set = train_set + test_set
        Q_dict = loaded_data["Q_matrix"]
        Q_matrix = np.zeros((exercise_n, knowledge_n))
        for i_id, concept_id in Q_dict.items():
            for c_id in concept_list(concept_id):  # multi-skill exercises: multi-hot row
                Q_matrix[i_id, c_id - 1] = 1

        response_matrix = np.zeros((student_n, exercise_n))
        concept_num_matrix = np.zeros(knowledge_n)
        for idx in range(len(train_set)):
            u_id = train_set[idx][0]
            i_id = train_set[idx][1]
            for c_id in concept_list(Q_dict[i_id]):
                concept_num_matrix[c_id - 1] += 1
            y_label = train_set[idx][2]
            if y_label == 1:
                response_matrix[u_id, i_id] = y_label
            else:
                response_matrix[u_id, i_id] = -1
        output = {"train": train_data, "test": test_data, "Q": Q_matrix, "R": response_matrix, "DOA_set": np.array(all_set), "train_set": train_set, "concept_num_matrix":concept_num_matrix}
        return output
    else:
        raise ValueError("Split should be one of cold/standard/zeroshot/colditem")


class EduData(data.Dataset):
    def __init__(self, data_set):
        super(EduData, self).__init__()
        self.data = np.array(data_set)

    def __len__(self):
        return  self.data.shape[0]

    def __getitem__(self, idx):
        u_id = self.data[idx][0]
        i_id = self.data[idx][1]
        y_label = self.data[idx][2]
        concept_id = self.data[idx][3]-1
        return u_id, i_id, concept_id, y_label

if __name__ == '__main__':
    DAG, emb = load_LLM_generation()
