---
name: query-ki
description: >-
  Retrieve Knowledge Indicators (pre-computed context) from the Elasticsearch AI Index before
  answering a question about Privatbank Albisgrat's data. Use it first, once, for any question
  that depends on choosing an index, on a bank-specific term or definition, or on which policy
  version is in force.
---

# Retrieving Knowledge Indicators

Knowledge Indicators live in the Elasticsearch index `ai-index-idx-albisgrat`. Retrieve them with
one hybrid query: a keyword branch and a semantic branch, fused. Replace both `<question>`
placeholders with the user's question. If the question is not in German, append its key terms in
German. Escape any double quote inside the question.

```
../esql.sh 'FROM ai-index-idx-albisgrat METADATA _id, _index, _score | FORK (WHERE MATCH(content, "<question>") OR MATCH(title, "<question>") | SORT _score DESC | LIMIT 15) (WHERE MATCH(content.semantic, "<question>") OR MATCH(description.semantic, "<question>") | SORT _score DESC | LIMIT 15) | FUSE | SORT _score DESC | KEEP type, title, content | LIMIT 8'
```

The result has four kinds of rows:

- `index_metadata_entry`: what an index contains, what it does not contain, its key fields.
- `business_definition`: how the bank defines a term, with the ES|QL query that computes it.
- `policy_register_entry`: which version of a policy is in force.
- `glossary_entry`: one term in English, German, French and Italian.

Ground your answer in what the query returns. When a business definition matches the question,
run the query it gives and say that you applied that definition. If nothing relevant comes back,
say so instead of guessing.
