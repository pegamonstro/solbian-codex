#!/usr/bin/env python3
"""Stage 7 — one-time living-store migration.

Seeds the Stage 5 engine tables (``analysis_run`` + PROPOSED ``proposal`` /
``concept`` / ``relationship`` / ``provenance_link`` rows) into the living store:
``/Users/archcore/solbian/codex-phase-i-stage4/data/codex_phase_i.sqlite``.

Idempotent: rows are copied with ``INSERT OR IGNORE`` and the seed is skipped
once the living store already has proposals (use ``--force`` to top it up).

    python3 migrate_living_store.py            # migrate the living store
    python3 migrate_living_store.py --info     # show counts + policy (no writes)
    python3 migrate_living_store.py --force    # re-run the seed
"""

from __future__ import annotations

import argparse
import os
import sys

import living_store as ls


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Stage 7 living-store migration")
    p.add_argument("--db", default=None, help=f"living store (default: {ls.LIVING_DB})")
    p.add_argument("--stage5-db", default=ls.STAGE5_DB,
                   help="Stage 5 seed store (read-only)")
    p.add_argument("--force", action="store_true", help="re-run the seed")
    p.add_argument("--info", action="store_true", help="show counts + policy only")
    args = p.parse_args(argv)

    db = ls.resolve_living_db(args.db)
    if not os.path.exists(db):
        print(f"living store not found: {db}", file=sys.stderr)
        return 2

    if args.info:
        with ls.connect(db) as conn:
            ls.ensure_base_schema(conn)
            meta = ls.living_meta(conn)
        print(f"living_db: {db}")
        print(f"policy   : {meta['policy']}")
        print("counts   : " + ", ".join(
            f"{k}={v}" for k, v in meta["counts"].items()))
        return 0

    with ls.connect(db) as conn:
        summary = ls.migrate(conn, args.stage5_db, force=args.force)
    print(f"living_db : {db}")
    print(f"stage5_db : {summary['stage5_db']}")
    print(f"seeded    : {summary['seeded']} ({summary['reason']})")
    print("copied    : " + ", ".join(
        f"{k}={v}" for k, v in summary["copied"].items()))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ls.LivingStoreError as exc:
        print(f"migrate error: {exc}", file=sys.stderr)
        raise SystemExit(2)
