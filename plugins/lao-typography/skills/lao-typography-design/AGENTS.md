# AGENTS.md — lao_typography_design

Instructions for any coding agent that reads `AGENTS.md` (Codex, Claude Code, and others) when it produces, edits, proofreads, translates or typesets Lao (ພາສາລາວ) text: documents, slides, spreadsheets, PDFs, web pages, design files and artwork, including bilingual Lao/Thai/English work. `SKILL.md` in this folder carries the same rules for Claude skills. Paths are relative to this folder.

## Workflow

1. Read the reference that matches the task. Load only what you need.
   - `references/lao-alphabet.md`: consonants, classes, tone marks, digits.
   - `references/lao-vowels.md`: vowel forms, positions, syllable types.
   - `references/lao-typography.md`: fonts, spacing, line breaking, numerals, dates, per-format settings, QA checklist.
   - `references/unicode.md`: codepoints, Thai look-alikes, normalization, invisible characters, safe truncation, CSV/JSON/legacy encodings.
   - `references/recipes.md`: tested code for HTML/PDF, Word, PowerPoint, Excel, Pillow, headline artwork, preview commands.
   - `references/fonts.md`: bundled fonts and licenses. Charts: `references/images/*.gif` (French).
2. Install the font: `bash scripts/setup_fonts.sh default` (Noto Sans Lao). No network is needed.
3. Produce the file with a shaping-capable engine.
4. Check it: `python3 scripts/lao_check.py <file> [--font assets/fonts/<font>]`. Fix High findings or explain them.
5. Render a preview and look at it. Then report what you checked and what you could not verify.

## Hard rules

1. Lao is a complex script. Use a font with OpenType shaping (default **Noto Sans Lao**, used automatically unless the user names another font) and a shaping-capable engine: Chromium, LibreOffice, WeasyPrint, XeTeX/LuaTeX. Do not use ReportLab, FPDF, or PIL text drawing for Lao (Pillow only when `features.check("raqm")` is True).
2. Lao codepoints (U+0E80–U+0EFF) only. Never put Thai codepoints (U+0E00–U+0E7F) inside Lao text, and never convert Thai to Lao by shifting codepoints.
3. Files are UTF-8. HTML gets `<meta charset="utf-8">` and `lang="lo"`; tag Thai `th`, English `en`. Excel CSV needs `utf-8-sig`. Keep file names ASCII.
4. Body text: line-height 1.5 or more, letter-spacing 0, left-aligned, true bold only, no italic (use bold, colour or size), no uppercase.
5. Prefixed vowels (ເ ແ ໂ ໄ ໃ) are written before the consonant but read after it. Never reorder them.
6. Never split a vowel sign or tone mark from its consonant, or cut or wrap inside a syllable. Cut at word or phrase breaks (ICU segmenter). Grapheme-cluster cuts alone can strand a prefixed vowel; use the helper in `references/unicode.md`.
7. Set a font for each script (Lao, Thai, Latin). In Word set the complex-script font (`w:cs`, `w:szCs`, and `w:bCs` for bold); in PowerPoint set `a:cs`. Do not rely on fallback.
8. One numeral system per document. Dates `ວັນທີ 26 ຕຸລາ 2026`. Currency `1,500,000 ກີບ`.
9. Do not apply NFKC normalization to Lao (it rewrites ໜ ໝ ຳ).
10. Vowel spelling has many exceptions, especially ໃ- words and short diphthongs. Do not invent spellings. Mark anything uncertain for review by a native speaker.

## Behaviour with Lao text

- Edit with exact-substring replacement; do not regenerate or retype the user's Lao.
- Do not correct or reword the user's Lao unless asked. Flag suspected issues as "possible".
- Do not state tone pitches from memory. Say what you could not verify.
- Never let an image generator draw Lao. Generate artwork without text and overlay live text.
- Do not say you reviewed a render until you have opened it.
- Fonts cannot normally be downloaded in a sandbox. Use `assets/fonts/`. If a needed tool is missing, say so instead of falling back to a font without Lao glyphs.

## Decorative headlines and artwork

For a styled Lao title (stroke, shadow, slant, gradient) build it in HTML/CSS and render to PNG with headless Chromium; do not draw Lao with PIL or SVG paths. Use Noto Sans Lao weight 900, `-webkit-text-stroke` with `paint-order: stroke fill`, stacked spans for double outlines, `line-height` 1.5 or more, `letter-spacing: 0`, measure with `getBoundingClientRect()`, and render at 2x or more (plus a transparent PNG when it goes over photos). Details: `references/recipes.md`, section 7.

## Verify before delivery

1. Open the rendered image or PDF. Check for boxes (□), floating tone marks and overlapping vowels.
2. Zoom into tall clusters (a consonant with a vowel above and a tone mark, such as ມື້ ທ້າຍ ແລ້ວ ຮຶ).
3. Confirm nothing is clipped at any edge.
4. Confirm the right font was applied and embedded (`pdffonts`) or loaded (web).
5. Run `scripts/lao_check.py` and report any text you could not confirm.
