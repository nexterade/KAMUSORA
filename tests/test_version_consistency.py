import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ProjectIdentityTests(unittest.TestCase):
    def test_project_has_version_file(self):
        self.assertRegex((ROOT/"VERSION").read_text(encoding="utf-8").strip(), r"^\d+\.\d+\.\d+$")
    def test_project_version_is_synced(self):
        data=json.loads((ROOT/"PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(data["version"], (ROOT/"VERSION").read_text(encoding="utf-8").strip())
        self.assertEqual(data["project"], "KAMUSORA")
    def test_build_script_supports_both_modes(self):
        text=(ROOT/"scripts/build_release.py").read_text(encoding="utf-8")
        self.assertIn('if version_file.exists():',text)
        self.assertIn('Genesis-Starter.zip',text)
        self.assertIn('f"{project_name}-v{version}.zip"',text)
    def test_boot_surfaces_use_project_version(self):
        for rel in ["PROJECT_BOOT.md","PROJECT_CONTINUATION.md","docs/STATE.md","docs/RELEASE-MANIFEST.md"]:
            text=(ROOT/rel).read_text(encoding="utf-8")
            self.assertIn(f"- Version: `{(ROOT / 'VERSION').read_text(encoding='utf-8').strip()}`",text,rel)
if __name__=="__main__": unittest.main()
