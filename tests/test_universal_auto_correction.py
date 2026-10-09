import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")

class UniversalAutoCorrectionTests(unittest.TestCase):
    def test_hybrid_correction_is_local_and_has_no_api(self):
        self.assertIn("function findAutoCorrection(q)", HTML)
        self.assertIn("const sentenceCorrections = [", HTML)
        self.assertIn("status:'auto'", HTML)
        self.assertNotIn("fetch(", HTML)
        self.assertNotIn("XMLHttpRequest", HTML)

    def test_exact_match_precedes_auto_correction(self):
        exact_phrase = HTML.index("if(p){showResult(p[1]")
        exact_word = HTML.index("if(w){showResult(w[1]")
        correction = HTML.index("const correction=findAutoCorrection(q)")
        self.assertLess(exact_phrase, correction)
        self.assertLess(exact_word, correction)

    def test_sentence_examples_and_multilingual_dataset_candidate_support(self):
        for sample in ["i dont no were to go", "I don't know where to go", "selmat mkan", "terima kasi"]:
            self.assertIn(sample, HTML)
        self.assertIn("phrases.forEach(p=>[p[0],p[1],p[2],p[3],p[4],p[5]]", HTML)
        self.assertIn("unique.forEach(w=>[w[0],w[1],w[2],w[3],w[4]]", HTML)

    def test_auto_correction_exposes_undo_and_original_text(self):
        self.assertIn('id="correctionStatus"', HTML)
        self.assertIn('id="undoCorrection"', HTML)
        self.assertIn("Kembalikan teks asli", HTML)
        self.assertIn("correctionOriginal=original", HTML)
        self.assertIn("if(correctionOriginal)renderCorrectionStatus(correctionOriginal,q)", HTML)

    def test_ambiguous_correction_keeps_original_and_offers_choices(self):
        self.assertIn("status:'ambiguous'", HTML)
        self.assertIn("renderAmbiguousCorrections(q,correction.candidates)", HTML)
        self.assertIn("teks asli belum diubah", HTML)

    def test_glossary_and_version_are_synchronized(self):
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.3.6")
        self.assertIn("Universal Auto-Correction", (ROOT / "docs/Glosarium.html").read_text(encoding="utf-8"))
        self.assertIn("e-2026-10-09-universal-auto-correction", (ROOT / "docs/Perjalanan.html").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
