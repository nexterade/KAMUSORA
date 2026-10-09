#!/usr/bin/env python3
"""Build a deterministic, flat-root release ZIP and preflight it.

Usage: python3 scripts/build_release.py [OUTPUT_DIR]
If VERSION exists, builds the versioned project artifact. If VERSION is absent, builds Genesis-Starter.zip.
"""
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JUNK = {"__pycache__", ".pytest_cache", "__MACOSX", ".git", ".DS_Store"}


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent
    version_file = ROOT / "VERSION"
    if version_file.exists():
        version = version_file.read_text(encoding="utf-8").strip()
        if not version:
            raise SystemExit("VERSION exists but is empty")
        project_name = json.loads((ROOT / "PROJECT_STATE.json").read_text(encoding="utf-8")).get("project", "Project")
        out = out_dir / f"{project_name}-v{version}.zip"
    else:
        version = "STARTER"
        out = out_dir / "Genesis-Starter.zip"
    if out.exists():
        raise SystemExit(f"refusing to overwrite immutable artifact: {out}")
    files = sorted(
        p for p in ROOT.rglob("*")
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & JUNK) and p.suffix.lower() not in {".pyc", ".pyo", ".zip"}
    )
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in files:  # fixed timestamp => reproducible bytes
            info = zipfile.ZipInfo(p.relative_to(ROOT).as_posix(), (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, p.read_bytes())
    r = subprocess.run([sys.executable, "-I", str(ROOT / "tests/release_preflight.py"), str(out)])
    if r.returncode:
        out.unlink()
        raise SystemExit("preflight failed; artifact removed")
    print(out)


if __name__ == "__main__":
    main()
