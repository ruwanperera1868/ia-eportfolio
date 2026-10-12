# Reflective Case Studies

Three case studies, each grounded in incidents from my own project and module work and structured with Rolfe, Freshwater and Jasper's (2001) What, So what, Now what framework.

## 1. Bias in autonomous decision-making

**Evidence to draw on.** In the Investigator, fix R1 found that the phrase "LLM-based" never matched abstracts saying "large language models", so relevant papers were silently excluded and the agent spent all three cycles on 2 relevant papers; synonym folding raised this to 10 papers in one cycle. Fix R2 found that evidence where every paper was neutral was being flagged as one-sided. Coverage is also limited to papers that free APIs index and that have abstracts. In Unit 10, a classifier showed 1% overall error while erring on 31.8% of a group making up 2% of the training data.

::: todo
Write What, So what and Now what in your own words (about 250 words).
:::

## 2. AI safety constraints

**Evidence to draw on.** The Investigator's autonomy is bounded: at most 3 search cycles, with LangGraph's recursion limit as a backstop; the decision to stop is a tested rule, not the model's opinion of its own work; a briefing that hits the limit is labelled provisional; and offline demo data is never substituted silently for a failed live search. In Unit 4, a reactive safety layer cut collisions from 4.2 to 0.1 per run, yet its detours stranded the agent in 146 of 200 runs until its battery reserve was raised, and no setting reached zero failures.

::: todo
Write What, So what and Now what in your own words (about 250 words).
:::

## 3. Explainable decisions

**Evidence to draw on.** The Investigator's audit trail records every search, re-plan and decision, and which steps used the LLM or a deterministic fallback; the evidence status is written by Python, so the system cannot overstate its evidence. By contrast, the Unit 9 neural network solved XOR with weights that explain nothing. Your Research Methods proposal applies SHAP explanations to cyber underwriting decisions, which links this case study to your future practice.

::: todo
Write What, So what and Now what in your own words (about 250 words).
:::
