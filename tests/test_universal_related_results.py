import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


class UniversalRelatedResultsTests(unittest.TestCase):
    def test_universal_prefix_suggestions_are_local_and_bounded(self):
        self.assertIn("function findPhraseSuggestions(q)", HTML)
        body = re.search(r"function findPhraseSuggestions\(q\)\{(.*?)\n\}", HTML, re.S)
        self.assertIsNotNone(body)
        self.assertIn("norm(p[0]).startsWith(n+' ')", body.group(1))
        self.assertIn("seen.has(key)", body.group(1))
        self.assertIn("slice(0,8)", body.group(1))

    def test_english_root_has_explicit_clickable_continuations(self):
        for alias in ("good night", "good morning", "good afternoon", "good evening", "good luck", "good job"):
            self.assertIn("['" + alias + "'", HTML)
        self.assertIn("Frasa terkait untuk", HTML)
        self.assertIn('data-suggestion=\"${esc(p[0])}\"', HTML)

    def test_indonesian_root_has_contextual_phrase_options(self):
        for alias in ("selamat makan", "selamat jalan", "selamat menikmati", "selamat ulang tahun", "selamat datang", "selamat sore"):
            self.assertIn("['" + alias + "'", HTML)
        self.assertIn("showResult('Pilih konteks'", HTML)
        priority = re.search(r"n==='selamat'\?\[(.*?)\]:n==='good'", HTML, re.S)
        self.assertIsNotNone(priority)
        for alias in ("selamat makan", "selamat jalan", "selamat menikmati", "selamat ulang tahun", "selamat datang"):
            self.assertIn(alias, priority.group(1))

    def test_word_exact_match_is_preserved_before_related_options(self):
        translate = re.search(r"function translate\(\)\{(.*?)\n\}", HTML, re.S)
        self.assertIsNotNone(translate)
        body = translate.group(1)
        self.assertLess(body.index("if(w){"), body.index("if(findPhraseSuggestions(q).length)"))
        self.assertIn("renderSuggestions(q)", body)

    def test_phrase_options_reuse_existing_lookup_handler(self):
        self.assertIn("$('suggestions').addEventListener('click'", HTML)
        self.assertIn("$('query').value=btn.dataset.suggestion", HTML)
        self.assertIn("translate()", HTML)

    def test_feature_term_is_recorded_in_glossary(self):
        glossary = (ROOT / "docs/Glosarium.html").read_text(encoding="utf-8")
        self.assertIn("Universal Related Results", glossary)


if __name__ == "__main__":
    unittest.main()
