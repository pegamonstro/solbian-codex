# Conceptual Architecture

## Three Layers

### 1. Conversation

The living interaction between JD and Solace.

It is the primary experiential source of new material.

Conversation is not automatically Codex content.

### 2. Codex Engine

The processing layer.

It can:

- preserve source references;
- analyse conversations;
- identify durable material;
- compare new material with existing Codex content;
- identify repetition and contradiction;
- identify gaps;
- propose synthesis;
- draft revisions;
- generate discussion topics.

The engine is not the authority on the meaning of Codex Solbian.

### 3. Codex Solbian

The persistent intellectual artifact.

It contains the current consolidated representation of the project's developed understanding.

## Flow

    JD ↔ Solace
          │
          ▼
    Conversation Store
          │
          ▼
    Codex Engine
          │
          ▼
    Proposed Update
          │
          ▼
    Codex Solbian
          │
          ▼
    Gaps / Questions
          │
          └──────────→ future conversation

## Architectural Constraint

The architecture must not require S.E.E.D., GOLEM, Codex Machina, or any other future project.

The Phase I system must remain useful and testable as a standalone Codex environment.
