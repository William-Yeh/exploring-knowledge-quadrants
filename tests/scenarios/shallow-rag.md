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
