# Unit 1: Introduction to Agent-Based Computing

An agent is a computer system situated in an environment and capable of autonomous action there to meet its objectives (Wooldridge and Jennings, 1995), with four properties: autonomy, reactivity, pro-activeness and social ability. Wooldridge (2009) traces the rise of agents to five trends: ubiquity, interconnection, intelligence, delegation and human-orientation.

## Artefact: comparing agent types

The script compares two agent programs from Russell and Norvig (2021) in a corridor of dirty cells. Both perceive only their own cell. The simple reflex agent moves at random when its cell is clean; the model-based agent remembers where it has been and heads for the nearest unvisited cell.

| Corridor (cells) | Simple reflex, mean steps | Model-based, mean steps |
| --- | --- | --- |
| 5 | 17.7 | 6.3 |
| 10 | 86.9 | 15.4 |
| 20 | 390.5 (some runs hit the 1,000-step cap) | 34.9 |

A little internal state turned a random walk into a near-linear sweep. The cost is an assumption: the model-based agent believes visited cells stay clean, which would be wrong in a world where dirt returns.

{{code:unit1/agent_types.py}}

## Discussion 1 preparation

The additional task asked how LLM-powered agents are designed for research and information gathering. The key ideas were planning by task decomposition, tool use, memory and self-critique (Weng, 2023; Wang et al., 2024), with ReAct interleaving reasoning and actions (Yao et al., 2023) and Reflexion learning from failed attempts (Shinn et al., 2023). These same ideas later shaped the team's Planner and Critic design.
