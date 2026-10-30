---
name: lao-typography-design
description: Lao (ພາສາລາວ) language and typography skill. Use whenever a task produces, edits, proofreads, translates or typesets Lao text (Word, PowerPoint, Excel, PDF, web pages, posters, packaging, subtitles), or involves broken, boxed or garbled Lao, Lao fonts or Unicode, or bilingual Lao/Thai/English layouts. Covers the script, vowels and tones, Unicode, font and layout rules, per-format settings, and a checker script for common Lao text errors. Use it even when the request never says "typography", for example "make this Lao menu a PDF" or "why do I see boxes?".
license: MIT for this project's text and scripts. Bundled fonts keep their own licenses (see references/fonts.md).
---

# Lao typography and language (lao_typography_design)

Lao is a complex script written without word spaces. Almost every failure has one of five causes: the wrong font, a tool that does not shape Lao, Thai codepoints mixed in, a vowel or tone mark separated from its consonant, or text that an AI retyped or invented. This skill prevents them. Paths below are relative to this skill's folder.

## Workflow

1. **Classify the task** and read the matching reference (table below). Load only what you need.
2. **Set up the font.** Default: **Noto Sans Lao**, used automatically unless the user, an official template or a brand guide names another font. In a sandbox run `bash scripts/setup_fonts.sh default` so tools find it by name.
3. **Produce real text** with a shaping-capable tool (Word, LibreOffice, Chromium, WeasyPrint, XeTeX/LuaTeX). Working code for each format is in `references/recipes.md`.
4. **Check.** Run `python3 scripts/lao_check.py <file>` (add `--font <font file>` to test glyph coverage). Fix every High finding, or explain why you left it.
5. **Look.** Render a page or slide to an image and open it: look for boxes (□), floating tone marks, overlapping vowels, clipped lines, the wrong font.
6. **Report.** Name the font used, what you checked, and what you could not verify (spelling, meaning, rendering, licenses).

## Which reference to read

| Task | Read |
|---|---|
| Consonant names and classes, tone marks, digits, digraphs | `references/lao-alphabet.md` |
| Vowel forms, positions, short/long pairs, diphthongs, the carrier ອ, syllable types | `references/lao-vowels.md` |
| Fonts, size, line height, alignment, line breaking, mixed scripts, numerals, dates, per-format settings, QA checklist | `references/lao-typography.md` |
| Unicode codepoints, Thai look-alikes, normalization, invisible characters, counting and truncating, CSV/JSON/legacy encodings | `references/unicode.md` |
| Code that works: HTML to PDF, Word, PowerPoint, Excel, Pillow, headline artwork, preview commands | `references/recipes.md` |
| Bundled display fonts (`assets/fonts/`), coverage gaps, licensing, how to load them | `references/fonts.md` |
| French-language charts of consonants and vowels | `references/images/langue-lao-consonnes.gif`, `references/images/langue-lao-voyelles.gif` |

## Core rules (always apply)

1. **Default font: Noto Sans Lao** (`assets/fonts/NotoSansLao-VariableFont_wdthwght.ttf`, weights 100–900). Switch only when the user, an official template or a brand guide names another font (Phetsarath OT, Noto Serif Lao, a bundled display font). Always give a fallback stack and set a font per script.
2. Line height 1.5 or more (headings 1.4 or more). Letter-spacing 0. No italic, no faux bold, no uppercase. Prefer left alignment. Lao about 1–2 pt larger than the Latin text next to it.
3. Never split a vowel sign or tone mark from its consonant, and never cut text in the middle of a syllable. Grapheme-cluster cuts are not enough; see `references/unicode.md`.
4. Prefixed vowels (ເ ແ ໂ ໄ ໃ) are stored and written before the consonant but read after it. Never reorder them.
5. Lao codepoints (U+0E80–U+0EFF) only inside Lao text, never Thai (U+0E00–U+0E7F). Keep Thai in separate blocks. Tag `lo`, `th`, `en`. Files are UTF-8.
6. One numeral system per document (Western digits for business and finance, ໐–໙ for formal or ceremonial use). Dates like `ວັນທີ 26 ຕຸລາ 2026` (CE unless told to use the Buddhist Era). One currency format (`1,500,000 ກີບ`).
7. Real text, never generated: Lao on posters, packaging and logos is live text in a Lao font laid over artwork that was generated without text.
8. Vowel spelling has many exceptions. Have a native speaker confirm important, official, legal, financial or published text.

## Working with Lao text as an AI

- **Edit, do not retype.** To change a Lao document, replace only the requested spans (exact-substring replace in a script or editor tool). Regenerating the whole text from memory silently changes letters, vowel order and tone marks.
- **Never "fix" the user's Lao.** Do not change spelling or wording unless asked. Flag suspected problems as "possible" and keep the original.
- **Do not invent.** If you are unsure how a Lao word is spelled or what it means, say so, give the English meaning, and mark it for native review. Do not state tone pitches from memory.
- **Lao is not Thai.** The scripts look alike and models slip Thai letters, vowel signs (ะ า ำ) and tone marks into Lao words. Never convert between them by shifting codepoints.
- **Write real characters.** Type Lao as UTF-8, not `\u` escapes or romanization, then run the checker. Keep file names and paths ASCII.
- **Never let an image model draw Lao.** Generate the artwork without text and overlay live text.
- **Be economical.** Lao uses many tokens. For long documents work file to file with scripts, and show only changed lines and findings.
- **Do not claim you looked** at a render until you have opened the image.

## Sandboxes (Claude's workspace, ChatGPT's code interpreter, Codex)

- Fonts usually cannot be downloaded. Use the bundled files in `assets/fonts/` and `scripts/setup_fonts.sh`; load by file path when a tool takes one. In ChatGPT the font must be in the GPT's or project's files.
- Before drawing text with Pillow check shaping: `python3 -c "from PIL import features; print(features.check('raqm'))"`. If it prints False, render through HTML (WeasyPrint or Chromium) or LibreOffice instead.
- Convert with `soffice --headless --convert-to pdf`, list fonts with `pdffonts`, render with `pdftoppm`, when installed. If a tool is missing, say so and give the user the manual step. Never silently fall back to a font that has no Lao glyphs.

## Report format

- **Reviews:** one-line verdict, findings table (Severity High/Medium/Low, Location, Problem, Fix), checklist, then a "Not verified" list.
- **Translations:** the translation first, then short notes only for real ambiguities.
- **Files with Lao:** say which font is required and whether it is embedded; ship a PDF alongside Word or PowerPoint files when the reader may lack the font.
