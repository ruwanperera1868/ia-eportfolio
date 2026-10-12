# Final Project: Design and Implementation

::: card
**Academic Evidence Investigator.** Group F (Ruwan Perera, Isaac Shalaan, Tugba Unal and Luis Torres Zambrano) designed the system in Unit 6. I implemented it individually for Unit 11. Code: [github.com/ruwanperera1868/llmplanningagent](https://github.com/ruwanperera1868/llmplanningagent).
:::

## Purpose

Postgraduate researchers spend much of their time turning a question into searches, reading abstracts and judging evidence. The Investigator supports a Graduate School or Postgraduate Research Support Unit: it takes a research question such as "Does generative AI improve university students' academic performance?", decomposes it, retrieves scholarly papers, appraises them and produces a structured briefing. It supports rather than replaces the researcher, and frames research gaps only within the papers it retrieved.

## Design phase (Unit 6)

The team design specified a supervisor-based multi-agent architecture built on LangGraph, with Qwen2.5-7B-Instruct as the model, Semantic Scholar and Crossref for retrieval, deterministic Python for cleaning and deduplication, JSON as the interface between stages, SQLite for persistence and a Flask interface.

| Agent | Responsibility in the design |
| --- | --- |
| Planner / Supervisor | Interprets the question, creates subtasks and search queries |
| Retrieval | Queries Semantic Scholar and Crossref; Python removes duplicates and ranks |
| Evidence Analysis / Critic | Interprets findings, methods and limitations; returns control to the Planner if evidence is weak or unbalanced |
| Reporting | Produces the structured briefing and stores it |

The design drew on ReAct for alternating reasoning and acting (Yao et al., 2023), Reflexion for the Critic-to-Planner feedback loop (Shinn et al., 2023), retrieval-augmented generation for grounding (Lewis et al., 2020) and a BDI mapping of shared state to beliefs and the Planner's strategy to intentions (Archibald et al., 2024). LangGraph was preferred to CrewAI for its explicit control of state transitions and loops.

**How the design evolved.** An earlier concept used an LLM planner with three edge small-language-model agents. Isaac Shalaan's proposal memo argued that edge inference added hardware complexity without removing the dependency on online academic databases, and proposed the evidence investigator instead. A draft dated 23 August 2026 had five agents with a separate Critic; the submitted version merged analysis and critique into one agent and added the BDI and CrewAI discussion.

::: todo
Add screenshots of Figure 1 (architecture) and Figure 2 (activity flow) from the team report, and state which parts of the report you wrote or led.
:::

## Implementation (Unit 11)

The implementation wires the agents as a LangGraph `StateGraph` sharing one `ResearchState`, with a conditional edge from the Critic back to the Planner bounded by `MAX_CYCLES` (default 3). The guiding rule is that the LLM proposes and Python verifies.

| Agent | LLM does | Python guarantees |
| --- | --- | --- |
| Planner | Decomposes the question, writes queries | Schema check, no repeated queries, keyword fallback |
| Retrieval | Nothing | Rate limits, retries only transient errors, logs outages |
| Processing | Nothing, by design | Deduplication by DOI then title and first author, relevance ranking |
| Critic | Appraises abstracts in one batched call | Drops invented paper ids; the stop decision uses explicit thresholds |
| Reporter | Drafts the briefing | Every finding must cite a retrieved paper |

## Design versus implementation

| Design commitment | Implementation | Kept or changed, and why |
| --- | --- | --- |
| Four specialist agents under a supervisor | Planner, Retrieval, Critic, Reporter plus a deterministic processing step | Kept |
| Critic-to-Planner loop | Conditional edge, bounded at 3 cycles | Kept; stopping made a rule rather than the model's self-assessment (Ji et al., 2023) |
| Qwen2.5-7B via Hugging Face, configurable | Any OpenAI-compatible endpoint; live demo ran Qwen locally under Ollama | Changed: the hosted model was withdrawn and free credit ran out (R6) |
| HTTPX for API calls | Requests only | Changed: HTTPX added nothing for synchronous calls |
| Findings linked to sources | Citations to unretrieved papers stripped, uncited findings dropped | Kept and strengthened (Huang et al., 2025) |
| JSON schema, audit trail, cycle limit, deduplication | Pydantic schemas, SQLite audit trail, `MAX_CYCLES`, pandas deduplication | Kept |
| Not in the design | Explicit offline mode, never a silent fallback | Added for reproducible tests without misrepresenting evidence |
| Not in the design | Deterministic fallback for every LLM step | Added so rate limits lower quality, not availability |
| PostgreSQL later | Not done | Future work |

## Testing and what it changed

83 automated tests pass with 96% line coverage and need no network, because the sources and the LLM are injected and tests use scripted fakes. Functional tests prove the re-plan loop, the cycle limit, a source outage, cross-source deduplication, removal of an invented citation, a total LLM outage still producing a briefing, and escaping of hostile HTML.

| Fix | Problem found | Change |
| --- | --- | --- |
| R1 | "LLM-based" never matched "large language models" | Synonym folding and stemming: 2 relevant papers in 3 cycles became 10 in 1 |
| R2 | All-neutral evidence flagged as one-sided | Only uniform supports or opposes counts as imbalance |
| R3 | Unclosed SQLite connections | Shared storage; the suite fails on any leak |
| R4 | HTTP 404 retried like a rate limit | Retry only timeouts, 429 and 5xx |
| R5 | References ordered by title | Alphabetical by first author |
| R6 | Hosted Qwen withdrawn, credit exhausted | Configurable endpoint; Qwen run locally under Ollama |
| R7 | Semantic Scholar throttling (429) | Longer back-off, Retry-After, optional API key |
| R8 | One bad appraisal discarded all 12 | Per-item validation; 11 of 12 kept |
| R9 | Briefing JSON missing a comma | Opt-in JSON mode constrains output |

R1 to R5 came from offline testing; R6 to R9 from live runs on 11 October 2026 (Windows 11, Ollama, `qwen2.5:7b`), each taking 5 to 10 minutes on a CPU.

## Limitations

Without the LLM, appraisal falls back to a keyword heuristic; only abstracts are read; relevance is term overlap rather than semantic similarity; and the web app handles one user at a time. Next steps are embedding-based relevance, PostgreSQL and evaluation against a hand-labelled set of appraisals.

::: todo
Add screenshots from the repository's evidence folder (the briefing page, the audit trail and the live CLI run), your presentation slides or recording, and any tutor feedback.
:::

::: todo
Write your critical evaluation here in your own words (it also forms part of the submitted document): what the design got right, where it was naive (for example, assuming a stable hosted model and free APIs), what testing revealed that design could not, and what you would do differently.
:::
