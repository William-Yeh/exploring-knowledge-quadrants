# exploring-knowledge-quadrants Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a pure SKILL.md agent skill that generates a four-quadrant knowledge map (Known Knowns, Known Unknowns, Unknown Knowns, Unknown Unknowns) from any topic using structured LLM prompting.

**Architecture:** Three-phase workflow (draft → user review → emit). Shallow mode uses a five-technique UU stack in a single call; deep mode adds adversarial persona rotation across orthogonal axes (STEEP/CATWOE/temporal/adversarial) plus a TRIZ supplement (9-Windows + contradiction scan). No Python scripts in v1 — all orchestration lives in `skill/SKILL.md`.

**Tech Stack:** SKILL.md (agentskills.io spec), Markdown, GitHub Actions CI with inline Python validation.

---

## File Map

| File | Purpose |
|------|---------|
| `skill/SKILL.md` | Main skill — agent instructions for all three phases |
| `skill/references/persona-axes.md` | Lookup table of axis types for deep-mode persona generation |
| `README.md` | Installation, usage, badges |
| `LICENSE` | Apache-2.0 |
| `.github/workflows/ci.yml` | Validates SKILL.md frontmatter + README structure + LICENSE |
| `tests/scenarios/shallow-rag.md` | Shallow-mode scenario fixture: "Building a RAG system" |
| `tests/scenarios/deep-saas.md` | Deep-mode scenario fixture: "Launching a B2B SaaS product" |

---

## Task 1: Repo Scaffolding + CI (Test Harness)

**Files:**
- Create: `LICENSE`
- Create: `.github/workflows/ci.yml`
- Create: `skill/` (empty directory marker)

- [ ] **Step 1: Write the LICENSE file**

Fetch the full Apache-2.0 text:
```bash
curl -sSL https://www.apache.org/licenses/LICENSE-2.0.txt \
  -o /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants/LICENSE
```

Verify:
```bash
head -3 /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants/LICENSE
```

Expected:
```
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/
```

- [ ] **Step 2: Write CI workflow**

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check SKILL.md frontmatter
        run: |
          python3 - <<'EOF'
          import sys
          with open("skill/SKILL.md") as f:
              content = f.read()
          if not content.startswith("---"):
              print("ERROR: skill/SKILL.md missing frontmatter")
              sys.exit(1)
          required = ["name:", "description:", "license:", "metadata:"]
          missing = [r for r in required if r not in content]
          if missing:
              print(f"ERROR: Missing frontmatter fields: {missing}")
              sys.exit(1)
          print("skill/SKILL.md frontmatter OK")
          EOF

      - name: Check README badges
        run: |
          python3 - <<'EOF'
          import sys
          with open("README.md") as f:
              content = f.read()
          required = ["CI", "License", "Agent Skills", "## Installation", "## Usage"]
          missing = [r for r in required if r not in content]
          if missing:
              print(f"ERROR: README.md missing: {missing}")
              sys.exit(1)
          print("README.md structure OK")
          EOF

      - name: Check LICENSE exists
        run: test -f LICENSE || (echo "ERROR: LICENSE missing" && exit 1)

      - name: Check references file exists
        run: test -f skill/references/persona-axes.md || (echo "ERROR: skill/references/persona-axes.md missing" && exit 1)
```

- [ ] **Step 3: Run CI locally to verify it fails**

```bash
cd /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants
python3 - <<'EOF'
import sys, os
if not os.path.exists("skill/SKILL.md"):
    print("EXPECTED FAIL: skill/SKILL.md not found")
else:
    print("skill/SKILL.md exists")
EOF
```

Expected: `EXPECTED FAIL: skill/SKILL.md not found`

- [ ] **Step 4: Commit scaffolding**

```bash
cd /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants
git init
git add LICENSE .github/
git commit -m "chore: scaffold repo with CI validation workflow"
```

---

## Task 2: Persona Axes Reference

**Files:**
- Create: `skill/references/persona-axes.md`

- [ ] **Step 1: Create references directory**

```bash
mkdir -p /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants/skill/references
```

- [ ] **Step 2: Write persona-axes.md**

Create `skill/references/persona-axes.md`:

```markdown
# Persona Axes Reference

Use this reference in deep mode to select two orthogonal axis types for
persona generation. Personas at the intersection of two different axis types
are structurally non-redundant — they see different blind spots.

## Axis Types

