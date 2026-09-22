#!/usr/bin/env python3
"""Smoke tests for the Hybrid Synthesis Engine.

Creates a throwaway copy of the fixture DB, runs the deterministic synthesis
path against the "Who are we?" conversation, verifies Accept -> WORKING, and
confirms that the LLM path fails closed when no model is reachable.

The optional live-LLM smoke is gated by ``SOLBIAN_LLM_SMOKE=1`` and a reachable
endpoint (default Ollama).  A deterministic mock path is gated by
``SOLBIAN_LLM_MOCK=1`` so CI can verify the LLM pipeline without a running
model.
"""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path

from codex_hybrid.config import EngineConfig
from codex_hybrid.db import LivingStore
from codex_hybrid.synthesis import HybridSynthesisEngine


PASS = "PASS"
FAIL = "FAIL"


def _copy_fixture() -> Path:
    here = Path(__file__).resolve().parent
    src = here / "fixtures" / "who_are_we.sqlite"
    if not src.exists():
        raise FileNotFoundError(f"Fixture DB missing: {src}")
    tmp_dir = Path(tempfile.mkdtemp(prefix="codex_hybrid_smoke_"))
    dst = tmp_dir / "living.sqlite"
    shutil.copy(src, dst)
    return dst


def _assert(check: bool, msg: str) -> str:
    if not check:
        print(f"  {FAIL}: {msg}")
        return FAIL
    print(f"  {PASS}: {msg}")
    return PASS


def smoke_default_db_path() -> str:
    print("\n[SMOKE] default living DB path")
    default = EngineConfig.default_living_db()
    status = PASS
    status = _assert(
        "codex-phase-i-stage4/data/codex_phase_i.sqlite" in default,
        "default path points at Stage 4 living store",
    ) or status

    old = os.environ.pop("SOLBIAN_LIVING_DB", None)
    os.environ["SOLBIAN_LIVING_DB"] = "/tmp/test_living.sqlite"
    try:
        overridden = EngineConfig.default_living_db()
        status = _assert(
            overridden == "/tmp/test_living.sqlite",
            "SOLBIAN_LIVING_DB overrides default",
        ) or status
    finally:
        if old is None:
            os.environ.pop("SOLBIAN_LIVING_DB", None)
        else:
            os.environ["SOLBIAN_LIVING_DB"] = old
    return status


def smoke_historical_corpus_guard() -> str:
    print("\n[SMOKE] refuse writes to historical corpus")
    status = PASS
    status = _assert(
        LivingStore.is_historical_corpus("/Users/archcore/solbian/codex/foo.sqlite"),
        "detects Mac historical corpus path",
    ) or status
    status = _assert(
        not LivingStore.is_historical_corpus("/tmp/codex_phase_i.sqlite"),
        "does not flag unrelated living-store paths",
    ) or status
    return status


def smoke_deterministic() -> str:
    print("\n[SMOKE] deterministic path")
    db = _copy_fixture()
    with LivingStore(db) as store:
        config = EngineConfig.from_env(use_llm=False)
        engine = HybridSynthesisEngine(store, config)
        result = engine.synthesize_conversation("conv_5bbf3990a8ce4b47")

    status = PASS
    status = _assert(result.deterministic_count >= 1, "created at least one deterministic extract") or status
    status = _assert(len(result.proposed_ids) >= 1, "created at least one PROPOSED document") or status
    status = _assert(not result.llm_drafted, "LLM stayed off by default") or status
    status = _assert(result.llm_error is None, "no LLM error when LLM disabled") or status
    return status


