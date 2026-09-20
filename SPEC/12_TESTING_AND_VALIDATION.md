# Testing and Validation

## Primary Test Corpus

The existing Codex Solbian corpus is the first major validation target.

## Baseline Tests

Before enabling continuous evolution, the system should demonstrate that it can:

1. ingest the existing corpus;
2. preserve source documents;
3. represent the corpus without substantial loss;
4. reproduce the visible Codex structure;
5. preserve known historical distinctions;
6. expose provenance where available;
7. avoid silently changing content.

## Engine Tests

The engine should be evaluated for:

- extraction quality;
- duplicate detection;
- contradiction detection;
- synthesis quality;
- provenance preservation;
- stability across repeated processing;
- failure handling.

## Human Validation

Generated synthesis must be inspectable.

The project should prefer observable proposals over opaque automatic transformations.

## Regression Principle

A new engine version must not silently rewrite the historical baseline.

Changes should be reviewable and reversible.
