#!/usr/bin/env python3
"""lao_check.py - find common errors in Lao (ພາສາລາວ) text and files.

Usage
  python3 lao_check.py FILE_OR_DIR [FILE_OR_DIR ...]
  python3 lao_check.py report.docx --font assets/fonts/NotoSansLao-VariableFont_wdthwght.ttf
  echo "ສະບາຍດີ" | python3 lao_check.py -

Reads: .txt .md .html .htm .css .svg .xml .json .csv .tsv .srt .vtt .yml .yaml, .docx, .pptx, .xlsx
and .pdf (needs pdftotext/pdffonts from poppler, or pypdf). Standard library only; fontTools is
optional and only needed for --font.

What it checks (code, severity)
  LAO001 High    Thai and Lao letters mixed inside one word
  LAO002 High    Vowel sign or tone mark with no consonant before it
  LAO003 High    Prefixed vowel (ເ ແ ໂ ໄ ໃ) not followed by a consonant (often typed in reading order)
  LAO004 High    Two stacked marks of the same kind (for example two tone marks)
  LAO005 Medium  Tone mark typed before the vowel sign (Unicode order is vowel, then tone mark)
  LAO006 Medium  Lao digits and ASCII digits mixed in Lao text
  LAO007 Low     Variant spellings mixed (ໜ and ຫນ, ໝ and ຫມ, ຫຼ and ຫລ)
  LAO008 High    Zero-width space inside a syllable
  LAO009 High    Replacement characters (U+FFFD), boxes (□) or invalid UTF-8
  LAO010 Medium  Private-use characters (legacy Lao fonts) in Lao text
  LAO011 Low     Thai text inside a Lao line (fine if intentional; keep it in its own block)
  LAO012 Low     Vowel signs or tone marks standing alone as words (normal in charts; --teaching hides it)
  LAO020 .. 029  File-level settings (HTML lang and charset, CSS spacing and line height,
                 Word/PowerPoint complex-script font, PDF fonts not embedded)
  LAO030 High    A used character is missing from the --font file; LAO031 font has no Lao shaping tables

Exit status: 0 = no High findings, 1 = High findings (or Medium with --strict), 2 = a file could not be read.
It does NOT check spelling, grammar, meaning or how the text looks. Always render and look at the result.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import zipfile
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------- Unicode sets
LAO_LO, LAO_HI = 0x0E80, 0x0EFF
THAI_LO, THAI_HI = 0x0E00, 0x0E7F
CONS = {cp for cp in range(0x0E81, 0x0EAF) if unicodedata.name(chr(cp), "").startswith("LAO LETTER")}
CONS |= {0x0EDC, 0x0EDD, 0x0EDE, 0x0EDF}                  # ໜ ໝ and the Khmu letters
PREFIX = set(range(0x0EC0, 0x0EC5))                          # ເ ແ ໂ ໄ ໃ
UPPER = {0x0EB1, 0x0EB4, 0x0EB5, 0x0EB6, 0x0EB7, 0x0EBB}    # ັ ິ ີ ຶ ື ົ
LOWER = {0x0EB8, 0x0EB9}                                     # ຸ ູ
TONE = set(range(0x0EC8, 0x0ECC))                            # ່ ້ ໊ ໋
OTHER_MARK = {0x0EBA, 0x0EBC, 0x0ECC, 0x0ECD, 0x0ECE}        # ຺ ຼ ໌ ໍ ໎
MARKS = UPPER | LOWER | TONE | OTHER_MARK
SPACING_V = {0x0EB0, 0x0EB2, 0x0EB3}                         # ະ າ ຳ
LAO_DIGITS = set(range(0x0ED0, 0x0EDA))
PLACEHOLDERS = set("-–—◌_….")            # used in teaching charts: ເ-ະ  -ົວ  ◌໎
INVISIBLE = {0x200B: "ZWSP", 0x200C: "ZWNJ", 0x200D: "ZWJ", 0x2060: "WJ", 0xFEFF: "BOM", 0x00AD: "SHY"}
SEVERITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

TEXT_EXT = {".txt", ".md", ".markdown", ".html", ".htm", ".css", ".svg", ".xml", ".json", ".csv", ".tsv",
            ".srt", ".vtt", ".yml", ".yaml"}
OFFICE_EXT = {".docx", ".pptx", ".xlsx"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}


def is_lao(ch: str) -> bool:
    return LAO_LO <= ord(ch) <= LAO_HI


def is_thai(ch: str) -> bool:
    return THAI_LO <= ord(ch) <= THAI_HI


def uplus(ch: str) -> str:
    return "U+%04X" % ord(ch)


class Report:
    def __init__(self, name: str):
        self.name = name
        self.findings: list[dict] = []
        self.lao_chars = 0
        self.thai_chars = 0
        self.lao_digits = 0
        self.ascii_digits_in_lao = 0
        self.standalone = 0
        self.teaching = False
        self.variants = {"ໜ": 0, "ຫນ": 0, "ໝ": 0, "ຫມ": 0, "ຫຼ": 0, "ຫລ": 0}
        self.used_lao: set[str] = set()
        self.notes: list[str] = []

    def add(self, code, severity, where, message, context=""):
        self.findings.append({"code": code, "severity": severity, "where": where,
                              "message": message, "context": context})


SIGN_CHARS = MARKS | SPACING_V | PREFIX
EDGE_PUNCT = "*_()[]{}<>|,;:.!?\"'`“”‘’/"


def standalone_signs(text: str) -> set[int]:
    """Indexes of vowel signs and tone marks that sit alone as their own word (ິ  ເ  ເ-ະ  **ັ**).
    That is normal in alphabet and vowel charts; in running text it is a bug, so it is counted and reported."""
    idx: set[int] = set()
    for m in re.finditer(r"\S+", text):
        tok = m.group(0)
        core = tok.strip(EDGE_PUNCT)
        if core and all(ord(c) in SIGN_CHARS or c in PLACEHOLDERS for c in core) and any(ord(c) in SIGN_CHARS for c in core):
            start = m.start() + tok.index(core)
            idx.update(k for k in range(start, start + len(core)) if ord(text[k]) in SIGN_CHARS)
    return idx


def excerpt(text: str, i: int, width: int = 9) -> str:
    s = text[max(0, i - width): i + width + 1]
    return "".join(c if c.isprintable() or c == " " else "\\u%04x" % ord(c) for c in s)


# ---------------------------------------------------------------- text scanning
def scan_segment(rep: Report, where: str, text: str) -> None:
    if not text:
        return
    n = len(text)
    lao_n = sum(1 for c in text if is_lao(c))
    lao_here = lao_n > 0
    latin_n = sum(1 for c in text if c.isascii() and c.isalpha())
    lao_major = lao_here and lao_n >= latin_n          # a Lao-language segment, not an English sentence quoting Lao
    standalone = standalone_signs(text)
    for i, ch in enumerate(text):
        cp = ord(ch)
        prev = text[i - 1] if i > 0 else ""
        nxt = text[i + 1] if i + 1 < n else ""
        pcp = ord(prev) if prev else -1
        ncp = ord(nxt) if nxt else -1

        if cp == 0xFFFD or (ch == "□" and lao_here):
            rep.add("LAO009", "High", where, "Replacement or box character %s: the text was damaged or a font lacks the glyph" % uplus(ch), excerpt(text, i))
            continue
        if i in standalone:                       # a sign shown on its own, as in an alphabet or vowel chart
            rep.standalone += 1
            rep.lao_chars += 1
            rep.used_lao.add(ch)
            continue
        if cp in INVISIBLE:
            if cp == 0x200B and (ncp in MARKS or ncp in SPACING_V or pcp in PREFIX):
                rep.add("LAO008", "High", where, "Zero-width space inside a syllable (splits a vowel or mark from its consonant)", excerpt(text, i))
            continue
        if 0xE000 <= cp <= 0xF8FF and lao_here:
            rep.add("LAO010", "Medium", where, "Private-use character %s in Lao text: possible legacy Lao font encoding" % uplus(ch), excerpt(text, i))
            continue
        if is_thai(ch):
            rep.thai_chars += 1
            continue
        if cp in LAO_DIGITS:
            rep.lao_digits += 1
            continue
        if not is_lao(ch):
            if ch.isascii() and ch.isdigit() and lao_major:
                rep.ascii_digits_in_lao += 1
            continue

        rep.lao_chars += 1
        rep.used_lao.add(ch)
        ph_prev = prev in PLACEHOLDERS if prev else False

        if cp in MARKS:
            if not (pcp in CONS or pcp in MARKS or ph_prev):
                rep.add("LAO002", "High", where, "Mark %s has no consonant before it" % uplus(ch), excerpt(text, i))
            if cp in TONE and pcp in TONE or cp in UPPER and pcp in UPPER or cp in LOWER and pcp in LOWER:
                rep.add("LAO004", "High", where, "Two stacked marks of the same kind (%s after %s)" % (uplus(ch), uplus(prev)), excerpt(text, i))
            if cp in UPPER and pcp in TONE:
                rep.add("LAO005", "Medium", where, "Tone mark typed before the vowel sign: use consonant, vowel sign, tone mark", excerpt(text, i))
        elif cp in SPACING_V:
            if not (pcp in CONS or pcp in MARKS or ph_prev or pcp == 0x0EBD or (cp == 0x0EB0 and pcp == 0x0EB2)):  # ເ-າະ
                rep.add("LAO002", "Medium", where, "Vowel sign %s has no consonant before it" % uplus(ch), excerpt(text, i))
        elif cp in PREFIX:
            if not (ncp in CONS or (nxt and nxt in PLACEHOLDERS)):
                hint = " It looks like the vowel was typed after its consonant (reading order); type it before." if pcp in CONS else ""
                rep.add("LAO003", "High", where, "Prefixed vowel %s is not followed by a consonant.%s" % (uplus(ch), hint), excerpt(text, i))

    # variant spellings
    for key in rep.variants:
        rep.variants[key] += text.count(key)

    # mixed Lao/Thai words, Thai inside Lao lines
    thai_tokens = 0
    for tok in re.split(r"[\s​]+", text):
        has_l = any(is_lao(c) for c in tok)
        has_t = any(is_thai(c) for c in tok)
        if has_l and has_t:
            rep.add("LAO001", "High", where, "Thai and Lao letters mixed in one word", tok[:30])
        elif has_t and lao_here:
            thai_tokens += 1
    if thai_tokens:
        rep.add("LAO011", "Low", where, "%d Thai word(s) in a line that also contains Lao" % thai_tokens)


# ---------------------------------------------------------------- readers
class _TextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        for k, v in attrs:
            if k in ("alt", "title", "placeholder", "aria-label") and v:
                self.parts.append(v)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def read_bytes_text(rep: Report, data: bytes, label: str) -> str:
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError as e:
        rep.add("LAO009", "High", label, "File is not valid UTF-8 (%s). Re-save as UTF-8." % e.reason)
        return data.decode("utf-8", errors="replace")


def check_plain(rep: Report, path: str, data: bytes) -> None:
    raw = read_bytes_text(rep, data, path)
    ext = os.path.splitext(path)[1].lower()
    if ext in (".html", ".htm", ".svg", ".xml"):
        p = _TextParser()
        p.feed(raw)
        for i, part in enumerate(p.parts, 1):
            for line in part.splitlines() or [part]:
                scan_segment(rep, "text %d" % i, line)
        check_markup(rep, raw, ext)
    else:
        for n, line in enumerate(raw.splitlines(), 1):
            scan_segment(rep, "line %d" % n, line)
        if ext == ".css":
            check_css(rep, raw)


def check_css(rep: Report, css: str) -> None:
    for m in re.finditer(r"letter-spacing\s*:\s*([^;}\"']+)", css):
        v = m.group(1).strip()
        if not re.fullmatch(r"(normal|0(\.0+)?(px|em|rem|pt)?)", v):
            rep.add("LAO022", "Low", "CSS", "letter-spacing is %s; it must stay 0 on Lao text (it pulls marks off their consonant)" % v)
    for m in re.finditer(r"line-height\s*:\s*([0-9.]+)\s*[;}\"']", css):
        try:
            if float(m.group(1)) < 1.4:
                rep.add("LAO023", "Medium", "CSS", "Unitless line-height %s is below 1.4; Lao marks will clip or collide (use 1.5 or more)" % m.group(1))
        except ValueError:
            pass
    if re.search(r"font-style\s*:\s*(italic|oblique)", css):
        rep.add("LAO024", "Low", "CSS", "Italic or oblique style: Lao has no italic; check it is not applied to Lao text")
    if re.search(r"text-align\s*:\s*justify", css):
        rep.add("LAO025", "Low", "CSS", "Justified text leaves uneven gaps in Lao; prefer left alignment")


def check_markup(rep: Report, raw: str, ext: str) -> None:
    check_css(rep, raw)
    if ext in (".html", ".htm") and rep.lao_chars:
        if not re.search(r"<meta[^>]+charset", raw, re.I):
            rep.add("LAO020", "Medium", "HTML", 'No <meta charset="utf-8"> found')
        if not re.search(r"""lang\s*=\s*["']?lo\b|:lang\(\s*lo\s*\)""", raw, re.I):
            rep.add("LAO021", "Medium", "HTML", 'No lang="lo" on the page or on the Lao elements')
        if re.search(r"<(i|em)\b", raw, re.I):
            rep.add("LAO024", "Low", "HTML", "<i> or <em> found; browsers slant Lao synthetically. Use bold, colour or size")


