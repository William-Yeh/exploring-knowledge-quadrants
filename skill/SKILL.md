---
name: exploring-knowledge-quadrants
description: >-
  Use when the user says "knowledge quadrants", "四象限", "explore quadrants",
  "KQ", or "what do I know / not know about" followed by a topic or seed.
license: Apache-2.0
metadata:
  author: William-Yeh
  version: "0.3"
---

# exploring-knowledge-quadrants

Generate a four-quadrant knowledge map for any topic or rough seed, surfacing
conscious knowledge (👁️), identified gaps (🔍), tacit knowledge (🌫️), and
hidden blind spots (🌑).

## Flags

| Flag | Values | Default | Effect |
|------|--------|---------|--------|
| `--depth` | `shallow`, `deep` | `shallow` | Controls Unknown Unknowns exploration depth |
| `--web` | (boolean) | off | Grounds Unknown Unknowns in real-world search |
| `--refresh` | `<path>` | off | Re-explores an existing KQ file: migrates items across quadrants, probes for fresh items, emits a new versioned file |

Input may be a focused topic, a rough prose description, or a seed with
`[ ]` checkbox items for suggested angles.

---

## Web Mode Pre-Phase (`--web` only)

If `--web` was specified, run these two searches **before** Phase 1:

1. Search: `<topic> domain expert concerns risks`
2. Search: `<topic> recent failures surprises`

Summarize findings in 3–5 bullets labeled "Web grounding." Inject this summary
as additional context into the Unknown Unknowns draft in Phase 1.

If `--web` was not specified, skip this section entirely.

---

## Refresh Pre-Phase (`--refresh <file>` only)

If `--refresh` was specified — or the user asks to refresh/update an existing
knowledge map (e.g. "refresh this KQ", "更新這份四象限") — run this before
Phase 1. Otherwise skip this section entirely.

1. Read the old KQ file. Extract: topic, seed-context blockquote (if any),
   version (`vN` from the metadata line; treat a file without a version
   marker as `v1`), and every bullet item per quadrant.
2. If `--web` was also specified, add a third search to the Web Mode
   Pre-Phase: `<topic> latest research evidence`.
3. **Re-assessment pass** — assign EVERY existing item one verdict:

| Verdict | Meaning | Action |
|---------|---------|--------|
| CONFIRMED | UU/UK item is now established knowledge | promote to KK |
| ANSWERED | KU item has been resolved | promote to KK |
| STILL-OPEN | unchanged | keep in place |
| AWARE-NOW | UU item the user clearly knows about now | demote to KU |
| STALE | no longer relevant | retire (appears only in the Migration Log) |

Record the non-STILL-OPEN verdicts in a migration table and display it with
the Phase 1 draft:

| Item (abbreviated) | From | To | Reason |
|--------------------|------|----|--------|
| <first ~8 words of the item> | UU | KK | <one-line reason> |

4. Run Phase 1 with two changes:
   - Seed each quadrant with the migrated items in their post-verdict
     positions.
   - Add this instruction to the probe stack: *surface only items absent
     from the old map — do not restate migrated items.*
5. In Phase 2, ask the user to review the migration table alongside the
   quadrants.
6. In Phase 3, write a NEW file dated today with the same slug — never
   modify the old file — and apply the refresh additions to the template
   (version bump + Migration Log; see Phase 3).

---

## Phase 1 — Draft Generation

### Shallow mode (default: `--depth shallow`)

Generate a draft of all four quadrants in a single response.

**👁️ Known Knowns — Conscious Knowledge**

Generate 3–5 bullets of explicit, articulable things a practitioner working
on `<topic>` would consciously know. Focus on the core mental model and
established facts. Each bullet: one sentence + brief note on why it matters.

**🔍 Known Unknowns — Identified Gaps**

Generate 3–5 bullets of gaps the person knows they need to answer but hasn't
yet. Focus on open decisions, unresolved research questions, and next-step
blockers. Each bullet: one sentence framed as a question or gap statement.

**🌫️ Unknown Knowns — Tacit Knowledge**

