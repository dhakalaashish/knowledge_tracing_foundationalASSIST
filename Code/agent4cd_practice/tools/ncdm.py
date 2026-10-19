"""
NeuralCDM (Wang et al., AAAI 2020), the knowledge-state tool of Agent4CD.

Net and NoneNegClipper are ported from the official implementation, model.py of
https://github.com/bigdata-ustc/Neural_Cognitive_Diagnosis-NeuralCD. train_ncdm follows its train.py:
Adam (lr 0.002), NLLLoss on log([1 - p, p]), apply_clipper() after every step, batches of 32 and a
multi-hot knowledge relevancy vector built from the Q-matrix (knowledge_code - 1). The official script
saves every epoch; here the epoch with the best validation AUC is kept.
"""

import copy

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import roc_auc_score


class Net(nn.Module):
    '''
    NeuralCDM
    '''
    def __init__(self, student_n, exer_n, knowledge_n):
        self.knowledge_dim = knowledge_n
        self.exer_n = exer_n
        self.emb_num = student_n
        self.stu_dim = self.knowledge_dim
        self.prednet_input_len = self.knowledge_dim
        self.prednet_len1, self.prednet_len2 = 512, 256  # changeable

        super(Net, self).__init__()

        # network structure
        self.student_emb = nn.Embedding(self.emb_num, self.stu_dim)
        self.k_difficulty = nn.Embedding(self.exer_n, self.knowledge_dim)
        self.e_discrimination = nn.Embedding(self.exer_n, 1)
        self.prednet_full1 = nn.Linear(self.prednet_input_len, self.prednet_len1)
        self.drop_1 = nn.Dropout(p=0.5)
        self.prednet_full2 = nn.Linear(self.prednet_len1, self.prednet_len2)
        self.drop_2 = nn.Dropout(p=0.5)
        self.prednet_full3 = nn.Linear(self.prednet_len2, 1)

        # initialization
        for name, param in self.named_parameters():
            if 'weight' in name:
                nn.init.xavier_normal_(param)

    def forward(self, stu_id, exer_id, kn_emb):
        '''
        :param stu_id: LongTensor
        :param exer_id: LongTensor
        :param kn_emb: FloatTensor, the knowledge relevancy vectors
        :return: FloatTensor, the probabilities of answering correctly
        '''
        # before prednet
        stu_emb = torch.sigmoid(self.student_emb(stu_id))
        k_difficulty = torch.sigmoid(self.k_difficulty(exer_id))
        e_discrimination = torch.sigmoid(self.e_discrimination(exer_id)) * 10
        # prednet
        input_x = e_discrimination * (stu_emb - k_difficulty) * kn_emb
        input_x = self.drop_1(torch.sigmoid(self.prednet_full1(input_x)))
        input_x = self.drop_2(torch.sigmoid(self.prednet_full2(input_x)))
        output = torch.sigmoid(self.prednet_full3(input_x))

        return output

    def apply_clipper(self):
        clipper = NoneNegClipper()
        self.prednet_full1.apply(clipper)
        self.prednet_full2.apply(clipper)
        self.prednet_full3.apply(clipper)

    def get_knowledge_status(self, stu_id):
        stat_emb = torch.sigmoid(self.student_emb(stu_id))
        return stat_emb.data

    def get_exer_params(self, exer_id):
        k_difficulty = torch.sigmoid(self.k_difficulty(exer_id))
        e_discrimination = torch.sigmoid(self.e_discrimination(exer_id)) * 10
        return k_difficulty.data, e_discrimination.data


class NoneNegClipper(object):
    def __init__(self):
        super(NoneNegClipper, self).__init__()

    def __call__(self, module):
        if hasattr(module, 'weight'):
            w = module.weight.data
            a = torch.relu(torch.neg(w))
            w.add_(a)


def knowledge_matrix(q_matrix, n_exercises, n_concepts):
    """Exercises x concepts multi-hot relevancy (official loader: knowledge_emb[knowledge_code - 1] = 1)."""
    kn = np.zeros((n_exercises, n_concepts), dtype=np.float32)
    for e, cids in q_matrix.items():
        for c in cids:
            kn[e, c - 1] = 1.0
    return kn


@torch.no_grad()
def predict(net, records, kn_matrix, device, batch_size=8192):
    net.eval()
    probs = []
    for start in range(0, len(records), batch_size):
        batch = torch.from_numpy(records[start:start + batch_size]).to(device)
        stu, exer = batch[:, 0], batch[:, 1]
        probs.append(net(stu, exer, kn_matrix[exer]).view(-1).cpu().numpy())
    return np.concatenate(probs) if probs else np.zeros(0)


def train_ncdm(records, cfg, seed):
    """Train on records['train'], keep the epoch with the best AUC on records['val']."""
    device = torch.device(cfg["device"] if torch.cuda.is_available() else "cpu")
    torch.manual_seed(seed)
    np.random.seed(seed)
    n_students, n_exercises, n_concepts = records["n_students"], records["n_exercises"], records["n_concepts"]
    kn_matrix = torch.from_numpy(knowledge_matrix(records["Q"], n_exercises, n_concepts)).to(device)
    net = Net(n_students, n_exercises, n_concepts).to(device)
    optimizer = optim.Adam(net.parameters(), lr=cfg["lr"])
    loss_function = nn.NLLLoss()
    train = torch.from_numpy(records["train"]).to(device)
    generator = torch.Generator(device="cpu").manual_seed(seed)

    best = {"auc": -1.0}
    for epoch in range(cfg["epochs"]):
        net.train()
        running_loss = 0.0
        permutation = torch.randperm(len(train), generator=generator).to(device)
        n_batches = 0
        for start in range(0, len(train), cfg["batch_size"]):
            batch = train[permutation[start:start + cfg["batch_size"]]]
            stu, exer, labels = batch[:, 0], batch[:, 1], batch[:, 2]
            optimizer.zero_grad()
            output_1 = net.forward(stu, exer, kn_matrix[exer])
            output_0 = torch.ones(output_1.size()).to(device) - output_1
            output = torch.cat((output_0, output_1), 1)
            loss = loss_function(torch.log(output), labels)
            loss.backward()
            optimizer.step()
            net.apply_clipper()
            running_loss += loss.item()
            n_batches += 1

        val_probs = predict(net, records["val"], kn_matrix, device)
        val_auc = roc_auc_score(records["val"][:, 2], val_probs)
        val_acc = float(((val_probs >= 0.5) == records["val"][:, 2]).mean())
        print(f"NCDM epoch {epoch + 1}: loss {running_loss / max(n_batches, 1):.4f}  "
              f"val ACC {val_acc:.4f}  val AUC {val_auc:.4f}", flush=True)
        if val_auc > best["auc"]:
            best = {"auc": val_auc, "acc": val_acc, "epoch": epoch + 1, "state": copy.deepcopy(net.state_dict())}

    net.load_state_dict(best["state"])
    test_probs = predict(net, records["test"], kn_matrix, device)
    all_students = torch.arange(n_students, device=device)
    proficiency = net.get_knowledge_status(all_students).cpu().numpy()
    return {
        "proficiency": proficiency,           # students x concepts (column c - 1 is concept id c)
        "test_pred": test_probs,              # aligned with records['test']
        "best_epoch": best["epoch"],
        "val_auc": best["auc"],
        "val_acc": best["acc"],
    }
