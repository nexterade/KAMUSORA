# KAMUSORA v0.3.4 — Implementation Plan

## Goal
Deliver exact-match-first translator results with relevant local related entries and expand the bundled offline vocabulary/phrase dataset without changing KAMUSORA's standalone/offline boundary.

## Scope
- Preserve the universal input and heuristic detection for Indonesian, English, Romaji, and Japanese script.
- Preserve hidden result before submission/when empty, local typo suggestions, Enter-to-submit/Shift+Enter newline, and mobile keyboard dismissal/result focus.
- Keep the exact match as the primary result; display up to four additional deduplicated entries from the same explicitly assigned phrase relation group.
- Show Japanese script, complete Romaji, English/Indonesian meanings, and available metadata on each related entry; per-entry copy controls must copy the selected representation.
- Correct the `arigatou` entry to its casual form `ありがとう / arigatou`, and offer related polite/expanded forms such as `ありがとうございます / arigatou gozaimasu` and `どうもありがとう / doumo arigatou` only as dataset-backed related entries.
- Expand common JLPT vocabulary and everyday phrase coverage, keeping entries local and no external API.
- Keep unrelated visual/template layers untouched. `docs/Perjalanan.html` is append-only content-only; classify Glossary impact explicitly before document sync.

## Acceptance criteria
1. `arigatou` exact match appears first as `ありがとう`, with `arigatou` input still following adaptive result rules.
2. Related results are deduplicated, bounded (maximum four extras), relevant by explicit group, and each has complete Romaji plus EN/ID meanings.
3. `thank you`, `terima kasih`, `arigatou gozaimasu`, and other supported aliases resolve locally to appropriate entries.
4. New vocabulary is discoverable in dictionary and translator, with no accidental duplicate Romaji keys.
5. Existing translator interaction behavior remains intact.
6. Tests pass on source and exact extracted release ZIP; release preflight passes; artifact layout is flat-root and clean.
7. Version, README, boot/handoff state, state/backlog/changelog, tutorial, release manifest, and Perjalanan history are synchronized.

## Plan order
CHECKPOINT → boot/README/state/backlog/changelog → source/tests → Perjalanan/Glosarium → this plan → implementation → tests → document sync → package → exact-artifact preflight → checksum and delivery.
