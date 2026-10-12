# Key Concepts

A working glossary of the ideas each unit relied on. Each entry gives a short definition, then the place in this portfolio where the idea showed up in practice. Full sources are in the [references](references.html).

## Agents and their properties

**Agent.** A computer system situated in an environment and able to act autonomously there to meet its objectives (Wooldridge and Jennings, 1995). In the [final project](final-project.html) the agent is the whole LangGraph workflow, not the language model inside it.

**Autonomy.** Control over some decisions without step-by-step direction. Its scope has to be named: the Investigator may re-plan its own search, but only three times and only against approved sources.

**Reactivity and pro-activeness.** Reactivity is responding to change in time to matter; pro-activeness is taking initiative towards a goal. The [Unit 1](unit1.html) model-based agent is pro-active (it heads for unvisited cells), while the reflex agent only reacts to the cell it is in.

**Social ability.** Interacting with other agents or people through an agreed protocol. Multiple agents do not by themselves give independent judgement, a point that matters for the project's Critic.

## Reasoning and architectures

**Predicates and quantifier scope.** First-order logic states properties and relations over objects; the order of quantifiers changes meaning. "Every paper has a reviewer" does not mean one reviewer reviews every paper ([Unit 2](unit2.html)).

**Subsumption.** Layered situation-action rules with no world model, where higher layers suppress lower ones (Brooks, 1986). Fast and robust, but in [Unit 3](unit3.html) it collected a quarter of what the BDI agent did because it forgot what it had seen.

**Belief, desire, intention (BDI).** Beliefs are what the agent holds true, desires are options, intentions are the options it has committed to and that filter later choices (Rao and Georgeff, 1995). The Unit 3 BDI agent remembers packages it has seen and commits to one trip at a time, at the risk of acting on stale beliefs.

**Safety versus liveness.** Safety means nothing bad happens; liveness means something good eventually does. The [Unit 4](unit4.html) reserve sweep shows the trade directly: a larger battery reserve cut strandings from 146 to 10 but also cut deliveries from 17.4 to 4.9.

## Communication and cooperation

**Performative.** The act a message performs, such as tell, ask-one or achieve, separate from its content (Finin et al., 1994). Agreeing to do something is a different act from reporting it done, so a protocol needs both.

**Ontology.** An explicit specification of a shared conceptualisation (Gruber, 1993). In [Unit 5](unit5.html) the same question under a different ontology name failed outright.

**Contract Net.** Task allocation by announcement, bids and award (Smith, 1980). The project deliberately did not use it: a fixed LangGraph route was easier to test and audit than agents negotiating for work, at the cost of flexibility.

## Language and learning

**Distributional hypothesis.** Words that occur in similar contexts have similar meanings (Firth, 1957), the idea behind Word2Vec. The [Unit 7](unit7.html) skip-gram model placed words from the same group at cosine similarity 0.98 against 0.45 across groups.

**Structural ambiguity.** One sentence, more than one valid parse. The [Unit 8](unit8.html) grammar gives two trees for a sentence with a prepositional phrase that can attach to the verb or the noun.

**Linear separability.** A single perceptron can only draw one straight boundary, so it cannot learn XOR (Minsky and Papert, 1969). A hidden layer solved it in 10 of 10 runs in [Unit 9](unit9.html).

**Representation bias.** When a group is under-represented in training data, overall accuracy can look good while that group is served badly. In [Unit 10](unit10.html), at a 2% share, overall error was 1.0% but the minority group's error was 31.8%.

## Agents in action

**Emergence.** System-level behaviour that no single agent was programmed to produce. In the [Unit 11](unit11.html) market, letting traders switch strategy turned calm prices into volatility clustering and bubbles.

**Reasoning and acting.** Interleaving model reasoning with tool calls and observations (Yao et al., 2023). The Investigator follows this pattern but keeps the control loop in code, so the model never decides on its own when to stop.

**Evidence gate and its trade-off.** A rule that only lets supported claims into the final output. Measured alone it can be gamed: a system that drops every difficult claim reaches 100% support while answering little. Support and coverage have to be reported together.

**Human oversight.** Keeping a person able to understand, check and override what an agent does, one of the governance questions in [Unit 12](unit12.html). The Investigator supports this with an audit trail of every search, appraisal and stopping decision, and it drafts a briefing for a person to judge rather than acting on its findings.
