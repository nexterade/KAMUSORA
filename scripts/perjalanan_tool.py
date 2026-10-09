#!/usr/bin/env python3
"""Perjalanan guard tool (stdlib only).

Commands:
  check                          validate docs/Perjalanan.html against the template contract
  adoption                       validate that a derived Project uses Perjalanan and starts from an approved selected concept
  manifest --append              append NEW entries to tests/perjalanan_manifest.json (history is immutable)
  manifest --accept-correction ID [ID...]
                                 re-fingerprint specific entries after an explicit, user-approved correction
  lock --accept-presentation-change
                                 re-record the CSS/JS fingerprint after an explicit, user-approved template change
  brand-replacement check          validate explicit user-approved Project Identity authorization

Why: CHECKPOINT 3.27A/3.28 — a content update must not rewrite old history or the approved
presentation layer (theme, layout, navigation, search, responsive behavior, CSS/JS).
"""
import hashlib
import json
import re
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERJALANAN = ROOT / "docs/Perjalanan.html"
MANIFEST = ROOT / "tests/perjalanan_manifest.json"
LOCK = ROOT / "tests/perjalanan_template_lock.json"
IDENTITY = ROOT / "PROJECT_IDENTITY.json"
ACCEPTANCE = ROOT / "PROJECT_ACCEPTANCE.json"
BASIS = {"fact", "summary", "inference"}
START, END = "<!-- PERJALANAN CONTENT START -->", "<!-- PERJALANAN CONTENT END -->"


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.entries = [], []
        self._part = None
        self._entry = None
        self._article_depth = 0
        self._tag_stack = []
        self._capture = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        if tag == "section" and "part" in cls:
            self._part = {"id": a.get("id"), "no": a.get("data-part"), "title": ""}
            self.parts.append(self._part)
        if tag == "article" and "entry-card" in cls:
            self._entry = {"id": a.get("id"), "part": self._part["id"] if self._part else None,
                           "date": a.get("data-date"), "basis": a.get("data-basis"),
                           "origin": a.get("data-origin"), "approval": a.get("data-approval"),
                           "concept_id": a.get("data-concept-id"), "title": "", "time": None, "basis_label": None, "text": []}
            self._article_depth = 1
        elif self._entry is not None:
            self._article_depth += 1
            if tag == "time":
                self._entry["time"] = a.get("datetime")
            if tag == "span" and "basis" in cls:
                self._entry["basis_label"] = a.get("data-basis")
        if tag == "h2" and self._part is not None and "part-title" in cls:
            self._capture = ("part", None)
        if tag == "h3" and self._entry is not None:
            self._capture = ("entry", None)

    def handle_endtag(self, tag):
        if self._capture and tag in ("h2", "h3"):
            self._capture = None
        if self._entry is not None:
            self._article_depth -= 1
            if self._article_depth == 0:
                e = self._entry
                e["fingerprint"] = hashlib.sha256(
                    "\x1f".join([str(e["id"]), str(e["date"]), str(e["basis"]), norm(" ".join(e["text"]))]).encode("utf-8")
                ).hexdigest()
                self.entries.append(e)
                self._entry = None
        if tag == "section" and self._part is not None and not self._entry:
            pass

    def handle_data(self, data):
        if self._capture:
            kind, _ = self._capture
            if kind == "part" and self._part is not None:
                self._part["title"] = norm(self._part["title"] + " " + data)
            elif kind == "entry" and self._entry is not None:
                self._entry["title"] = norm(self._entry["title"] + " " + data)
        if self._entry is not None:
            self._entry["text"].append(data)


def parse(html):
    p = _Parser()
    p.feed(html)
    return p.parts, p.entries


def presentation_fingerprint(html):
    blocks = re.findall(r"<style[^>]*>(.*?)</style>|<script[^>]*>(.*?)</script>", html, re.S)
    joined = "\x1e".join(norm(a or b) for a, b in blocks)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def content_region(html):
    if START not in html or END not in html or html.index(START) > html.index(END):
        return None
    return html[html.index(START) + len(START): html.index(END)]