Generate 3–5 bullets of things an experienced practitioner would do
instinctively without being able to articulate why. Frame as "you probably
know this but may not have written it down." Each bullet: one sentence
describing the tacit pattern or instinct.

**🌑 Unknown Unknowns — Hidden Risks & Blind Spots (shallow technique stack)**

Fill in the probe worksheet: a markdown table with one row per probe, in
order. Each row gets 0–2 candidate items. Write `—` when a probe yields
nothing genuine — an empty row is better than a forced item. Render the
completed worksheet in the draft response *before* the consolidated UU
bullets, so skipped probes are visible.

| # | Probe (tag) | Candidate item(s) |
|---|-------------|-------------------|
| 1 | pre-mortem | |
| 2 | assumption-audit | |
| 3 | JTBD | |
| 4 | non-consumption | |
| 5 | workarounds | |
| 6 | adjacent-domain | |
| 7 | distant-domain | |
| 8 | second-order | |
| 9 | contradiction | |
| 10 | reversal | |
| 11 | constraint-audit | |
| 12 | novice-lens | |

The `(tag)` column holds the canonical probe tag used for attribution in the
final output. The twelve probes, in worksheet order:

1. **Pre-mortem**: Imagine this effort around `<topic>` fails in 3 years.
   What caused it? List failure modes that aren't in Known Unknowns —
   especially failure modes that come from *locally rational, well-managed
   decisions*, not from mistakes or negligence (cf. Christensen's
   Innovator's Dilemma: the right call in the current frame is the wrong
   call for the long arc).

2. **Assumption audit**: What is a practitioner implicitly assuming about
   `<topic>` that could be wrong? Focus on hidden premises, not explicit
   gaps. Then flip the lens: what about `<topic>` will *not* change over
   the next 10 years, and should anchor the strategy regardless of trend
   noise? (Bezos invariant principle.)

3. **Jobs-to-be-Done reframe**: What task is the user actually *hiring*
   `<topic>` to complete, regardless of product form? What non-obvious
   alternatives — possibly from outside the industry — could fulfill the
   same underlying task and make `<topic>` irrelevant? (Drill → 3M
   Command Strip: the customer wanted a hung picture, not a hole.)

4. **Non-consumption probe**: Who has the same underlying need but consumes
   *nothing* in this category today? Which barrier — financial, skill,
   access, or time — keeps them out? Removing a barrier often opens a
   market 10–100× larger than improving the product for existing users.

5. **User-workarounds probe** (使用者改造): Where are practitioners
   jury-rigging their own solutions today (workaround scripts, manual
   processes, third-party add-ons, kludges)? Behavioral workarounds are
   loud, empirical signals of unmet need that surveys and interviews
   systematically miss — and they point directly at the next breakthrough.

6. **Adjacent domain transfer**: What does a closely related field (name it)
   know that this framing ignores? What lesson transfers?

7. **Distant domain transfer**: What does a completely different industry or
   discipline — aviation, medicine, nuclear energy, finance, law, or another
   field far from `<topic>` — know about this *class* of problem? Name the
   field and the hard-won lesson that transfers.

8. **Second-order effects**: What non-obvious downstream consequences of
   `<topic>` aren't already captured in Known Unknowns?

9. **Contradiction scan** (TRIZ): What parameter improvements in `<topic>`
   necessarily degrade something else? Name the tension explicitly.

10. **Contrarian reversal**: Take the most fundamental assumption about
    `<topic>` and deliberately reverse it. What does the reversed premise
    reveal that the current framing cannot see? (de Bono Provocation / 逆向思維)

11. **Constraint audit**: What is being treated as a hard, immovable constraint
    in `<topic>` that is actually a conventional obstacle — i.e., something
    that feels fixed but could be removed or redesigned? Name the
    misclassified constraint and what becomes possible if it is dissolved.

12. **Novice lens**: Imagine a skilled practitioner from an unrelated discipline
    encounters `<topic>` for the first time. What would they find arbitrary,
    unnecessarily complex, or "just the way it's done" that experts have stopped
    perceiving as a choice? What has domain experience normalized that a
    beginner's eye would flag as strange?

