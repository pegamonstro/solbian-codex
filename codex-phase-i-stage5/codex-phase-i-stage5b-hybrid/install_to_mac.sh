#!/usr/bin/env bash
# Install the Hybrid Synthesis Engine onto the Mac Stage 5 area.
# Run this script on the Mac (rpi4 cannot assume a writable Mac mount).
#
# It copies the portable package from the DSH workspace to the canonical
# Stage 5 directory and prints the commands needed to run smoke against a
# throwaway copy of the Stage 4/7 living store.

set -euo pipefail

DSH_SRC="${DSH_SRC:-$(cd "$(dirname "$0")" && pwd)}"
MAC_STAGE5="${MAC_STAGE5:-/Users/archcore/solbian/codex-phase-i-stage5}"
MAC_STAGE4="${MAC_STAGE4:-/Users/archcore/solbian/codex-phase-i-stage4}"
MAC_STAGE7="${MAC_STAGE7:-/Users/archcore/solbian/codex-phase-i-stage7}"

HYBRID_DIR="${MAC_STAGE5}/codex-phase-i-stage5b-hybrid"

echo "=== Codex Solbian Hybrid Synthesis Engine install ==="
echo "Source:  ${DSH_SRC}"
echo "Target:  ${HYBRID_DIR}"
echo "Stage 4: ${MAC_STAGE4}"
echo "Stage 7: ${MAC_STAGE7}"

# 1. Wipe old copy and install fresh package.
rm -rf "${HYBRID_DIR}"
mkdir -p "${MAC_STAGE5}"
cp -R "${DSH_SRC}" "${HYBRID_DIR}"

# 2. Ensure the package is executable.
chmod +x "${HYBRID_DIR}/engine.py"
chmod +x "${HYBRID_DIR}/smoke_hybrid.py"
chmod +x "${HYBRID_DIR}/fixtures/build_fixture_db.py"

echo ""
echo "Installed files:"
find "${HYBRID_DIR}" -maxdepth 2 -type f | sort

echo ""
echo "=== Smoke ==="
echo "Run the built-in smoke suite:"
echo "  cd ${HYBRID_DIR}"
echo "  python3 smoke_hybrid.py"
echo ""
echo "Optional mock-LLM smoke (no running model required):"
echo "  SOLBIAN_LLM_MOCK=1 python3 smoke_hybrid.py"
echo ""

echo "=== Smoke on throwaway copy of living store ==="
echo "Make a copy of the Stage 4/7 living DB and run the engine:"
echo ""
LIVING="${MAC_STAGE4}/data/codex_phase_i.sqlite"
if [ ! -f "$LIVING" ]; then
    echo "  # Living DB not found at ${MAC_STAGE4}/data/codex_phase_i.sqlite"
    echo "  # Adjust LIVING to the actual Stage 4/7 SQLite path or set SOLBIAN_LIVING_DB."
fi
echo "  cp \"\${LIVING}\" /tmp/codex_hybrid_smoke.sqlite"
echo "  python3 \"${HYBRID_DIR}/engine.py\" --db /tmp/codex_hybrid_smoke.sqlite \\"
echo "      synthesize-dialogue --conversation conv_5bbf3990a8ce4b47"
echo ""
echo "Because the default DB is the Stage 4 living store, you can also run"
echo "against the live DB with care (do not use on a production DB until"
echo "smoke passes on a copy):"
echo ""
echo "  python3 \"${HYBRID_DIR}/engine.py\" \\"
echo "      synthesize-dialogue --conversation conv_5bbf3990a8ce4b47"
echo ""
echo "Then inspect proposals and Accept explicitly:"
echo ""
echo "  python3 \"${HYBRID_DIR}/engine.py\" --db /tmp/codex_hybrid_smoke.sqlite list-proposed"
echo "  python3 \"${HYBRID_DIR}/engine.py\" --db /tmp/codex_hybrid_smoke.sqlite accept --document <ID>"
echo ""
echo "Quieter list flags:"
echo "  list-proposed                 # hybrid-only, Theme:* hidden"
echo "  list-proposed --themes        # include Theme:*"
echo "  list-proposed --all           # include older Stage-5 archaeology"
echo "  list-proposed --verbose       # --all --themes"
echo "  list-proposed --limit 10      # cap output"
echo ""

echo "=== Optional: enable LLM draft ==="
echo "  export SOLBIAN_LLM_BASE=http://localhost:11434/v1"
echo "  export SOLBIAN_LLM_MODEL=kimi-k2.7-code:cloud"
echo "  python3 \"${HYBRID_DIR}/engine.py\" --db /tmp/codex_hybrid_smoke.sqlite --llm \\"
echo "      synthesize-dialogue --conversation conv_5bbf3990a8ce4b47"
echo ""
echo "If Ollama is unreachable, the deterministic path still runs and a"
echo "fail-closed LLM error is recorded."
echo ""

echo "=== Stage 4 UI hook ==="
echo "See ${HYBRID_DIR}/stage4_ui/README.md"
echo "See ${HYBRID_DIR}/apply_to_stage4.sh"
echo "See ${HYBRID_DIR}/APPLY_MAC.md"
echo ""
echo "Install complete: ${HYBRID_DIR}"