def smoke_accept_path() -> str:
    print("\n[SMOKE] explicit Accept path")
    db = _copy_fixture()
    with LivingStore(db) as store:
        config = EngineConfig.from_env(use_llm=False)
        engine = HybridSynthesisEngine(store, config)
        result = engine.synthesize_conversation("conv_5bbf3990a8ce4b47")

        status = PASS
        status = _assert(len(result.proposed_ids) >= 1, "proposals exist before Accept") or status
        if result.proposed_ids:
            doc_id = result.proposed_ids[0]
            store.accept_document(doc_id)
            working = store.list_working_documents()
            proposed = store.list_proposed_documents(hybrid_only=False, include_themes=True)
            status = _assert(
                any(d["id"] == doc_id and d["status"] == "WORKING" for d in working),
                "Accept moved document to WORKING",
            ) or status
            status = _assert(
                not any(d["id"] == doc_id for d in proposed),
                "Accepted document no longer appears in PROPOSED list",
            ) or status
        status = _assert(
            all(d.get("status") != "CANONICAL" for d in store.list_working_documents()),
            "no CANONICAL documents were written",
        ) or status
    return status


def smoke_quiet_list() -> str:
    print("\n[SMOKE] quiet list-proposed hides Theme:* by default")
    db = _copy_fixture()
    with LivingStore(db) as store:
        config = EngineConfig.from_env(use_llm=False)
        engine = HybridSynthesisEngine(store, config)
        result = engine.synthesize_conversation("conv_5bbf3990a8ce4b47")

    with LivingStore(db) as store:
        all_rows = store.list_proposed_documents(hybrid_only=False, include_themes=True)
        theme_rows = [r for r in all_rows if (r.get("title") or "").startswith("Theme:")]
        quiet_rows = store.list_proposed_documents(hybrid_only=True, include_themes=False)

    status = PASS
    status = _assert(result.deterministic_count >= len(theme_rows), "deterministic path produced Theme:* rows") or status
    status = _assert(len(theme_rows) >= 1, "at least one Theme:* row exists to be hidden") or status
    status = _assert(len(quiet_rows) >= 1, "quiet list still shows non-theme hybrid rows") or status
    status = _assert(
        not any((r.get("title") or "").startswith("Theme:") for r in quiet_rows),
        "quiet list hides Theme:* rows",
    ) or status
    status = _assert(
        all(
            (r.get("attribution") or "").startswith("hybrid:")
            or r.get("engine") in ("deterministic", "llm")
            for r in quiet_rows
        ),
        "quiet list only hybrid rows",
    ) or status
    return status


def smoke_list_flags() -> str:
    print("\n[SMOKE] list-proposed flags")
    db = _copy_fixture()
    with LivingStore(db) as store:
        config = EngineConfig.from_env(use_llm=False)
        engine = HybridSynthesisEngine(store, config)
        engine.synthesize_conversation("conv_5bbf3990a8ce4b47")

    with LivingStore(db) as store:
        quiet = store.list_proposed_documents(hybrid_only=True, include_themes=False)
        with_themes = store.list_proposed_documents(hybrid_only=True, include_themes=True)
        all_rows = store.list_proposed_documents(hybrid_only=False, include_themes=True)
        limited = store.list_proposed_documents(hybrid_only=True, include_themes=False, limit=2)

    status = PASS
    status = _assert(len(quiet) <= len(with_themes), "--themes shows at least as many rows as quiet") or status
    status = _assert(len(with_themes) <= len(all_rows), "--all shows at least as many rows as hybrid-only") or status
    status = _assert(len(limited) <= 2, "--limit caps output") or status
    return status


def smoke_llm_fail_closed() -> str:
    print("\n[SMOKE] LLM fail-closed path (no reachable model)")
    db = _copy_fixture()
    with LivingStore(db) as store:
        # Point at a port that is almost certainly closed.
        config = EngineConfig(
            llm_base="http://127.0.0.1:65432/v1",
            llm_model="no-such-model",
            deterministic_only=False,
        )
        engine = HybridSynthesisEngine(store, config)
        result = engine.synthesize_conversation("conv_5bbf3990a8ce4b47")

    status = PASS
    status = _assert(result.deterministic_count >= 1, "deterministic path still ran") or status
    status = _assert(not result.llm_drafted, "LLM did not silently draft") or status
    status = _assert(result.llm_error is not None, "LLM error recorded (fail-closed)") or status
    status = _assert(
        "unreachable" in result.llm_error.lower() or "failed" in result.llm_error.lower(),
        "error indicates endpoint failure",
    ) or status
    return status


