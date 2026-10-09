# ROMAJI — Architecture

## 1. Product boundary
KAMUSORA is a standalone, offline-first Japanese/Romaji learning utility. The first release does not call an external translation API.

## 2. Core flows
- One universal input auto-detects Indonesian, English, Romaji, and Japanese-script queries.
- Local phrase/word lookup adapts fields to source representation and can show up to four deduplicated related phrases from explicit relation groups: Romaji input displays Japanese script and available English/Indonesian meaning without repeating Romaji; English/Indonesian/Japanese-script input displays Japanese script, Romaji, and available meanings.
- Source-language detection and bounded typo suggestions and hybrid auto-correction are heuristic and dataset-aware; unmatched input is reported honestly with optional local suggestions rather than sent to an external service. High-confidence local corrections show the original and provide undo; ambiguous corrections preserve the input and show selectable choices. Sentence corrections use curated local patterns, not a universal grammar engine. The result panel stays hidden before submission or when the input is empty. Enter submits (Shift+Enter preserves an intentional newline); mobile submission closes the virtual keyboard and brings the result into view.
- Exact word/phrase matches remain primary. Short English/Indonesian root words can show up to eight deduplicated, clickable phrase-prefix choices from local records; ambiguous roots prompt for context rather than inventing a translation. Selecting a choice reuses the normal exact lookup flow. Exact phrase matches can additionally show up to four explicit-group related cards with Japanese, complete Romaji, EN/ID meanings, and local copy actions.
- A–Z Romaji-indexed dictionary with Japanese, kana, meaning, JLPT, and part of speech

## 3. Source of truth
The vocabulary dataset embedded in `index.html` is canonical for v0.1.0. Future releases may extract it into a data file, but the UI must remain able to rebuild the dictionary from that source.

## 4. UX principle
Romaji is a first-class representation. Japanese script remains visible as the paired source/target form rather than replacing Romaji.

## 5. Privacy
No user text is transmitted in v0.1.0. Clipboard and speech features use browser-local capabilities only.
