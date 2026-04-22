# Design: exploring-knowledge-quadrants

_Date: 2026-04-22_

## Overview

An agent skill that takes a topic (rough idea or seed) and generates a structured
four-quadrant knowledge map, helping the user surface both explicit and hidden
dimensions of what they know and don't know about a subject.

The four quadrants (知識探索四象限):

| Quadrant | Label | Nature |
|----------|-------|--------|
| 👁️ Known Knowns | Conscious Knowledge | Explicit, articulable knowledge |
| 🔍 Known Unknowns | Identified Gaps | Gaps you're aware of |
| 🌫️ Unknown Knowns | Tacit Knowledge | Knowledge you have but can't yet articulate |
| 🌑 Unknown Unknowns | Hidden Risks & Blind Spots | What you don't know you don't know |

---

## Trigger Conditions

The skill activates on phrases such as:

- "knowledge quadrants \<topic\>"
- "四象限 \<topic\>"
- "explore quadrants \<topic\>"
- "KQ \<topic\>"
- "what do I know / not know about \<topic\>"

Input may be a focused topic or a rough prose seed (with optional `[ ]` checkbox
items for suggested angles, similar to `delphi-research` seed format).

---

## Flags

| Flag | Values | Default | Effect |
|------|--------|---------|--------|
| `--depth` | `shallow`, `deep` | `shallow` | Controls UU exploration mechanism (see below) |
| `--web` | (boolean) | off | Grounds UU in real-world search results |

---

## Workflow

### Phase 1 — Draft Generation

The skill generates a draft of all four quadrants from the input topic.

- **shallow**: single LLM call; UU populated via structured technique stack
- **deep**: KK + KU + UK in one call, then a dedicated UU sub-phase (persona rotation)

### Phase 2 — User Review (Hybrid)

Present the draft and invite the user to:

- Correct or extend KK and KU (explicit knowledge — user knows best)
- Optionally add to UK and UU ("anything missing?")

### Phase 3 — Refine & Emit

Incorporate corrections. Write the final Markdown document to the output path.

---

## Unknown Unknowns Mechanism

This is the hardest quadrant. UU items cannot be found by direct introspection —
they require indirect strategies that systematically shift perspective.

### Shallow mode — Structured Technique Stack

A single LLM call applies nine cognitive probes in sequence:

1. **Pre-mortem** — "This effort fails in 3 years. What caused it?"
2. **Assumption audit** — "What are you implicitly assuming that could be wrong?"
3. **Adjacent domain transfer** — "What does a closely related field know that this framing ignores?"
4. **Distant domain transfer** — "What does a completely different industry or discipline (aviation, medicine, nuclear, finance, law…) know about this *class* of problem?"
5. **Second-order effects** — "What non-obvious downstream consequences aren't in the Known Unknowns?"
6. **Contradiction scan** (TRIZ) — "What parameter improvements in this domain necessarily degrade something else?"
7. **Contrarian reversal** (de Bono Provocation / 逆向思維) — "Deliberately reverse the most fundamental assumption. What does the reversed premise reveal?"
8. **Constraint audit** (Minerva `#constraints`) — "What is being treated as a hard constraint that is actually a conventional obstacle? What becomes possible if it is dissolved?"
9. **Novice lens** (vuja de / 缺乏經驗的經驗) — "What would a skilled outsider find arbitrary, unnecessarily complex, or 'just the way it's done' that domain experience has made imperceptible?"

