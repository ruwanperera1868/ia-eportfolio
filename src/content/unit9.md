# Unit 9: Introduction to Adaptive Algorithms

A single perceptron (Rosenblatt, 1958) can only draw one straight line, so it cannot learn XOR (Minsky and Papert, 1969). Backpropagation made multi-layer networks trainable (Rumelhart, Hinton and Williams, 1986), and deep learning stacks many layers to learn features from raw data (LeCun, Bengio and Hinton, 2015), at the cost of data, compute and transparency (Rudin, 2019).

## Artefact: perceptron versus hidden-layer network

| Model | Task | Target | Learned |
| --- | --- | --- | --- |
| Perceptron | AND | 0 0 0 1 | 0 0 0 1 |
| Perceptron | XOR | 0 1 1 0 | 1 1 0 0 |
| 4 hidden units, backpropagation | XOR | 0 1 1 0 | 0 1 1 0 |

| Epoch | 0 | 100 | 1,000 | 5,000 | 9,999 |
| --- | --- | --- | --- | --- | --- |
| Mean squared error | 0.3430 | 0.2502 | 0.2188 | 0.0022 | 0.0008 |

The network solved XOR from all 10 random starting points tried, after a long plateau where it appeared to learn nothing. Its final weights give the right answers but explain nothing about how.

{{code:unit9/neural_xor.py}}

::: todo
Add your own notes on this unit: what you found difficult or surprising, how it felt, and what happened in your team that week.
:::
