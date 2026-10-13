# Final Reflection

## What

The Intelligent Agents module changed how I think about building dependable AI systems. Working through logic, agent architectures, NLP and neural networks gave me the foundations, but the group design and individual implementation showed me where those ideas become difficult in practice. I use Rolfe, Freshwater and Jasper's (2001) What, So what, Now what model to reflect on that experience. I worked with Group F, a virtual team based in different countries, to design an Academic Evidence Investigator, which I later implemented independently.

Our first idea was a thesis-planning assistant, with an LLM planner coordinating three small language models on edge devices. In his proposal memo, Isaac Shalaan questioned whether edge inference justified the hardware complexity when the system still depended on a network connection. I was reluctant to abandon an idea I had helped shape. After considering his argument against our requirements, though, I supported the change to a system that plans literature searches, retrieves papers, appraises evidence and produces a referenced briefing.

Our draft of 23 August had five agents. The submitted design combined analysis and critique, mapped the agents to the belief--desire--intention (BDI) model and selected LangGraph over CrewAI for its explicit control of loops. I contributed mainly to the agent architecture and produced the initial draft, drawing on my professional experience of building decision tools. In Unit 11, I implemented the system using LangGraph, Qwen2.5-7B, Semantic Scholar and Crossref. The final test suite contained 83 automated tests with 96% code coverage. Testing and live runs exposed nine faults that led to code changes.

## So what

The change of direction taught me how easily attachment to an idea can affect judgement. I had challenged parts of the original proposal because I thought they were unnecessarily complicated, yet I also hesitated when a teammate challenged an approach I had helped develop. Tuckman's (1965) account of the storming stage helps me understand this disagreement. We kept the discussion focused on what the system needed to do and were able to revise the design without making the disagreement personal.

My self-evaluation score was 29 out of 35. I rated my contribution and initiative highly, but missing one meeting exposed a weakness in how I participated. I caught up through shared notes and messages, and the team consulted me before finalising decisions. Even so, reading the outcome afterwards was different from hearing the reasoning as it developed. Their effort to include me should not replace my own preparation and attendance.

The gap between the design and implementation was equally instructive. The hosted Qwen endpoint was withdrawn and the free credit ran out, so I made the endpoint configurable and ran the model locally through Ollama. Semantic Scholar throttled requests, which required longer retry delays. These problems made assumptions about external services visible in a way that the design document had not.

The stopping condition also needed work. Our design referred to evidence being 'sufficiently relevant and balanced', without defining what that meant. I replaced this with a tested rule requiring at least five relevant papers and varied study designs, with a maximum of three cycles and a provisional label when that limit was reached. This made the behaviour inspectable, although the rule alone could not establish the quality or balance of the evidence. Huang et al. (2025) discuss how LLMs can produce plausible but unsupported output. In my implementation, validation, bounded loops and an audit trail became practical ways of managing that risk.

One fault was particularly revealing. My first offline run used all three cycles but found only two relevant papers because the keyword rule did not match 'LLM-based' with 'large language models'. Adding synonym folding and light stemming raised this to ten papers in one cycle. I had initially looked for a problem in the model or architecture; the immediate cause was a simple matching rule. The result showed the value of checking against known answers, rather than assuming that a system which completes its workflow is working correctly.

The Unit 10 exercise reinforced this lesson: a classifier with 1% overall error had a 31.8% error rate for an under-represented group. The Unit 4 hybrid agent, whose safety layer initially stranded it in 146 of 200 runs, and the instability that emerged in the Unit 11 market model also made me look more closely at interactions between components. Together, these examples changed what I wanted from testing. High code coverage was useful, but I also needed to examine which cases failed and whether the system still achieved its purpose.

## Now what

For my next project, I will write acceptance criteria before implementation and test assumptions about external services early. I will include configurable endpoints, bounded retries and clearly labelled fallbacks from the outset. Evaluation will cover individual cases and relevant groups, alongside overall results, with records that allow me to investigate errors.

In virtual teamwork, I will prepare for meetings and send my input beforehand if I cannot attend, then confirm my understanding of decisions afterwards.

These lessons are relevant to my work in insurance underwriting and my Research Methods proposal for an explainable agentic underwriting workbench. I plan to use explicit rules where decisions require justification, record each agent step and assess SHAP explanations for the learned risk score (Lundberg and Lee, 2017). I will also monitor errors by sector and company size. I will check which EU AI Act obligations apply to the intended use and deployment rather than assume that these measures alone establish compliance (European Parliament and Council of the European Union, 2024). The module has left me more cautious about judging an agent by its output alone. I now want to understand how it reached that output, where it fails and what evidence supports trusting it.

## References

European Parliament and Council of the European Union (2024) 'Regulation (EU) 2024/1689 of 13 June 2024 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act)', *Official Journal of the European Union*, L 2024/1689, 12 July. Available at: https://eur-lex.europa.eu/eli/reg/2024/1689/oj (Accessed: 12 October 2026).

Huang, L. et al. (2025) 'A survey on hallucination in large language models: principles, taxonomy, challenges, and open questions', *ACM Transactions on Information Systems*, 43(2), Article 42, pp. 1--55. Available at: https://doi.org/10.1145/3703155.

Lundberg, S.M. and Lee, S.-I. (2017) 'A unified approach to interpreting model predictions', *Advances in Neural Information Processing Systems 30 (NIPS 2017)*, pp. 4765--4774. Available at: https://arxiv.org/abs/1705.07874.

Rolfe, G., Freshwater, D. and Jasper, M. (2001) *Critical Reflection in Nursing and the Helping Professions: A User's Guide*. Basingstoke: Palgrave Macmillan.

Tuckman, B.W. (1965) 'Developmental sequence in small groups', *Psychological Bulletin*, 63(6), pp. 384--399. Available at: https://doi.org/10.1037/h0022100.
