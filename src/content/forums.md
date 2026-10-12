# Collaborative Discussions

## Team meetings and decisions

Group F met on video calls and coordinated in a WhatsApp group, so there are no forum threads to reproduce here. This record of the main discussions and decisions serves as the team's meeting notes; the [team work](team.html) page has the full history of the design.

| Discussion | Outcome |
| --- | --- |
| Choosing the project | The original thesis-planning idea, an LLM planner with three edge small-language-model agents, was challenged in Isaac Shalaan's memo: edge inference added hardware complexity without removing the network dependency. The team moved to the Academic Evidence Investigator. |
| Agent structure | The 23 August draft had five agents with a separate Critic. The team merged analysis and critique into one agent for the submitted design. |
| Framework | LangGraph was chosen over CrewAI for its explicit control of state transitions and feedback loops. |
| Theory | The design was mapped to the BDI model: shared research state as beliefs, each agent's objective as its desire, and the Planner's revisable research strategy as intentions (Archibald et al., 2024). |
| Review | Peer evaluation at the end of the project described the team as well organised and constructively challenging. |

## Module discussion topics

| Discussion | Units | Topic |
| --- | --- | --- |
| 1 | 1 to 3 | Agent-based systems, including how LLM-powered agents are designed for research and information gathering |
| 2 | 5 to 7 | Agent communication languages |
| 3 | 9 to 11 | Deep learning, including an ethical or safety issue in intelligent agents |

The ideas from these topics are developed on the unit pages: agent types in [Unit 1](unit1.html), KQML and ontologies in [Unit 5](unit5.html) and [Unit 6](unit6.html), and deep learning and bias in [Unit 9](unit9.html) and [Unit 10](unit10.html).
