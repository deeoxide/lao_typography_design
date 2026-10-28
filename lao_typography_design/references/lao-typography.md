---
name: lao-typography
description: Topic note on Lao typography (ການຈັດພິມພາສາລາວ) — letterform anatomy, font choice, size and spacing, alignment, line breaking, mixed scripts, numerals, and settings for CSS, Office, PDF, and design tools.
---

# Topic: Lao typography (ການຈັດພິມພາສາລາວ)

Lao is a **complex script**. Its letters, vowel signs, and tone marks must be shaped by the rendering engine, and the text needs more vertical space than Latin. Good Lao typography is mostly about the right font, generous spacing, and a shaping-capable tool.

## 1. Letterform anatomy

- Lao letters are **rounded and open**, with a fairly uniform stroke. Many are simplified forms that resemble Thai but have no heads or loops.
- Text has **three vertical layers**: a base row (consonants and most vowels), an **upper layer** (vowel signs ິ ີ ຶ ື ັ ົ and tone marks ່ ້ ໊ ໋), and a **lower layer** (ຸ ູ and ຼ).
- Tone marks sit on top of vowel signs, so a single syllable can be three layers tall (for example ກິ່ນ).
- **Prefixed vowels** (ເ ແ ໂ ໄ ໃ) are wide and sit before the consonant. They must stay attached to the consonant they belong to.
- Several tall letters (ຫຼ, ຝ, ຟ, ຜ, ພ) and stacked marks define the real height of a line. Design the line around them, not around the x-height.

## 2. Choosing a font

| Use | Suggested fonts | Notes |
|---|---|---|
| Government, formal Word/Excel documents | **Phetsarath OT** | The standard text font for formal documents in Lao PDR. Regular and bold only. |
| Web, apps, cross-platform | **Noto Sans Lao**, **Noto Sans Lao UI** | Open-source (SIL OFL), multiple weights, wide platform support. |
| Print with a serif feel | **Noto Serif Lao** | Good for long text and reports. |
| Windows / macOS system | **Lao UI**, **Lao Sangam MN** | Use as fallbacks. |
| Other text faces | Saysettha OT, Dokchampa, Souliyo | Check weights and glyph coverage first. |

- Check the **license** before embedding or using a font commercially.
- Choose fonts with **real bold** and complete glyph coverage (digits ໐–໙, ຼ, ໜ, ໝ, ₭).
- Pair with a Latin font that matches in weight and proportion (for example Noto Sans Lao + Noto Sans or Inter; Phetsarath OT + Times New Roman or Arial).
- Define a **fallback stack** so a missing font never drops text to a font without Lao glyphs.

## 3. Size, leading, and spacing

- **Size:** Lao looks smaller than Latin at the same point size. Use body text about 1–2 pt larger than the Latin equivalent: 12–14 pt in print, 16 px or more on screen.
- **Leading (line height):** 1.5–1.8 for body text. Never use 1.0–1.2; marks will clip or collide with the line above.
- **Headings:** keep line height at 1.4 or more. Add padding inside buttons, table cells, and fixed-height boxes.
- **Letter-spacing:** keep it at 0. Tracking separates combining marks from their consonant.
- **Word spacing:** Lao has no word spaces, so there is nothing to adjust. Spaces are phrase or sentence breaks.
- **Paragraph spacing:** use 0.5–1 line of space between paragraphs, rather than indents.
- **Measure:** 30–45 Lao characters per line on narrow columns (slides, mobile) is comfortable. Avoid very long lines.

## 4. Emphasis, weight, and case

- **No italic.** Lao has no italic tradition, and synthetic oblique distorts the marks. Use bold, color, size, or quotation marks.
- **Bold:** use a true bold weight. Faux bold smears the marks.
- **Underline:** use sparingly, and check that it does not cut through lower vowel signs (ຸ ູ). Use `text-underline-offset` on the web.
- **No uppercase or small caps.** In bilingual headings, apply uppercase only to the Latin text.

