# Unit 5: Agent Communication

Speech act theory treats saying as doing (Austin, 1962; Searle, 1969). Agent communication languages turn this into performatives: KQML messages such as tell, ask-one and achieve carry a content expression, a content language and an ontology (Finin et al., 1994). An ontology is an explicit specification of a shared conceptualisation (Gruber, 1993). FIPA-ACL later gave each act a formal semantics (FIPA, 2002), though Singh (1998) argued mental-state semantics cannot be verified from outside.

## Artefact: KQML agents over a shared ontology

A buyer agent sends KQML messages to a warehouse agent, which checks the ontology and terms, answers from its beliefs and reasons over the class hierarchy.

| Exchange | Buyer sent | Warehouse replied | Lesson |
| --- | --- | --- | --- |
| 1 | ask-one (stock Laptop) | tell (= (stock Laptop) 12) | Query and answer linked by reply ids |
| 2 | ask-one (stock Electronics) | tell (= (stock Electronics) 12) | Answered by summing subclasses in the ontology |
| 3 | ask-one (stock Tablet) | sorry: not in ontology | Terms outside the shared vocabulary fail |
| 4 | achieve (stock Phone) | tell (= (stock Phone) 10) | A directive asks the receiver to act |
| 5 | ask-one using ontology retail-v2 | sorry: unknown ontology | Same words, different ontology: communication fails |

The warehouse here always complies; a truly autonomous agent could refuse, which is the key difference between a message and a method call.

{{code:unit5/kqml_agents.py}}
