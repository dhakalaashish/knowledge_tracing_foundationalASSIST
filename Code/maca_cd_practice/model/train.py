''' HFUT SPY @2025
MACA-CD/SLP/model/train.py, run from Code/maca_cd/model/ (paths are relative to it).
This code is run by agent environment.
important package: torch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu115 #your cuda vision
'''
import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import pdb, json, math, copy, pickle, random, time, re
import numpy as np
import pandas as pd
import torch.utils.data as data
from utils import sparse_graph_construction, degree_of_agreement
from torch.utils.data import DataLoader
from sklearn.metrics import roc_auc_score
import glob
from collections import defaultdict
import pickle
from OurModel import OurModelV
from data_loader import load_response_logs, load_LLM_generation, load_practice_embedding
import argparse

with open('../parameter.json', 'r') as f:
    parameter = json.load(f)

parser = argparse.ArgumentParser(description='Configuration')
parser.add_argument('--split', type=str, default=parameter["split"],
                    choices=["standard", "cold", "zeroshot"],
                    help='dataset split')
parser.add_argument('--device', type=str, default=parameter["device"],
                    help='device')
parser.add_argument('--CDE', type=int, default=parameter["CDE"],
                    help='CDE')
parser.add_argument('--practice_q', type=str, default=parameter.get("practice_q", "practice_probabilities"),
                    choices=["practice_probabilities", "practice_one_hot"],
                    help='source of Q_practice (run data/data_preprocess.py with the same setting first)')
args = parser.parse_args()

device = args.device
split = args.split
practice_q = args.practice_q
test_model = "OurModel_" + practice_q  # practice version: results/OurModel_<practice_q>/
CDE_label = bool(args.CDE)
student_n, exercise_n, knowledge_n = parameter["student_num"], parameter["exercise_num"], parameter["concept_num"]
assert min(student_n, exercise_n, knowledge_n) > 0, "Run data/data_preprocess.py first: it writes the counts to parameter.json"

response_data_info = load_response_logs(split, student_n, exercise_n, knowledge_n, False, practice_q=practice_q)

DAG, pre_emb = load_LLM_generation()
pre_practice_emb = load_practice_embedding(response_data_info["practice_names"])  # practice version

concept_parameters_diff_i, concept_parameters_diff_v = sparse_graph_construction(DAG, knowledge_n, device)

train_dataset = response_data_info["train"]
test_dataset = response_data_info["test"]
Q_matrix = response_data_info["Q"]
Q_matrix = torch.from_numpy(Q_matrix).to(device)

response_matrix = response_data_info["R"]
response_matrix = torch.from_numpy(response_matrix).to(device)
concept_num_matrix = response_data_info["concept_num_matrix"]
concept_num_matrix = torch.from_numpy(concept_num_matrix).to(device)
QP_matrix = torch.from_numpy(response_data_info["QP"]).to(device).float()  # practice version: exercise x practice scores
train_loader = DataLoader(train_dataset, batch_size=parameter["batch_size"], shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=parameter["batch_size"], shuffle=False)

