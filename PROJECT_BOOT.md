# PROJECT BOOT SNAPSHOT

> Fast orientation aid. Not a source of truth higher than CHECKPOINT/STATE/BACKLOG.

## Identity

- Project: `KAMUSORA`
- Purpose: `[ONE-LINE PURPOSE]`
- Version: `0.3.6`
- Status: `active`
- Milestone: `Universal hybrid auto-correction for words, phrases, and selected sentence patterns`

## Current continuation

- Current next gate: `Expand local correction coverage and improve confidence calibration without changing valid exact inputs`
- Current task: `Universal hybrid correction is implemented locally; next expand correction coverage and calibrate confidence with regression tests`
- Blockers: `None known`

## Validation

- Test command: `python3 -m unittest discover -s tests -v`
- Expected status: `All starter tests pass (0 failures, 0 skipped)`
- Exact artifact validation: `Required before delivery`

## Mandatory context

- `docs/CHECKPOINT.md`
- `README.md`
- `docs/STATE.md`
- `docs/BACKLOG.md`
- `docs/CHANGELOG.md`
- `docs/ARCHITECTURE.md`
- `docs/TUTORIAL.md`
- `docs/Perjalanan.html`
- `docs/Glosarium.html`
- `docs/SECURITY.md`
- source
- tests

## Working style

- Bahasa Indonesia, natural, santai, jelas, tidak kaku.
- AI = Co-Developer + Partner Diskusi.
- Bukan yes-man.
- Proaktif terhadap risiko dan alternatif yang materially membantu.
- Cost/resource-aware.
- Default: free/local/offline/low-cost when sufficient.

## Continuity

**CHAT IS EPHEMERAL. ARTIFACT IS CONTINUOUS.**


## Knowledge-surface gate
- Before DOCUMENT SYNC, explicitly classify impact as BOTH/GLOSSARY/PERJALANAN/NONE.
- Existing canonical Glossary/Perjalanan surfaces are never implicitly excluded.
- Uncertain impact is fail-closed: inspect before syncing.

## Perjalanan template lock
- Perjalanan = presentation layer terkunci + content layer append-only (CHECKPOINT 3.27A).
- Starter: Perjalanan sengaja kosong. Project turunan WAJIB mengadopsi dan menggunakannya.
- Entry pertama Project X WAJIB berasal dari konsep yang dipilih/disetujui user.
- Adoption gate: `python3 scripts/perjalanan_tool.py adoption`.
- Update: `python3 scripts/perjalanan_tool.py manifest --append` lalu `check`.

## Identity & acceptance gates
- Starter: Brand Replacement Exception inactive.
- Derived Project: explicit user-approved Project Identity is required before branding replacement.
- Derived Project: `PROJECT_ACCEPTANCE.json` must record the selected concept before Perjalanan adoption.
- Gates: `python3 scripts/perjalanan_tool.py brand-replacement check` and `python3 scripts/perjalanan_tool.py adoption`.
