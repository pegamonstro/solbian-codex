# S.A.T.I. Academy — Project Spec (Standalone; Codex-Compatible)
DOC_VERSION: 1.0.0
DATE: 2025-10-25
STATUS: active

## Purpose
A symbolic adaptive tutoring interface providing tailored lessons across a **tree of subjects/skills**.
Students earn **merit points** to unlock tasks/projects and progress along personalised trajectories.

## Data Model (SREF/NDJSON)
- `student.sref` (`identity.schema.json`)
- `subject.sref` (TREE; tags, prerequisites, mastery thresholds)
- `lesson.sref` (content, difficulty, outcomes, rubric)
- `assessment.sref` (rubrics, archetype signals, MAP-C context)
- `project.sref` (deliverables, peer review, MAP-S symbolic links)

## Merit Logic
- Each subject defines **thresholds** for unlocking next tasks.
- Merit points accrue via **lessons → assessments → projects**.
- Projects add **symbolic continuity** (MAP-S) to the student's record.

## Integration
- SREF v5 envelopes (see `schema/`).
- Interoperable with S.E.E.D. **MAP-C/MAP-S** memory contracts.
- Export and import via NDJSON streams.
