# KAMUSORA v0.3.6 — Universal Auto-Correction Plan

## Raw intent
Add a hybrid, local-first correction layer that can repair clear typos in words, phrases, and selected sentence patterns across English, Indonesian, Romaji, and Japanese script, while avoiding silent changes to valid input or intended meaning.

## Requirements
- Preserve exact valid word/phrase lookup precedence; never autocorrect an exact match.
- High-confidence local matches may replace the input automatically, show the original and corrected text, and provide an undo action.
- Ambiguous candidates must leave the original input unchanged and present selectable local suggestions.
- Cover single-word/phrase fuzzy matching plus a small explicit set of common sentence typo patterns; do not claim universal grammar correction.
- Use only bundled vocabulary/phrase data and deterministic local heuristics; no network, API, or external dependency.
- Preserve existing phrase-prefix suggestions, related cards, copy actions, hidden empty result, Enter/Shift+Enter behavior, and mobile focus behavior.
- Update Glosarium and append a Perjalanan milestone; classification `BOTH`.
- Preserve v0.3.5 as an immutable checkpoint backup outside the release package.

## Acceptance criteria
1. `good` and other exact valid entries are not autocorrected.
2. `goood mornig` can be corrected to `good morning` when a unique high-confidence local candidate exists.
3. Curated sentence typo `i dont no were to go` corrects to `I don't know where to go`.
4. Indonesian/Romaji/Japanese typo candidates can be offered when supported by local data; uncertain cases do not rewrite input.
5. Automatic correction shows original and corrected text with a working undo control.
6. Ambiguous corrections display selectable options while preserving the original input.
7. All existing behavior remains regression-tested.
8. Source tests, Perjalanan integrity checks, release preflight, and the exact built ZIP all pass.

## Known limits
- Sentence correction is bounded to curated patterns and local phrase candidates; it is not a full grammar or semantic rewriting engine.
- Dataset coverage and language detection remain finite and heuristic.

## Implementation sequence
Checkpoint backup → source implementation → regression tests → Glosarium + Perjalanan update → document sync → full test suite → immutable ZIP build → exact-artifact preflight → SHA-256 and delivery.
