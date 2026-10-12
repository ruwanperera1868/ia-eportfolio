# Unit 4: Hybrid Agent Architectures

Hybrid architectures layer a reactive component for urgent events beneath a deliberative one for planning. Layers can be horizontal, each proposing an action to a mediator (Ferguson, 1992), or vertical, with control passing through the layers (Müller, 1996). Real deployments include Stanley, the car that won the 2005 DARPA Grand Challenge (Thrun et al., 2006), and NASA's Remote Agent (Muscettola et al., 1998).

## Artefact: adding a safety layer

The Unit 3 world gains four moving hazards; a collision costs 5 battery. The hybrid agent keeps the BDI layer for deciding what to do and adds a reactive layer that can veto any move onto or next to a hazard.

| Agent | Packages | Collisions per run | Ran out of battery (of 200) |
| --- | --- | --- | --- |
| BDI only | 12.3 | 4.2 | 180 |
| Hybrid, original reserve of 1 | 17.4 | 0.1 | 146 |
| Hybrid, reserve of 6 | 21.1 | 0.1 | 53 |

| Battery reserve | 1 | 4 | 6 | 10 | 15 | 20 |
| --- | --- | --- | --- | --- | --- | --- |
| Packages, mean | 17.4 | 21.3 | 21.1 | 17.5 | 9.7 | 4.9 |
| Ran out of battery | 146 | 82 | 53 | 27 | 13 | 10 |

The safety layer worked, but its detours used battery the planner had not budgeted for: two individually correct layers with clashing assumptions. Raising the reserve traded output for safety, and no setting reached zero failures because hazards could block the way home.

{{code:unit4/hybrid.py}}
