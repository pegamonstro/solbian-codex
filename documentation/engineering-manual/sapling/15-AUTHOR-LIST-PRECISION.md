# 15 — Author-List Precision in Deep-Research Citations

> **A Wave-7 finding**: several deep-research
> entries have imprecise author lists. The
> imprecision falls into four patterns: missing
> authors (Differentiable Plasticity), abbreviated
> lists ("et al." where the full list is
> canonical), wrong author names (HTM "Cui"
> fabrication), and bundle attributions
> (multiple papers under one author list). This
> chapter names the patterns, proposes a
> precision convention, and lists the specific
> entries that need updating.

## Why this chapter

A research knowledge base is only as useful as
its citations. An author list that drops a name
or invents one propagates downstream: a future
reader who searches for the dropped author's
work will not find this paper, and a future
verifier who searches for the invented author's
work will find nothing and flag the entry.

The Wave 6 / Wave 7 verification passes caught
several author-list issues that prior authoring
passes missed. They are recorded here so the next
authoring pass can apply the precision convention
proposed below.

## The four patterns

### Pattern 1: Missing authors

The entry's `**Year / citation**` field lists
fewer authors than the canonical paper. This is
usually an oversight (the author recalled the
first three names and wrote "et al."), but it
degrades the entry's value as a citation
reference.

**Example**: §4.6 Differentiable Plasticity in
`neuro-primitives.md` and §1.10 in
`nslp-algorithms.md` both cite "Miconi et al.
2018" or "Miconi, Clune, Stanley 2018" — the
real paper has 4 authors (Miconi, Rawal, Clune,
Stanley). The missing author is **Aditya Rawal**,
who is the second author on the ICML 2018 paper.

### Pattern 2: Wrong author names (LLM hallucination)

The entry's `**Year / citation**` field lists
authors who did not write the paper. This is
almost always an LLM hallucination (the model
knew the topic but invented the author list).

**Example**: §1.1 HTM in `memory-reasoning.md`
cited "Hawkins, Ahmad, Cui 2017" for the paper
"Why Neurons Have Thousands of Synapses." The
real paper is by **Hawkins and Ahmad** (2
authors, not 3). The "Cui" is a hallucination.

### Pattern 3: Abbreviated lists

The entry writes "X et al. YYYY" for a paper
where the full author list is canonical and
should be reproduced. This is acceptable in
some contexts (a 19-author DQN paper, a
50-author LLM paper) but is incorrect for
small-author-list papers (≤4 authors) where
the full list is short and canonical.

**Example**: §6.6 Decision Transformer in
`cognitive-cycles.md` cites "Chen et al. 2021"
for a paper with 9 authors. The full list is
**Lili Chen, Kevin Lu, Aravind Rajeswaran,
Kimin Lee, Adithyavairavan Murali, Mohit
Hessel, Pieter Abbeel, Aravind Srinivas, Igor
Mordatch** (first three contributed equally).
For a 9-author paper, the full list is
canonical.

### Pattern 4: Bundle attributions

