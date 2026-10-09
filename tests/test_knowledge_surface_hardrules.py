import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = (ROOT / "docs/CHECKPOINT.md").read_text(encoding="utf-8")
CONTINUATION = (ROOT / "PROJECT_CONTINUATION.md").read_text(encoding="utf-8")


class KnowledgeSurfaceGateTests(unittest.TestCase):
    # NOTE: these used to be bare pytest-style functions, which
    # `unittest discover` (the canonical command) silently never ran.
    def test_fail_closed_knowledge_surface_gate_exists(self):
        self.assertIn("3.34.3 KNOWLEDGE-SURFACE GATE", CHECKPOINT)
        self.assertIn("FAIL-CLOSED", CHECKPOINT)
        self.assertIn("BOTH / GLOSSARY / PERJALANAN / NONE", CHECKPOINT)

    def test_canonical_surfaces_cannot_be_implicitly_excluded(self):
        self.assertIn("MUST NOT exclude a surface", CHECKPOINT)
        self.assertIn("Existing canonical Glossary/Perjalanan files MUST be treated", CHECKPOINT)
        self.assertIn(
            "Existing canonical Glossary/Perjalanan surfaces are never implicitly\nexcluded.",
            CONTINUATION,
        )

    def test_uncertain_impact_fails_closed(self):
        self.assertIn("default is FAIL-CLOSED", CHECKPOINT)
        self.assertIn("fail closed", CONTINUATION.lower())


if __name__ == "__main__":
    unittest.main()
