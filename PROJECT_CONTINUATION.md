# Project — Continuation / Handoff State

## Authority

This file is a compact handoff aid, not a replacement for `docs/CHECKPOINT.md`.

Authority:
1. `docs/CHECKPOINT.md`
2. `docs/STATE.md`
3. `docs/BACKLOG.md`
4. `docs/CHANGELOG.md`
5. `README.md` / `docs/TUTORIAL.md`
6. `docs/ARCHITECTURE.md`
7. this file
8. `PROJECT_BOOT.md` / `PROJECT_STATE.json` as derived boot aids

## Mandatory continuation

**CHECKPOINT → PROJECT_BOOT → README → STATE → BACKLOG → CHANGELOG → SOURCE + TESTS →
PERJALANAN + GLOSARIUM (WAJIB) → PLAN → IMPLEMENT → TEST → DOCUMENT SYNC →
PACKAGE → TEST EXACT ARTIFACT → DELIVER ACCESSIBLE ARTIFACT**

The latest ZIP is the primary evidence. Old chat memory cannot replace artifact inspection.

## Artifact continuity

**CHAT IS EPHEMERAL. ARTIFACT IS CONTINUOUS.**

Important project state must live in the artifact.

## Knowledge-surface gate (mandatory)

Before `DOCUMENT SYNC`, run an explicit impact check. Enumerate the canonical
knowledge surfaces present in the artifact (including `docs/Glosarium.html` and
`docs/Perjalanan.html` when present), classify the change as
`BOTH`, `GLOSSARY`, `PERJALANAN`, or `NONE`, and record the affected files and
evidence. Existing canonical Glossary/Perjalanan surfaces are never implicitly
excluded. If impact is uncertain, **fail closed** and inspect the artifact before
proceeding.

## Perjalanan template lock (mandatory)

Saat membuat atau memperbarui `docs/Perjalanan.html`: JANGAN ubah CSS, JavaScript, layout, tema,
atau navigasi. Edit hanya content layer (antara `PERJALANAN CONTENT START` dan `END`), append-only.
Setelah itu jalankan `python3 scripts/perjalanan_tool.py manifest --append` lalu `check`. Lihat CHECKPOINT 3.27A.

## Current handoff

- Project: `KAMUSORA`
- Version: `0.3.6`
- Milestone: `Universal hybrid auto-correction for words, phrases, and selected sentence patterns`
- Next gate: `Expand local correction coverage and improve confidence calibration without changing valid exact inputs`
- Blockers: `No known blockers; next gate is correction coverage and confidence calibration; exact-artifact preflight required`

## Collaboration

AI acts as Co-Developer + Partner Diskusi: proactive, critical, constructive, not a yes-man,
and resource-aware. Project Owner retains final decision authority.

## Resume rule

Read the artifact to continue the project. Do not stop after proving that files were read.
If the artifact determines the next gate, continue without redundant confirmation.

## Identity & project-birth contracts
- `PROJECT_IDENTITY.json` separates active project branding from Genesis governance.
- `PROJECT_ACCEPTANCE.json` is the canonical record of the user-approved selected concept.
- Provenance may retain source lineage without inheriting source branding.
