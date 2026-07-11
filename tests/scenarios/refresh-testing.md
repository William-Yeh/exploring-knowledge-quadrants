# Scenario: Refresh mode — re-exploring an existing KQ file

## Invocation

```
KQ --refresh <path-to-existing-kq-file.md> --web
```

(Modeled on the real-world pair: `2026-04-23-kq-ai-是個穩定可靠的測試者嗎.md`
was manually refreshed into `2026-05-05-kq-ai-是個穩定可靠的測試者嗎.md`.)

## Expected Behavior

1. Refresh Pre-Phase: skill reads the old file, extracts topic, seed context,
   version, and all quadrant items.
2. Web pre-phase (because `--web`): the two standard searches plus
   `<topic> latest research evidence`.
3. Re-assessment pass: every old item gets a verdict (CONFIRMED / ANSWERED /
   STILL-OPEN / AWARE-NOW / STALE); a migration table is displayed with the
   draft.
4. Phase 1 probes run with the instruction to surface only NEW items.
5. Phase 2: user reviews migration table + quadrants.
6. Phase 3: a NEW file dated today, same slug, version bumped
   (`v2` if the old file had no version marker), `🔁 Migration Log` section
   appended. The old file is byte-for-byte unchanged.

## Pass Criteria

- [ ] Migration table displayed before user review, with a reason per move
- [ ] New file's metadata line contains `v<N+1> (refreshed from <old filename>)`
- [ ] New file contains a `## 🔁 Migration Log` section with one line per
      promote/demote/retire
- [ ] Old file is unchanged (`git diff --stat <old file>` is empty / file
      untouched on disk)
- [ ] No migrated item is restated as a "fresh" UU bullet
- [ ] `python3 skill/scripts/validate_kq.py <new-file> --level full` exits 0