### Domain Dimension (STEEP)

| Label | Focus |
|-------|-------|
| Social | Human behavior, culture, communities, ethics |
| Technological | Tools, systems, technical constraints |
| Economic | Cost, incentives, markets, resource flows |
| Environmental | Physical environment, sustainability, externalities |
| Political | Power, policy, regulation, governance |
| Legal | Law, liability, compliance, intellectual property |

### System Position (CATWOE-inspired)

| Label | Focus |
|-------|-------|
| Customer / End User | Who receives value from the system |
| Actor / Creator | Who builds or operates the system |
| Owner | Who is accountable for the system |
| Regulator | Who sets rules the system must follow |
| Competitor | Who builds alternatives or benefits from failure |
| Maintainer / Inheritor | Who lives with the system long-term |

### Temporal Horizon

| Label | Focus |
|-------|-------|
| Operational | Days to weeks — immediate execution concerns |
| Strategic | Months to 1–3 years — planning and adaptation |
| Systemic | Decade+ — civilizational, path-dependency concerns |

### Adversarial Triad

| Label | Focus |
|-------|-------|
| Attacker | Wants the effort to fail — adversarial, exploit-focused |
| Regulator | Holds the effort accountable — compliance, accountability |
| Inheritor | Has to live with outcomes long-term — maintenance, technical debt |

## Selecting Axes

Choose two axes from **different** types. Good pairs:

| Pair | Example persona generated |
|------|--------------------------|
| STEEP × CATWOE | Economic × Regulator → economist who evaluates regulatory incentives |
| STEEP × Adversarial | Social × Attacker → social-engineering threat analyst |
| CATWOE × Temporal | End User × Systemic → researcher studying decade-long user behavior shifts |
| STEEP × Temporal | Technological × Strategic → CTO planning 2-year technology bets |

Avoid pairing axes of the **same type** (e.g., Social × Economic, or
Operational × Strategic) — personas will overlap in what they see.
```

- [ ] **Step 3: Verify file exists**

```bash
test -f /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants/skill/references/persona-axes.md && echo "OK"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
cd /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants
git add skill/references/persona-axes.md
git commit -m "feat: add persona-axes reference for deep-mode UU generation"
```

---

## Task 3: SKILL.md — Shallow Mode (Complete Workflow)

**Files:**
- Create: `skill/SKILL.md`

- [ ] **Step 1: Write the frontmatter + overview**

Create `skill/SKILL.md` beginning with:

```markdown
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

Apply all five probes in sequence. For each, generate 1–2 candidate items:

1. **Pre-mortem**: Imagine this effort around `<topic>` fails in 3 years.
   What caused it? List failure modes that aren't in Known Unknowns.

2. **Assumption audit**: What is a practitioner implicitly assuming about
   `<topic>` that could be wrong? Focus on hidden premises, not explicit gaps.

3. **Adjacent domain transfer**: What does a closely related field (name it)
   know that this framing ignores? What lesson transfers?

4. **Second-order effects**: What non-obvious downstream consequences of
   `<topic>` aren't already captured in Known Unknowns?

5. **Contradiction scan** (TRIZ): What parameter improvements in `<topic>`
   necessarily degrade something else? Name the tension explicitly.

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
before UU generation."** Then proceed to Phase 2.

---

## Phase 2 — User Review

Present the draft and ask:

> "Here's the draft knowledge map. Please review:
> - **👁️ Known Knowns**: Does this match what you actually know? Add, remove, or correct.
> - **🔍 Known Unknowns**: Are these the right gaps? Any missing questions?
> - **🌫️ Unknown Knowns**: Resonates? Anything to add or challenge?
> - **🌑 Unknown Unknowns** *(shallow only)*: Anything to add or challenge?
>
> Reply with corrections, or say 'looks good' to proceed."

Wait for the user's response. Incorporate all corrections before continuing.

- In **shallow mode**: after incorporating corrections, go directly to Phase 3.
- In **deep mode**: after incorporating corrections, run the **Deep Mode UU Sub-Phase** below, then Phase 3.

---

## Deep Mode UU Sub-Phase (`--depth deep` only)

Run this after Phase 2 corrections are incorporated.

Read [references/persona-axes.md](references/persona-axes.md) now.

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
4. Draft 3–5 UU bullets. Note the source persona in parentheses for each item.

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

Write the final document using this exact format:

