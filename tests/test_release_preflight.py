import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "tests" / "release_preflight.py"
JUNK = {"__pycache__", ".git"}


def project_files():
    return [p for p in ROOT.rglob("*")
            if p.is_file() and not (set(p.relative_to(ROOT).parts) & JUNK) and p.suffix.lower() not in {".pyc", ".zip"}]


def make_zip(path, extra=None, skip=None, prefix=""):
    with zipfile.ZipFile(path, "w") as zf:
        for p in project_files():
            rel = p.relative_to(ROOT).as_posix()
            if skip and rel.startswith(skip):
                continue
            zf.write(p, prefix + rel)  # file entries only, no directory entries
        for name, data in (extra or {}).items():
            zf.writestr(name, data)


def run(zip_path):
    return subprocess.run([sys.executable, str(PREFLIGHT), str(zip_path)],
                          capture_output=True, text=True)


@unittest.skipIf(os.environ.get("GENESIS_PREFLIGHT_ACTIVE"), "already inside preflight; avoid recursion")
class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.dir = Path(self.td.name)

    def tearDown(self):
        self.td.cleanup()

    def test_flat_zip_without_directory_entries_passes(self):
        z = self.dir / "ok.zip"
        make_zip(z)
        r = run(z)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("PASS", r.stdout)

    def test_missing_src_is_still_rejected(self):
        z = self.dir / "nosrc.zip"
        make_zip(z, skip="src/")
        r = run(z)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("src", r.stdout)

    def test_junk_is_rejected(self):
        z = self.dir / "junk.zip"
        make_zip(z, extra={"__MACOSX/x": b"x"})
        self.assertNotEqual(run(z).returncode, 0)

    def test_wrapper_directory_is_rejected(self):
        z = self.dir / "wrapped.zip"
        make_zip(z, prefix="wrapped/")
        self.assertNotEqual(run(z).returncode, 0)

    def test_project_version_mismatch_is_rejected(self):
        z = self.dir / "drift.zip"
        current_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        state_text = (ROOT / "PROJECT_STATE.json").read_text(encoding="utf-8")
        make_zip(z, skip="PROJECT_STATE.json",
                 extra={"PROJECT_STATE.json": state_text.replace(
                     f'"version": "{current_version}"', '"version": "9.9.9"')})
        r = run(z)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("PROJECT_STATE.json", r.stdout)


    def test_nested_zip_is_rejected(self):
        z = self.dir / "nested.zip"
        make_zip(z, extra={"release/old-release.zip": b"not a nested release"})
        r = run(z)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("nested archive", r.stdout)

    def test_plain_unthemed_perjalanan_is_rejected(self):
        z = self.dir / "plain-perjalanan.zip"
        make_zip(z, skip="docs/Perjalanan.html",
                 extra={"docs/Perjalanan.html": "<!doctype html><html><body><h1>Awal Mula Kisah</h1><h3>x</h3></body></html>"})
        r = run(z)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Perjalanan", r.stdout)


if __name__ == "__main__":
    unittest.main()