def validate(html):
    """Return a list of human-readable problems (empty list = OK)."""
    problems = []
    region = content_region(html)
    if region is None:
        return ["content markers missing or out of order: " + START + " ... " + END]
    parts, entries = parse(region)
    starter_empty = 'data-starter-empty="true"' in html
    if not parts and not starter_empty:
        problems.append("no <section class=\"part\"> found in content region")
    seen = set()
    last = None
    for e in entries:
        eid = e["id"]
        if not eid or not re.fullmatch(r"e-[a-z0-9][a-z0-9\-]*", eid):
            problems.append(f"entry id invalid (expected e-<kebab>): {eid!r}")
        if eid in seen:
            problems.append(f"duplicate entry id: {eid}")
        seen.add(eid)
        if e["part"] is None:
            problems.append(f"{eid}: entry outside any part")
        try:
            d = date.fromisoformat(e["date"] or "")
        except ValueError:
            problems.append(f"{eid}: data-date must be YYYY-MM-DD, got {e['date']!r}")
            d = None
        if e["time"] != e["date"]:
            problems.append(f"{eid}: <time datetime> must equal data-date")
        if d and last and d < last:
            problems.append(f"{eid}: chronological order violated ({d} < {last})")
        last = d or last
        if e["basis"] not in BASIS:
            problems.append(f"{eid}: data-basis must be one of {sorted(BASIS)}")
        if e["basis_label"] != e["basis"]:
            problems.append(f"{eid}: <span class=\"basis\" data-basis> must equal article data-basis")
        if not e["title"]:
            problems.append(f"{eid}: missing <h3> title")
    part_ids = [p["id"] for p in parts]
    if len(part_ids) != len(set(part_ids)) or any(not i for i in part_ids):
        problems.append("part ids must be unique and non-empty")
    return problems


def validate_acceptance_record(record):
    problems=[]
    if not isinstance(record, dict):
        return ["PROJECT_ACCEPTANCE.json must be an object"]
    if record.get("status") != "accepted":
        problems.append("PROJECT_ACCEPTANCE.json status must be accepted for a derived Project")
    approval=record.get("approval") or {}
    if approval.get("approved") is not True or approval.get("approved_by") != "user":
        problems.append("selected concept requires explicit user approval in PROJECT_ACCEPTANCE.json")
    concept=record.get("selected_concept") or {}
    if not concept.get("id") or not concept.get("title"):
        problems.append("selected_concept requires non-empty id and title")
    return problems


def validate_brand_authorization(record):
    problems=[]
    if not isinstance(record, dict):
        return ["PROJECT_IDENTITY.json must be an object"]
    ex=record.get("brand_replacement_exception") or {}
    if ex.get("status") != "active":
        problems.append("Brand Replacement Exception is not active")
    if ex.get("explicit_user_approval_required") is not True:
        problems.append("explicit_user_approval_required must remain true")
    if ex.get("approved_by") != "user" or not ex.get("approved_name"):
        problems.append("Project Identity requires explicit user approval and approved_name")
    if set(ex.get("allowed_fields",[])) != {"name","logo","favicon","branding_title"}:
        problems.append("Brand Replacement Exception allowed scope is invalid")
    forbidden=set(ex.get("forbidden_fields",[]))
    required_forbidden={"accent_color","typography","layout","spacing","component_styling","theme_mechanism","javascript_behavior","structure","governance","guards"}
    if not required_forbidden.issubset(forbidden):
        problems.append("Brand Replacement Exception forbidden scope is incomplete")
    return problems


def validate_adoption(html, acceptance_record=None):
    """Validate the mandatory Perjalanan adoption + project-birth acceptance contract."""
    problems = validate(html)
    region = content_region(html)
    _, entries = parse(region or "")
    if 'data-starter-empty="true"' in html:
        problems.append("derived Project adoption cannot remain starter-empty: Perjalanan must be used")
        return problems
    if not entries:
        problems.append("Perjalanan adoption requires at least one historical entry")
        return problems
    if acceptance_record is None:
        if not ACCEPTANCE.exists():
            problems.append("PROJECT_ACCEPTANCE.json missing")
            return problems
        acceptance=json.loads(ACCEPTANCE.read_text(encoding="utf-8"))
    else:
        acceptance=acceptance_record
    problems.extend(validate_acceptance_record(acceptance))
    first = entries[0]
    concept=acceptance.get("selected_concept") or {}
    if first.get("origin") != "selected-concept":
        problems.append("first Perjalanan entry must have data-origin=selected-concept")
    if first.get("approval") != "user-approved":
        problems.append("first Perjalanan entry must have data-approval=user-approved")
    if first.get("concept_id") != concept.get("id"):
        problems.append("first Perjalanan entry data-concept-id must match PROJECT_ACCEPTANCE.json selected_concept.id")
    return problems