The entry cites multiple papers under one
author list (e.g., "Silver et al. 2016, 2017,
2018" for the AlphaGo/AlphaZero family). This
is acceptable in narrative form but is a
citation precision issue if the entry's claims
differ across the bundled papers (e.g., "MuZero
learns the rules of the game from scratch" is
attributed to Silver 2018 in the bundle, but
the real paper is **Schrittwieser 2020**, *Nature*
588: 604–609).

**Example**: §6.3 in `cognitive-cycles.md`
cites "Silver et al. 2016, 2017, 2018
(AlphaGo/Zero/MuZero)" as a single bundle.
The real attributions are:

- AlphaGo: Silver et al. 2016, *Nature* 529:
  484–489.
- AlphaGo Zero: Silver et al. 2017, *Nature*
  550: 354–359.
- AlphaZero: Silver et al. 2018, *Science* 362:
  1140–1144.
- MuZero: **Schrittwieser et al. 2020**,
  *Nature* 588: 604–609. (Different first
  author.)

The MuZero attribution in the bundle is wrong;
the entry's description matches Schrittwieser
2020, not Silver 2018.

## The precision convention

Future authoring passes on the deep-research
files (and on any new solbian research content)
should follow this convention for the
`**Year / citation**` field:

1. **For papers with ≤4 authors**: list every
   author by surname. The full list is short
   and canonical. Example: "Miconi, Rawal,
   Clune & Stanley 2018."

2. **For papers with 5-10 authors**: list every
   author by surname if the entry is making a
   load-bearing claim about the paper's content;
   abbreviate to "FirstAuthor et al. YYYY" if
   the entry is just citing the paper as
   background. Example: a Decision Transformer
   entry that explains the architecture should
   list all 9 authors; an entry that mentions
   Decision Transformer in passing should
   abbreviate.

3. **For papers with >10 authors**: abbreviate
   to "FirstAuthor et al. YYYY" always. Listing
   all 19 DQN authors adds noise without value.

4. **Never invent author names.** If the author
   cannot recall the full list, write "et al."
   and add a `**Notes**` line: "full author list
   at the canonical reference URL." This is
   better than guessing.

5. **Never copy an author list from a different
   paper.** A bundle like "Silver et al. 2016,
   2017, 2018 (AlphaGo/Zero/MuZero)" is a
   *narrative* attribution; it should not be
   used as a *citation*. Each paper gets its
   own author list and year.

6. **Always verify the author list against the
   canonical reference URL.** The URL is the
   source of truth. The author's parametric
   memory of the author list is not.

## Specific entries that need updating

The Wave 7 verification log records the
discrepancies. The next authoring pass should
update the following entries:

### `nslp-algorithms.md` (Wave 6)

- §1.10 Differentiable Plasticity: 3 authors →
  4 (add Rawal between Miconi and Clune).
  *Pending re-edit; the verification log
  flagged the count but the parent file was
  not updated.*
- §4.6 Learned Optimization: 7 authors → 8
  (add Shillingford between Schaul and de
  Freitas). The Wave 6 verification caught
  this and applied the correction.

### `cognitive-cycles.md` (Wave 7)

- §6.3 MCTS / AlphaGo family: split the bundle
  into 4 separate citations (Silver 2016,
  Silver 2017, Silver 2018, Schrittwieser 2020)
  with correct first authors and venues.
- §6.6 Decision Transformer: "Chen et al."
  → 9 authors (Chen, Lu, Rajeswaran, Lee,
  Murali, Hessel, Abbeel, Srinivas, Mordatch).

### `memory-reasoning.md` (Wave 7)

- §1.1 HTM: 3 authors → 2 (remove the
  hallucinated "Cui"). The real paper is
  Hawkins & Ahmad 2017.

### `neuro-primitives.md` (Wave 7)

- §4.6 Differentiable Plasticity: 3 authors →
  4 (add Rawal). Same fix as the nslp-algorithms
  §1.10 entry; the two files should agree.

## How to read this chapter

If you are authoring a new entry:

1. Open the canonical reference URL and copy
   the exact author list. Do not paraphrase.
2. For small-author-list papers (≤4), list
   everyone.
3. For bundle attributions, split into
   separate citations.

If you are running a verification wave:

1. For every entry, fetch the canonical
   reference URL.
2. Compare the entry's author list to the URL's
   author list.
3. If they differ, flag the entry 🟢 and add a
   `**Notes**` line describing the discrepancy.
4. For load-bearing claims (the entry makes a
   specific assertion about the paper's content),
   the author list must be exact. Set the flag
   to 🟢 and request a correction.

If you are a future reader of the deep-research
files:

1. If an entry has "et al." where you would
   expect a full list, the entry is using the
   abbreviation convention. Open the canonical
   reference URL to get the full list.
2. If an entry's author list is shorter than
   expected, the entry may be a candidate for
   the next precision pass.

## See also

- [`../sapling/13-DETECTING-LLM-HALLUCINATIONS.md`](13-DETECTING-LLM-HALLUCINATIONS.md) —
  the LLM hallucination pattern. Pattern 2
  (wrong author names) above is the LLM
  hallucination pattern applied to author
  lists; the verification contract in chapter
  13 covers the same ground.
- [`../sapling/12-DISCOVERY-PATTERN.md`](12-DISCOVERY-PATTERN.md) — the
  DRIRR document pattern. The precision
  convention above is the DRIRR pattern's
  "Decision" applied to citation metadata.
- `sapling/NSLP/deep-research/verification/claude-verifier-2026-07-17*.md` —
  the Wave 6 and Wave 7 verification logs,
  which record the specific author-list
  discrepancies per entry.
