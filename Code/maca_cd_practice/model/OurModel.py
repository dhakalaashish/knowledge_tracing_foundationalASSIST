import torch,pdb
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict,defaultdict
import json
import numpy as np
import math
import copy
import networkx as nx
import pickle
from utils import PosLinear, build_mlp, normalized_matrix

def InfoNCE(view1, view2, temperature: float, b_cos: bool = True):
    """
    Args:
        view1: (torch.Tensor - N x D)
        view2: (torch.Tensor - N x D)
        temperature: float
        b_cos (bool)

    Return: Average InfoNCE Loss
    """
    if b_cos:
        view1, view2 = F.normalize(view1, dim=1), F.normalize(view2, dim=1)

    pos_score = (view1 @ view2.T) / temperature
    score = torch.diag(F.log_softmax(pos_score, dim=1))
    return -score.mean()


class FusionKnowledgeEncoder(nn.Module):
    def __init__(self, text_dim, embed_dim, residual_eps=0.2):
        super().__init__()
        self.residual_eps = residual_eps
        self.text_proj = nn.Sequential(
            nn.Linear(text_dim, embed_dim),
            nn.Sigmoid()
        )
        self.gate_mlp = nn.Sequential(
            nn.Linear(embed_dim*2, embed_dim),
            nn.ReLU(),
            nn.Linear(embed_dim, 1),
            nn.Sigmoid()
        )
        self.free_embed_init = None

    def set_init_free_embed(self, init_emb):
        self.free_embed_init = init_emb.clone().detach()  # shape: [concept_num, embed_dim]

    def forward(self, text_emb, id_emb, epoch=0):    
        text_proj = self.text_proj(text_emb)  # shape: [concept_num, embed_dim]
        o_t = id_emb  # current embedding
        o_t_init = self.free_embed_init  # initialization embedding
            
        concat = torch.cat([
            torch.abs(o_t - o_t_init),  # = sqrt((o_t - o_t_init) ** 2), whose gradient is NaN where the difference is 0
            o_t * o_t_init
        ], dim=-1)  # shape: [concept_num, embed_dim*4]

        g_t = self.gate_mlp(concat).squeeze(-1)
        g_t = torch.clamp(g_t, min=self.residual_eps, max=1.0) # shape: [concept_num]
        # fusion
        o_t_final = (1 - g_t.unsqueeze(-1)) * text_proj + g_t.unsqueeze(-1) * o_t
        gate_info = {
            "gate_weight_f": g_t
        }
        return o_t_final, gate_info

class GraphEncoder(nn.Module):
    def __init__(self, graph, shape1, shape2, device = "cuda:0", num_layers=1, epsilon=1e-3, tau=0.2):
        super().__init__()
        self.device = device
        self.num_layers = num_layers
        self.eps = epsilon  # 控制扰动大小
        self.tau = tau  # 对比学习温度参数

        # concept_parameters_diff_i, concept_parameters_diff_v = graph[0], graph[1]
        # num_edges = concept_parameters_diff_v.shape[0]
        # self.P =  torch.sparse_coo_tensor(
        #     concept_parameters_diff_i.t(),
        #     concept_parameters_diff_v,
        #     (shape1, shape2)
        # )

        concept_parameters_diff_i, concept_parameters_diff_v = graph[0], graph[1]
        num_edges = concept_parameters_diff_v.shape[0]
        self.shape = (shape1, shape2)
        self.register_buffer("edge_indices", concept_parameters_diff_i.t().long())
        self.register_buffer("edge_values", concept_parameters_diff_v.float())
        self.raw_weights = nn.Parameter(
            torch.ones(num_edges, device=concept_parameters_diff_v.device)
        )
    
    def forward(self, x, perturb=False):
        weights = torch.sigmoid(self.raw_weights) * self.edge_values
        graph = torch.sparse_coo_tensor(
            self.edge_indices,
            weights,
            self.shape,
            device=x.device
        ).coalesce()
        all_embeddings = [x]
        out = x
        if perturb:
            for _ in range(self.num_layers):
                out = torch.sparse.mm(graph, out)
                random_noise = 0.1 * torch.rand_like(out)
                out += torch.sign(out) * F.normalize(random_noise, dim=-1) * self.eps
                all_embeddings.append(out)
        else:
            all_embeddings = [x]
            out = x
            for _ in range(self.num_layers):
                out = torch.sparse.mm(graph, out)
                all_embeddings.append(out)
                
        all_embeddings = torch.stack(all_embeddings, dim=1)
        all_embeddings = torch.mean(all_embeddings, dim=1)  
        return all_embeddings


