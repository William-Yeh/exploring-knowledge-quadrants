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
- [Item]: [brief note] (Security auditor)
- [Item]: [brief note] (End user researcher)
- [3–7 items total with persona attribution]
```

## Pass Criteria

- [ ] Axes selection is from two different axis types (not same type)
- [ ] Personas line present in UU section header
- [ ] Each UU item has a source persona in parentheses
- [ ] TRIZ 9-Windows scan (UU sub-phase Step 4) contributes at least one item
- [ ] Contradiction scan (UU sub-phase Step 4) contributes at least one item
- [ ] No UU item duplicates a KU item
- [ ] File written and path announced