def smoke_no_canonical() -> str:
    print("\n[SMOKE] no CANONICAL writes")
    db = _copy_fixture()
    with LivingStore(db) as store:
        config = EngineConfig.from_env(use_llm=False)
        engine = HybridSynthesisEngine(store, config)
        engine.synthesize_conversation("conv_5bbf3990a8ce4b47")
        cur = store._con.execute("SELECT COUNT(*) AS n FROM codex_document WHERE status = 'CANONICAL'")
        canonical_count = cur.fetchone()["n"]
    return _assert(canonical_count == 0, f"zero CANONICAL rows (found {canonical_count})")


def smoke_mock_llm() -> str:
    print("\n[SMOKE] mock LLM path (gated by SOLBIAN_LLM_MOCK=1)")
    db = _copy_fixture()
    old_mock = os.environ.get("SOLBIAN_LLM_MOCK")
    os.environ["SOLBIAN_LLM_MOCK"] = "1"
    try:
        with LivingStore(db) as store:
            config = EngineConfig.from_env(use_llm=True)
            engine = HybridSynthesisEngine(store, config)
            result = engine.synthesize_conversation("conv_5bbf3990a8ce4b47")
    finally:
        if old_mock is None:
            os.environ.pop("SOLBIAN_LLM_MOCK", None)
        else:
            os.environ["SOLBIAN_LLM_MOCK"] = old_mock

    status = PASS
    status = _assert(result.llm_drafted, "mock LLM produced a draft") or status
    status = _assert(
        len(result.proposed_ids) > result.deterministic_count,
        "mock LLM added an extra proposal",
    ) or status

    with LivingStore(db) as store:
        proposals = store.list_proposed_documents(hybrid_only=True, include_themes=True)
        hybrid_llm = [
            p
            for p in proposals
            if (p.get("attribution") or "").startswith("hybrid:llm")
            or p.get("engine") == "llm"
        ]
        status = _assert(
            len(hybrid_llm) >= 1,
            "at least one hybrid:llm PROPOSED exists",
        ) or status
    return status


def smoke_live_llm() -> str:
    print("\n[SMOKE] optional live LLM (gated by SOLBIAN_LLM_SMOKE=1)")
    if os.getenv("SOLBIAN_LLM_SMOKE") not in ("1", "true", "yes"):
        return _assert(True, "SKIPPED - set SOLBIAN_LLM_SMOKE=1 to run live LLM smoke")

    db = _copy_fixture()
    with LivingStore(db) as store:
        config = EngineConfig.from_env(use_llm=True)
        engine = HybridSynthesisEngine(store, config)
        result = engine.synthesize_conversation("conv_5bbf3990a8ce4b47")

    if result.llm_error and (
        "unreachable" in result.llm_error.lower() or "failed" in result.llm_error.lower()
    ):
        return _assert(True, f"SKIPPED - live LLM unreachable: {result.llm_error}")

    status = PASS
    status = _assert(result.llm_drafted, "live LLM produced a draft") or status
    status = _assert(
        len(result.proposed_ids) > result.deterministic_count,
        "LLM added an extra proposal",
    ) or status
    return status


def main() -> int:
    print("Codex Solbian Hybrid Synthesis Engine — smoke tests")
    results = [
        smoke_default_db_path(),
        smoke_historical_corpus_guard(),
        smoke_deterministic(),
        smoke_accept_path(),
        smoke_quiet_list(),
        smoke_list_flags(),
        smoke_llm_fail_closed(),
        smoke_no_canonical(),
        smoke_mock_llm(),
        smoke_live_llm(),
    ]
    print("\n[SUMMARY]")
    print(f"  Results: {results}")
    if FAIL in results:
        print("  OVERALL: FAIL")
        return 1
    print("  OVERALL: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
