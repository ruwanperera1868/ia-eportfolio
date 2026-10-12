# Unit 7: Natural Language Processing

Language is ambiguous at every level: lexical, syntactic, referential, pragmatic and figurative (Jurafsky and Martin, 2024). NLP moved from rules to statistics to neural models; Word2Vec learns dense word vectors by predicting context words (Mikolov et al., 2013), building on the distributional hypothesis (Firth, 1957). Embeddings also absorb social bias from their training text (Bolukbasi et al., 2016).

## Artefact: Word2Vec from scratch

A skip-gram model with negative sampling, written in NumPy, trained on 3,000 template sentences with four hidden word groups the model is never told about.

| Word | Three nearest neighbours (cosine similarity) |
| --- | --- |
| robot | drone 0.98, rover 0.98, base 0.68 |
| cat | horse 0.99, dog 0.98, meat 0.73 |
| fish | meat 0.99, grain 0.97, dog 0.77 |
| dock | base 0.99, station 0.99, rover 0.70 |

Words in the same hidden group averaged 0.98 similarity against 0.45 across groups. The model also learned which groups co-occur (robot near base, cat near meat), the same mechanism by which real embeddings absorb stereotypes.

{{code:unit7/word2vec_mini.py}}
