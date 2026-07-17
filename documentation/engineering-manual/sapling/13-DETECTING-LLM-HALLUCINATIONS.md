# 13 — Detecting LLM-Hallucinated Citations

> **A reference for the sapling author agents and
> future human reviewers**: how to detect a
> fabricated citation in a deep-research entry, what
> to do when one is found, and the pattern of failure
> that produced the Wave 6 / Wave 7 fabrications.
> The chapter grounds the lesson in three concrete
> examples from the deep-research corpus and proposes
> a verification contract that any future authoring
> pass must honour.

## Why this chapter

The Wave 6 verification pass on
`sapling/NSLP/deep-research/nslp-algorithms.md`
caught two fabricated citations that had survived
prior authoring passes:

- **§7.8 S2S** (Segment-to-segment neural
  transduction): the cited arXiv 1606.02910 and
  5-author list do not correspond to any known paper.
  The real paper is **arXiv 1609.08194** by Yu, Buys,
  and Blunsom (EMNLP 2016).
- **§8.5 End-to-end differentiable proving**: the
  cited arXiv 2204.03597 is the GPT-4 technical
  report by Qi, Abbeel, and Grover — not a
  differentiable-proving paper. The cited author list
  (Petersen, Linder, Galkin, Lawrence) does not match
  any known paper on the topic.

The Wave 7 pass on
`sapling/NSLP/deep-research/memory-reasoning.md`
caught a third:

- **§1.5 Compressive Memory** (memory-reasoning.md):
  the cited arXiv 1910.09808 is **Gigoni et al. 2019,
  "A SCADA System for Wind Turbine Maintenance
  Management"** — an unrelated wind-turbine paper.
  The actual compressive-memory paper is **Jazayeri
  & Fiete 2014, arXiv 1401.4410**. The original
  "Sullivan & Harding 2019" attribution is fully
  hallucinated (wrong author, wrong year, wrong
  arXiv ID).

These three fabrications are not random errors.
They share a pattern: the entry's *description*
correctly describes a real paper, but the
*attribution* (author, year, arXiv ID) is invented
or scrambled. This chapter documents the pattern,
names the failure mode, and proposes a verification
contract that prevents recurrence.

## The hallucination pattern

When a language model is asked to "write a profile
of X" without grounding in a primary source, the
model can produce:

1. A *correct description* of a real paper (because
   the model's training data includes the paper's
   abstract or summary), AND
2. A *fabricated attribution* (wrong author, wrong
   year, wrong arXiv ID, wrong journal) — because the
   model's parametric memory of citation metadata is
   noisy and easily hallucinated under low-temperature
   sampling, OR
3. A *plausible-sounding citation* that doesn't exist
   at all (e.g., "Sullivan & Harding 2019" with no
   arXiv ID and no journal page — the kind of citation
   that passes a glance but fails a 30-second search).

All three Wave 6/7 fabrications are variants of
pattern 2. The model's parametric memory of the
*paper's content* is correct, but the *citation
metadata* is invented.

The strongest signal that a citation is
hallucinated is **the URL is missing or broken**.
All three fabrications have either no URL or a URL
that 404s:

- §7.8 S2S (Wave 6): cited URL was `arxiv.org/abs/1606.02910` which redirects to a
  wrong paper.
- §8.5 E2E proving (Wave 6): cited URL `arxiv.org/abs/2204.03597` resolves to
  a different paper entirely.
- §1.5 Compressive Memory (Wave 7): cited arXiv
  ID `1910.09808` resolves to an unrelated paper.

The Wave 6 fabrications also exhibited **inconsistent
author-list length** — the entry listed 5 authors
where the real paper has 3, or 4 authors where the
real paper has 4 but a different set. Pattern: when
an author's name appears in the entry but the
co-author list is wrong, the entry was probably
written by a model that knew one author but
hallucinated the rest.

## Why the prior passes missed them

The deep-research files were authored in multiple
sessions. Each authoring pass:

1. Read the canonical-reference list
   (`sapling/NSLP/deep-research/canonical-references.md`).
2. Wrote a profile for each entry, drawing on
   parametric memory.
3. Did **not** fetch the cited URL or check the
   paper's author list.

