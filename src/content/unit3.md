# Unit 3: Agent Architectures

Deliberative agents reason over a symbolic world model; reactive agents such as Brooks' (1986; 1991) subsumption architecture act through layered situation-action rules with no model; BDI agents, rooted in Bratman's (1987) practical reasoning, separate beliefs, desires and intentions. Desires are options the agent would like to achieve; intentions are the desires it has committed to, which persist and filter later choices (Rao and Georgeff, 1995).

## Artefact: reactive versus BDI agent

Both agents collect packages on a 10 by 10 grid with a charger and a battery, sensing packages only within 2 cells. The subsumption agent has three layers (survive, collect, wander); the BDI agent remembers packages it has seen and commits to one trip at a time.

| Agent | Packages, mean of 200 runs | Min | Max | Ran out of battery |
| --- | --- | --- | --- | --- |
| Subsumption (reactive) | 8.8 | 0 | 33 | 0 |
| BDI | 35.0 | 11 | 49 | 0 |

Tracing a zero-package reactive run showed the survive layer kept pulling the agent back to the charger, so it never reached packages on the far side. It was safe but ineffective. The BDI agent's memory and commitment let it plan whole trips, at the cost of more code and of acting on beliefs that may be stale.

{{code:unit3/architectures.py}}

::: todo
Add your own notes on this unit: what you found difficult or surprising, how it felt, and what happened in your team that week.
:::
