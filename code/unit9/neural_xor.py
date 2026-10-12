"""Unit 9: why neural networks need hidden layers.

A single perceptron can only draw one straight line, so it cannot learn XOR
(Minsky and Papert, 1969). Adding a hidden layer trained by backpropagation
(Rumelhart, Hinton and Williams, 1986) solves it. Written in NumPy so every
step of the forward and backward pass is visible.
"""
import numpy as np

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y_and = np.array([0, 0, 0, 1], dtype=float)
y_xor = np.array([0, 1, 1, 0], dtype=float)


def perceptron(X, y, epochs=100, lr=0.1):
    """Rosenblatt's perceptron learning rule with a step activation."""
    w, b = np.zeros(2), 0.0
    for _ in range(epochs):
        for xi, target in zip(X, y):
            pred = float(xi @ w + b > 0)
            w += lr * (target - pred) * xi
            b += lr * (target - pred)
    return (X @ w + b > 0).astype(int)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def mlp(X, y, hidden=4, epochs=10000, lr=0.5, seed=0):
    """Two-layer network: 2 inputs -> hidden sigmoid units -> 1 sigmoid output."""
    rng = np.random.default_rng(seed)
    W1, b1 = rng.normal(0, 1, (2, hidden)), np.zeros(hidden)
    W2, b2 = rng.normal(0, 1, hidden), 0.0
    history = []
    for epoch in range(epochs):
        h = sigmoid(X @ W1 + b1)                 # forward pass
        out = sigmoid(h @ W2 + b2)
        loss = np.mean((out - y) ** 2)
        d_out = 2 * (out - y) / len(y) * out * (1 - out)   # backward pass
        d_h = np.outer(d_out, W2) * h * (1 - h)
        W2 -= lr * h.T @ d_out
        b2 -= lr * d_out.sum()
        W1 -= lr * X.T @ d_h
        b1 -= lr * d_h.sum(axis=0)
        if epoch in (0, 100, 1000, 5000, epochs - 1):
            history.append((epoch, loss))
    return out, history


if __name__ == "__main__":
    print("Perceptron (no hidden layer)")
    print(f"  AND  target {y_and.astype(int)}  learned {perceptron(X, y_and)}")
    print(f"  XOR  target {y_xor.astype(int)}  learned {perceptron(X, y_xor)}")

    print("\nMulti-layer network (4 hidden units) on XOR")
    out, history = mlp(X, y_xor)
    for epoch, loss in history:
        print(f"  epoch {epoch:>5}: mean squared error {loss:.4f}")
    print(f"  outputs {np.round(out, 3)} -> rounded {np.round(out).astype(int)}")

    print("\nSame network, 10 different random starting weights")
    solved = sum(np.array_equal(np.round(mlp(X, y_xor, seed=s)[0]), y_xor) for s in range(10))
    print(f"  solved XOR in {solved} of 10 runs")