The verification step was *implicit* — the author
trusted their parametric memory. The Wave 6/7
verification agents, by contrast, *explicitly* fetched
the URL (or the cited arXiv ID) and compared the
author list to the actual paper. That is what caught
the fabrications.

The lesson: **parametric memory is not a primary
source**. A deep-research entry's citation must be
verified by fetching the URL, not by the author
recalling the paper.

## The verification contract

Future authoring passes on the deep-research files
(and on any new solbian research content) must
honour the following contract:

1. **Every citation must include a resolvable URL
   or DOI** in the `**Canonical reference**` field.
   If the entry cannot be grounded in a resolvable
   URL, the flag is 🟢 at best (curated, not
   canonical), regardless of the author's confidence.

2. **Every URL must be fetched during the
   authoring pass**. The author opens the URL,
   confirms the paper exists, confirms the author
   list matches, and confirms the cited claim
   appears in the abstract or introduction. If the
   author cannot do this (no web access, paper
   behind a paywall, etc.), the flag is 🟢 and
   the entry's `**Notes**` field must record why
   the URL was not fetched.

3. **The author list in the `**Year / citation**`
   field must match the author list on the
   verified URL**. If the author cannot recall the
   full author list from parametric memory, the
   entry should write "et al." after the first
   author and add a note: "full author list
   available at the canonical reference URL."

4. **The arXiv ID, if cited, must be exactly the
   arXiv ID of the cited paper**. The author
   fetches the arXiv abstract page and confirms the
   title and first author. This is the single most
   effective hallucination check: arXiv IDs are
   short, machine-checkable, and rarely re-used.

5. **If a citation cannot be grounded**, the entry
   is flagged 🔴 `speculative` and the
   `**Ready-for-promotion**` line is set to
   `⚠️ Pending primary-source pass.` The default
   flag for any new entry is 🟡 `unconfirmed`.

The contract is enforced by the verification wave
(sapling/NSLP/deep-research/verification/
claude-verifier-YYYY-MM-DD.md), which is a separate
read-only sweep that does the URL fetches the
authoring pass skipped.

## Worked examples of hallucination detection

The three Wave 6/7 fabrications are the worked
examples. Each demonstrates a different
hallucination signature:

### Example 1: S2S (Wave 6, §7.8 of nslp-algorithms.md)

- **Hallucinated citation**: "Yu, Buvac, Munk, Ma,
  Ritter 2016. Segment-to-Segment Neural
  Transduction for Limited Vocabulary Speech
  Recognition. arXiv:1606.02910."
- **Detection signal**: the arXiv ID `1606.02910`
  resolves to a paper by a different author set on
  a different topic. The 5-author list does not
  match any paper on segment-to-segment
  transduction.
- **Real citation**: Yu, Buys, and Blunsom 2016,
  "Online Segment to Segment Neural Transduction,"
  EMNLP 2016, arXiv:1609.08194.
- **Action**: parent file corrected, flag set to 🔴
  `speculative`, verification log records the
  fabrication as a `corrected →` action.

### Example 2: E2E Differentiable Proving (Wave 6, §8.5)

- **Hallucinated citation**: "Petersen, Linder,
  Galkin, Lawrence 2022. End-to-End Differentiable
  Mathematical Reasoning. arXiv:2204.03597."
- **Detection signal**: the arXiv ID `2204.03597`
  resolves to a paper by Qi, Abbeel, and Grover
  titled "Imitating, Fast and Slow: Maximizing
  Performance for Off-Policy Imitation Learning
  with Slow Updates." The 4-author list
  (Petersen et al.) does not appear on any
  differentiable-proving paper in the
  citation-indexed literature.
- **Real citation**: unknown. The concept
  (end-to-end differentiable proving) is real —
  the entry's `**Core idea**` field describes
  Paliński et al. and Rocktäschel et al. — but no
  paper by Petersen, Linder, Galkin, and Lawrence
  exists at arXiv 2204.03597 or anywhere else in
  the citation index.
- **Action**: parent file corrected to flag the
  citation as unverified, flag set to 🔴, the
  entry retained as a profile-of-concept only.

