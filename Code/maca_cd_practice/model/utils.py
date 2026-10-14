import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import scipy.linalg as slin
import scipy.sparse as sp
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os
import glob
import re
import pickle
import math,pdb
from tqdm import tqdm
from joblib import Parallel, delayed
from collections import defaultdict

def normalized_matrix(matrix):
    row_sum = matrix.sum(dim=1, keepdim=True)
    row_sum[row_sum == 0] = 1

    col_sum = matrix.sum(dim=0, keepdim=True)
    col_sum[col_sum == 0] = 1

    return torch.sqrt(matrix / row_sum / col_sum)

def build_mlp(layer_dims, dropout=0.5):
    layers = []
    for i in range(len(layer_dims) - 1):
        layers.append(PosLinear(layer_dims[i], layer_dims[i + 1]))
        if i < len(layer_dims) - 2:
            layers.append(nn.Dropout(p=dropout))
            layers.append(nn.LeakyReLU(0.2))
        else:
            layers.append(nn.Sigmoid())
    return nn.Sequential(*layers)

class PosLinear(nn.Linear):
    def forward(self, input: torch.Tensor) -> torch.Tensor:
        weight = 2 * F.relu(1 * torch.neg(self.weight)) + self.weight
        return F.linear(input, weight, self.bias)

def sparse_graph_construction(concept_pairs, node_number, device):
    concept_graph_set = defaultdict(set)
    concept_D = defaultdict(int)
    for pairs in concept_pairs:
        concept_A, concept_B = pairs[0]-1, pairs[1]-1
        concept_graph_set[concept_A].add(concept_B)
        concept_D[concept_B] += 1

    parameters_diff_v = []
    parameters_diff_i = []
    for out,value in concept_graph_set.items():
        for in_ in value:
            parameters_diff_i.append([in_,out])
            tmp_V = 1.0 / (concept_D[in_] + 1.0)
            if tmp_V > 1:
                pdb.set_trace()
            parameters_diff_v.append(tmp_V)

    for i in range(node_number):
        parameters_diff_i.append([i, i])
        parameters_diff_v.append(1.0 / (concept_D[i] + 1.0))

    parameters_diff_i=torch.LongTensor(parameters_diff_i).to(device)
    parameters_diff_v=torch.FloatTensor(parameters_diff_v).to(device)
    # graph = torch.sparse_coo_tensor(parameters_diff_i.t(), parameters_diff_v,
    #                     (node_number, node_number))
    return parameters_diff_i, parameters_diff_v


def get_top_k_concepts(q, a, topk = 10):
    '''
    :param q:  Q-matrix question 0: 00010 
    :param a:  stu exer score # num of data * 3
    :return:
    '''
    skill_dict = {}
    for k in range(q.shape[1]): # exercise shape 0; concept shape 1
        skill_dict[k] = 0
    for k in range(a.shape[0]): # stu exer score, # num of data * 3
        stu_id = a[k, 0]
        prob_id = a[k, 1]
        skills = np.where(q[int(prob_id), :] != 0)[0].tolist() # exercise to concept id
        for skill in skills:
            skill_dict[skill] += 1

    sorted_dict = dict(sorted(skill_dict.items(), key=lambda x: x[1], reverse=True))
    all_list = list(sorted_dict.keys())  # top 10 concept
    return all_list[:topk]

def get_doa(q_matrix, r_records, mastery_level, r_matrix):
    # q_matrix = config['q'].detach().cpu().numpy()
    # r_matrix = config['r']

    check_concepts = get_top_k_concepts(q_matrix, r_records)

    doa_k_list = Parallel(n_jobs=-1)(
        delayed(calculate_doa_k_block)(mastery_level, q_matrix, r_matrix, k) for k in check_concepts)

    # doa_k_list = []
    # for k in check_concepts:
    #     doa = calculate_doa_k_block(mastery_level, q_matrix, r_matrix, k)
    #     doa_k_list.append(doa)
    # print(doa_k_list)
    return [np.mean(doa_k_list), np.mean(doa_k_list[:5]), doa_k_list[0]]

def calculate_doa_k_block(mas_level, q_matrix, r_matrix, k, block_size=50):
    n_students, n_skills = mas_level.shape
    n_questions, _ = q_matrix.shape
    n_attempts = r_matrix.shape[1]
    numerator = 0
    denominator = 0
    question_hask = np.where(q_matrix[:, k] != 0)[0].tolist()
    for start in range(0, n_students, block_size):
        end = min(start + block_size, n_students)
        # mas_level_block = mas_level[start:end, :]
        delta_matrix_block = mas_level[start:end, k].reshape(-1, 1) > mas_level[start:end, k].reshape(1, -1)
        # pdb.set_trace()
        r_matrix_block = r_matrix[start:end, :]
        for j in question_hask:
            # (r_matrix_block[:, j].reshape(1, -1) != 0) answered exercise j.
            row_vector = (r_matrix_block[:, j].reshape(1, -1) != 0).astype(int)
            columen_vector = (r_matrix_block[:, j].reshape(-1, 1) != 0).astype(int)
            mask = row_vector * columen_vector
            delta_r_matrix = r_matrix_block[:, j].reshape(-1, 1) > r_matrix_block[:, j].reshape(1, -1)
            I_matrix = r_matrix_block[:, j].reshape(-1, 1) != r_matrix_block[:, j].reshape(1, -1)
            numerator +=  np.sum(delta_matrix_block * mask * delta_r_matrix)
            denominator += np.sum(delta_matrix_block  * mask * I_matrix)

    if denominator == 0:
        DOA_k = 0
    else:
        DOA_k = numerator / denominator
    return DOA_k

