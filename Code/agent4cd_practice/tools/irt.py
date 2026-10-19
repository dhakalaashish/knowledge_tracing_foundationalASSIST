"""
Two-parameter logistic IRT (Eq. 2 of Agent4CD): P(r_se = 1 | P^ab_s) = 1 / (1 + exp(-alpha_e (P^ab_s - beta_e))).
The learner's latent ability P^ab_s is the cognitive factor of the agent's profile.
"""

import copy

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score


class IRT2PL(nn.Module):
    def __init__(self, n_students, n_exercises):
        super().__init__()
        self.ability = nn.Embedding(n_students, 1)         # P^ab_s
        self.discrimination = nn.Embedding(n_exercises, 1)  # alpha_e = softplus(.) > 0
        self.difficulty = nn.Embedding(n_exercises, 1)      # beta_e
        for emb in (self.ability, self.discrimination, self.difficulty):
            nn.init.normal_(emb.weight, mean=0.0, std=0.1)

    def alpha(self, exercises):
        return F.softplus(self.discrimination(exercises)).view(-1)

    def forward(self, students, exercises):
        theta = self.ability(students).view(-1)
        beta = self.difficulty(exercises).view(-1)
        return torch.sigmoid(self.alpha(exercises) * (theta - beta))


@torch.no_grad()
def predict(model, records, device, batch_size=65536):
    model.eval()
    probs = []
    for start in range(0, len(records), batch_size):
        batch = torch.from_numpy(records[start:start + batch_size]).to(device)
        probs.append(model(batch[:, 0], batch[:, 1]).cpu().numpy())
    return np.concatenate(probs) if probs else np.zeros(0)


def train_irt(records, cfg, seed):
    """Fit by binary cross-entropy on records['train']; keep the epoch with the best AUC on records['val']."""
    device = torch.device(cfg["device"] if torch.cuda.is_available() else "cpu")
    torch.manual_seed(seed)
    model = IRT2PL(records["n_students"], records["n_exercises"]).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg["lr"])
    train = torch.from_numpy(records["train"]).to(device)
    generator = torch.Generator(device="cpu").manual_seed(seed)

    best = {"auc": -1.0}
    for epoch in range(cfg["epochs"]):
        model.train()
        permutation = torch.randperm(len(train), generator=generator).to(device)
        total = 0.0
        for start in range(0, len(train), cfg["batch_size"]):
            batch = train[permutation[start:start + cfg["batch_size"]]]
            optimizer.zero_grad()
            probs = model(batch[:, 0], batch[:, 1])
            loss = F.binary_cross_entropy(probs, batch[:, 2].float())
            loss.backward()
            optimizer.step()
            total += loss.item() * len(batch)
        val_probs = predict(model, records["val"], device)
        val_auc = roc_auc_score(records["val"][:, 2], val_probs)
        val_acc = float(((val_probs >= 0.5) == records["val"][:, 2]).mean())
        print(f"IRT epoch {epoch + 1}: loss {total / len(train):.4f}  val ACC {val_acc:.4f}  val AUC {val_auc:.4f}",
              flush=True)
        if val_auc > best["auc"]:
            best = {"auc": val_auc, "acc": val_acc, "epoch": epoch + 1, "state": copy.deepcopy(model.state_dict())}

    model.load_state_dict(best["state"])
    all_exercises = torch.arange(records["n_exercises"], device=device)
    return {
        "ability": model.ability.weight.detach().view(-1).cpu().numpy(),             # P^ab per student
        "discrimination": model.alpha(all_exercises).detach().cpu().numpy(),        # alpha_e
        "difficulty": model.difficulty.weight.detach().view(-1).cpu().numpy(),      # beta_e
        "test_pred": predict(model, records["test"], device),                        # aligned with records['test']
        "best_epoch": best["epoch"],
        "val_auc": best["auc"],
        "val_acc": best["acc"],
    }
