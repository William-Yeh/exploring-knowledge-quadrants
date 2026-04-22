---
name: exploring-knowledge-quadrants
description: >-
  Use when the user says "knowledge quadrants", "四象限", "explore quadrants",
  "KQ", or "what do I know / not know about" followed by a topic or seed.
license: Apache-2.0
metadata:
  author: William-Yeh
  version: "0.1"
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

Apply all nine probes in sequence. For each, generate 1–2 candidate items:

1. **Pre-mortem**: Imagine this effort around `<topic>` fails in 3 years.
   What caused it? List failure modes that aren't in Known Unknowns.

2. **Assumption audit**: What is a practitioner implicitly assuming about
   `<topic>` that could be wrong? Focus on hidden premises, not explicit gaps.

3. **Adjacent domain transfer**: What does a closely related field (name it)
   know that this framing ignores? What lesson transfers?

4. **Distant domain transfer**: What does a completely different industry or
   discipline — aviation, medicine, nuclear energy, finance, law, or another
   field far from `<topic>` — know about this *class* of problem? Name the
   field and the hard-won lesson that transfers.

5. **Second-order effects**: What non-obvious downstream consequences of
   `<topic>` aren't already captured in Known Unknowns?

6. **Contradiction scan** (TRIZ): What parameter improvements in `<topic>`
   necessarily degrade something else? Name the tension explicitly.

7. **Contrarian reversal**: Take the most fundamental assumption about
   `<topic>` and deliberately reverse it. What does the reversed premise
   reveal that the current framing cannot see? (de Bono Provocation / 逆向思維)

8. **Constraint audit**: What is being treated as a hard, immovable constraint
   in `<topic>` that is actually a conventional obstacle — i.e., something
   that feels fixed but could be removed or redesigned? Name the
   misclassified constraint and what becomes possible if it is dissolved.

9. **Novice lens**: Imagine a skilled practitioner from an unrelated discipline
   encounters `<topic>` for the first time. What would they find arbitrary,
   unnecessarily complex, or "just the way it's done" that experts have stopped
   perceiving as a choice? What has domain experience normalized that a
   beginner's eye would flag as strange?

Consolidate probe results: deduplicate, then rank by surprise value. Demote
any item the user almost certainly already knows to Known Unknowns. Keep 3–5
genuinely surprising items as the Unknown Unknowns bullets.

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
Write final UU bullets (3–7 items in deep mode).

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

## 👁️ Known Knowns — Conscious Knowledge
- <item>: <brief note>

## 🔍 Known Unknowns — Identified Gaps
- <item>: <brief note>

## 🌫️ Unknown Knowns — Tacit Knowledge
- <item>: <brief note>

## 🌑 Unknown Unknowns — Hidden Risks & Blind Spots
- <item>: <brief note>
```

**Deep mode template:**
```markdown
# Knowledge Quadrants: <topic>
_<YYYY-MM-DD> · depth: deep · web: on|off_

## 👁️ Known Knowns — Conscious Knowledge
- <item>: <brief note>

## 🔍 Known Unknowns — Identified Gaps
- <item>: <brief note>

## 🌫️ Unknown Knowns — Tacit Knowledge
- <item>: <brief note>

## 🌑 Unknown Unknowns — Hidden Risks & Blind Spots
_Personas consulted: [axes: <axis A> × <axis B>] → [Persona 1, Persona 2, ...]_
- <item>: <brief note> (<Persona name>)
```

After writing the file, tell the user: "Knowledge map written to `<path>`."
