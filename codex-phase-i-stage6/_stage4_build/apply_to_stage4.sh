#!/usr/bin/env bash
# Apply the Stage 4 Engine/Proposals tab from this staged bundle.
#
# The DSH file sandbox for the Stage 6 session only permits writes inside the
# Stage 6 workspace, so the modified Stage 4 files could not be installed
# directly. Run this script (outside that sandbox) to install them:
#
#     bash /Users/archcore/solbian/codex-phase-i-stage6/_stage4_build/apply_to_stage4.sh
#
# It backs up the existing files, copies the Engine-tab versions in, and runs
# the Stage 4 smoke test. Idempotent: re-running just re-installs + re-tests.

set -euo pipefail

BUILD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAGE4_DIR="${1:-/Users/archcore/solbian/codex-phase-i-stage4}"

if [[ ! -d "$STAGE4_DIR" ]]; then
  echo "ERROR: Stage 4 dir not found: $STAGE4_DIR" >&2
  exit 2
fi

STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$BUILD_DIR/_backup_$STAMP"
mkdir -p "$BACKUP_DIR/static"

echo "[apply] build   : $BUILD_DIR"
echo "[apply] stage4  : $STAGE4_DIR"
echo "[apply] backup  : $BACKUP_DIR"

# Back up current files (if present).
for f in app.py smoke_ui.py README.md DSH_RESULT.md; do
  [[ -f "$STAGE4_DIR/$f" ]] && cp -p "$STAGE4_DIR/$f" "$BACKUP_DIR/$f"
done
for f in index.html app.js; do
  [[ -f "$STAGE4_DIR/static/$f" ]] && cp -p "$STAGE4_DIR/static/$f" "$BACKUP_DIR/static/$f"
done

# Install the Engine-tab versions.
cp "$BUILD_DIR/app.py"                    "$STAGE4_DIR/app.py"
cp "$BUILD_DIR/smoke_ui.py"               "$STAGE4_DIR/smoke_ui.py"
cp "$BUILD_DIR/README.md"                 "$STAGE4_DIR/README.md"
[[ -f "$BUILD_DIR/DSH_RESULT.md" ]] && cp "$BUILD_DIR/DSH_RESULT.md" "$STAGE4_DIR/DSH_RESULT.md"
cp "$BUILD_DIR/static/index.html"         "$STAGE4_DIR/static/index.html"
cp "$BUILD_DIR/static/app.js"             "$STAGE4_DIR/static/app.js"
chmod 644 "$STAGE4_DIR/app.py" "$STAGE4_DIR/smoke_ui.py" \
          "$STAGE4_DIR/README.md" "$STAGE4_DIR/DSH_RESULT.md" \
          "$STAGE4_DIR/static/index.html" "$STAGE4_DIR/static/app.js" 2>/dev/null || true

echo "[apply] installed; running python3 smoke_ui.py ..."
cd "$STAGE4_DIR"
python3 smoke_ui.py
echo "[apply] DONE (exit 0)"
