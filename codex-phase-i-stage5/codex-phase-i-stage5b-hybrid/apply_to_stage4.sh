#!/usr/bin/env bash
# Optional Stage 4 UI hook instructions.
#
# This script does not modify the Mac Stage 4 build directly; it documents the
# exact integration points for the Partner who has write access to the Mac.
#
# If the DSH sandbox blocked Stage 4 writes, this file plus stage4_ui/ contains
# the build artifacts to apply manually.

set -euo pipefail

MAC_STAGE4="${MAC_STAGE4:-/Users/archcore/solbian/codex-phase-i-stage4}"
MAC_STAGE5="${MAC_STAGE5:-/Users/archcore/solbian/codex-phase-i-stage5}"
HYBRID_DIR="${MAC_STAGE5}/codex-phase-i-stage5b-hybrid"

echo "=== Stage 4 integration points ==="
echo ""
echo "Default living DB (used when --db is omitted):"
echo "  ${MAC_STAGE4}/data/codex_phase_i.sqlite"
echo "Override with SOLBIAN_LIVING_DB if the live store is elsewhere."
echo ""
echo "1. Copy or link the engine into a Stage 4 accessible path:"
echo "   ln -s \"${HYBRID_DIR}\" \"${MAC_STAGE4}/hybrid-engine\""
echo ""
echo "2. Add a 'Synthesize dialogue' button to the conversation review page."
echo "   See: ${HYBRID_DIR}/stage4_ui/README.md"
echo "   See: ${HYBRID_DIR}/stage4_ui/synthesize_button.html"
echo ""
echo "3. Wire the button to the deterministic path (default, safe):"
echo "   POST /api/synthesize?conversation_id=conv_5bbf3990a8ce4b47"
echo "   Handler:"
echo "     python3 \"${HYBRID_DIR}/engine.py\" \\"
echo "         synthesize-dialogue --conversation \${conversation_id}"
echo "   This uses the default Stage 4 living DB and never writes the historical"
echo "   corpus."
echo ""
echo "4. Wire an optional 'Draft with LLM' action behind explicit confirm or ?llm=1:"
echo "   POST /api/synthesize?conversation_id=...&llm=1"
echo "   Handler:"
echo "     python3 \"${HYBRID_DIR}/engine.py\" --llm \\"
echo "         synthesize-dialogue --conversation \${conversation_id}"
echo ""
echo "5. Display PROPOSED candidates on the review surface alongside source turns."
echo "   Use provenance_link to map each candidate back to message IDs."
echo "   Default list-proposed is quiet (hybrid-only, Theme:* hidden). Add --verbose"
echo "   to the review surface if you want archaeology proposals and themes visible."
echo ""
echo "6. Keep Accept as a human-only action in the UI:"
echo "   POST /api/accept?document_id=..."
echo "   Handler:"
echo "     python3 \"${HYBRID_DIR}/engine.py\" accept --document \${document_id}"
echo ""
echo "Done. No Stage 4 files were modified by this script."