def _load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else []


def _record(e):
    return {"id": e["id"], "date": e["date"], "title": e["title"], "sha256": e["fingerprint"]}


def cmd_check():
    html = PERJALANAN.read_text(encoding="utf-8")
    problems = validate(html)
    _, entries = parse(content_region(html) or "")
    if [_record(e) for e in entries] != _load_manifest():
        problems.append("entries differ from tests/perjalanan_manifest.json (use `manifest --append`)")
    if not LOCK.exists():
        problems.append("tests/perjalanan_template_lock.json missing")
    elif presentation_fingerprint(html) != json.loads(LOCK.read_text(encoding="utf-8"))["style_script_sha256"]:
        problems.append("CSS/JS presentation layer differs from tests/perjalanan_template_lock.json")
    if 'data-perjalanan-template="genesis-perjalanan"' not in html:
        problems.append("template marker data-perjalanan-template missing (plain HTML is not allowed)")
    for p in problems:
        print("FAIL:", p)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


def cmd_brand_replacement(args):
    if args != ["check"]:
        print("usage: python3 scripts/perjalanan_tool.py brand-replacement check"); return 2
    if not IDENTITY.exists():
        print("FAIL: PROJECT_IDENTITY.json missing"); return 1
    problems=validate_brand_authorization(json.loads(IDENTITY.read_text(encoding="utf-8")))
    if problems:
        for p in problems: print("FAIL:",p)
        return 1
    print("BRAND REPLACEMENT AUTHORIZED: explicit user-approved Project Identity is active")
    return 0


def cmd_adoption():
    html = PERJALANAN.read_text(encoding="utf-8")
    problems = validate_adoption(html)
    if problems:
        for p in problems:
            print("FAIL:", p)
        return 1
    print("ADOPTION OK: Perjalanan is active and its first entry records the user-approved selected concept")
    return 0


def cmd_manifest(args):
    html = PERJALANAN.read_text(encoding="utf-8")
    _, entries = parse(content_region(html) or "")
    current = [_record(e) for e in entries]
    old = _load_manifest()
    accept = set()
    if "--accept-correction" in args:
        accept = set(args[args.index("--accept-correction") + 1:])
    elif "--append" not in args:
        print(__doc__); return 2
    if len(current) < len(old):
        print("FAIL: entries were removed; history is append-only"); return 1
    for i, o in enumerate(old):
        c = current[i]
        if c["id"] != o["id"]:
            print(f"FAIL: order/identity changed at position {i}: {o['id']} -> {c['id']}"); return 1
        if c != o:
            if o["id"] in accept:
                continue
            print(f"FAIL: historical entry modified: {o['id']} (needs explicit user-approved --accept-correction)"); return 1
    MANIFEST.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"manifest updated: {len(current)} entries ({len(current) - len(old)} new)")
    return 0


def cmd_lock(args):
    if "--accept-presentation-change" not in args:
        print("refusing: pass --accept-presentation-change only after explicit user approval of a template change"); return 2
    html = PERJALANAN.read_text(encoding="utf-8")
    LOCK.write_text(json.dumps({"template": "genesis-perjalanan", "template_version": 1,
                                "style_script_sha256": presentation_fingerprint(html)}, indent=2) + "\n", encoding="utf-8")
    print("template lock updated")
    return 0


def main(argv):
    if not argv:
        print(__doc__); return 2
    if argv[0] == "check": return cmd_check()
    if argv[0] == "adoption": return cmd_adoption()
    if argv[0] == "brand-replacement": return cmd_brand_replacement(argv[1:])
    if argv[0] == "manifest": return cmd_manifest(argv[1:])
    if argv[0] == "lock": return cmd_lock(argv[1:])
    print(__doc__); return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
