"""Unit 10: how unrepresentative training data produces unequal error rates.

A classifier is trained on data where group B makes up only a small share,
and group B's examples follow a slightly different pattern. Overall accuracy
looks fine; splitting the errors by group (as Buolamwini and Gebru, 2018,
did for face analysis) shows who pays for the imbalance.
"""
import numpy as np

rng = np.random.default_rng(1)


def make_group(n, shift):
    """Two features; the true decision boundary is rotated by `shift`."""
    X = rng.normal(0, 1, (n, 2))
    w_true = np.array([np.cos(shift), np.sin(shift)])
    y = (X @ w_true > 0).astype(float)
    return X, y


def train_logistic(X, y, epochs=500, lr=0.5):
    Xb = np.hstack([X, np.ones((len(X), 1))])
    w = np.zeros(Xb.shape[1])
    for _ in range(epochs):
        p = 1 / (1 + np.exp(-Xb @ w))
        w -= lr * Xb.T @ (p - y) / len(y)
    return w


def error_rate(w, X, y):
    Xb = np.hstack([X, np.ones((len(X), 1))])
    return float(np.mean(((Xb @ w) > 0) != y))


SHIFT_B = 1.0                      # group B's pattern differs by ~57 degrees
XA_test, yA_test = make_group(5000, 0.0)
XB_test, yB_test = make_group(5000, SHIFT_B)

print(f"{'share of B in training':>24} | {'overall error':>13} | {'error on A':>10} | {'error on B':>10}")
for share_b in (0.02, 0.10, 0.30, 0.50):
    n = 2000
    XA, yA = make_group(int(n * (1 - share_b)), 0.0)
    XB, yB = make_group(int(n * share_b), SHIFT_B)
    w = train_logistic(np.vstack([XA, XB]), np.concatenate([yA, yB]))
    ea, eb = error_rate(w, XA_test, yA_test), error_rate(w, XB_test, yB_test)
    overall = (1 - share_b) * ea + share_b * eb   # population with the same mix
    print(f"{share_b:>23.0%} | {overall:>13.1%} | {ea:>10.1%} | {eb:>10.1%}")
