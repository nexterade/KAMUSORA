import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


class TranslatorInteractionTests(unittest.TestCase):
    def test_result_starts_hidden_and_has_suggestion_region(self):
        self.assertRegex(HTML, r'<div class="result" id="result"[^>]*\bhidden\b')
        self.assertIn('id="suggestions"', HTML)
        self.assertIn('id="relatedResults"', HTML)
        self.assertIn('.result[hidden],.suggestions[hidden]{display:none!important}', HTML)

    def test_adaptive_result_hides_duplicate_romaji_for_romaji_input(self):
        self.assertIn("$('resultRomaji').hidden=detectedKey==='romaji'", HTML)
        self.assertIn("$('resultJP').hidden=false", HTML)
        self.assertIn("$('resultMeaning').hidden=false", HTML)

    def test_related_results_are_local_bounded_deduplicated_and_copyable(self):
        self.assertIn('function relatedPhrases(match)', HTML)
        self.assertIn('new Set([`${norm(match[1])}|${norm(match[3])}`])', HTML)
        self.assertIn('slice(0,4)', HTML)
        self.assertIn('data-copy-value=', HTML)
        self.assertIn("$('relatedResults').addEventListener('click'", HTML)

    def test_typo_suggestions_are_local_and_selectable(self):
        self.assertIn('function findSuggestions(q)', HTML)
        self.assertIn('function renderSuggestions(q)', HTML)
        self.assertIn('data-suggestion=', HTML)
        self.assertIn("$('suggestions').addEventListener('click'", HTML)
        self.assertIn('Mungkin yang kamu maksud? · Kecocokan terdekat dari dataset lokal', HTML)

    def test_enter_submits_and_shift_enter_is_preserved(self):
        self.assertIn("if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing&&e.keyCode!==229)", HTML)
        self.assertIn('e.preventDefault();translate()', HTML)

    def test_mobile_submit_closes_keyboard_and_focuses_result(self):
        self.assertIn("matchMedia('(max-width:700px)').matches", HTML)
        self.assertIn("$('query').blur()", HTML)
        self.assertIn("$('result').scrollIntoView({behavior:'smooth',block:'start'})", HTML)
        self.assertIn("$('result').focus({preventScroll:true})", HTML)

    def test_clear_returns_translator_to_empty_hidden_state(self):
        clear_handler = re.search(r"\$\('clear'\)\.addEventListener\('click',\(\)=>\{(.*?)\}\);", HTML, re.S)
        self.assertIsNotNone(clear_handler)
        self.assertIn("$('result').hidden=true", clear_handler.group(1))


if __name__ == "__main__":
    unittest.main()
