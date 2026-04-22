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
| `--web` | off | Pre-ground UU with web searches (expert concerns + recent failures) |

### CLI

```
knowledge quadrants <topic> [--depth shallow|deep] [--web]
KQ <topic>
四象限 <topic>
```

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
