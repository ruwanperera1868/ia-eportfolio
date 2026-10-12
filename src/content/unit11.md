# Unit 11: Intelligent Agents in Action

Industry 4.0 describes cyber-physical production in which connected machines make decentralised decisions (Kagermann, Wahlster and Helbig, 2013); multi-agent control lets a shop floor re-route work when a machine fails (Leitão, 2009). In finance, agent-based models simulate markets as interacting traders (Farmer and Foley, 2009), and the 2010 Flash Crash showed how interacting automated traders can amplify a shock (Kirilenko et al., 2017).

## Artefact: an agent-based market

Two hundred traders follow either a fundamentalist rule (trade towards a value of 100) or a chartist rule (follow the trend). In the adaptive version, traders switch to whichever strategy has recently earned more.

| Traders | Volatility per step | Clustering | Largest deviation from value | Time chartist-led |
| --- | --- | --- | --- | --- |
| Fixed, 30% chartists | 0.0026 | 0.24 | 4% | 0% |
| Adaptive, switching | 0.0147 | 0.95 | 718% | 78% |

Copying the winning strategy recruited more trend-followers, which strengthened the trend: volatility rose about sixfold and prices ran away, with no outside shock. The model is a toy, as nothing brings prices back once chartists dominate, but it shows why exchanges use circuit breakers as a market-wide kill switch.

{{code:unit11/market_abm.py}}

## Individual project presentation

This unit's assessment presented the individual implementation of the Academic Evidence Investigator. See [Final Project](final-project.html).

::: todo
Add your own notes on this unit: what you found difficult or surprising, how it felt, and what happened in your team that week.
:::
