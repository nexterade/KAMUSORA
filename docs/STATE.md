# KAMUSORA — State

- Version: `0.3.6`
- Status: `active`
- Milestone: `Universal hybrid auto-correction for words, phrases, and selected sentence patterns`
- Product: offline-first Japanese dictionary and translator, indexed by Romaji, with English/Indonesian meanings.
- Implemented: KAMUSORA brand and K mark; single-field auto-detect translator for Indonesian, English, Romaji, and Japanese input; Romaji-indexed dictionary; JLPT/type filters; paginated dictionary rendering; Python static-web launcher; responsive navigation; exact-match-first related phrase cards (up to four extras) with per-entry copy controls; clickable, bounded universal phrase-prefix suggestions for English and Indonesian root words; hybrid local auto-correction for words, phrases, and selected sentence patterns with undo/ambiguity choices; expanded offline vocabulary/phrase dataset.
- Translator behavior: result stays hidden until a non-empty query is submitted; Romaji input emphasizes Japanese script plus English/Indonesian meaning, while English/Indonesian/Japanese-script input also shows Romaji; unmatched input can offer selectable local typo suggestions.
- Mobile interaction: Enter submits (Shift+Enter keeps an intentional newline); after submission on mobile, the virtual keyboard is blurred/closed and the result panel is brought into view.
- Data boundary: bundled local dataset only; no external API dependency. Dataset remains local/offline; current release expands common vocabulary, grouped phrase variants, and root-word phrase suggestions.
- Known limits: launcher serves static files only; it is not an application backend. Dictionary and correction coverage remain finite; language detection and typo/sentence corrections are heuristic and dataset-bound, not a universal grammar checker.
- Release packaging guard: build_release.py excludes nested .zip files; exact-artifact preflight rejects nested archives.
- Validation: source tests and exact extracted release artifact must pass `python3 -m unittest discover -s tests -v` and `python3 tests/release_preflight.py <ZIP>`.
- Next: expand local correction coverage and improve confidence calibration without changing valid exact inputs; continue vocabulary expansion with data-integrity tests.
