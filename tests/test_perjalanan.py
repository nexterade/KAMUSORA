import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import perjalanan_tool as ct  # noqa: E402

HTML = (ROOT / "docs/Perjalanan.html").read_text(encoding="utf-8")


class PerjalananTemplateTests(unittest.TestCase):
    """CHECKPOINT 3.27A: the approved themed template must survive every content update."""

    def test_template_markers_present(self):
        for marker in [
            'data-perjalanan-template="genesis-perjalanan"', 'id="themeToggle"', 'id="print"',
            'id="sidebarToggle"', 'id="sidebarIndex"', 'id="perjalananIndex"', 'id="search"',
            'id="timeline"', 'id="totalCount"', 'id="visibleCount"', 'id="noResults"',
            'id="floatTop"', 'class="sitebar"', 'class="masthead"', 'class="layout"',
 'prefers-reduced-motion', '@media print',
            ':root[data-theme="dark"]', "genesis-perjalanan-theme", 'href="../favicon.svg"',
            'href="Glosarium.html"', 'name="viewport"', ct.START, ct.END,
        ]:
            self.assertIn(marker, HTML, marker)

    def test_theme_tokens_match_glossary(self):
        gloss = (ROOT / "docs/Glosarium.html").read_text(encoding="utf-8")
        for rx in (r":root\{--bg:[^}]+\}", r':root\[data-theme="dark"\]\{[^}]+\}'):
            self.assertEqual(re.search(rx, HTML).group(0), re.search(rx, gloss).group(0))


    def test_project_theme_defaults_dark_and_is_page_specific(self):
        self.assertIn('<html lang="id" data-theme="dark"', HTML)
        self.assertIn("genesis-perjalanan-theme", HTML)
        self.assertNotIn("genesis-theme", HTML)
        self.assertNotIn("v==='system'", HTML)

    def test_governance_separates_protected_core_identity_and_content(self):
        checkpoint = (ROOT / "docs/CHECKPOINT.md").read_text(encoding="utf-8")
        self.assertIn("TIGA lapisan kontrak", checkpoint)
        self.assertIn("PROTECTED PRESENTATION CORE", checkpoint)
        self.assertIn("PROJECT IDENTITY", checkpoint)
        self.assertIn("CONTENT LAYER", checkpoint)
        self.assertIn("mekanisme tema DARK/LIGHT", checkpoint)
        self.assertNotIn("tema (light/dark/system)", checkpoint)
        self.assertNotIn("Tidak ada mode `system`", HTML)
        self.assertIn("PERJALANAN ADOPTION CONTRACT", checkpoint)
        self.assertIn('data-origin="selected-concept"', checkpoint)
        self.assertIn('data-approval="user-approved"', checkpoint)
        self.assertIn("scripts/perjalanan_tool.py adoption", checkpoint)

    def test_brand_replacement_exception_is_explicit_and_scoped(self):
        checkpoint = (ROOT / "docs/CHECKPOINT.md").read_text(encoding="utf-8")
        self.assertIn("BRAND REPLACEMENT EXCEPTION", checkpoint)
        for allowed in ("nama project/brand", "logo", "favicon", "branding title"):
            self.assertIn(allowed, checkpoint)
        for forbidden in ("accent color", "typography system", "layout", "spacing",
                          "component styling", "dark/light\n  mechanism", "JavaScript behavior"):
            self.assertIn(forbidden, checkpoint)
        self.assertIn("HAH? · CATATAN SEJARAH", checkpoint)
        # A Project Identity rename must not alter the locked visual language.
        renamed = (HTML.replace("GENESIS", "HAH?")
                        .replace("Genesis", "HAH?")
                        .replace("GENESIS / PERJALANAN", "HAH? / PERJALANAN"))
        self.assertEqual(ct.presentation_fingerprint(HTML), ct.presentation_fingerprint(renamed))
        self.assertIn("--accent:#176B1D", HTML)
        self.assertIn("--accent:#2BEE34", HTML)
        self.assertNotIn("--accent:#ff0000", renamed)

    def test_brand_replacement_authorization_is_active_for_project(self):
        identity = json.loads((ROOT / "PROJECT_IDENTITY.json").read_text(encoding="utf-8"))
        self.assertEqual(identity["brand_replacement_exception"]["status"], "active")
        self.assertTrue(identity["brand_replacement_exception"]["explicit_user_approval_required"])
        self.assertEqual(identity["brand_replacement_exception"]["approved_by"], "user")
        self.assertEqual(identity["brand_replacement_exception"]["approved_name"], "KAMUSORA")
        self.assertEqual(ct.validate_brand_authorization(identity), [])
        self.assertIn('brand-replacement', ct.__doc__)

    def test_source_branding_is_provenance_not_active_identity(self):
        favicon=(ROOT/"favicon.svg").read_text(encoding="utf-8")
        self.assertIn("Genesis Starter", favicon)
        self.assertNotIn("PERNAH Continuity P", favicon)
        self.assertIn("provenance", (ROOT/"docs/RELEASE-MANIFEST.md").read_text(encoding="utf-8").lower())

    def test_no_external_resources(self):
        for bad in ("fonts.googleapis.com", "fonts.cdnfonts.com", "cdn.", "https://", "http://"):
            self.assertNotIn(bad, HTML, bad)
        self.assertNotRegex(HTML, r'<script[^>]+src=')
        self.assertNotRegex(HTML, r'<link[^>]+rel="stylesheet"')

    def test_presentation_layer_is_locked(self):
        lock = json.loads((ROOT / "tests/perjalanan_template_lock.json").read_text(encoding="utf-8"))
        self.assertEqual(ct.presentation_fingerprint(HTML), lock["style_script_sha256"],
                         "CSS/JS changed: a content-only update must not touch the presentation layer")

    def test_glossary_links_back_to_perjalanan(self):
        gloss = (ROOT / "docs/Glosarium.html").read_text(encoding="utf-8")
        self.assertIn('href="Perjalanan.html"', gloss)

    def test_utf8_integrity(self):
        self.assertNotIn("�", HTML)
        self.assertNotRegex(HTML, r"[\u0080-\u009f]")
        self.assertNotRegex(HTML, r"(?:â|Â)[\x80-\xbf]")


