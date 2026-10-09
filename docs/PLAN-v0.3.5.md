# KAMUSORA v0.3.5 — Universal Related Results Plan

## Raw intent
Expand “Bentuk lengkap & hasil terkait” so it works across English, Indonesian, and Romaji input. A user who enters a short root word should be offered selectable phrase continuations, while exact matches remain the primary result.

## Requirements
- Keep the single auto-detect input and the local/offline-only data boundary.
- For an exact word such as `good`, preserve the exact dictionary result and add clickable phrase choices such as `good night`, `good morning`, and `good afternoon`.
- For a context-dependent root such as `selamat`, do not invent a single Japanese equivalent. Show a short context-selection result and clickable locally-backed phrase options such as `selamat makan`, `selamat jalan`, `selamat menikmati`, and `selamat ulang tahun`.
- Clicking a phrase option replaces the input and runs the ordinary exact lookup, including the existing result fields and explicit relation-group cards.
- Suggestions must be deduplicated by canonical Japanese/Romaji pair, bounded to eight options, and drawn only from explicit local phrase records.
- Preserve exact-match-first behavior, existing phrase relation groups, typo suggestions as fallback, adaptive output fields, hidden empty results, Enter/Shift+Enter, mobile keyboard dismissal/result focus, and copy actions.
- Add useful dataset records and relation groups for common English and Indonesian phrases. Do not imply that every possible phrase is supported.
- Keep KAMUSORA standalone and offline; no API or dependency is added.

## Constraints
- Start from the exact v0.3.4 clean artifact and preserve a checkpoint backup before edits.
- Bump the product version to `0.3.5` because this adds user-facing behavior and data.
- Keep the release ZIP flat-root, immutable, and free of nested ZIPs/cache files.
- Perjalanan presentation layer is locked; append one historical entry only inside the content markers.
- The new recurring feature concept is recorded in Glosarium with one primary tag and no more than three secondary tags; synchronize both glossary manifests.
- Document the explicit knowledge-surface classification as `BOTH` because the feature concept and product milestone are recorded in Glosarium and Perjalanan.

## Acceptance criteria
1. `good` keeps the exact word result and shows clickable phrase options including `good night`, `good morning`, and `good afternoon`.
2. `selamat` shows a context-selection prompt and clickable phrase options including `selamat makan`, `selamat jalan`, `selamat menikmati`, and `selamat ulang tahun`.
3. Clicking a phrase option fills the input and runs the existing lookup flow.
4. Phrase suggestions are local, deduplicated, and capped at eight.
5. Existing exact-match-first related cards remain capped at four and preserve complete Japanese, Romaji, English, and Indonesian fields.
6. Existing translator and dictionary behavior remains intact.
7. All tests pass, Perjalanan checks pass, release preflight passes against the exact built ZIP, and the ZIP contains no nested archives or generated cache files.
8. Version/state/backlog/changelog/README/architecture/tutorial/release manifest/continuation snapshots are synchronized.

## Implementation sequence
Checkpoint backup → this plan → dataset and translator implementation → regression tests → glossary + Perjalanan knowledge-surface updates → document sync → source test suite → immutable release build → exact-artifact preflight → SHA-256 and delivery.
