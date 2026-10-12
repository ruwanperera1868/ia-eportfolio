# Unit 8: Understanding NLP

Constituency parse trees show how a sentence breaks into nested phrases under a context-free grammar (Chomsky, 1957). The trees below were checked with an NLTK chart parser, which returns every tree the grammar allows.

## Creating parse trees

**The government raised interest rates.**

```
(S (NP (Det the) (N government)) (VP (V raised) (NP (N interest) (N rates))))
```

**The internet gives everyone a voice.** "Gives" is ditransitive, so the verb phrase holds two noun phrases.

```
(S (NP (Det the) (N internet)) (VP (V gives) (NP (Pro everyone)) (NP (Det a) (N voice))))
```

**The man saw the dog with the telescope.** Two valid trees: the prepositional phrase attaches to the verb phrase (he used the telescope) or to the noun phrase (the dog had it).

```
(S (NP (Det the) (N man)) (VP (V saw) (NP (Det the) (N dog)) (PP (P with) (NP (Det the) (N telescope)))))
(S (NP (Det the) (N man)) (VP (V saw) (NP (Det the) (N dog) (PP (P with) (NP (Det the) (N telescope))))))
```

Grammar alone cannot choose between them; a statistical parser picks the likelier tree and a person uses world knowledge.

{{code:unit8/parse_trees.py}}

{{code:unit8/parse_trees_output.txt}}

::: todo
Add your own notes on this unit: what you found difficult or surprising, how it felt, and what happened in your team that week.
:::
