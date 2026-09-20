# Scope and Boundaries

## In Scope

- Existing Codex Solbian corpus as baseline input.
- JD ↔ Solace conversational interface.
- Conversation persistence.
- Source and provenance metadata.
- Codex Engine processing.
- Extraction of concepts, claims, questions, contradictions, relationships, and candidate revisions.
- Draft/proposed Codex updates.
- Versioned Codex storage.
- Read-only Codex browsing.
- Basic history and provenance inspection.
- Testing against the existing corpus.
- Simple, deterministic operational behaviour where practical.

## Explicitly Out of Scope

The following are not Phase I requirements:

- S.E.E.D. implementation.
- GOLEM implementation.
- Codex Machina implementation.
- Autonomous synthetic organisms.
- Metabolic or homeostatic architectures.
- General-purpose agent orchestration.
- IRC ingestion.
- WhatsApp ingestion.
- Email ingestion.
- Universal multi-channel ingestion infrastructure.
- Distributed microservice architecture.
- Blockchain.
- DAO infrastructure.
- Mandatory vector databases.
- Mandatory knowledge graphs.
- Machine-operable governance.
- Hardware integration.
- Robotics.
- Autonomous external action.
- Large-scale deployment infrastructure.

These may be reconsidered later. Their possible future value does not make them Phase I requirements.

## Scope-Creep Test

Before adding a feature, answer:

1. What concrete Phase I problem does it solve?
2. Can the problem be solved more simply?
3. Does it alter the three-layer model?
4. Does it introduce a dependency on a future system?
5. Does it create infrastructure that has not yet been demonstrated necessary?

If the feature cannot justify itself against Phase I requirements, defer it.
