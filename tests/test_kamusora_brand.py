import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf-8')
class KamusoraBrandTests(unittest.TestCase):
    def test_brand_and_tagline(self):
        self.assertIn('KAMUSORA', HTML)
        self.assertIn('Find your Sora.', HTML)
    def test_character_background_asset_is_present(self):
        self.assertTrue((ROOT/'sora-bg.png').exists())
        self.assertIn('sora-bg.png', HTML)
    def test_background_is_full_page_and_non_interactive(self):
        self.assertIn('pointer-events:none', HTML)
        self.assertIn('inset:76px 0 0', HTML)
        self.assertIn('url("sora-bg.png") center top/100% auto no-repeat', HTML)
        self.assertNotIn('sora-bg.png") center top/cover', HTML)
        self.assertIn('opacity:1', HTML)
if __name__=='__main__': unittest.main()
