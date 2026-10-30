# Recipes: producing Lao in each format

Short, working code for the common outputs. Sections 1–3 (HTML-to-PDF with WeasyPrint, Word, PowerPoint) were run, converted to PDF, and viewed with Noto Sans Lao. Sections 4 and 6 (Excel, Pillow) were run but not visually reviewed. Sections 7 and 8 (headline artwork, LaTeX, subtitles) were not run here, so test them. Paths are relative to this skill's folder. Replace sample text with the user's real text, and write Lao as UTF-8 characters.

Before any recipe: `bash scripts/setup_fonts.sh` (installs the bundled fonts so tools find "Noto Sans Lao" by name), and after: `python3 scripts/lao_check.py <output file>`.

## 1. HTML and PDF (best default for documents)

Chromium, WeasyPrint and LibreOffice shape Lao correctly. WeasyPrint is easy to install (`pip install weasyprint --break-system-packages`).

```html
<!doctype html>
<html lang="lo">
<head>
<meta charset="utf-8">
<style>
@font-face { font-family: "Noto Sans Lao"; src: url("NotoSansLao-VariableFont_wdthwght.ttf") format("truetype"); font-weight: 100 900; }
@page { size: A4; margin: 20mm; }
:lang(lo) {
  font-family: "Noto Sans Lao", "Phetsarath OT", "Lao UI", sans-serif;
  font-size: 14pt; line-height: 1.7; letter-spacing: 0; font-style: normal; text-align: left;
}
:lang(en) { font-family: "Noto Sans", Inter, Arial, sans-serif; font-size: 13pt; }
h1 { font-weight: 700; line-height: 1.4; }
</style>
</head>
<body>
<h1>ຫົວຂໍ້ເອກະສານ</h1>
<p>ເນື້ອຫາພາສາລາວ.</p>
<p lang="en">English text in its own element.</p>
</body>
</html>
```

```python
from weasyprint import HTML
HTML("page.html").write_pdf("page.pdf")        # copy the .ttf next to page.html first
```

Chromium alternative: `chromium --headless --no-pdf-header-footer --print-to-pdf=page.pdf page.html`.

## 2. Word (.docx) with python-docx

Word needs the complex-script slots (`w:cs`, `w:szCs`, `w:bCs`), and the Lao language. `run.bold = True` alone does not bold Lao in Word.

```python
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

LAO_FONT = "Noto Sans Lao"

def lao_rpr(rpr, font=LAO_FONT, size_pt=None, bold=None):
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts"); rpr.insert(0, rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(a), font)
    if size_pt:
        for tag in ("w:sz", "w:szCs"):
            el = rpr.find(qn(tag))
            if el is None:
                el = OxmlElement(tag); rpr.append(el)
            el.set(qn("w:val"), str(int(size_pt * 2)))
    if bold is not None:
        for tag in ("w:b", "w:bCs"):
            el = rpr.find(qn(tag))
            if bold and el is None:
                rpr.append(OxmlElement(tag))
            elif not bold and el is not None:
                rpr.remove(el)
    lang = rpr.find(qn("w:lang"))
    if lang is None:
        lang = OxmlElement("w:lang"); rpr.append(lang)
    lang.set(qn("w:bidi"), "lo-LA")

doc = Document()
normal = doc.styles["Normal"]
lao_rpr(normal.element.get_or_add_rPr(), size_pt=14)       # style, so every paragraph inherits it
normal.paragraph_format.line_spacing = 1.5

p = doc.add_paragraph()
run = p.add_run("ຫົວຂໍ້"); lao_rpr(run._r.get_or_add_rPr(), size_pt=22, bold=True)
doc.add_paragraph("ເນື້ອຫາພາສາລາວ")
doc.save("out.docx")
```

The reader's computer needs the font installed unless you embed it. Say so when you deliver, or also deliver a PDF.

## 3. PowerPoint (.pptx) with python-pptx