Consolidate probe results: deduplicate, then rank by surprise value. Demote
any item the user almost certainly already knows to Known Unknowns. Keep 3–5
genuinely surprising items as the Unknown Unknowns bullets. End every final
UU bullet with its source tag from the worksheet, e.g. `(probe: pre-mortem)`,
`(probe: JTBD)`. When an item merges findings from several probes, tag the
dominant one.

Present the full draft clearly labeled **"Draft — please review."**

### Deep mode (`--depth deep`)

Generate 👁️ Known Knowns, 🔍 Known Unknowns, and 🌫️ Unknown Knowns using
the exact same prompts as shallow mode above.

For Unknown Unknowns: write a placeholder:
> 🌑 *Unknown Unknowns — will be generated after your review via persona rotation.*

Present the partial draft labeled **"Draft (KK/KU/UK only) — please review
before UU generation."** Then **wait for user review at Phase 2** (do not
re-present the draft there).

---

## Phase 2 — User Review

Ask the user to review the draft:

> "Here's the draft knowledge map. Please review:
> - **👁️ Known Knowns**: Does this match what you actually know? Add, remove, or correct.
> - **🔍 Known Unknowns**: Are these the right gaps? Any missing questions?
> - **🌫️ Unknown Knowns**: Resonates? Anything to add or challenge?
> - **🌑 Unknown Unknowns** *(shallow: review draft bullets / deep: review placeholder framing)*: Anything to add or challenge?
>
> Reply with corrections, or say 'looks good' to proceed."

Wait for the user's response. Incorporate all corrections before continuing.

- In **shallow mode**: after incorporating corrections, go directly to Phase 3.
- In **deep mode**: after incorporating corrections, run the **Deep Mode UU Sub-Phase** below, then Phase 3.

---

## Deep Mode UU Sub-Phase (`--depth deep` only)

Run this after Phase 2 corrections are incorporated.

Read [references/persona-axes.md](references/persona-axes.md) now.
If the file is not accessible, use the four axis types from memory:
STEEP (Social/Technological/Economic/Environmental/Political/Legal),
CATWOE-inspired (Customer/Actor/Owner/Regulator/Competitor/Maintainer),
Temporal Horizon (Operational/Strategic/Systemic),
Adversarial Triad (Attacker/Regulator/Inheritor).

### Step 1: Axis Selection

Select two orthogonal axis types from the reference most relevant to `<topic>`.
State your choice in one sentence:
> "Axes chosen: `<axis type A>` × `<axis type B>` — because [one-sentence reason]."

Generate 3–5 personas at the intersection. List them:
> Personas: [Persona 1 — brief role description], [Persona 2], ...

### Step 2: Persona Review