```markdown
# Knowledge Quadrants: <topic>
_<YYYY-MM-DD> · depth: shallow|deep · web: on|off_

## 👁️ Known Knowns — Conscious Knowledge
- <item>: <brief note>

## 🔍 Known Unknowns — Identified Gaps
- <item>: <brief note>

## 🌫️ Unknown Knowns — Tacit Knowledge
- <item>: <brief note>

## 🌑 Unknown Unknowns — Hidden Risks & Blind Spots
_Personas consulted: [axes: <axis A> × <axis B>] → [Persona 1, Persona 2, ...]_
_(omit personas line in shallow mode)_
- <item> (<source persona in deep mode>)
```

After writing the file, tell the user: "Knowledge map written to `<path>`."
```

- [ ] **Step 2: Run CI frontmatter check locally to verify it passes**

```bash
cd /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants
python3 - <<'EOF'
import sys
with open("skill/SKILL.md") as f:
    content = f.read()
if not content.startswith("---"):
    print("FAIL: missing frontmatter")
    sys.exit(1)
required = ["name:", "description:", "license:", "metadata:"]
missing = [r for r in required if r not in content]
if missing:
    print(f"FAIL: missing fields: {missing}")
    sys.exit(1)
print("PASS: frontmatter OK")
EOF
```

Expected: `PASS: frontmatter OK`

- [ ] **Step 3: Commit**

```bash
cd /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants
git add skill/SKILL.md
git commit -m "feat: add SKILL.md with shallow and deep mode workflows"
```

---

## Task 4: README.md

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write README.md**

Create `README.md`:

```markdown
# exploring-knowledge-quadrants