def _xml_paragraphs(xml: bytes, para: str, text: str):
    root = ET.fromstring(xml)
    for p in root.iter(para):
        yield "".join(t.text or "" for t in p.iter(text))


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def check_office(rep: Report, path: str) -> None:
    ext = os.path.splitext(path)[1].lower()
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        blob = b""
        if ext == ".docx":
            parts = [n for n in names if re.match(r"word/(document|header\d*|footer\d*|footnotes|endnotes|comments)\.xml$", n)]
            for part in parts:
                xml = z.read(part)
                blob += xml
                for i, t in enumerate(_xml_paragraphs(xml, W + "p", W + "t"), 1):
                    scan_segment(rep, "%s p%d" % (part.split("/")[-1], i), t)
            styles = z.read("word/styles.xml") if "word/styles.xml" in names else b""
            allx = blob + styles
            if rep.lao_chars:
                if b"w:cs=" not in allx:
                    rep.add("LAO026", "Medium", "Word", "No complex-script font (w:cs) is set anywhere; Word may use a font without Lao glyphs")
                if (b"<w:b/>" in blob or b"<w:b " in blob) and b"<w:bCs" not in blob:
                    rep.add("LAO026", "Medium", "Word", "Runs are bold with w:b but not w:bCs; Word does not bold Lao text without bCs")
                if b'w:bidi="lo' not in allx:
                    rep.add("LAO027", "Low", "Word", "Complex-script language is not set to Lao (w:lang w:bidi=\"lo-LA\")")
        elif ext == ".pptx":
            for part in sorted(n for n in names if re.match(r"ppt/(slides|notesSlides)/[^/]+\.xml$", n)):
                xml = z.read(part)
                blob += xml
                for i, t in enumerate(_xml_paragraphs(xml, A + "p", A + "t"), 1):
                    scan_segment(rep, "%s p%d" % (part.split("/")[-1], i), t)
            theme = b"".join(z.read(n) for n in names if n.startswith("ppt/theme/"))
            if rep.lao_chars:
                cs_faces = [m for m in re.findall(rb'<a:cs typeface="([^"]*)"', blob + theme) if m.strip()]
                if not cs_faces:
                    rep.add("LAO026", "Medium", "PowerPoint", "No complex-script typeface (a:cs) is set on the runs or in the theme; Lao may fall back to a font without Lao glyphs")
                if b"<a:normAutofit" in blob:
                    rep.add("LAO028", "Low", "PowerPoint", "Auto-shrink is on; shrunk Lao text becomes hard to read")
        else:  # xlsx
            if "xl/sharedStrings.xml" in names:
                root = ET.fromstring(z.read("xl/sharedStrings.xml"))
                for i, si in enumerate(root.iter(S + "si"), 1):
                    scan_segment(rep, "string %d" % i, "".join(t.text or "" for t in si.iter(S + "t")))
            for n in names:
                if re.match(r"xl/worksheets/sheet\d+\.xml$", n):
                    root = ET.fromstring(z.read(n))
                    for is_ in root.iter(S + "is"):
                        scan_segment(rep, n.split("/")[-1], "".join(t.text or "" for t in is_.iter(S + "t")))
            if rep.lao_chars and "xl/styles.xml" in names:
                styles = z.read("xl/styles.xml").decode("utf-8", "replace")
                if not re.search(r'<name val="[^"]*Lao[^"]*"', styles):
                    rep.add("LAO026", "Low", "Excel", "No Lao-capable font name found in the cell styles; set Noto Sans Lao on the used range")


