# Unit 2: Introducing First Order Logic

First order logic adds objects, relations and quantifiers to propositional logic, so that one sentence can describe every robot rather than each one separately (Russell and Norvig, 2021). Deliberative agents store beliefs as such sentences and decide by reasoning over them (Wooldridge, 2009).

## Artefact: model checking and forward chaining

The script builds a small world of three robots and a dock, checks quantified sentences against it, then derives new facts by forward chaining.

| Sentence | Value |
| --- | --- |
| ∀x Robot(x) → Charged(x) | True |
| ∃x Robot(x) ∧ ¬Charged(x) | False |
| ∀x Robot(x) ∧ Charged(x) (a common wrong translation) | False |
| ∀x Robot(x) → ∃y Trusts(x, y) | True |
| ∃y ∀x Robot(x) → Trusts(x, y) | False |

The wrong translation is false even though every robot is charged, because the dock is also in the domain. Swapping quantifier order turns a true sentence false because the trust relation is a cycle. Forward chaining derived CanDock(r1) and CanDock(r2), then CanReachDockVia(r3, r1), and stopped at a fixed point.

{{code:unit2/fol_demo.py}}
