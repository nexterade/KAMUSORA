#!/usr/bin/env python3
"""Exact-artifact release preflight.

Usage: python3 tests/release_preflight.py PATH_TO_ZIP

Validates the delivered ZIP itself (not the working tree): required files,
flat-root layout, junk-free, version sync, knowledge-surface classification,
CHECKPOINT hard rules, then runs the canonical unittest command against the
extracted artifact.
"""
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REQUIRED_FILES = {
    "README.md", "PROJECT_BOOT.md", "PROJECT_CONTINUATION.md",
    "PROJECT_IDENTITY.json", "PROJECT_ACCEPTANCE.json",
    "PROJECT_CONTINUATION_PROMPT.md", "PROJECT_STATE.json", "docs/CHECKPOINT.md",
    "docs/STATE.md", "docs/BACKLOG.md", "docs/CHANGELOG.md", "docs/ARCHITECTURE.md",
    "docs/TUTORIAL.md", "docs/RELEASE-MANIFEST.md", "docs/SECURITY.md",
    "docs/Perjalanan.html", "docs/Glosarium.html",
    "scripts/perjalanan_tool.py", "tests/perjalanan_manifest.json", "tests/perjalanan_template_lock.json",
}
# Directories must contain at least one file. Derived from file paths, because
# many zip tools do not write explicit directory entries.
REQUIRED_DIRS = {"tests", "src"}
JUNK_PARTS = {"__pycache__", ".pytest_cache", "__MACOSX", ".git", ".DS_Store", "Thumbs.db"}
JUNK_SUFFIXES = (".pyc", ".pyo")
FORBIDDEN_ARCHIVE_SUFFIXES = (".zip",)
KNOWLEDGE_CLASSES = {"BOTH", "GLOSSARY", "PERJALANAN", "NONE"}
HARD_RULES = [
    "TEST DISCOVERY CONTRACT", "DATA CLASSIFICATION & PRIVACY BOUNDARY",
    "RAW IDEA → REQUIREMENT → PROMPT TRANSLATION",
    "KNOWLEDGE-SURFACE IMPACT CHECK", "Artifact Compliance Gate",
    "PERJALANAN TEMPLATE LOCK", "BRAND REPLACEMENT EXCEPTION",
]


def fail(msg):
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def check_layout(zf, artifact):
    names = [n for n in zf.namelist() if n]
    files = {n for n in names if not n.endswith("/")}
    dirs = {p.as_posix() for n in files for p in Path(n).parents if p.as_posix() != "."}
    dirs |= {n.rstrip("/") for n in names if n.endswith("/")}
    missing = sorted(f for f in REQUIRED_FILES if f not in files)
    missing += sorted(d for d in REQUIRED_DIRS if d not in dirs)
    if missing:
        fail("required files missing: " + ", ".join(missing))
    top = {n.split("/", 1)[0] for n in names}
    if artifact.stem in top:
        fail("archive has an enclosing wrapper directory; flat-root contract violated")
    for n in names:
        if Path(n.rstrip("/")).suffix.lower() in FORBIDDEN_ARCHIVE_SUFFIXES:
            fail(f"nested archive found in release ZIP: {n}")
        parts = set(Path(n.rstrip("/")).parts)
        if parts & JUNK_PARTS or n.endswith(JUNK_SUFFIXES):
            fail(f"junk/cache entry found in ZIP: {n}")
    return files


def read(zf, name):
    return zf.read(name).decode("utf-8")


def check_identity(zf):
    files = set(zf.namelist())
    has_version = "VERSION" in files
    state = json.loads(read(zf, "PROJECT_STATE.json"))
    if has_version:
        version = read(zf, "VERSION").strip()
        if not version:
            fail("VERSION empty")
        if state.get("version") != version:
            fail(f"PROJECT_STATE.json version {state.get('version')!r} != VERSION {version!r}")
        return version
    if state.get("version") != "[PROJECT VERSION]":
        fail("versionless Starter must use [PROJECT VERSION] placeholder in PROJECT_STATE.json")
    for rel in ("PROJECT_BOOT.md", "PROJECT_CONTINUATION.md", "docs/STATE.md", "docs/RELEASE-MANIFEST.md"):
        m = re.search(r"^- Version: `([^`]+)`", read(zf, rel), re.M)
        if not m or m.group(1) != "[PROJECT VERSION]":
            fail(f"{rel} must contain [PROJECT VERSION] in the versionless Starter")
    return "STARTER"

def check_knowledge_surface(zf):
    manifest = read(zf, "docs/RELEASE-MANIFEST.md")
    m = re.search(r"^- Classification: `([A-Z]+)`", manifest, re.M)
    if not m or m.group(1) not in KNOWLEDGE_CLASSES:
        fail("RELEASE-MANIFEST lacks knowledge-surface classification (BOTH/GLOSSARY/PERJALANAN/NONE)")
    cls = m.group(1)
    if "- Affected surfaces:" not in manifest or "- Evidence:" not in manifest:
        fail("knowledge-surface record needs 'Affected surfaces' and 'Evidence'")
    perjalanan = read(zf, "docs/Perjalanan.html")
    if 'data-perjalanan-template="genesis-perjalanan"' not in perjalanan:
        fail("Perjalanan is not the approved themed template (3.27A); plain HTML is not allowed")
    starter_empty = 'data-starter-empty="true"' in perjalanan
    if cls in ("BOTH", "PERJALANAN") and 'class="entry-card"' not in perjalanan and not starter_empty:
        fail("classification requires a Perjalanan entry but none found")
    if cls in ("BOTH", "GLOSSARY") and "Affected surfaces: `docs/Glosarium.html`" not in manifest \
            and "docs/Glosarium.html" not in manifest.split("## Knowledge-surface impact")[-1]:
        fail("classification requires Glosarium evidence in the manifest")
    print(f"knowledge-surface impact: {cls}")


def check_hard_rules(zf):
    checkpoint = read(zf, "docs/CHECKPOINT.md")
    for phrase in HARD_RULES:
        if phrase not in checkpoint:
            fail(f"CHECKPOINT missing required hard rule: {phrase}")


def run_tests(artifact):
    with tempfile.TemporaryDirectory(prefix="genesis-release-preflight-") as td:
        extract = Path(td) / "artifact"
        extract.mkdir()
        with zipfile.ZipFile(artifact) as zf:
            zf.extractall(extract)
        env = {"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin:/usr/local/bin", "GENESIS_PREFLIGHT_ACTIVE": "1"}
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=extract, text=True, capture_output=True, env=env,
        )
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        if result.returncode:
            fail("full test suite failed against exact extracted artifact")
        m = re.search(r"Ran (\d+) tests?", result.stderr)
        if not m or int(m.group(1)) == 0:
            fail("test discovery ran zero tests")
        return int(m.group(1))


def main():
    if len(sys.argv) != 2:
        fail("usage: python3 tests/release_preflight.py PATH_TO_ZIP")
    artifact = Path(sys.argv[1]).resolve()
    if not artifact.is_file():
        fail(f"artifact not found: {artifact}")
    try:
        zf = zipfile.ZipFile(artifact)
    except zipfile.BadZipFile:
        fail("not a valid ZIP file")
    with zf:
        check_layout(zf, artifact)
        version = check_identity(zf)
        check_knowledge_surface(zf)
        check_hard_rules(zf)
    count = run_tests(artifact)
    print(f"PASS: exact artifact validated ({version}, {count} tests)")


if __name__ == "__main__":
    main()
