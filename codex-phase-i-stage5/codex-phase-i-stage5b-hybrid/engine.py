#!/usr/bin/env python3
"""Codex Solbian Hybrid Synthesis Engine CLI.

Usage:
    python engine.py [--db PATH] synthesize-dialogue --conversation ID [--llm] [--dry-run]
    python engine.py [--db PATH] accept --document DOC_ID
    python engine.py [--db PATH] list-proposed [--all] [--themes] [--limit N] [--verbose]
    python engine.py [--db PATH] list-working

``--db`` is optional.  When omitted the engine uses ``SOLBIAN_LIVING_DB`` and
falls back to the Stage 4 living-store default:
  /Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite

Without --llm: deterministic extraction only; creates PROPOSED candidates.
With --llm:    additionally attempts to draft a richer PROPOSED body via an
               OpenAI-compatible local endpoint.  Fails closed if unavailable.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from codex_hybrid.config import EngineConfig
from codex_hybrid.db import LivingStore
from codex_hybrid.synthesis import HybridSynthesisEngine


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="engine.py",
        description="Hybrid synthesis engine for Codex Solbian living loop.",
    )
    p.add_argument(
        "--db",
        default=None,
        help="Path to living SQLite store (default: SOLBIAN_LIVING_DB or Stage 4 path)",
    )
    p.add_argument(
        "--llm", action="store_true", help="Enable optional LLM drafting (OFF by default)"
    )
    p.add_argument(
        "--dry-run", action="store_true", help="Run without writing proposals"
    )

    sub = p.add_subparsers(dest="command", required=True)

    syn = sub.add_parser(
        "synthesize-dialogue", help="Create PROPOSED candidates from a conversation"
    )
    syn.add_argument("--conversation", required=True, help="Conversation external_id")

    acc = sub.add_parser(
        "accept", help="Explicitly Accept a PROPOSED document -> WORKING"
    )
    acc.add_argument("--document", required=True, help="Document id")

    lst = sub.add_parser(
        "list-proposed",
        help="List PROPOSED documents (quiet by default: hybrid-only, no Theme:*)",
    )
    lst.add_argument(
        "--all", action="store_true", help="Include older Stage-5 archaeology proposals"
    )
    lst.add_argument(
        "--themes", action="store_true", help="Include titles matching Theme:*"
    )
    lst.add_argument(
        "--limit", type=int, default=None, help="Maximum rows to show (default quiet filter)"
    )
    lst.add_argument(
        "--verbose", action="store_true", help="Equivalent to --all --themes"
    )

    sub.add_parser("list-working", help="List WORKING documents")

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    db_path = args.db or EngineConfig.default_living_db()
    if args.db is None:
        print(f"INFO: using default living DB: {db_path}", file=sys.stderr)

    if not Path(db_path).exists():
        print(f"ERROR: database not found: {db_path}", file=sys.stderr)
        return 1

    config = EngineConfig.from_env(use_llm=args.llm)
    if args.dry_run:
        config = config.__class__(
            llm_base=config.llm_base,
            llm_model=config.llm_model,
            llm_timeout=config.llm_timeout,
            llm_api_key=config.llm_api_key,
            deterministic_only=config.deterministic_only,
            dry_run=True,
            min_message_length=config.min_message_length,
            max_llm_body_chars=config.max_llm_body_chars,
            min_llm_body_chars=config.min_llm_body_chars,
        )

    with LivingStore(db_path) as store:
        if store.safety_warnings:
            for warning in store.safety_warnings:
                print(f"WARNING: {warning}", file=sys.stderr)

        try:
            if args.command == "synthesize-dialogue":
                return cmd_synthesize(store, config, args.conversation)
            elif args.command == "accept":
                return cmd_accept(store, args.document)
            elif args.command == "list-proposed":
                return cmd_list_proposed(store, args)
            elif args.command == "list-working":
                return cmd_list_working(store)
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
    return 0


def cmd_synthesize(store: LivingStore, config: EngineConfig, external_id: str) -> int:
    engine = HybridSynthesisEngine(store, config)
    result = engine.synthesize_conversation(external_id)

    print(f"Conversation: {external_id}")
    print(f"Deterministic extracts: {result.deterministic_count}")
    print(f"LLM drafted: {result.llm_drafted}")
    if result.llm_error:
        print(f"LLM error (fail-closed): {result.llm_error}")
    if result.warnings:
        for w in result.warnings:
            print(f"WARNING: {w}")
    if result.proposed_ids:
        print("PROPOSED document IDs:")
        for pid in result.proposed_ids:
            print(f"  - {pid}")
    else:
        print("No PROPOSED documents created.")

    return 0 if result.proposed_ids else 1


def cmd_accept(store: LivingStore, doc_id: str) -> int:
    store.accept_document(doc_id)
    print(f"Accepted PROPOSED document -> WORKING: {doc_id}")
    return 0


def cmd_list_proposed(store: LivingStore, args: argparse.Namespace) -> int:
    include_themes = args.themes or args.verbose
    hybrid_only = not (args.all or args.verbose)
    limit = None if (args.all or args.verbose) else args.limit

    all_count = store.count_proposed(hybrid_only=False, include_themes=True)
    filtered_count = store.count_proposed(
        hybrid_only=hybrid_only, include_themes=include_themes
    )
    rows = store.list_proposed_documents(
        hybrid_only=hybrid_only,
        include_themes=include_themes,
        limit=limit,
    )
    hidden = max(0, all_count - filtered_count)

    print(f"PROPOSED documents ({len(rows)} shown, {hidden} hidden by quiet filters):")
    for r in rows:
        title = r.get("title") or "(untitled)"
        body_preview = (r.get("body") or "")[:80].replace("\n", " ")
        engine = r.get("engine") or r.get("attribution") or ""
        print(f"  {r['id']} | {engine} | {title} | {body_preview}...")
    return 0


def cmd_list_working(store: LivingStore) -> int:
    rows = store.list_working_documents()
    print(f"WORKING documents ({len(rows)}):")
    for r in rows:
        title = r.get("title") or "(untitled)"
        body_preview = (r.get("body") or "")[:80].replace("\n", " ")
        attribution = r.get("attribution") or ""
        print(f"  {r['id']} | {attribution} | {title} | {body_preview}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