[![CI](https://github.com/William-Yeh/exploring-knowledge-quadrants/actions/workflows/ci.yml/badge.svg)](https://github.com/William-Yeh/exploring-knowledge-quadrants/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/agent--skills-compatible-brightgreen)](https://agentskills.io/specification)

An [Agent Skill](https://agentskills.io/specification) that generates a
four-quadrant knowledge map for any topic, surfacing conscious knowledge,
identified gaps, tacit knowledge, and hidden blind spots (知識探索四象限).

## What It Does

Given a topic or rough seed, the skill generates:

| Quadrant | Emoji | What it surfaces |
|----------|-------|-----------------|
| Known Knowns | 👁️ | Explicit, articulable knowledge |
| Known Unknowns | 🔍 | Identified gaps and open questions |
| Unknown Knowns | 🌫️ | Tacit knowledge you have but haven't articulated |
| Unknown Unknowns | 🌑 | Hidden risks and blind spots via structured probing |

**Shallow mode** (default): fast single-call draft using a five-technique UU
stack (pre-mortem, assumption audit, adjacent domain transfer, second-order
effects, TRIZ contradiction scan).

**Deep mode** (`--depth deep`): dedicated Unknown Unknowns sub-phase using
adversarial persona rotation across orthogonal axes (STEEP × CATWOE ×
temporal × adversarial triad), plus a TRIZ 9-Windows supplement.

## Installation

```bash
npx skills add William-Yeh/exploring-knowledge-quadrants
```

Manual installation — copy `skill/` to your agent's skills directory:

| Agent | Directory |
|-------|-----------|
| Claude Code | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` |
| Gemini CLI | `.gemini/skills/` |

## Usage

Invoke with any of:

- `knowledge quadrants <topic>`
- `四象限 <topic>`
- `explore quadrants <topic>`
- `KQ <topic>`
- `what do I know / not know about <topic>`

### Options

| Flag | Default | Effect |
|------|---------|--------|
| `--depth shallow\|deep` | `shallow` | UU exploration depth |
| `--web` | off | Ground UU in real-world search |

### Examples

```
KQ building a RAG system
```

```
knowledge quadrants launching a B2B SaaS --depth deep
```

```
四象限 機器學習基礎設施 --depth deep --web
```

## Output

A Markdown file with four labeled sections, suitable for filing in Obsidian
or any PKM system. Default path: `./YYYY-MM-DD-kq-<slug>.md`.

## License

Apache-2.0
```

- [ ] **Step 2: Run README check locally**

```bash
cd /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants
python3 - <<'EOF'
import sys
with open("README.md") as f:
    content = f.read()
required = ["CI", "License", "Agent Skills", "## Installation", "## Usage"]
missing = [r for r in required if r not in content]
if missing:
    print(f"FAIL: missing: {missing}")
    sys.exit(1)
print("PASS: README structure OK")
EOF
```

Expected: `PASS: README structure OK`

- [ ] **Step 3: Commit**

```bash
cd /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants
git add README.md
git commit -m "docs: add README with installation and usage"
```

---

## Task 5: Scenario Test Fixtures

**Files:**
- Create: `tests/scenarios/shallow-rag.md`
- Create: `tests/scenarios/deep-saas.md`

These are manual test cases — human-readable fixtures defining expected
behavior for the skill's two main modes.

- [ ] **Step 1: Create tests directory**

```bash
mkdir -p /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants/tests/scenarios
```

- [ ] **Step 2: Write shallow-mode scenario**

Create `tests/scenarios/shallow-rag.md`:

```markdown
# Scenario: Shallow mode — "Building a RAG system"

## Invocation

```
KQ building a RAG system
```

(No flags — defaults to `--depth shallow`, `--web off`)

## Expected Behavior

1. Skill generates a draft with all four quadrants in one response.
2. Skill presents draft labeled "Draft — please review."
3. Skill asks for corrections to KK, KU, UK, UU.
4. After user says "looks good" (or provides corrections), skill writes file.
5. Output path announced: `./YYYY-MM-DD-kq-building-a-rag-system.md`

## Expected Output Structure

```markdown
# Knowledge Quadrants: Building a RAG system
_2026-04-22 · depth: shallow · web: off_

## 👁️ Known Knowns — Conscious Knowledge
- Vector embeddings encode semantic meaning: ...
- Chunking strategy affects retrieval quality: ...
- [3–5 items total]

## 🔍 Known Unknowns — Identified Gaps
- What chunk size and overlap work best for this domain?: ...
- How to handle multi-hop questions that require joining chunks?: ...
- [3–5 items total]

## 🌫️ Unknown Knowns — Tacit Knowledge
- You likely know intuitively when retrieval has failed even without metrics: ...
- [3–5 items total]

## 🌑 Unknown Unknowns — Hidden Risks & Blind Spots
- [Pre-mortem finding]: ...
- [Assumption audit finding]: ...
- [Adjacent domain finding]: ...
- [Second-order effect finding]: ...
- [TRIZ contradiction finding]: ...
- [3–5 items after consolidation]
```

## Pass Criteria

- [ ] Four labeled sections present with correct emoji headers
- [ ] UU section has no "personas consulted" line (shallow mode)
- [ ] UU items cover at least 3 of the 5 probe techniques
- [ ] No item in UU is a straightforward KU (surprise-value ranking worked)
- [ ] File is written to disk and path announced
```

- [ ] **Step 3: Write deep-mode scenario**

Create `tests/scenarios/deep-saas.md`:

```markdown
# Scenario: Deep mode — "Launching a B2B SaaS product"

## Invocation

```
knowledge quadrants launching a B2B SaaS product --depth deep
```

## Expected Behavior

1. Phase 1: Skill generates KK, KU, UK draft. UU shows placeholder.
2. Phase 2: Skill asks for corrections to KK/KU/UK.
3. After user review, skill runs Deep Mode UU Sub-Phase:
   a. Announces axis selection (e.g., "Axes chosen: STEEP × CATWOE")
   b. Lists 3–5 generated personas
   c. Shows persona review findings
   d. Runs TRIZ supplement (9-Windows + contradiction scan)
   e. Shows consolidated UU list
4. Phase 3: Skill writes file and announces path.

## Expected Output Structure

```markdown
# Knowledge Quadrants: Launching a B2B SaaS product
_2026-04-22 · depth: deep · web: off_

## 👁️ Known Knowns — Conscious Knowledge
- [3–5 items]

## 🔍 Known Unknowns — Identified Gaps
- [3–5 items]

## 🌫️ Unknown Knowns — Tacit Knowledge
- [3–5 items]

## 🌑 Unknown Unknowns — Hidden Risks & Blind Spots
_Personas consulted: [axes: STEEP × CATWOE] → [Security auditor, Legal counsel, ...]_
- [Item] (Security auditor)
- [Item] (End user researcher)
- [3–7 items total with persona attribution]
```

## Pass Criteria

- [ ] Axes selection is from two different axis types (not same type)
- [ ] Personas line present in UU section header
- [ ] Each UU item has a source persona in parentheses
- [ ] TRIZ 9-Windows and contradiction scan each contribute at least one item
- [ ] No UU item duplicates a KU item
- [ ] File written and path announced
```

- [ ] **Step 4: Commit**

```bash
cd /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants
git add tests/
git commit -m "test: add shallow and deep mode scenario fixtures"
```

---

## Task 6: Full CI Validation

Run the complete CI check locally to verify all files pass before push.

- [ ] **Step 1: Run full validation suite**

```bash
cd /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants

echo "=== Check 1: SKILL.md frontmatter ==="
python3 - <<'EOF'
import sys
with open("skill/SKILL.md") as f:
    content = f.read()
if not content.startswith("---"):
    print("FAIL: missing frontmatter"); sys.exit(1)
required = ["name:", "description:", "license:", "metadata:"]
missing = [r for r in required if r not in content]
if missing:
    print(f"FAIL: {missing}"); sys.exit(1)
print("PASS")
EOF

echo "=== Check 2: README badges and sections ==="
python3 - <<'EOF'
import sys
with open("README.md") as f:
    content = f.read()
required = ["CI", "License", "Agent Skills", "## Installation", "## Usage"]
missing = [r for r in required if r not in content]
if missing:
    print(f"FAIL: {missing}"); sys.exit(1)
print("PASS")
EOF

echo "=== Check 3: LICENSE ==="
test -f LICENSE && echo "PASS" || echo "FAIL: LICENSE missing"

echo "=== Check 4: persona-axes.md ==="
test -f skill/references/persona-axes.md && echo "PASS" || echo "FAIL: references missing"
```

Expected output:
```
=== Check 1: SKILL.md frontmatter ===
PASS
=== Check 2: README badges and sections ===
PASS
=== Check 3: LICENSE ===
PASS
=== Check 4: persona-axes.md ===
PASS
```

- [ ] **Step 2: Fix any failures before pushing**

If any check fails, identify the missing content from the relevant task above
and add it. Re-run the validation suite until all four checks pass.

- [ ] **Step 3: Manual smoke test — shallow mode**

With the skill installed (or pointed at directly), run:

```
KQ building a RAG system
```

Verify against `tests/scenarios/shallow-rag.md` pass criteria:
- [ ] Four emoji-headed sections present
- [ ] UU section has no personas line
- [ ] Draft → review → emit flow completed
- [ ] File written to `./YYYY-MM-DD-kq-building-a-rag-system.md`

- [ ] **Step 4: Manual smoke test — deep mode**

Run:

```
knowledge quadrants launching a B2B SaaS product --depth deep
```

Verify against `tests/scenarios/deep-saas.md` pass criteria:
- [ ] Two-stage draft (KK/KU/UK first, UU after review)
- [ ] Axis selection from two different axis types
- [ ] Personas listed in UU section header
- [ ] TRIZ 9-Windows and contradiction scan both contribute items

- [ ] **Step 5: Final commit**

```bash
cd /Users/william/Documents/AtWork/github/ai/exploring-knowledge-quadrants
git add -A
git commit -m "chore: verify all CI checks pass"
```

---

## Self-Review Against Spec

Spec requirement → plan coverage:

| Spec requirement | Task |
|-----------------|------|
| Trigger: "KQ", "四象限", "explore quadrants", "knowledge quadrants", "what do I know/not know" | Task 3 (SKILL.md frontmatter description) |
| `--depth shallow\|deep` flag | Task 3 (Flags table + Phase 1 branching) |
| `--web` flag | Task 3 (Web Mode Pre-Phase section) |
| Hybrid review (user corrects KK/KU) | Task 3 (Phase 2) |
| Shallow: 5-technique UU stack | Task 3 (Phase 1 shallow UU section) |
| Deep: persona rotation with orthogonal axes | Task 3 (Deep Mode UU Sub-Phase Steps 1–3) |
| Deep: TRIZ 9-Windows | Task 3 (Sub-Phase Step 4) |
| Deep + shallow: contradiction scan | Task 3 (shallow stack technique 5 + Step 4) |
| Surprise-value ranking | Task 3 (Step 3 consolidation) |
| Output format with emoji headers | Task 3 (Phase 3) |
| persona-axes.md reference | Task 2 |
| Repo layout matching CLAUDE.md convention | Tasks 1–5 |
| README with badges | Task 4 |
| LICENSE | Task 1 |
| CI validation | Task 1 |
| Scenario tests | Task 5 |
