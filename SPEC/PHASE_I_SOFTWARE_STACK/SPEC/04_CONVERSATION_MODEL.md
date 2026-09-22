# Conversation Model

## Purpose

Represent the living JD ↔ Solace dialogue as durable source material.

## Minimum Concepts

A conversation should have:

- stable identifier;
- participants;
- timestamps;
- ordered messages;
- source identifier;
- conversation/session metadata;
- attachments or references where applicable;
- immutable or append-only source history.

## Source Abstraction

The model should not hard-code the assumption that every future source is a chat application.

A source may eventually be:

- Solace chat;
- IRC;
- email;
- WhatsApp;
- another human conversation;
- document or research material.

However, only Solace chat is required in Phase I.

## Preservation Rule

Raw source material must remain distinguishable from Codex interpretation.

The engine may create derived records, but derived material must not overwrite the original conversation.
