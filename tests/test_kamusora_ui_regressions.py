import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


class KamusoraUIRegressionTests(unittest.TestCase):
    def test_light_theme_has_explicit_surface_coverage(self):
        for selector in [
            ':root[data-theme="light"] body{background:#eaf1f8}',
            ':root[data-theme="light"] .translator{background:var(--surface)',
            ':root[data-theme="light"] .input-wrap{background:#edf4fb',
            ':root[data-theme="light"] .result{background:#f1f6fc',
            ':root[data-theme="light"] .info-card',
            ':root[data-theme="light"] .feature-card',
            ':root[data-theme="light"] .footer',
        ]:
            self.assertIn(selector, HTML)

    def test_shell_does_not_create_sticky_scroll_container(self):
        self.assertIn('.shell{width:100%;min-height:100vh;position:relative;overflow:clip;', HTML)
        self.assertIn('.topbar{position:sticky;top:0;z-index:100;', HTML)

    def test_theme_toggle_changes_root_theme_and_persists_preference(self):
        self.assertIn("theme.addEventListener('click',()=>applyTheme(document.documentElement.dataset.theme==='dark'?'light':'dark'))", HTML)
        self.assertIn("localStorage.setItem('kamusora-theme',v)", HTML)

    def test_navigation_targets_reserve_sticky_header_offset(self):
        self.assertIn('#tests,#dictionary,#translator,#settings{scroll-margin-top:calc(var(--topbar-offset, 112px) + 12px)}', HTML)


if __name__ == "__main__":
    unittest.main()