For each persona, write 1–3 findings in their voice:
> "As a `<persona>` reviewing this knowledge map about `<topic>`, I would flag:
> - [Finding 1 — something missing the user isn't asking about]
> - [Finding 2]"

Do not repeat items already in Known Unknowns. Focus strictly on what the
user's current framing fails to see.

### Step 3: Consolidation

1. Collect all persona findings.
2. Deduplicate and cluster overlapping findings.
3. Rank by surprise value:
   - Items the user almost certainly knows but hasn't addressed → demote to Known Unknowns
   - Items representing genuine blind spots → keep in Unknown Unknowns
4. Tentatively list 3–5 UU candidates internally (do not display yet — this working list will be revised in Step 4). Note the source persona for each.

### Step 4: TRIZ Supplement

After persona rotation, run two additional probes and fold results back into
Step 3 consolidation before writing final bullets.

**9-Windows scan** — traverse the 3×3 matrix of system level × time horizon.
For each cell, ask: "What is happening here that the current map ignores?"
Extract 1–2 UU candidates from underexplored cells.

| | Past | Present | Future |
|--|------|---------|--------|
| **Super-system** | What path dependencies were created by the super-system's past? | What does the super-system constrain right now? | Where is the super-system heading that will invalidate current assumptions? |
| **System** | What legacy decisions shaped the current state? | What systemic tensions exist now? | What systemic changes are coming? |
| **Sub-system** | What component-level history is being ignored? | What component-level issues aren't surfaced? | What component-level changes will cascade upward? |

**Contradiction scan** — "What parameter improvements in `<topic>` necessarily
degrade something else?" Extract 1–2 structural tension items. These are TRIZ
physical contradictions baked into the domain.

Merge Step 4 findings into the Step 3 list. Re-deduplicate and re-rank.
Write final UU bullets (3–7 items in deep mode). Attribute every bullet:
persona-sourced items end with `(<Persona name>)`, 9-Windows items with
`(9-windows)`, contradiction-scan items with `(contradiction)`.

---

## Phase 3 — Refine & Emit

Incorporate all Phase 2 corrections and (in deep mode) the UU sub-phase results.

Determine output path:
- If the user specified a path, use it.
- Otherwise: `./YYYY-MM-DD-kq-<slug>.md` where `<slug>` is the topic in
  kebab-case (e.g., topic "Building a RAG system" → `2026-04-22-kq-building-a-rag-system.md`).

Write the final document. Use the template for the active mode:

**Shallow mode template:**
```markdown
# Knowledge Quadrants: <topic>
_<YYYY-MM-DD> · depth: shallow · web: on|off_

> **Seed context:** <the user's seed, verbatim or lightly edited — include
> this blockquote only when the user supplied more than a bare topic phrase>

## 👁️ Known Knowns — Conscious Knowledge
- **<short label>**: <brief note>

## 🔍 Known Unknowns — Identified Gaps
- **<short label>**: <brief note>

## 🌫️ Unknown Knowns — Tacit Knowledge
- **<short label>**: <brief note>

## 🌑 Unknown Unknowns — Hidden Risks & Blind Spots
- **<short label>**: <brief note> (probe: <tag>)
```

**Deep mode template:**
```markdown
# Knowledge Quadrants: <topic>
_<YYYY-MM-DD> · depth: deep · web: on|off_

> **Seed context:** <the user's seed, verbatim or lightly edited — include
> this blockquote only when the user supplied more than a bare topic phrase>

## 👁️ Known Knowns — Conscious Knowledge
- **<short label>**: <brief note>

## 🔍 Known Unknowns — Identified Gaps
- **<short label>**: <brief note>

## 🌫️ Unknown Knowns — Tacit Knowledge
- **<short label>**: <brief note>

## 🌑 Unknown Unknowns — Hidden Risks & Blind Spots
_Personas consulted: [axes: <axis A> × <axis B>] → [Persona 1, Persona 2, ...]_
- **<short label>**: <brief note> (<Persona name> | 9-windows | contradiction)
```

**Refresh additions (either template, `--refresh` only):**

- Metadata line becomes:
  `_<YYYY-MM-DD> · depth: shallow|deep · web: on|off · v<N+1> (refreshed from <old filename>)_`
- Keep (or extend) the old file's seed-context blockquote.
- Append at the end of the document:

```markdown
## 🔁 Migration Log
- <item (abbreviated)>: <From> → <To> — <one-line reason>
```

- Every promote/demote/retire from the re-assessment pass gets one line.
- Carried-over (STILL-OPEN) UU items keep their original attribution when
  present; items from a pre-v0.3 file that have none get `(probe: carried-over)`.

### Self-check before finishing

Run the structural validator that ships with this skill on the emitted file:

```bash
python3 <this-skill's-directory>/scripts/validate_kq.py <output-path> --level full
```

- All checks PASS → tell the user: "Knowledge map written to `<path>` (validated)."
- Any check FAILs → fix the output file and re-run, at most 2 retries. If
  failures remain after that, tell the user which checks still fail — never
  hide a failing check.
- If `python3` is unavailable, verify by hand against this checklist: H1
  starts with `# Knowledge Quadrants:`; metadata line present; all four
  emoji quadrant headers present; ≥3 bullets per quadrant; UU bullets carry
  probe/persona attribution.
