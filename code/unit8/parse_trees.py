"""Unit 8: constituency parse trees with a hand-written grammar (NLTK).

A context-free grammar lists how phrases are built from smaller phrases.
NLTK's chart parser finds every tree the grammar allows, so an ambiguous
sentence returns more than one tree. Install with: pip install nltk
"""
import nltk

grammar = nltk.CFG.fromstring("""
    S   -> NP VP
    NP  -> Det N | Det N PP | N N | Pro
    VP  -> V NP | V NP NP | V NP PP
    PP  -> P NP
    Det -> 'the' | 'a'
    N   -> 'government' | 'rates' | 'interest' | 'internet' | 'voice'
    N   -> 'man' | 'dog' | 'telescope'
    Pro -> 'everyone'
    V   -> 'raised' | 'gives' | 'saw'
    P   -> 'with'
""")
parser = nltk.ChartParser(grammar)

sentences = [
    "the government raised interest rates",
    "the internet gives everyone a voice",
    "the man saw the dog with the telescope",
]

for sentence in sentences:
    trees = list(parser.parse(sentence.split()))
    print(f"\n{sentence!r}: {len(trees)} parse(s)")
    for i, tree in enumerate(trees, 1):
        print(f"\nParse {i}: {tree.pformat(margin=200)}")
        tree.pretty_print(unicodelines=True)