def item_objects(joint_q):
    """Practice version: the objects of each item for the relational item encoder, i.e. its
    (concept, practice) cells with weight > 0. Returns obj_idx (N x S, cell index k * P + p) and obj_w
    (N x S, the cell's joint Q-matrix weight), where S is the largest number of objects of an item;
    items with fewer objects are padded with weight 0."""
    exer_n, con_n, prac_n = joint_q.shape
    flat = joint_q.reshape(exer_n, con_n * prac_n)
    max_objects = max(int((flat > 0).sum(dim=1).max()), 1)
    obj_w, obj_idx = torch.topk(flat, max_objects, dim=1)  # padding cells have weight 0
    return obj_idx, obj_w


class OurModelV(nn.Module):
    def __init__(self, stu_n, exer_n, con_n, hidden_dim, device = "cuda:0", pre_concept_e=None, concept_graph = None, concept_num_matrix = None, pre_practice_e = None, joint_q = None, item_residual_penalty = 0.01, practice_interaction_penalty = 0.001):
        super().__init__()
        self.con_n = con_n
        # Practice version: P practices, embedded from their definitions (z_p)
        self.pre_practice_e = torch.from_numpy(pre_practice_e).to(device).float()
        self.prac_n = self.pre_practice_e.shape[0]
        self.exer_n = exer_n
        self.stu_n = stu_n
        self.emb_dim = hidden_dim
        # Practice version: the item's free embedding is only its residual delta_n (penalized); the rest of
        # the item comes from its (concept, practice) requirements through the relational item encoder
        self.Exer_Encoder = nn.Embedding(self.exer_n, self.emb_dim)
        self.User_Encoder = nn.Embedding(self.stu_n, self.emb_dim)
        self.pre_concept_e = torch.from_numpy(pre_concept_e).to(device).float()
        if pre_concept_e is not None:
            self.Con_free = nn.Embedding(self.con_n, self.emb_dim)
            self.Con_Encoder = FusionKnowledgeEncoder(text_dim=pre_concept_e.shape[1], embed_dim=self.emb_dim, residual_eps = 0.2)
        else:
            self.Con_free = nn.Embedding(self.con_n, self.emb_dim)

        self.layers = self.build_mlp([self.con_n, 1])

        self.stu_bias = nn.Embedding(self.stu_n, 1)
        self.exer_bias = nn.Embedding(self.exer_n, 1)
        d = self.emb_dim
        # Practice version (relational).
        # z_p: projection of the practice-definition embedding (like text_proj)
        self.Prac_Encoder = nn.Sequential(
            nn.Linear(self.pre_practice_e.shape[1], d),
            nn.Sigmoid()
        )
        # e_kp = phi_obj([o_k ; z_p]): concatenation lets a practice add its own directions
        self.Obj_Encoder = nn.Sequential(
            nn.Linear(2 * d, d),
            nn.ReLU(),
            nn.Linear(d, d)
        )
        # pi_m: the student's ability in each practice, shared across concepts (<pi_m, z_p>)
        self.Prac_Ability = nn.Embedding(self.stu_n, d)
        # g_psi([pi_m ; z_p ; o_k]): its first layer is split into the student, practice and concept parts,
        # so the M x K x P hidden values are sums of broadcast vectors
        self.Inter_student = nn.Linear(d, d)
        self.Inter_practice = nn.Linear(d, d, bias=False)
        self.Inter_concept = nn.Linear(d, d, bias=False)
        self.Inter_out = nn.Linear(d, 1)
        # Relational item encoder: g_theta([e_a ; e_b]) (first layer split into the e_a and e_b parts) and f_phi
        self.Rel_first = nn.Linear(d, d)
        self.Rel_second = nn.Linear(d, d, bias=False)
        self.Rel_out = nn.Linear(d, d)
        self.Item_Encoder = nn.Sequential(
            nn.Linear(d, d),
            nn.ReLU(),
            nn.Linear(d, d)
        )
        # The prediction MLP reads the flattened K x P interaction
        self.layers = build_mlp([self.con_n * self.prac_n, 64, 32, 1])
        # The joint Q-matrix (N x K x P) and each item's objects for the relational encoder
        joint_q = joint_q.float().to(device)
        self.register_buffer("joint_q", joint_q)
        obj_idx, obj_w = item_objects(joint_q)
        self.register_buffer("obj_idx", obj_idx)
        self.register_buffer("obj_w", obj_w)
        self.item_residual_penalty = item_residual_penalty
        self.practice_interaction_penalty = practice_interaction_penalty

        if concept_graph is not None:
            self.Con_graph_Encoder = GraphEncoder(concept_graph, shape1=self.con_n, shape2 = self.con_n, device = device)
        else:
            self.Con_graph_Encoder = None

        for name, param in self.named_parameters():
            if 'weight' in name:
                nn.init.normal_(param, mean=0, std=0.01)

        init_embeds = self.Con_free.weight.clone().detach().to(device)
        self.Con_Encoder.set_init_free_embed(init_embeds)

    def practice_matrices(self, know_vec):
        """Practice version (relational). o_k = know_vec (fused concept embedding), a and b are an item's
        objects (its (concept, practice) cells with joint Q-matrix weight w > 0).
        z_p   = Prac_Encoder(practice-definition embedding)                                  P x d
        e_kp  = phi_obj([o_k ; z_p])                                                         K x P x d
        C_mkp = sigmoid(<u_m, e_kp> + <pi_m, z_p> + g_psi([pi_m ; z_p ; o_k]) + b_m)         M x K x P (proficiency)
        v_n   = f_phi( sum_a sum_b w_a w_b g_theta([e_a ; e_b]) ) + delta_n                  N x d
        D_nkp = sigmoid(<v_n, e_kp>)                                                         N x K x P (difficulty)
        Returns C, D, g_psi (M x K x P) and delta (N x d), the last two for their penalties."""
        con_n, prac_n, d = self.con_n, self.prac_n, self.emb_dim
        z = self.Prac_Encoder(self.pre_practice_e)                                             # P x d
        e = self.Obj_Encoder(torch.cat([know_vec.unsqueeze(1).expand(con_n, prac_n, d),
                                        z.unsqueeze(0).expand(con_n, prac_n, d)], dim=-1))     # K x P x d

        # Proficiency: concept mastery + practice ability across concepts + their interaction
        u = self.User_Encoder.weight
        pi = self.Prac_Ability.weight
        hidden = F.relu(self.Inter_student(pi)[:, None, None, :] + self.Inter_concept(know_vec)[None, :, None, :]
                        + self.Inter_practice(z)[None, None, :, :])                              # M x K x P x d
        g = self.Inter_out(hidden).squeeze(-1)                                                   # M x K x P
        C = torch.einsum('md,kpd->mkp', u, e) + (pi @ z.t()).unsqueeze(1) + g + self.stu_bias.weight.view(-1, 1, 1)
        C = torch.sigmoid(C)

        # Difficulty: relational encoder over each item's objects plus the item's residual delta_n
        objects = e.reshape(con_n * prac_n, d)[self.obj_idx]                                     # N x S x d
        pairs = F.relu(self.Rel_first(objects).unsqueeze(2) + self.Rel_second(objects).unsqueeze(1))  # N x S x S x d
        pair_w = self.obj_w.unsqueeze(2) * self.obj_w.unsqueeze(1)                               # N x S x S
        relations = (pair_w.unsqueeze(-1) * self.Rel_out(pairs)).sum(dim=(1, 2))                 # N x d
        delta = self.Exer_Encoder.weight
        v = self.Item_Encoder(relations) + delta
        D = torch.sigmoid(torch.einsum('nd,kpd->nkp', v, e))
        return C, D, g, delta

    def forward(self, stu_id, stu_vector, exer_id, exer_vector, kid, knowledge_vec, epoch = 0, sign=False):
        know_vec = self.Con_free.weight

        if self.Con_graph_Encoder is not None:
            graph_know_vec_view1 = self.Con_graph_Encoder(know_vec, perturb=True)
            graph_know_vec_view2 = self.Con_graph_Encoder(know_vec, perturb=True)
            graph_know_vec = self.Con_graph_Encoder(know_vec)
            ssl_loss = InfoNCE(graph_know_vec_view1, graph_know_vec_view2, 0.2)

        if self.pre_concept_e is not None:
            know_vec, _ = self.Con_Encoder(self.pre_concept_e, graph_know_vec, epoch)

        # Practice version: concept x practice proficiency and difficulty instead of per concept
        C, D, g, delta = self.practice_matrices(know_vec)

        # Q_joint_n: concept x practice weights of the exercises in the batch (B x K x P, built from the
        # per-concept practice scores in data_loader.joint_q_tensor); x_mn = Q_joint_n * (C_m - D_n)
        q_joint = self.joint_q[exer_id]
        input_x = (q_joint * (C[stu_id] - D[exer_id])).reshape(len(exer_id), -1)

        output = self.layers(input_x)
        if sign:
            # Penalties: the item residual delta_n per response (so it is weighed like the loss of the item's
            # responses) and the practice-concept interaction g_psi (kept small, a refinement)
            reg_loss = self.item_residual_penalty * (delta[exer_id] ** 2).sum(dim=1).mean() \
                       + self.practice_interaction_penalty * (g ** 2).mean()
            return output.view(-1), ssl_loss, reg_loss
        else:
            return output.view(-1)


    def proficiency(self):
        """Students x concepts x practices proficiency C exactly as forward() computes it, without the
        perturbed graph views. Used for DOA (mastery_levels combines the graph differently)."""
        know_vec = self.Con_free.weight
        if self.Con_graph_Encoder is not None:
            know_vec = self.Con_graph_Encoder(know_vec)
        if self.pre_concept_e is not None:
            know_vec, _ = self.Con_Encoder(self.pre_concept_e, know_vec)
        C, _, _, _ = self.practice_matrices(know_vec)
        return C

    def mastery_levels(self,stu_vec, exer_vec, knowledge_vec, epoch):
        know_vec = self.Con_free.weight

        if self.Con_graph_Encoder is not None:
            know_vec = self.Con_graph_Encoder(know_vec) + know_vec

        if self.pre_concept_e is not None:
            know_vec, _ = self.Con_Encoder(self.pre_concept_e, know_vec, epoch)

        # Practice version: proficiency of every student on every (concept, practice), M x K x P
        C, _, _, _ = self.practice_matrices(know_vec)

        # print(_["gate_weight_f"].view(-1))
        return C

    def build_mlp(self, layer_dims, dropout=0.5):
        layers = []
        for i in range(len(layer_dims) - 1):
            layers.append(nn.Linear(layer_dims[i], layer_dims[i + 1]))
            if i < len(layer_dims) - 2:
                layers.append(nn.Dropout(p=dropout))
                layers.append(nn.LeakyReLU(0.2))
            else:
                layers.append(nn.Sigmoid())
        return nn.Sequential(*layers)
    
    # def set_graph(self, matrix_):
    #     pos_mask = (matrix_ == 1)
    #     neg_mask = (matrix_ == -1)

    #     norm_pos_mask = normalized_matrix(pos_mask)
    #     norm_neg_mask = normalized_matrix(neg_mask)

    #     self.stu_d_pos = 1.0 / (pos_mask.sum(dim=-1).reshape(-1, 1) + 1)
    #     self.stu_d_neg = 1.0 / (neg_mask.sum(dim=-1).reshape(-1, 1) + 1)
    #     self.exe_d_pos = 1.0 / (pos_mask.sum(dim=0).reshape(-1, 1) + 1)
    #     self.exe_d_neg = 1.0 / (neg_mask.sum(dim=0).reshape(-1, 1) + 1)

    #     self.s_e_graph_pos = norm_pos_mask.to_sparse() # 4918 * 948
    #     self.s_e_graph_neg = norm_neg_mask.to_sparse() # 4918 * 948
    #     self.e_s_graph_pos = norm_pos_mask.t().to_sparse() # 948 * 4918
    #     self.e_s_graph_neg = norm_neg_mask.t().to_sparse() # 948 * 4918
