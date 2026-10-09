import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
class RomajiProjectTests(unittest.TestCase):
    def test_universal_auto_detect_input_replaces_manual_modes(self):
        self.assertIn('Auto-detect · offline', HTML)
        self.assertIn('Contoh: good night, selamat makan, arigatou', HTML)
        self.assertIn('function detectLanguage(q)', HTML)
        self.assertNotIn('data-mode=', HTML)
        self.assertNotIn('id=\"swap\"', HTML)
        self.assertIn('id=\"detectedLanguage\"', HTML)
        self.assertIn('id=\"resultJP\"', HTML)
        self.assertIn('id=\"resultRomaji\"', HTML)
        self.assertIn('id=\"resultMeaning\"', HTML)
    def test_canonical_examples_are_present(self):
        for phrase in ['eiga','映画','えいが','taberu','食べる','nihongo','日本語','good night','selamat makan','oyasumi','itadakimasu']:
            self.assertIn(phrase, HTML)
    def test_local_first_boundary(self):
        self.assertIn('offline', HTML)
        self.assertNotRegex(HTML, r'https?://[^\"\']+')
    def test_dictionary_has_substantial_entries(self):
        match=re.search(r"const words = \[(.*?)\];",HTML,re.S)
        self.assertIsNotNone(match)
        self.assertGreaterEqual(match.group(1).count("['"), 80)
if __name__=='__main__': unittest.main()
