# DUPLICATES — candidates only (NO merges)
**As-of:** 2026-09-20 PT · **CANONICAL:** NONE

| ID | Location A | Location B | Similarity | Differences | Confidence |
|----|------------|------------|------------|-------------|------------|
| D1 | Mac `source_original/scrolls/codex_solbian_scroll_20.sref` | Mac `…/scroll_21.sref` | Same scroll_no 21, same ids/titles/body_sig (timestamps stripped) | Raw sha256 differ; size 3611 vs 3612 (packaging/newlines) | **HIGH** |
| D2 | Mac laws A/B under `manifest/` | Box mirror same paths | Byte-identical (sha256 match this pass) | Tree HEAD differs elsewhere | **HIGH** |
| D3 | Mac full `scrolls/*.md` | Box/GH stub `scrolls/*.md` (older commits) | Same filenames | Substantive vs ~163–347 B stubs | **HIGH** (VARIANT not true dup) |
| D4 | Law catalogue **B** Mac/GH solbian-codex | Law **B′** GH seed | Same schema; B′ ⊂ B | B has 48a/48b | **HIGH** (prior VARIANTS map; B′ not re-hashed this pass) |
| D5 | Law **C** Mac seed-dsh / GH seed / rpi4 mount | Gitea LAWS.md narrative | Title alignment Continuity→Finality claimed | Format MD vs sref | **MED–HIGH** (cite LAWS_VARIANTS; C not in C1 tree) |
| D6 | Mac protocols 01–05 | Gitea PROTOCOLS.md five | Titles align | Gitea lacks 06–08 | **HIGH** |
| D7 | `/workspace/codex-solbian-working` | GH `main` / `working/synthesis-*` | Same WORKING layout family | Sync lag UNKNOWN | **MED** |
| D8 | Helios WORKING_SYNTHESIS_2026-09-20 | Box `codex-solbian-working` | Consolidation sibling | Exact byte identity not rechecked | **MED** |
| D9 | `scroll_04.sref` vs Tribunal/`scroll_05` | (prior ANOMALIES) | Possible embedded duplicate content | Not re-parsed deep this pass | **LOW–MED** (cite prior; re-verify later) |
| D10 | AppleDouble `._*` next to real files | Real files | Metadata forks | Not corpus content | **HIGH** (noise) |

**Action:** Record only. No collapse, no delete, no “winner”.