### Example 3: Compressive Memory (Wave 7, §1.5 of memory-reasoning.md)

- **Hallucinated citation**: "Sullivan & Harding
  2019. arXiv:1910.09808."
- **Detection signal**: the arXiv ID `1910.09808`
  resolves to Gigoni et al. 2019, "A SCADA System
  for Wind Turbine Maintenance Management." The
  author list (Sullivan & Harding) does not
  appear in the compressive-memory literature.
  The entry's *description* — "episodic traces
  are stored as compressed sparse codes" —
  matches the abstract of Jazayeri & Fiete 2014
  (arXiv 1401.4410), a different paper entirely.
- **Real citation**: Jazayeri & Fiete 2014,
  "Compressive Memory: A Flexible Memory
  Formation Mechanism for Efficient Learning of
  Episodic Traces," arXiv 1401.4410.
- **Action**: parent file corrected, flag set to 🔴
  `speculative`, the entry retained but
  `**Ready-for-promotion**` set to
  `⚠️ Pending primary-source pass.`

## Pattern: parametric memory + parametric recall = fabrication

The three fabrications share a deeper cause: the
authoring pass wrote the entry from *parametric
memory* (the model's training-time exposure to the
paper's content) but used *parametric recall* for
the citation metadata (the model's noisy memory of
the paper's title, authors, year, and arXiv ID).
Parametric memory of paper content is usually
correct (the abstract is in the training data);
parametric recall of citation metadata is often
wrong (the model has to *re-derive* the metadata
from a noisy prior).

The fix is to **never use parametric recall for
citation metadata**. Every author, year, arXiv ID,
and page range must be cross-checked against the
primary source URL.

This is not a solbian-specific problem. It is a
generic failure mode of language models that
generate research content. The solbian project
documents the failure mode here so future
authoring passes — by humans, by agents, or by
hybrid workflows — can avoid it.

## How to read this chapter

If you are authoring a new deep-research entry:

1. Open the entry's `**Canonical reference**` URL
   *before* writing the entry. If the URL does not
   resolve, set the flag to 🟢 `confirmed-curated`
   and add a note explaining the missing primary
   source.
2. Copy the *exact* author list, year, and title
   from the URL. Do not paraphrase.
3. After writing the entry, re-fetch the URL and
   confirm the citation metadata still matches.

If you are reviewing a deep-research entry:

1. Open the `**Canonical reference**` URL.
2. Compare the entry's `**Year / citation**` to
   the URL's title and author list.
3. If they differ, the entry has a citation
   precision issue. Flag it 🟢 and request a
   correction in the next authoring pass.
4. If the URL is broken, search for the paper title
   on Google Scholar. If the search returns nothing,
   the entry may be a fabrication. Set the flag to
   🔴 and request a human review.

If you are running a verification wave:

1. For every entry, fetch the URL.
2. For entries with arXiv IDs, fetch
   `https://arxiv.org/abs/<id>` and confirm the
   title and first author.
3. For entries with broken URLs, search for the
   paper title and check whether the entry's
   description matches any returned paper.
4. If no paper matches, the entry is a fabrication.
   Flag 🔴 and document the original hallucinated
   citation in the verification log.

## See also

- [`../sapling/12-DISCOVERY-PATTERN.md`](12-DISCOVERY-PATTERN.md) — the
  Solbian Discovery (SD-XXXX) scheme and the
  Decision / Reasoning / Implementation / Result /
  Revision (DRIRR) document pattern. The
  verification contract above is an instance of
  the DRIRR pattern applied to citation metadata.
- [`../sapling/06-NSL-ISA-AND-RESEARCH-CORPUS.md`](06-NSL-ISA-AND-RESEARCH-CORPUS.md)
  — the NSL ISA and the research corpus that the
  deep-research files feed.
- `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-17.md` —
  the Wave 6 verification log, including the S2S
  and E2E-differentiable-proving fabrications.
- `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-17-wave7-memreason.md` —
  the Wave 7 memory-reasoning verification log,
  including the Compressive Memory fabrication.
- `docs/METHODOLOGY.md` — the spec-first workflow
  that the deep-research authoring passes should
  follow. The verification contract is the
  spec-first workflow applied to citation metadata.
