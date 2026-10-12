# Reflective Case Studies

Three case studies, each grounded in incidents from my own project and module work and structured with Rolfe, Freshwater and Jasper's (2001) What, So what, Now what framework.

::: todo
These three drafts were prepared with AI assistance from my project records and must be disclosed as such. Before submitting, reword them in your own voice and add one or two sentences in each "So what" on how the incident felt to you at the time.
:::

## 1. Bias in autonomous decision-making

**What.** During the first offline run of the Academic Evidence Investigator, the question "How do LLM-based agents plan, act and reflect?" found only two relevant papers after all three search cycles. Tracing the relevance scores showed the cause: abstracts that said "large language models" never matched the query term, so relevant work was silently excluded. Fix R1 added synonym folding and stemming, and the same query found ten relevant papers in a single cycle. Fix R2 corrected a second skew, where evidence in which every paper was neutral was flagged as one-sided.

**So what.** Neither fault was in the language model. Both sat in ordinary keyword and counting rules, and both looked like plausible behaviour until tested against a known answer. This matches the Unit 10 exercise, where a classifier reported 1% overall error while misclassifying 31.8% of a group that made up 2% of its training data. Bias often enters through data and pipeline choices rather than the model (Sambasivan et al., 2021), and aggregate metrics hide it (Buolamwini and Gebru, 2018). A further bias remains: the agent only sees papers that free APIs index and that have abstracts, which favours English-language and open-access work.

**Now what.** I will evaluate retrieval and scoring rules against labelled cases, not only the model, and report results per subgroup or source rather than one headline figure. In underwriting, that means checking model error by sector and company size before any decision support is used.

## 2. AI safety constraints

**What.** The team design specified a Critic-to-Planner loop that would stop once the evidence was "sufficiently relevant and balanced", with a maximum number of cycles, but left "sufficient" undefined. In the build I made it explicit: a tested rule (at least five relevant papers and varied study designs), at most three search cycles, LangGraph's recursion limit as a backstop, a rule-based stopping decision, a "provisional" label on any briefing that hits the limit, and no silent substitution of offline demo data when a live search fails. Unit 4 showed the cost of safety layers: a reactive veto cut collisions from 4.2 to 0.1 per run, but its detours stranded the agent in 146 of 200 runs, and no battery reserve setting reached zero failures.

**So what.** Defining the limits in code made the agent's failures predictable and testable, which a model's opinion of its own work is not; self-assessment by LLMs is a known source of overconfidence (Huang et al., 2025). Unit 4 adds the counterweight: each constraint interacts with the rest of the system, so safety cannot be added as one layer and assumed to work. Amodei et al. (2016) frame such problems as side effects of the objective, which is what the stranding was.

**Now what.** I will treat stopping conditions, budgets and fallbacks as requirements with their own tests, and measure what each constraint costs in task performance rather than assuming it is free.

## 3. Explainable decisions

**What.** Every run of the Investigator writes an audit trail: each search query, each re-plan and its reason, the stopping decision, and whether each step used the LLM or a deterministic fallback. The final evidence status is computed in Python from the appraisals, so the briefing cannot claim stronger evidence than the record supports. In contrast, the Unit 9 network solved XOR with weights that explain nothing about why it works.

**So what.** Explainability in an agent is mostly a design choice about where decisions are made. Putting the high-stakes decisions (when to stop, how strong the evidence is) in inspectable code made them explainable by construction, in line with Rudin's (2019) case for interpretable models where stakes are high. Post-hoc explanations such as SHAP (Lundberg and Lee, 2017) still have a place for the parts that must stay learned, and the EU AI Act (European Parliament and Council, 2024) makes transparency and human oversight legal duties for high-risk uses, which include some insurance pricing.

**Now what.** My Research Methods proposal applies SHAP to cyber underwriting decisions. This project changes how I will build it: decisions an underwriter must justify stay in rules or interpretable models, every agent step is logged, and SHAP explains the learned risk score rather than the whole workflow.
