## v0.3.6 release record

- Scope: hybrid offline-first auto-correction for high-confidence word/phrase typos and selected sentence patterns; undo for automatic correction; explicit choices for ambiguous candidates; exact valid matches preserved.
- Product version: `0.3.6`.
- Exact artifact validation: required; record SHA-256 and test output at delivery.
- Classification: `BOTH`
- Affected surfaces: `docs/Perjalanan.html`
- Affected surfaces: `docs/Glosarium.html`
- Evidence: appended `e-2026-10-09-universal-auto-correction` to the Perjalanan content-only region and added `Universal Auto-Correction` to the canonical Glossary with tag manifest synchronized.

## v0.3.5 release record

- Scope: universal phrase-prefix suggestions for English and Indonesian root words; exact word results remain primary, while context-dependent roots prompt for a phrase choice. Clicking a choice reuses the normal local lookup flow. Phrase suggestions are deduplicated and bounded to eight; exact phrase relation cards remain bounded to four.
- Product version: `0.3.5`.
- Exact artifact validation: required; record SHA-256 and test output at delivery.
- Classification: `BOTH`
- Affected surfaces: `docs/Perjalanan.html`
- Affected surfaces: `docs/Glosarium.html`
- Evidence: appended `e-2026-10-09-universal-related-results` to the Perjalanan content-only region and added the `Universal Related Results` canonical Glossary entry with the tag manifest synchronized.

# Project — Release Manifest

## Current artifact

- Project: `KAMUSORA`
- Version: `0.3.6`
- Previous artifact: `KAMUSORA-v0.3.5`
- Current artifact SHA-256: recorded at delivery time outside the ZIP.

## v0.3.4 packaging correction

- Scope: exclude nested ZIP archives and checkpoint backups from release packages; exact-artifact preflight rejects nested ZIP files.
- Product version: unchanged (`0.3.4`); packaging correction only.
- Classification: `PERJALANAN`
- Affected surfaces: `docs/Perjalanan.html`
- Evidence: appended `e-2026-10-09-release-archive-hygiene`; Glossary impact is `NONE` because no canonical glossary term or definition changed.

## v0.3.4 release record

- Scope: exact-match-first phrase lookup, up to four deduplicated related phrase cards, full Romaji/EN/ID/Japanese fields and per-entry copy controls, plus local vocabulary/phrase expansion.
- Exact artifact validation: required; record SHA-256 and test output at delivery.
- Classification: `PERJALANAN`
- Affected surfaces: `docs/Perjalanan.html`
- Evidence: appended `e-2026-10-09-related-results-dataset`. `docs/Glosarium.html` was inspected and classified `NONE`: no new canonical glossary term/definition was introduced.

## v0.3.3 release record

- Scope: adaptive translator result fields, hidden empty result, local typo suggestions, Enter-to-submit, and mobile keyboard/result focus behavior; dataset unchanged.
- Exact artifact validation: required; record SHA-256 and test output at delivery.
- Classification: `PERJALANAN`
- Affected surfaces: `docs/Perjalanan.html`
- Evidence: appended `e-2026-10-09-translator-interactions`. `docs/Glosarium.html` was inspected and classified `NONE`: no new canonical term/definition was introduced; this release implements existing product behavior and UI interaction.

## v0.3.1 release record

- Scope: light-theme consistency, sticky header/navigation reliability, version/document synchronization, and release artifact hygiene.
- Exact artifact validation: required; record SHA-256 and test output at delivery.
- Knowledge-surface classification: `PERJALANAN`
- Affected surfaces: `docs/Perjalanan.html`
- Evidence: appended `e-2026-10-09-ui-reliability` entry; glossary impact is `NONE` because no canonical term or definition was introduced.

## v0.3.2 release record

- Scope: universal translator input, local heuristic language detection, adaptive dictionary result, placeholder examples, and local phrase coverage.
- Exact artifact validation: required; record SHA-256 and test output at delivery.
- Classification: `PERJALANAN`
- Affected surfaces: `docs/Perjalanan.html`
- Evidence: appended `e-2026-10-09-translator-auto-detect`; Glossary impact is `NONE` because no new canonical terminology/definition was introduced.

## Origin

This starter carries universal governance and continuity patterns derived from a mature
project workflow. It intentionally does **not** carry the source project's identity,
roadmap, implementation, architecture, schema, or historical claims.

## Included baseline