def check_pdf(rep: Report, path: str) -> None:
    text = None
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", "-enc", "UTF-8", path, "-"], capture_output=True)
        if r.returncode == 0:
            text = r.stdout.decode("utf-8", "replace")
    if text is None:
        try:
            from pypdf import PdfReader  # type: ignore
            text = "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
        except Exception:
            rep.notes.append("PDF text not extracted: install poppler-utils (pdftotext) or pypdf.")
    if text is not None:
        for n, line in enumerate(text.splitlines(), 1):
            scan_segment(rep, "pdf line %d" % n, line)
        rep.notes.append("PDF text order can differ from the visual order; use this for boxes, Thai mix-ups and missing text, and look at the page too.")
        if not rep.lao_chars:
            rep.notes.append("No extractable Lao text. If the page shows Lao, it may be outlines or an image.")
    if shutil.which("pdffonts"):
        r = subprocess.run(["pdffonts", path], capture_output=True)
        for line in r.stdout.decode("utf-8", "replace").splitlines()[2:]:
            cols = line.split()
            if len(cols) >= 5 and "no" in cols[-6:-3]:
                emb = re.search(r"\b(yes|no)\s+(yes|no)\s+(yes|no)\b", line)
                if emb and emb.group(1) == "no":
                    rep.add("LAO029", "Medium", "PDF", "Font not embedded: %s" % cols[0])


