#!/usr/bin/env bash
# Stage 7 -> Stage 4 installer.
#
# The Stage 7 sandbox is workspace-write, so the Stage 4 tree could not be
# modified in place while building this stage.  All Stage 4 changes are staged
# under `_stage4_build/` and this script installs them.
#
#     bash apply_to_stage4.sh
#
# It is idempotent: originals are backed up once under `_stage4_build/backup/`,
# then the staged files (plus the shared living_store.py) are copied in.  The
# living store migration is attempted at the end (the app also auto-migrates on
# startup, so a failure here is not fatal).
set -euo pipefail

STAGE7_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAGE4_DIR="${SOLBIAN_STAGE4_DIR:-/Users/archcore/solbian/codex-phase-i-stage4}"
BUILD_DIR="$STAGE7_DIR/_stage4_build"
BACKUP_DIR="$BUILD_DIR/backup"

if [ ! -d "$STAGE4_DIR" ]; then
  echo "apply_to_stage4: Stage 4 dir not found: $STAGE4_DIR" >&2
  exit 2
fi

mkdir -p "$BACKUP_DIR" "$STAGE4_DIR/static"

# Back up (once) the files we are about to replace.
for rel in app.py smoke_ui.py static/index.html static/app.js static/style.css; do
  src="$STAGE4_DIR/$rel"
  dst="$BACKUP_DIR/$rel"
  if [ -f "$src" ] && [ ! -f "$dst" ]; then
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    echo "backup  $rel -> _stage4_build/backup/$rel"
  fi
done

# Install the staged Stage 4 files.
cp "$BUILD_DIR/app.py"                 "$STAGE4_DIR/app.py"
cp "$BUILD_DIR/smoke_ui.py"            "$STAGE4_DIR/smoke_ui.py"
cp "$BUILD_DIR/static/index.html"      "$STAGE4_DIR/static/index.html"
cp "$BUILD_DIR/static/app.js"          "$STAGE4_DIR/static/app.js"
cp "$BUILD_DIR/static/style.css"       "$STAGE4_DIR/static/style.css"
# Shared living-store core (single source of truth lives in Stage 7 root).
cp "$STAGE7_DIR/living_store.py"       "$STAGE4_DIR/living_store.py"
cp "$STAGE7_DIR/living_loop.py"        "$STAGE4_DIR/living_loop.py" 2>/dev/null || true

echo "installed app.py, smoke_ui.py, static/*, living_store.py -> $STAGE4_DIR"

# Prepare the living store (analysis_run + one-time Stage 5 seed).
LIVING_DB="$STAGE4_DIR/data/codex_phase_i.sqlite"
if [ -f "$LIVING_DB" ]; then
  echo "migrating living store: $LIVING_DB"
  ( cd "$STAGE7_DIR" && python3 living_store.py --db "$LIVING_DB" migrate ) \
    || echo "apply_to_stage4: migration skipped (the app auto-migrates on startup)" >&2
else
  echo "apply_to_stage4: living store not found yet ($LIVING_DB); app will build it" >&2
fi

echo
echo "Done. Verify with:"
echo "  cd $STAGE4_DIR && python3 smoke_ui.py"
echo "  cd $STAGE7_DIR && python3 smoke_stage7.py"