- CHECKPOINT governance
- mandatory continuation order
- artifact continuity
- boot snapshot
- machine-readable state snapshot
- compact handoff
- release manifest
- source-of-truth discipline
- plan-first workflow
- test and exact-artifact validation
- documentation sync
- glossary integrity baseline
- Perjalanan integrity baseline
- Co-Developer / discussion-partner behavior
- cost/resource-aware recommendation baseline

## Validation contract

- Define a canonical test command when implementation begins.
- Exact delivered artifact must be validated before delivery.
- No generated cache/junk should be included in a release artifact.
- Final artifact checksum is recorded outside the ZIP to avoid self-reference.


## Glossary UI lineage

The Genesis Buku Besar uses a presentation pattern adapted from a mature prior artifact.
That lineage is provenance only: no source-product branding or identity contract is inherited.
Active Starter identity remains Genesis, while the approved Brand Replacement Exception is the
only route for a derived Project X to adopt its own project-facing name/logo/favicon/title.

The glossary content remains inherited knowledge: 109 entries are preserved, consisting of
93 inherited entries, 7 Genesis adaptations, and 7 Genesis-native entries. Provenance is visible
in the UI so knowledge inheritance is distinguishable from project inheritance.


## 0.1.5-starter-hardrules.3 delta
- Replaced the provider-embedded music UI with a native HTML5 local mini player in the sticky footer.
- Default Ebiet G. Ade playlist remains metadata-only; users provide audio files they own or are licensed to use.
- Added `music/README.md` with the local filename contract.
- Added `tests/glossary_entry_manifest.json` so glossary entries cannot silently disappear in future releases.


## Glossary template + favicon delta
- Replaced the Genesis glossary UI shell with the mature PERNAH glossary HTML template.
- Preserved the exact 107-entry Genesis glossary payload, including inherited/adapted/native provenance fields.
- The favicon asset was later normalized to Genesis Starter identity; source-artifact lineage remains documented separately.
- Removed obsolete Genesis music-player UI assertions from glossary tests while leaving `music/` documentation and files untouched.


## Hard-rule integration delta
- Added universal test discovery contract and exact-artifact release preflight requirements.
- Added universal data classification/privacy boundary with `docs/SECURITY.md`.
- Added raw-idea to requirement/prompt translation contract.
- Added knowledge-surface impact classification for Glossary/Perjalanan.
- Added executable Artifact Compliance Gate requirement.
- Preserved project-agnostic architecture: no PERNAH-specific storage, memory model, runtime, provider, or product architecture was added by this hard-rule integration.


## 0.1.5-starter-hardrules.3 delta
- Reframed the glossary as the open-ended Genesis **BUKU BESAR**: hybrid vocabulary + glossary with no restrictive content taxonomy.
- Replaced category filtering with informational tag metadata and an alphabet-first navigation model.
- Enforced the strict multi-tag contract: exactly 1 primary tag, 0–3 secondary tags, maximum 4 total, semantic justification required, no tag dumping, and no duplicate tags.
- Search covers terms, definitions, examples, and tags.
- Added `tests/glossary_tag_manifest.json` and schema regression coverage.


## 0.1.5-starter-hardrules.5 delta
- Fixed `release_preflight.py` false failure `required files missing: src, tests` (ZIPs without explicit directory entries). Directories are now derived from file paths; `src/` and `tests/` remain required.
- Fixed silent test-discovery gap: `test_knowledge_surface_hardrules.py` used pytest-style functions that `unittest discover` never ran. Converted to `unittest.TestCase`.
- Starter identity is intentionally versionless. Versioning begins when this Starter is copied into a new project; the generated project establishes its own VERSION source of truth.
- Preflight now also rejects OS/VCS junk, verifies the knowledge-surface classification below, and refuses a run that discovers zero tests.
- Added `scripts/build_release.py` (deterministic flat-root ZIP, junk-free, self-preflighting).
- Canonical test command recorded: `python3 -m unittest discover -s tests -v`.

## starter baseline delta
- Perjalanan template lock: themed shell shared with the Glosarium, locked presentation layer, append-only content layer, `scripts/perjalanan_tool.py`, Perjalanan manifest + template lock, CHECKPOINT 3.27A, preflight enforcement.
- Glosarium grew from 107 to 109 entries (Template Lock, Content Layer).

## Knowledge-surface impact
- Classification: `PERJALANAN`
- Affected surfaces: `docs/Perjalanan.html`
- Evidence: v0.3.4 appends `e-2026-10-09-related-results-dataset` in the content-only Perjalanan region. The Glosarium was inspected and classified `NONE` because no canonical glossary term/definition was introduced.