# ---------------------------------------------------------------- font coverage
def check_font(rep: Report, font_path: str) -> None:
    try:
        from fontTools.ttLib import TTFont  # type: ignore
    except ImportError:
        rep.notes.append("--font needs fontTools (pip install fonttools).")
        return
    font = TTFont(font_path, fontNumber=0, lazy=True)
    cmap = font.getBestCmap() or {}
    missing = sorted(c for c in rep.used_lao if ord(c) not in cmap)
    if missing:
        rep.add("LAO030", "High", os.path.basename(font_path),
                "Font has no glyph for: " + " ".join("%s(%s)" % (c, uplus(c)) for c in missing))
    tags = set()
    for table in ("GSUB", "GPOS"):
        if table in font:
            tags |= {r.ScriptTag for r in font[table].table.ScriptList.ScriptRecord}
    if not tags & {"lao ", "lao2", "DFLT"}:
        rep.add("LAO031", "High", os.path.basename(font_path), "Font has no GSUB/GPOS script entry for Lao: vowels and tone marks may not stack")
    elif not tags & {"lao ", "lao2"}:
        rep.notes.append("%s has only a default (DFLT) shaping script; test Lao stacking visually." % os.path.basename(font_path))


# ---------------------------------------------------------------- driver
def finish(rep: Report) -> None:
    if rep.teaching:
        return
    if rep.standalone:
        rep.add("LAO012", "Low", "document", "%d vowel sign(s) or tone mark(s) stand alone as their own word. Normal in alphabet and vowel charts (use --teaching to hide this); a bug in running text" % rep.standalone)
    if rep.lao_digits and rep.ascii_digits_in_lao:
        rep.add("LAO006", "Medium", "document", "Lao digits (%d) and ASCII digits (%d) are both used in Lao text; use one numeral system per document" % (rep.lao_digits, rep.ascii_digits_in_lao))
    v = rep.variants
    for a, b in (("ໜ", "ຫນ"), ("ໝ", "ຫມ"), ("ຫຼ", "ຫລ")):
        if v[a] and v[b]:
            rep.add("LAO007", "Low", "document", "Both %s (%d) and %s (%d) are used; pick one form" % (a, v[a], b, v[b]))