class PerjalananContentTests(unittest.TestCase):
    def test_content_contract_has_no_problems(self):
        self.assertEqual(ct.validate(HTML), [])

    def test_history_is_append_only_and_unmodified(self):
        _, entries = ct.parse(ct.content_region(HTML))
        current = [ct._record(e) for e in entries]
        manifest = json.loads((ROOT / "tests/perjalanan_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(current, manifest,
                         "Perjalanan differs from manifest: run scripts/perjalanan_tool.py manifest --append "
                         "(old entries may never change without explicit user approval)")

    def test_project_acceptance_record_is_approved(self):
        record=json.loads((ROOT/"PROJECT_ACCEPTANCE.json").read_text(encoding="utf-8"))
        self.assertEqual(record["status"], "accepted")
        self.assertEqual(record["selected_concept"]["id"], "romaji-v1")
        self.assertTrue(record["approval"]["approved"])
        self.assertEqual(record["approval"]["approved_by"], "user")

    def test_acceptance_record_contract_is_machine_verifiable(self):
        accepted={"status":"accepted","selected_concept":{"id":"concept-1","title":"Example"},"approval":{"approved":True,"approved_by":"user"}}
        self.assertEqual(ct.validate_acceptance_record(accepted), [])
        bad=dict(accepted); bad["approval"]={"approved":False,"approved_by":"ai"}
        self.assertTrue(ct.validate_acceptance_record(bad))

    def test_project_perjalanan_is_adopted(self):
        self.assertNotIn('data-starter-empty="true"', HTML)
        self.assertEqual(ct.validate_adoption(HTML), [])
        parts, entries = ct.parse(ct.content_region(HTML))
        self.assertEqual(len(parts), 1)
        self.assertEqual(len(entries), 8)
        self.assertEqual(entries[0]["origin"], "selected-concept")
        self.assertEqual(entries[1]["id"], "e-2026-10-09-ui-reliability")
        self.assertEqual(entries[2]["id"], "e-2026-10-09-translator-auto-detect")
        self.assertEqual(entries[3]["id"], "e-2026-10-09-translator-interactions")
        self.assertEqual(entries[4]["id"], "e-2026-10-09-related-results-dataset")
        self.assertEqual(entries[5]["id"], "e-2026-10-09-release-archive-hygiene")
        self.assertEqual(entries[6]["id"], "e-2026-10-09-universal-related-results")
        self.assertEqual(entries[7]["id"], "e-2026-10-09-universal-auto-correction")


class PerjalananToolNegativeTests(unittest.TestCase):
    """The guard itself must actually bite."""

    def entry(self, eid="e-2026-10-09-x", date="2026-10-09", basis="fact", title="T", origin=None, approval=None, concept_id=None):
        attrs = f' data-origin="{origin}"' if origin else ''
        attrs += f' data-approval="{approval}"' if approval else ''
        attrs += f' data-concept-id="{concept_id}"' if concept_id else ''
        return (f'<article class="entry-card" id="{eid}" data-date="{date}" data-basis="{basis}"{attrs}>'
                f'<div class="entry-meta"><time datetime="{date}">{date}</time>'
                f'<span class="basis" data-basis="{basis}">L</span></div><h3>{title}</h3>'
                f'<div class="entry-body"><p>x</p></div></article>')

    def wrap(self, *entries):
        return (ct.START + '<section class="part" id="part-1" data-part="1"><h2 class="part-title">P</h2>'
                + "".join(entries) + "</section>" + ct.END)

    def test_valid_minimal_passes(self):
        self.assertEqual(ct.validate(self.wrap(self.entry())), [])

    def test_missing_markers_rejected(self):
        self.assertTrue(ct.validate("<html><h3>plain</h3></html>"))

    def test_bad_basis_date_and_order_rejected(self):
        self.assertTrue(ct.validate(self.wrap(self.entry(basis="guess"))))
        self.assertTrue(ct.validate(self.wrap(self.entry(date="2026-13-40"))))
        self.assertTrue(ct.validate(self.wrap(self.entry("e-a", "2026-10-09"), self.entry("e-b", "2026-10-01"))))

    def test_duplicate_id_rejected(self):
        self.assertTrue(ct.validate(self.wrap(self.entry("e-a"), self.entry("e-a"))))

    def test_editing_old_entry_changes_fingerprint(self):
        a = ct.parse(self.wrap(self.entry(title="Asli")))[1][0]["fingerprint"]
        b = ct.parse(self.wrap(self.entry(title="Diedit")))[1][0]["fingerprint"]
        self.assertNotEqual(a, b)

    def test_css_change_changes_presentation_fingerprint(self):
        self.assertNotEqual(ct.presentation_fingerprint(HTML),
                            ct.presentation_fingerprint(HTML.replace("--accent:#176B1D", "--accent:#ff0000", 1)))
        self.assertNotEqual(ct.presentation_fingerprint(HTML),
                            ct.presentation_fingerprint(HTML.replace("'use strict'", "'use strict';/*x*/", 1)))

    def test_content_edit_does_not_change_presentation_fingerprint(self):
        edited = HTML.replace("Release gate hardening", "Judul diedit", 1)
        self.assertEqual(ct.presentation_fingerprint(HTML), ct.presentation_fingerprint(edited))

    def test_adoption_rejects_starter_empty(self):
        empty = HTML.replace('data-perjalanan-template="genesis-perjalanan"', 'data-perjalanan-template="genesis-perjalanan" data-starter-empty="true"')
        a = empty.index(ct.START) + len(ct.START)
        b = empty.index(ct.END)
        empty = empty[:a] + empty[b:]
        problems = ct.validate_adoption(empty)
        self.assertTrue(any("starter-empty" in p for p in problems))

    def test_adoption_requires_selected_concept_and_user_approval(self):
        html = self.wrap(self.entry(origin="other", approval="user-approved"))
        problems = ct.validate_adoption(html)
        self.assertTrue(any("selected-concept" in p for p in problems))
        html = self.wrap(self.entry(origin="selected-concept", approval="pending"))
        problems = ct.validate_adoption(html)
        self.assertTrue(any("user-approved" in p for p in problems))

    def test_adoption_accepts_project_origin_entry(self):
        html = self.wrap(self.entry(origin="selected-concept", approval="user-approved", concept_id="concept-1"))
        acceptance={"status":"accepted","selected_concept":{"id":"concept-1","title":"Example"},"approval":{"approved":True,"approved_by":"user"}}
        self.assertEqual(ct.validate_adoption(html, acceptance), [])


if __name__ == "__main__":
    unittest.main()