def train():
    loss_function = nn.BCELoss(reduction="none")
    net = OurModelV(student_n, exercise_n, knowledge_n, parameter["mf_dim"], device = device, pre_concept_e = pre_emb, concept_graph = [concept_parameters_diff_i.to(device), concept_parameters_diff_v.to(device)], concept_num_matrix=concept_num_matrix, pre_practice_e = pre_practice_emb)
    net = net.to(device)
    optimizer_net = optim.Adam(net.parameters(), lr=parameter["learning_rate"])

    log_path = "results/"+ test_model

    if not os.path.exists(log_path):
        os.makedirs(log_path)
        print(f"{log_path} Created")
    else:
        print(f"{log_path} Exists")

    log_file = log_path + "/training_logs_"+ split +".txt"
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current = current_time + " Model:" + test_model + " batch_size:" + str(parameter["batch_size"]) + " learning_rate:" + str(parameter["learning_rate"])
    with open(log_file, "a") as f:
        f.write(json.dumps(current) + "\n")

    best_auc = 0.0

    for epoch in range(parameter["number_epoch"]):
        train_res = {
            'edu_loss': 0.0,
            'ACC': 0.0,
            'AUC': 0.0
        }
        net.train()
        for idx, (input_stu_ids, input_exer_ids, kid, labels) in enumerate(train_loader):
            kid = kid.to(device).long()
            Q_concept = Q_matrix.t().float()
            input_stu_ids = input_stu_ids.to(device).long()
            input_exer_ids = input_exer_ids.to(device).long()
            exer_vec = response_matrix.t().float()
            # exer_vec = torch.cat([response_matrix.t(), Q_matrix], dim=1).float()
            labels = labels.to(device).float()
            optimizer_net.zero_grad()       
            output, ssl_loss = net.forward(input_stu_ids, response_matrix.detach().float(), input_exer_ids, exer_vec, kid, Q_concept.detach(), epoch, True, practice_vec=QP_matrix)
            edu_loss = loss_function(output, labels)
            edu_loss = edu_loss.mean() + 0.001 * ssl_loss
            edu_loss.backward()
            optimizer_net.step()
            train_res['edu_loss'] += edu_loss.item()

        log_triggered = False
        ACC, AUC = predict(net, test_loader)
        if AUC > best_auc:
            best_auc = AUC
            log_triggered = True

        train_res["ACC"] = ACC
        train_res["AUC"] = AUC
        if log_triggered:  # DOA of the diagnosed proficiency at every new best epoch
            train_res["DOA"], doa_detail = evaluate_doa(net)
        training_logs = 'epoch: %d, ' % epoch
        for name, value in train_res.items():
            training_logs += name + ':' + '%.4f' % value + ' '
        if log_triggered:
            training_logs += doa_detail

        print(training_logs)
        if log_triggered:
            with open(log_file, "a") as f:
                f.write(json.dumps(training_logs) + "\n")


def evaluate_doa(net):
    """DOA of the students x (concept, practice) proficiency C over all responses of the split
    (train + test, response_data_info["DOA_set"]). The weight of exercise n for (k, p) is
    Q_joint[n, k, p] = Q_concept[n, k] * Q_practice[n, p]. Returns (DOA, per-practice DOA for the log line)."""
    net.eval()
    with torch.no_grad():
        C = net.proficiency()
    stu_n_, con_n_, prac_n_ = C.shape
    q_joint = (Q_matrix.float().unsqueeze(2) * QP_matrix.unsqueeze(1)).reshape(exercise_n, con_n_ * prac_n_)
    doa, doa_targets = degree_of_agreement(C.reshape(stu_n_, con_n_ * prac_n_).cpu().numpy(),
                                           response_data_info["DOA_set"], q_joint.cpu().numpy())
    doa_targets = doa_targets.reshape(con_n_, prac_n_)
    detail = "DOA by practice: "
    for p, name in enumerate(response_data_info["practice_names"]):
        values = doa_targets[:, p]
        values = values[~np.isnan(values)]
        detail += name + ':' + ('%.4f' % values.mean() if len(values) else 'n/a') + ' '
    return doa, detail


def predict(net, test_loader):
    net.eval()
    with torch.no_grad():
        correct_count, exer_count = 0, 0
        pred_all, label_all = [], []
        for idx, (input_stu_ids, input_exer_ids, kid, labels) in enumerate(test_loader):
            kid = kid.to(device).long()
            input_stu_ids = input_stu_ids.to(device).long()
            input_exer_ids = input_exer_ids.to(device).long()
            Q_concept = Q_matrix.t().float()

            exer_vec = response_matrix.t().float()
            labels = labels.to(device).float()
            output = net.forward(input_stu_ids, response_matrix.detach().float(), input_exer_ids, exer_vec, kid, Q_concept.detach(), 100, practice_vec=QP_matrix) # 100 is nothing, just > 1
            output = output.view(-1)
            correct_count += ((output >= 0.5) == labels).sum()
            exer_count += len(labels)
            pred_all += output.to(torch.device('cpu')).tolist()
            label_all += labels.to(torch.device('cpu')).tolist()
    pred_all = np.array(pred_all)
    label_all = np.array(label_all)
    accuracy = correct_count / exer_count
    auc = roc_auc_score(label_all, pred_all)
    return accuracy, auc

if __name__ == '__main__':
    train()