def collect(paths):
    for p in paths:
        if p == "-" or os.path.isfile(p):
            yield p
        elif os.path.isdir(p):
            for dp, dn, fn in os.walk(p):
                dn[:] = sorted(d for d in dn if d not in SKIP_DIRS)
                for f in sorted(fn):
                    if os.path.splitext(f)[1].lower() in TEXT_EXT | OFFICE_EXT | {".pdf"}:
                        yield os.path.join(dp, f)
        else:
            print("lao_check: not found: %s" % p, file=sys.stderr)
            yield None


def run(path: str, font: str | None, teaching: bool = False) -> Report | None:
    rep = Report("<stdin>" if path == "-" else path)
    rep.teaching = teaching
    ext = os.path.splitext(path)[1].lower()
    try:
        if path == "-":
            check_plain(rep, "<stdin>", sys.stdin.buffer.read())
        elif ext in OFFICE_EXT:
            check_office(rep, path)
        elif ext == ".pdf":
            check_pdf(rep, path)
        else:
            with open(path, "rb") as f:
                check_plain(rep, path, f.read())
    except (OSError, zipfile.BadZipFile, ET.ParseError) as e:
        print("lao_check: cannot read %s: %s" % (path, e), file=sys.stderr)
        return None
    finish(rep)
    if font:
        check_font(rep, font)
    return rep