```python
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.oxml.ns import qn

LAO_FONT = "Noto Sans Lao"

def lao_run(run, size_pt=24, bold=False, font=LAO_FONT):
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    rpr = run._r.get_or_add_rPr()
    rpr.set("lang", "lo-LA")
    for tag in ("a:latin", "a:ea", "a:cs"):             # a:cs is the one Lao uses
        el = rpr.find(qn(tag))
        if el is None:
            el = rpr.makeelement(qn(tag), {}); rpr.append(el)
        el.set("typeface", font)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
slide = prs.slides.add_slide(prs.slide_layouts[6])
tf = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.5), Inches(5)).text_frame
tf.word_wrap = True
p = tf.paragraphs[0]; p.line_spacing = 1.4
r = p.add_run(); lao_run(r, 40, True); r.text = "ຫົວຂໍ້"
prs.save("out.pptx")
```

Body 20 pt or more, no auto-shrink, 30–45 Lao characters per line on narrow text boxes.

## 4. Excel (.xlsx) with openpyxl

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

wb = Workbook(); ws = wb.active
ws["A1"] = "ຊື່"; ws["B1"] = "ຈຳນວນ"; ws.append(["ເສືອ", 12])
for row in ws.iter_rows():
    for c in row:
        c.font = Font(name="Noto Sans Lao", size=12, bold=(c.row == 1))
        c.alignment = Alignment(wrap_text=True, vertical="top")
for r in range(1, ws.max_row + 1):
    ws.row_dimensions[r].height = 12 * 1.8             # at least 1.4 x font size; set it, do not rely on auto
ws.column_dimensions["A"].width = 28
wb.save("out.xlsx")
```

Avoid merged cells for long Lao text. Use Western digits in finance sheets.

## 5. Check how it looks (do this every time)

```bash
soffice --headless --convert-to pdf out.docx        # also works for .pptx and .xlsx
pdffonts out.pdf                                    # the Lao font should be listed with emb = yes
pdftoppm -r 110 -png -f 1 -l 1 out.pdf preview      # then open preview-1.png and look at it
python3 scripts/lao_check.py out.docx --font assets/fonts/NotoSansLao-VariableFont_wdthwght.ttf
```

Look for boxes, floating or overlapping marks, clipped lines, and the wrong font. If a tool is missing, say what you could not check.

## 6. Pillow (only when RAQM is available)

```python
from PIL import Image, ImageDraw, ImageFont, features
assert features.check("raqm"), "No RAQM: do not draw Lao with Pillow; render HTML instead"
font = ImageFont.truetype("assets/fonts/PB-Warnjai-Bold.ttf", 64, layout_engine=ImageFont.Layout.RAQM)
img = Image.new("RGB", (1200, 300), "white")
ImageDraw.Draw(img).text((40, 60), "ສະບາຍດີ", font=font, fill="black")
img.save("title.png")
```

If `features.check("raqm")` is False, marks will misplace. Use section 1 and screenshot instead.

## 7. Styled headline artwork (stroke, shadow, slant, gradient)

Build it in HTML/CSS and render with headless Chromium (or Playwright). Do not draw Lao with PIL or SVG paths, and do not let an image model draw it.

- Noto Sans Lao weight 900. Keep `line-height` 1.5 or more and `letter-spacing: 0` so tone marks and lower vowels are not clipped.
- Stroke: `-webkit-text-stroke` with `paint-order: stroke fill`. For a double outline, stack duplicate spans (shadow, outline, fill).
- Shadow: a hard offset plus a soft blur, for example `12px 14px 0 #020b1d, 20px 26px 28px rgba(0,0,0,.5)`.
- Slant only when asked: `transform: skewX(-10deg)` (synthetic, not an italic).
- Gradient fill: `background-clip: text` with `color: transparent`.
- Measure with `getBoundingClientRect()` and scale the font size to the column; do not guess.
- Render at 2x or more of the delivery size. Also export a transparent PNG if it will sit over photos.

## 8. Other outputs

- **Subtitles (SRT/VTT):** UTF-8, at most two lines, break at phrase boundaries, keep lines short. Do not add zero-width spaces unless you have tested the player.
- **LaTeX:** XeTeX or LuaTeX with `fontspec`, `\setmainfont{Noto Sans Lao}`, `Script=Lao`. pdfLaTeX does not support Lao.
- **Design tools (Canva, Figma, InDesign):** generate the artwork without text and type the Lao in the tool with an installed or uploaded Lao font. Check the font list first.