def calculate_doa_k(mas_level, q_matrix, r_matrix, k):
    n_students, n_skills = mas_level.shape
    n_questions, _ = q_matrix.shape
    n_attempts = r_matrix.shape[1]
    DOA_k = 0.0
    numerator = 0
    denominator = 0
    delta_matrix = mas_level[:, k].reshape(-1, 1) > mas_level[:, k].reshape(1, -1)
    question_hask = np.where(q_matrix[:, k] != 0)[0].tolist()
    for j in question_hask:
        row_vector = (r_matrix[:, j].reshape(1, -1) != -1).astype(int)
        column_vector = (r_matrix[:, j].reshape(-1, 1) != -1).astype(int)
        mask = row_vector * column_vector
        delta_r_matrix = r_matrix[:, j].reshape(-1, 1) > r_matrix[:, j].reshape(1, -1)
        I_matrix = r_matrix[:, j].reshape(-1, 1) != r_matrix[:, j].reshape(1, -1)
        numerator_ = np.logical_and(mask, delta_r_matrix)
        denominator_ = np.logical_and(mask, I_matrix)
        numerator += np.sum(delta_matrix * numerator_)
        denominator += np.sum(delta_matrix * denominator_)

    if denominator != 0:
        DOA_k = numerator / denominator
        return DOA_k
    else:
        return 0

def doa_report(user, item, know_id, predicted_score, predicted_theta):
    '''

    :param user: 1 int
    :param item: 1 int
    :param know_id: [0,1,..., 1] 123*1
    :param predicted_score: 0.7 float
    :param predicted_theta: user on all concepts [0.9, 0.4, ..., ] 123*1
    :return:
    '''
    df = pd.DataFrame({
        "user_id": user,
        "item_id": item,
        "score": predicted_score,
        "theta": predicted_theta,
        "knowledge": know_id
    })

    knowledges = []
    knowledge_item = []
    knowledge_user = []
    knowledge_truth = []
    knowledge_theta = []
    for user, item, score, theta, knowledge in df[["user_id", "item_id", "score", "theta", "knowledge"]].values:
        # 遍历所有数据，转存数据为id信息
        if isinstance(theta, list):
            for i, (theta_i, knowledge_i) in enumerate(zip(theta, knowledge)):
                if knowledge_i == 1: # 如果这个知识点维度被采用，执行以下结果
                    knowledges.append(i)
                    knowledge_item.append(item)
                    knowledge_user.append(user)
                    knowledge_truth.append(score)
                    knowledge_theta.append(theta_i)
        else:  # pragma: no cover
            for i, knowledge_i in enumerate(knowledge):
                if knowledge_i == 1:
                    knowledges.append(i)
                    knowledge_item.append(item)
                    knowledge_user.append(user)
                    knowledge_truth.append(score)
                    knowledge_theta.append(theta)

    knowledge_df = pd.DataFrame({
        "knowledge": knowledges,
        "user_id": knowledge_user,
        "item_id": knowledge_item,
        "score": knowledge_truth,
        "theta": knowledge_theta
    })
    knowledge_ground_truth = []
    knowledge_prediction = []
    # 按照知识点区分所有样本
    for _, group_df in knowledge_df.groupby("knowledge"):
        _knowledge_ground_truth = []
        _knowledge_prediction = []
        # 每一个知识点对应着有若干个产品
        for _, item_group_df in group_df.groupby("item_id"):
            # 确定知识点，确定产品，可以把训练集和测试集涉及到这个产品的评分全部加入进去
            _knowledge_ground_truth.append(item_group_df["score"].values)
            # 确定知识点，确定产品，可以把训练集和测试集涉及到这个知识点的评分全部加入进去
            _knowledge_prediction.append(item_group_df["theta"].values)
        knowledge_ground_truth.append(_knowledge_ground_truth)
        knowledge_prediction.append(_knowledge_prediction)

    return doa_eval(knowledge_ground_truth, knowledge_prediction)


def doa_eval(y_true, y_pred):
    """
    >>> y_true = [[np.array([1, 0, 1])],[np.array([0, 1, 1])]]
    >>> y_pred = [[np.array([.5, .4, .6])],   [np.array([.2, .3, .5])]]
    >>> doa_eval(y_true, y_pred)['doa'] 1.0
    >>> y_pred = [[np.array([.4, .5, .6])],[np.array([.3, .2, .5])]]
    >>> doa_eval(y_true, y_pred)['doa'] 0.5
    """
    doa = []
    doa_support = 0
    z_support = 0
    niubi = []
    laji = []
    for knowledge_label, knowledge_pred in tqdm(zip(y_true, y_pred),
                                                "doa metrics"):
        _doa = 0
        _z = 0
        length = 0

        for label, pred in zip(knowledge_label, knowledge_pred):
            if sum(label) == len(label) or sum(label) == 0:
                continue
            pos_idx = []
            neg_idx = []
            for i, _label in enumerate(label):
                if _label == 1:
                    pos_idx.append(i)
                else:
                    neg_idx.append(i)
            pos_pred = pred[pos_idx]
            neg_pred = pred[neg_idx]
            invalid = 0
            for _pos_pred in pos_pred:
                _doa += len(neg_pred[neg_pred < _pos_pred])
                invalid += len(neg_pred[neg_pred == _pos_pred])
            _z += (len(pos_pred) * len(neg_pred)) #- invalid
            length = len(label)
        if _z > 0:
            if _doa/_z < 0.2:
                laji.append(length)
            if _doa/ _z > 0.8:
                niubi.append(length)
            doa.append(_doa / _z)
            z_support += _z
            doa_support += 1
    return {
        "doa": np.mean(doa),
        "doa_know_support": doa_support,
        "doa_z_support": z_support,
    }