def cap(findings, per_code):
    out, seen = [], {}
    findings = sorted(findings, key=lambda f: (SEVERITY_ORDER[f["severity"]], f["code"]))
    for f in findings:
        seen[f["code"]] = seen.get(f["code"], 0) + 1
        if seen[f["code"]] <= per_code:
            out.append(f)
    extra = {c: k - per_code for c, k in seen.items() if k > per_code}
    return out, extra


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Check Lao text and files for common errors (not spelling or meaning).")
    ap.add_argument("paths", nargs="+", help="files, folders, or - for stdin")
    ap.add_argument("--font", help="font file (.ttf/.otf) to test glyph coverage and Lao shaping tables")
    ap.add_argument("--max", type=int, default=15, help="max findings shown per code and file (default 15)")
    ap.add_argument("--strict", action="store_true", help="exit 1 on Medium findings too")
    ap.add_argument("--teaching", action="store_true",
                    help="alphabet/vowel charts and teaching notes: hide standalone-sign, mixed-digit and variant-spelling notices")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    reports, unreadable = [], False
    for p in collect(args.paths):
        if p is None:
            unreadable = True
            continue
        r = run(p, args.font, args.teaching)
        if r is None:
            unreadable = True
        else:
            reports.append(r)

    worst = 3
    for r in reports:
        for f in r.findings:
            worst = min(worst, SEVERITY_ORDER[f["severity"]])

    if args.json:
        print(json.dumps([{"file": r.name, "lao_chars": r.lao_chars, "thai_chars": r.thai_chars,
                           "findings": r.findings, "notes": r.notes} for r in reports], ensure_ascii=False, indent=2))
    else:
        for r in reports:
            shown, extra = cap(r.findings, args.max)
            print("== %s" % r.name)
            for f in shown:
                ctx = ("   [%s]" % f["context"]) if f["context"] else ""
                print("  %-6s %s  %-18s %s%s" % (f["severity"], f["code"], f["where"], f["message"], ctx))
            for c, k in extra.items():
                print("  ...    %s  %d more not shown" % (c, k))
            counts = {s: sum(1 for f in r.findings if f["severity"] == s) for s in SEVERITY_ORDER}
            print("  Summary: %d High, %d Medium, %d Low | Lao characters: %d | Thai characters: %d"
                  % (counts["High"], counts["Medium"], counts["Low"], r.lao_chars, r.thai_chars))
            for note in r.notes:
                print("  Note: " + note)
            if not r.findings:
                print("  No problems found by the automated checks.")
        print("\nThese checks do not verify spelling, meaning, or how the text looks. Render it and look; have a native reader confirm important text.")

    if unreadable:
        return 2
    return 1 if worst == 0 or (args.strict and worst == 1) else 0


if __name__ == "__main__":
    sys.exit(main())
