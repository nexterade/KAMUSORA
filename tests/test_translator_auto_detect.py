import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


class TranslatorAutoDetectTests(unittest.TestCase):
    def test_no_manual_source_mode_controls_remain(self):
        self.assertNotIn("data-mode=", HTML)
        self.assertNotIn("function setMode(", HTML)
        self.assertNotIn("id=\"swap\"", HTML)

    def test_single_input_has_examples_and_length_limit(self):
        self.assertIn('id="query" maxlength="500"', HTML)
        self.assertIn("Contoh: good night, selamat makan, arigatou", HTML)
        self.assertIn("id=\"inputCount\"", HTML)

    def test_detection_supports_three_requested_languages_and_japanese_script(self):
        body = re.search(r"function detectLanguage\(q\)\{(.*?)\n\}", HTML, re.S)
        self.assertIsNotNone(body)
        for token in ["Romaji", "Indonesia", "English", "Japanese"]:
            self.assertIn(token, body.group(1))

    def test_result_keeps_japanese_romaji_and_meaning_fields(self):
        for element_id in ["resultJP", "resultRomaji", "resultMeaning", "detectedLanguage"]:
            self.assertIn(f'id="{element_id}"', HTML)

    def test_new_phrase_examples_are_local_dataset_entries(self):
        self.assertIn("['good night','おやすみ','おやすみ','oyasumi'", HTML)
        self.assertIn("['selamat makan','いただきます','いただきます','itadakimasu'", HTML)
        self.assertIn("['arigatou','ありがとう','ありがとう','arigatou','thank you','terima kasih','gratitude']", HTML)
        self.assertIn("['arigatou gozaimasu','ありがとうございます','ありがとうございます','arigatou gozaimasu','thank you (polite)','terima kasih (sopan)','gratitude']", HTML)
        self.assertIn("['arigatou gozaimashita','ありがとうございました','ありがとうございました','arigatou gozaimashita'", HTML)
        self.assertIn("['doumo arigatou','どうもありがとう','どうもありがとう','doumo arigatou'", HTML)
        self.assertIn("['kazoku','家族','かぞく','family','keluarga','noun','N5']", HTML)
        self.assertIn("['onegaishimasu','お願いします','おねがいします','please','tolong / mohon','expression','N5']", HTML)
        self.assertIn("const romajiInputs=new Set(['arigatou','ohayou','konnichiwa'])", HTML)
        self.assertIn('function relatedPhrases(match)', HTML)
        self.assertIn('function renderRelatedResults(match)', HTML)
        self.assertIn('Bentuk lengkap &amp; hasil terkait', HTML)
        self.assertIn('slice(0,4)', HTML)
        self.assertIn("Local dictionary mode", HTML)


if __name__ == "__main__":
    unittest.main()
