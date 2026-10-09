# KAMUSORA — Backlog

## Completed in v0.3.6 — Universal Auto-Correction
- [x] Preserve exact valid matches before considering correction.
- [x] Add offline-first high-confidence correction for words/phrases with visible original text and undo.
- [x] Add selectable choices for ambiguous correction candidates without changing the original input.
- [x] Add a bounded set of common sentence typo patterns and local multilingual alias matching.
- [x] Add correction regression tests and sync Glosarium + Perjalanan (`BOTH`).
- [x] Keep corrections local; no API, network request, or new dependency.

## Completed in v0.3.2
- [x] Replace manual translator modes with one auto-detect input for Indonesian, English, Romaji, and Japanese-script lookups.
- [x] Remove redundant mode/banner controls and use the input placeholder for examples.
- [x] Show detected source language and adaptive dictionary result fields; keep lookup local/offline.

## Completed in v0.3.1
- [x] Fix light theme so backgrounds, cards, translator form/result, dictionary controls, and footer use a coherent light palette.
- [x] Fix sticky header behavior by removing the shell's scrolling-container interference and preserve section scroll offsets.
- [x] Synchronize project/version boot documents and validate the exact flat-root ZIP.

## Completed in v0.3.3 — Translator interaction reliability
- [x] Adapt result fields to detected input: Romaji input emphasizes Japanese script + EN/ID meanings; EN/ID/Japanese-script input includes Japanese script + Romaji + available meanings.
- [x] Hide the result panel until a non-empty query is submitted; clearing input returns to the hidden state.
- [x] Add local, bounded typo suggestions for unmatched input, with selectable suggestions that re-run lookup.
- [x] Make Enter submit (Shift+Enter remains available for a deliberate newline); on mobile submission, close the virtual keyboard and scroll/focus the result panel.
- [x] Add regression tests for adaptive output, hidden empty result, typo suggestions, keyboard behavior, and mobile result focus.
- [x] Keep the bundled dataset unchanged in this release; dataset expansion follows as a separate next step.

## Completed in v0.3.5 — Universal Related Results
- [x] Preserve exact word results and add clickable phrase-prefix suggestions for English roots such as `good`.
- [x] Add context-selection behavior for Indonesian roots such as `selamat` rather than asserting one universal translation.
- [x] Bound suggestions to eight unique local phrase records, prioritized to include the requested common Indonesian variants.
- [x] Reuse the existing lookup path when a phrase suggestion is selected; preserve typo fallback and mobile submit behavior.
- [x] Add common phrase records for daytime greetings, encouragement, farewell, enjoyment, welcome, and birthday wishes.
- [x] Add the Universal Related Results concept to the canonical Glossary and the feature milestone to Perjalanan; classification `BOTH`.
- [x] Add regression tests for universal prefix suggestions and glossary manifest synchronization.

## Completed in v0.3.4 — Related results and dataset expansion
- [x] Keep exact-match phrase result primary and display up to four deduplicated related phrases from explicit relation groups.
- [x] Show full Romaji, Japanese script, EN/ID meanings, and per-entry copy controls for related results.
- [x] Separate casual `arigatou` from polite `arigatou gozaimasu`; add relevant gratitude variants.
- [x] Expand local vocabulary with common everyday terms and phrases without adding external APIs.
- [x] Add regression coverage for related result bounds, deduplication, and expanded dataset examples.

## Packaging hygiene correction (v0.3.4 artifact refresh)
- [x] Exclude ZIP archives and checkpoint backups from release payloads.
- [x] Reject nested ZIP archives during exact-artifact preflight.
- [x] Add regression coverage for nested-archive rejection.

## Next work
1. Improve language-detection confidence and continue expanding vocabulary dataset by JLPT level while preserving canonical entries.
2. Add richer phrase/sentence templates for EN and ID.
3. Add kana/kanji toggle and reading display controls.
4. Add optional local favorites / study list only when scoped.
5. Add tests for translation lookup and dictionary integrity.
6. Review and reconcile KAMUSORA active branding across canonical knowledge pages without modifying locked presentation layers.
