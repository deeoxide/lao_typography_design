# Bundled Lao fonts

Font files are in `assets/fonts/`. Each one has OpenType shaping (GSUB and GPOS tables), so Lao vowels and tone marks stack correctly in shaping-capable tools. None of them includes Thai glyphs. For Thai text, set a separate Thai font.

| File | Family name (as installed) | Weight | Style | Best for |
|---|---|---|---|---|
| `Lao_Chanthavy.otf` | Lao_Chanthavy | 500 | Loopless, heavy, modern | Headlines, posters, social graphics |
| `Lao_Dokkham.ttf` | Lao_Dokkham | 400 | Looped, slanted, bold | Decorative headings, invitations |
| `Lao_Handwriting14.ttf` | Lao_Handwriting14 | 400 | Looped handwriting, upright | Friendly body text in short pieces, greeting cards |
| `Lao_Handwriting17.ttf` | Lao_Handwriting17 | 500 | Casual script | Signatures, quotes, playful accents |
| `Lao_Samakhee.otf` | Lao_Samakhee | 400 | Looped, slanted, heavy | Event titles, banners |
| `PB-Warnjai-Bold.ttf` | PB Warnjai | 700 (Bold) | Loopless, rounded, modern | Brand headlines, packaging, UI titles |

## Choosing a font

- These are display fonts. For long body text, formal letters, and official documents, use Phetsarath OT or Noto Sans Lao, then use a bundled font for titles only.
- Pair one bundled display font with one plain text font. Do not mix two bundled display fonts on one page.
- Only PB Warnjai has a true Bold. Do not apply faux bold or italic to any of them.
- The Latin letters and digits in these fonts are basic. In bilingual layouts, set English in a separate Latin font.

## Character coverage

All six fonts cover the 27 standard consonants, ໜ, ໝ, all vowels, all tone marks, and Lao digits. This covers modern everyday Lao. They are missing some rarer characters:

- **Lao_Dokkham, Lao_Handwriting14:** missing ຌ ຏ ຐ ຑ ຒ (Pali/Sanskrit letters) and ໞ ໟ (Khmu letters).
- **Lao_Chanthavy, Lao_Handwriting17, Lao_Samakhee:** missing the Pali/Sanskrit letters ຆ ຉ ຌ ຎ ຏ ຐ ຑ ຒ ຓ ຘ ຠ ຨ ຩ ຬ, the mark ◌໎, and ໞ ໟ.
- **PB Warnjai:** missing the same Pali/Sanskrit letters and ◌໎, plus the Pali virama ◌຺.

For Buddhist texts, Pali terms, or minority-language text, use Noto Sans Lao or Phetsarath OT.

## Using the fonts

- **Python / Pillow:** `ImageFont.truetype("assets/fonts/PB-Warnjai-Bold.ttf", 48, layout_engine=ImageFont.Layout.RAQM)`. Without RAQM, marks will not position correctly.
- **HTML / CSS:** copy the file next to the page and declare it:
  ```css
  @font-face { font-family: "PB Warnjai"; src: url("PB-Warnjai-Bold.ttf") format("truetype"); font-weight: 700; }
  :lang(lo) { font-family: "PB Warnjai", "Noto Sans Lao", sans-serif; }
  ```
  Always keep Noto Sans Lao as a fallback so rare characters do not show as boxes.
- **Word / PowerPoint (python-docx, python-pptx):** set the font name to the family name in the table above, and set the complex-script font (`w:cs`) as well as the regular font. The reader's computer needs the font installed, or the file must embed it.
- **PDF (ReportLab, WeasyPrint):** register the file path and embed it. WeasyPrint shapes Lao correctly; plain ReportLab does not, so prefer WeasyPrint or render through HTML.
- **Linux tools:** copy to `~/.fonts/` and run `fc-cache -f`, then use the family name.

## Licensing

- Lao_Chanthavy, Lao_Dokkham, Lao_Handwriting14, Lao_Handwriting17, Lao_Samakhee: from Free Lao Fonts Online. Embedding permission: editable embedding allowed.
- PB Warnjai: Copyright 2022 Souliphong, all rights reserved. Embedding permission: installable.
- Check the publisher's terms before using any of these in paid client work or redistributing the files.