Note: techniques 1–2 cover failure modes and hidden assumptions. Techniques 3–4
cover cross-domain gaps at two distances. Technique 5 covers downstream effects.
Technique 6 (TRIZ) adds structural tensions. Technique 7 (de Bono Provocation,
validated by Minerva's 逆向思維) reveals what the current frame cannot see by
inverting its core premise. Technique 8 (Minerva constraint audit) discriminates
between genuine structural limits and misclassified conventional obstacles — a
distinct UU source not covered by assumption audit. Technique 9 (novice lens,
cross-validated by vuja de in 創新者的DNA and 缺乏經驗的經驗 in 逆向工程) surfaces
what expertise has normalized to the point of invisibility — distinct from
assumption audit because the assumptions are no longer perceived as assumptions.

### Deep mode — Adversarial Persona Rotation

A dedicated sub-phase after Phase 2:

**Step 1: Axis selection**
The LLM infers which two orthogonal axes are most relevant for this topic, drawn from:

| Axis type | Examples |
|-----------|----------|
| Domain dimension (STEEP) | Social, Technological, Economic, Environmental, Political, Legal |
| System position (CATWOE) | Customer, Actor (creator), Owner, Regulator, Competitor, Maintainer |
| Temporal horizon | Operational (near-term), Strategic (1–3 yr), Systemic (decade+) |
| Adversarial triad | Attacker (wants it to fail), Regulator (holds it accountable), Inheritor (lives with it later) |

Two axes are selected; their intersection generates a non-redundant set of 3–5 personas.
The axes chosen are listed in the output so the user can challenge coverage.

**Step 2: Persona review**
Each persona reviews the current map (all confirmed quadrants) and answers:
_"What would I flag as missing that this person isn't even asking about?"_

**Step 3: Consolidation**
- Deduplicate and cluster overlapping findings
- Rank by **surprise value**: items the user almost certainly knows → demoted to KU; high-surprise items → UU
- Write ranked UU bullets with the contributing persona noted

**Step 4: TRIZ supplement**
After persona rotation, run two additional structured probes:

- **9-Windows scan** — traverse the 3×3 matrix of (sub-system / system / super-system) × (past / present / future). For each cell: "What is happening here that the current map ignores?"
- **Contradiction scan** — "What parameter improvements in this domain necessarily degrade something else?" Unacknowledged contradictions are structural UU items.

Step 4 items feed back into Step 3 consolidation before writing final UU bullets.

### Web mode (`--web`)

When enabled, Phase 1 draft generation is augmented with a search phase before
the LLM call:
- "What do domain experts currently worry about in this area?"
- "What recent failures or surprises occurred in this domain?"

Results are injected as grounding context into the UU draft. Works with both
shallow and deep depth modes.

---

## Output Format

```markdown
# Knowledge Quadrants: <topic>
_<date> · depth: shallow|deep · web: on|off_

## 👁️ Known Knowns — Conscious Knowledge
- <item with brief note>

## 🔍 Known Unknowns — Identified Gaps
- <item with brief note>

## 🌫️ Unknown Knowns — Tacit Knowledge
- <item with brief note>

## 🌑 Unknown Unknowns — Hidden Risks & Blind Spots
_Personas consulted: [axes: STEEP × adversarial triad] → [Security auditor, ...]_
- <item — source persona noted if deep mode>
```

**Output path:** user-specified, or defaults to `./YYYY-MM-DD-kq-<slug>.md`.
No hardcoded Obsidian vault path — the user places the file.

---

## Repository Layout

Following the project convention (`CLAUDE.md`):

```
exploring-knowledge-quadrants/
├── skill/                   ← installed by `npx skills add`
│   ├── SKILL.md
│   └── references/
│       └── persona-axes.md  ← STEEP / CATWOE / temporal / adversarial reference
├── docs/
│   └── specs/
│       └── 2026-04-22-knowledge-quadrants-skill-design.md
├── tests/
├── README.md
├── LICENSE
└── .github/
    └── workflows/
        └── ci.yml
```

No `scripts/` in v1 — pure `SKILL.md` orchestration. Phase boundaries in `SKILL.md`
are numbered explicitly (Phase 1 / Phase 2 / Phase 3) so individual phases can be
extracted into scripts in a future version without restructuring the workflow.

---

## SKILL.md Frontmatter

```yaml
---
name: exploring-knowledge-quadrants
description: >-
  Use when the user says "knowledge quadrants", "四象限", "explore quadrants",
  "KQ", or "what do I know / not know about" followed by a topic or seed.
  Generates a four-quadrant knowledge map: Known Knowns, Known Unknowns,
  Unknown Knowns, and Unknown Unknowns.
license: Apache-2.0
metadata:
  author: William-Yeh
  version: "0.1"
---
```

---

## Design Decisions

### Why UU needs a dedicated mechanism
The other three quadrants can be populated through direct elicitation or
introspection. Unknown Unknowns cannot — they require perspective rotation to
escape the user's current frame. Shallow mode approximates this with four
cognitive probes; deep mode does it structurally via persona rotation across
orthogonal axes.

### Why persona axes must be orthogonal
Using STEEP alone risks personas that overlap in what they see (e.g., a
"technology expert" and an "infrastructure expert" may notice the same gaps).
Crossing two axis types (e.g., domain dimension × system position) generates
structurally non-redundant perspectives and makes coverage gaps visible as blank
cells in the axis matrix.

### Why pure SKILL.md for v1
Unlike `delphi-research`, this skill has no multi-provider orchestration,
citation pipelines, or convergence scoring — all "parallelism" (persona rotation)
happens inside a single LLM context window as sequential prompting. Python scripts
would add setup overhead with no architectural benefit at this scale.

### Surprise value ranking
Without ranking, a naive LLM tends to populate UU with items that are actually
KU (risks the user has heard of but hasn't addressed). The ranking step
discriminates between "you know this is a gap" vs. "you didn't even frame it as
a question," keeping the UU quadrant epistemically honest.

### Why TRIZ is split across modes
The 9-Windows matrix (3×3 = 9 cells, each needing distinct reasoning) is too
expensive for shallow mode's single-call budget — it would either produce
perfunctory output or push the call into deep-mode territory. The contradiction
scan, by contrast, is a single focused question that adds a structurally distinct
UU source (domain tensions) not covered by the other four shallow-mode techniques.
Six Thinking Hats was evaluated and rejected: it is a cognitive mode framework
(how you think), not a knowledge domain framework (what you know), so it generates
structurally incoherent personas for the UU rotation.

### Why novice lens is distinct from assumption audit (probe 2)
Assumption audit surfaces premises that practitioners can still interrogate if
prompted — hidden but accessible. The novice lens (probe 9) targets habituation
blindness: conventions so deeply normalized by expertise that they are no longer
perceived as choices at all. A newcomer flags them; an expert cannot see them
without the explicit prompt to adopt an outsider's eye. Cross-validated by two
independent sources: vuja de in 創新者的DNA (deliberately seeing the familiar as
strange) and 缺乏經驗的經驗 in 逆向工程 (Marvel hiring directors outside the
superhero genre precisely because they hadn't been acculturated to its implicit
rules).
