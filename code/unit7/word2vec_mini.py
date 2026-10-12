"""Unit 7: a minimal Word2Vec (skip-gram with negative sampling) in NumPy.

Word2Vec (Mikolov et al., 2013) learns a vector for each word by training it
to predict the words around it. Words used in similar contexts end up with
similar vectors: the distributional hypothesis ("you shall know a word by the
company it keeps", Firth, 1957).

The corpus is generated from templates so that we know which words share
contexts, and can check whether the model discovers those groups by itself.
"""
import numpy as np

rng = np.random.default_rng(0)

# ---- 1. A synthetic corpus with hidden word groups ----
groups = {
    "machine": ["robot", "drone", "rover"],
    "animal": ["cat", "dog", "horse"],
    "food": ["fish", "meat", "grain"],
    "place": ["dock", "base", "station"],
}
templates = [
    ("the", "machine", "moves", "to", "the", "place"),
    ("the", "machine", "charges", "at", "the", "place"),
    ("the", "animal", "eats", "the", "food"),
    ("the", "animal", "sleeps", "near", "the", "food"),
    ("a", "machine", "senses", "the", "place"),
    ("a", "animal", "smells", "the", "food"),
]
sentences = []
for _ in range(3000):
    t = templates[rng.integers(len(templates))]
    sentences.append([str(rng.choice(groups[w])) if w in groups else w for w in t])

vocab = sorted({str(w) for s in sentences for w in s})
idx = {w: i for i, w in enumerate(vocab)}
counts = np.zeros(len(vocab))
for s in sentences:
    for w in s:
        counts[idx[w]] += 1

# ---- 2. Training pairs: (centre word, context word) within a window ----
WINDOW, DIM, NEG, EPOCHS, LR = 2, 16, 5, 5, 0.05
pairs = [(idx[s[i]], idx[s[j]])
         for s in sentences for i in range(len(s))
         for j in range(max(0, i - WINDOW), min(len(s), i + WINDOW + 1)) if j != i]
pairs = np.array(pairs)

# negative samples drawn from the unigram distribution raised to 3/4
noise = counts ** 0.75
noise /= noise.sum()

W_in = (rng.random((len(vocab), DIM)) - 0.5) / DIM     # word vectors we keep
W_out = np.zeros((len(vocab), DIM))                    # context vectors


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# ---- 3. Skip-gram with negative sampling, plain SGD ----
for epoch in range(EPOCHS):
    rng.shuffle(pairs)
    loss = 0.0
    for centre, context in pairs:
        targets = np.concatenate(([context], rng.choice(len(vocab), NEG, p=noise)))
        labels = np.zeros(NEG + 1)
        labels[0] = 1                                   # real pair = 1, noise = 0
        v = W_in[centre].copy()
        u = W_out[targets].copy()
        p = sigmoid(u @ v)
        grad = p - labels
        loss -= np.log(p[0] + 1e-9) + np.log(1 - p[1:] + 1e-9).sum()
        W_in[centre] -= LR * grad @ u
        W_out[targets] -= LR * np.outer(grad, v)
    print(f"epoch {epoch + 1}: mean loss {loss / len(pairs):.3f}")


# ---- 4. Did similar words get similar vectors? ----
def similar(word, k=3):
    norm = W_in / np.linalg.norm(W_in, axis=1, keepdims=True)
    sims = norm @ norm[idx[word]]
    order = [i for i in np.argsort(-sims) if vocab[i] != word]
    return [(vocab[i], round(float(sims[i]), 2)) for i in order[:k]]


print("\nNearest neighbours by cosine similarity:")
for w in ["robot", "cat", "fish", "dock", "moves"]:
    print(f"  {w:<7} {similar(w)}")

within, across = [], []
norm = W_in / np.linalg.norm(W_in, axis=1, keepdims=True)
members = {w: g for g, ws in groups.items() for w in ws}
for a in members:
    for b in members:
        if a < b:
            s = float(norm[idx[a]] @ norm[idx[b]])
            (within if members[a] == members[b] else across).append(s)
print(f"\nMean similarity within a hidden group: {np.mean(within):.2f}")
print(f"Mean similarity across groups:         {np.mean(across):.2f}")
