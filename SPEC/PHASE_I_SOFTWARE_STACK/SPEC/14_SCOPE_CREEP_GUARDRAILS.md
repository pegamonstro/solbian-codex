# Scope-Creep Guardrails

## The Rule

Future possibility is not a Phase I requirement.

## Admission Test

Any proposed feature must answer:

### Problem
What concrete problem exists now?

### Necessity
Why does the existing system fail without this feature?

### Simplicity
What is the simplest solution?

### Boundary
Does it require introducing another project, subsystem, service, or conceptual layer?

### Reversibility
Can it be removed without damaging the Codex or source history?

### Evidence
Has the requirement been demonstrated, or is it hypothetical?

## Automatic Deferrals

The following should normally be deferred when proposed without demonstrated need:

- new external integrations;
- distributed systems;
- agent frameworks;
- autonomous execution;
- elaborate ontologies;
- vector search;
- graph infrastructure;
- blockchain;
- hardware integration;
- S.E.E.D. coupling;
- GOLEM coupling;
- Codex Machina coupling.

## Architecture Smell

A Phase I implementation is drifting if its documentation starts requiring knowledge of S.E.E.D., GOLEM, Codex Machina, autonomous agents, or external channel integrations to explain how the basic Codex conversation loop works.

## Final Test

If the system cannot be explained simply as:

**talk → preserve → analyse → propose → consolidate → browse**

it has probably become more complicated than Phase I requires.
