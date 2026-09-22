"""Build a throwaway SQLite living store from the Who are we? JSON fixture."""

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from codex_hybrid.db import LivingStore


def main() -> None:
    here = Path(__file__).resolve().parent
    fixture_json = here / "who_are_we.json"
    db_path = here / "who_are_we.sqlite"

    # Always start fresh.
    if db_path.exists():
        shutil.copy(db_path, f"{db_path}.bak")
        db_path.unlink()

    with fixture_json.open() as fh:
        data = json.load(fh)

    with LivingStore(db_path) as store:
        store.ensure_core_schema()
        messages = [
            (m["role"], m["content"], m.get("created_at")) for m in data["messages"]
        ]
        store.load_fixture_conversation(
            external_id=data["external_id"],
            title=data["title"],
            messages=messages,
        )

    print(f"Built fixture DB: {db_path}")
    print(f"Conversation: {data['external_id']} - {data['title']}")
    print(f"Messages: {len(messages)}")


if __name__ == "__main__":
    main()
