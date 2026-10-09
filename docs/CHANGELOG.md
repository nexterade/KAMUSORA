## 0.3.6 — 2026-10-09
- Added offline-first hybrid auto-correction for words, phrases, and selected sentence typo patterns across English, Indonesian, Romaji, and Japanese-script inputs.
- Exact valid word/phrase matches retain precedence; high-confidence local corrections show the original text and provide an undo action.
- Ambiguous corrections leave the original input unchanged and present selectable local candidates.
- Added regression tests and synchronized Glosarium + append-only Perjalanan documentation; knowledge-surface classification is `BOTH`.
- Sentence correction is intentionally bounded to local patterns and data, not a universal grammar checker.


## 0.3.5 — 2026-10-09
- Added universal local phrase-prefix suggestions for short English and Indonesian root words while preserving exact word matches as the primary result.
- Added clickable English continuations (`good night`, `good morning`, `good afternoon`, `good evening`, `good luck`, `good job`) and contextual Indonesian phrase choices including `selamat makan`, `selamat jalan`, `selamat menikmati`, `selamat ulang tahun`, and `selamat datang`.
- Ambiguous roots such as `selamat` now prompt for context instead of inventing a single translation; selecting a phrase reuses the existing exact lookup flow.
- Suggestions are dataset-backed, deduplicated by Japanese/Romaji pair, and bounded to eight choices. Existing related cards remain bounded to four.
- Added `Universal Related Results` to the canonical Glosarium and appended the v0.3.5 milestone to Perjalanan; knowledge-surface classification is `BOTH`.
- Added regression tests for root suggestions, contextual selection, click-through behavior, and glossary manifest integrity.


# Changelog

## 0.3.4 packaging correction — 2026-10-09
- Fixed the release builder to exclude ZIP archives from the release payload, preventing prior releases/checkpoint backups from being recursively bundled.
- Added an exact-artifact preflight guard and regression test that rejects nested ZIP archives.
- Product version remains 0.3.4; this is a packaging correction, not a product behavior change.


## 0.3.4 — 2026-10-09
- Kept exact-match phrase result as the primary result and added up to four deduplicated related phrase cards based on explicit local relation groups.
- Related cards show Japanese script, complete Romaji, English/Indonesian meanings, and separate copy controls.
- Corrected `arigatou` to its casual form and added related polite/expanded gratitude variants.
- Expanded local vocabulary and everyday phrase coverage without external API dependencies.
- Added regression tests for related-result rendering contracts and expanded dataset entries.
- Recorded the milestone in Perjalanan; Glossary impact classified as NONE because no canonical glossary term/definition was introduced.


## 0.3.3 — 2026-10-09
- Adapted translator result fields to detected input: Romaji queries show Japanese script and available English/Indonesian meanings without duplicating the entered Romaji; English, Indonesian, and Japanese-script queries include Romaji.
- Kept the result panel hidden until a non-empty query is submitted and returned it to the hidden state when input is cleared.
- Added bounded, local typo suggestions for unmatched input; selecting a suggestion reruns the local lookup.
- Enter submits the query (Shift+Enter remains a deliberate newline); mobile submission blurs the input to close the virtual keyboard and scrolls/focuses the result panel.
- Added translator interaction regression tests. Dataset remains unchanged in this release; vocabulary expansion is the next gate.
- Recorded the interaction milestone in Perjalanan; Glossary impact classified as NONE because no new canonical terminology/definition was introduced.


## 0.3.2 — 2026-10-09
- Replaced the three manual translator modes with a single auto-detect input for Indonesian, English, Romaji, and Japanese-script lookups.
- Removed the separate auto-detect banner; examples now live in the input placeholder.
- Added local phrase coverage for “good night” and “selamat makan”; results retain Japanese script, Romaji, and available English/Indonesian meaning.
- Added source-language feedback and input character count while preserving offline-first behavior.
- Recorded Translator evolution in Perjalanan; Glossary impact classified as NONE because no new canonical term/definition was introduced.


## 0.3.1 — 2026-10-09
- Fixed light-theme contrast and surface consistency across the hero, cards, translator inputs/results, dictionary controls, and footer.
- Fixed sticky header behavior on mobile by avoiding an overflow scrolling-container conflict and retaining section scroll offsets.
- Synchronized project identity/version snapshots, README launcher instructions, and release manifest.
- Added the UI reliability milestone to Perjalanan; Glossary impact classified as NONE because this maintenance release adds no new canonical terminology.
- Updated release builder to name ZIP artifacts from the active project identity and made version tests derive their expectation from `VERSION`.


## 0.1.0 — 2026-10-08
- Born from Genesis Starter after explicit user approval.
- Added ROMAJI visual identity and editorial landing page.
- Added EN/ID → Japanese + Romaji, Romaji → Japanese + meaning, and Japanese → Romaji + meaning modes.
- Added large A–Z Romaji-indexed dictionary with JLPT and part-of-speech filters.
- Kept v0.1.0 local/offline with no external API dependency.

### Background fit-screen refinement (v0.3.6 maintenance)
- Changed the `sora-bg.png` background from `cover` cropping to width-fit (`100% auto`) so the complete artwork remains visible without stretching.
- Removed the mobile oversized pseudo-element sizing; unused vertical space falls back to the dark navy background.
- Product version remains v0.3.6.