## 5. Alignment and line breaking

- **Prefer left-aligned text.** Justified text creates uneven gaps because gaps only appear at phrase spaces. Use justification only where the engine supports Lao inter-character justification, and check the result.
- Line breaking needs a **Lao dictionary** (ICU). Modern browsers, Word, and LibreOffice have one.
- Add **U+200B (zero-width space)** to mark allowed break points in long strings. Use **U+2060 (word joiner)** or `white-space: nowrap` to keep names and terms together.
- **Never break inside a syllable**, and never separate a tone mark or vowel sign from its base.
- When truncating text in an interface, cut by word or grapheme cluster, not by byte or code unit.

## 6. Mixed scripts (Lao, Thai, English)

- Tag the language for each run: `lang="lo"`, `lang="th"`, `lang="en"`.
- Set a font for each script. Do not rely on automatic fallback.
- Adjust the Latin size (often 90–95% of the Lao size) so the two scripts look balanced on the same line.
- Keep Lao and Thai in **separate blocks** (paragraphs or columns). They look similar but must never be mixed inside a word.
- Keep punctuation, brackets, and numbers consistent across languages.

## 7. Numerals, dates, and currency

- **Lao digits (໐–໙)** are common in formal, ceremonial, and design use. **Western digits (0–9)** are normal in business, finance, and spreadsheets. Use one system per document.
- Right-align numbers in tables. Check that the font contains the digits you choose.
- **Dates:** `ວັນທີ 26 ຕຸລາ 2026`. Use CE unless told to use the Buddhist Era (CE + 543).
- **Currency:** `1,500,000 ກີບ`, `₭1,500,000`, or `LAK 1,500,000`. Keep one format.

## 8. Settings by format

**Web (CSS)**
```css
:lang(lo) {
  font-family: "Noto Sans Lao", "Phetsarath OT", "Lao UI", sans-serif;
  line-height: 1.7;
  letter-spacing: 0;
  font-style: normal;
  text-align: left;
  word-break: normal;
  overflow-wrap: anywhere;
}
```
Use `<meta charset="utf-8">` and `lang="lo"`.

**Word (.docx):** set the **complex script font** (cs) and **complex script size** (szCs), not just the Latin font. Set the language to Lao (lo-LA). Use styles, not manual formatting. Line spacing: multiple 1.5.

**Excel (.xlsx):** apply Phetsarath OT to the used range. Set row heights manually (at least 1.4 times the font size) and widen columns. Avoid merged cells for long text.

**PowerPoint (.pptx):** set the cs typeface on every run and in the theme. Body 20 pt or more, generous line spacing, no automatic shrink.

**PDF:** generate from an engine with proper shaping (Chrome/Chromium, WeasyPrint with HarfBuzz, LibreOffice, XeTeX/LuaTeX). Avoid ReportLab and FPDF for Lao. Embed the fonts and test copy-paste.

**Design tools:** in InDesign use the World-Ready Composer. In Illustrator enable the complex-script text engine. In Canva check the font list or upload your brand font. In Figma use Noto Sans Lao or Phetsarath OT. AI image generators draw Lao text badly, so create the image without text and add real text in a design tool.

## 9. Print and accessibility

- Minimum print size: 10 pt for notes, 12 pt for body.
- Keep enough contrast; thin weights at small sizes make tone marks hard to see.
- Provide a real-text PDF (not outlines) so screen readers and search work.
- For signage and packaging, test at the final size and leave extra space above and below lines.

## 10. Quality checklist

1. The right Lao font is applied in the correct slot and is embedded or installed.
2. No boxes (□), floating marks, or overlapping vowels.
3. Line height is 1.5 or more, with no letter-spacing, no faux italic, and left alignment.
4. No Thai codepoints (U+0E00–U+0E7F) inside Lao text.
5. Numerals, dates, and currency follow one system.
6. Latin and Lao sizes look balanced.
7. Line breaks fall at word or phrase boundaries.
8. A preview image or PDF has been viewed before delivery.
