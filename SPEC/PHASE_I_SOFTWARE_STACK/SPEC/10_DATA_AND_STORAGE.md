# Data and Storage

## Principles

Storage should be:

- durable;
- inspectable;
- versionable;
- backup-friendly;
- independent of any particular LLM;
- simple enough to understand and migrate.

## Logical Data Categories

At minimum:

- source conversations;
- messages;
- source metadata;
- Codex documents/sections;
- concepts and relationships where justified;
- proposals;
- revisions;
- provenance links.

## Technology Rule

Phase I does not mandate a particular database, search engine, vector store, graph database, or programming language.

Technology should be selected based on demonstrated requirements.

## Avoid Premature Infrastructure

Do not introduce:

- distributed databases;
- queues;
- event buses;
- graph databases;
- vector databases;
- microservices;

unless a concrete Phase I requirement demonstrates that simpler storage cannot satisfy the need.

## Backups

The source conversations and Codex states must be recoverable independently of the application process.
