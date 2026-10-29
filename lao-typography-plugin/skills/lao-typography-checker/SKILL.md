---
name: lao-typography-checker
description: Review Lao typography in documents, slides, PDFs, web pages, and design layouts for clipping, shaping, spacing, and readability. Use for requested typography checks or visible Lao rendering problems; do not rewrite the content as part of an audit.
---

# Lao typography review

> **Default font:** unless the user names a font, use **Noto Sans Lao** for all Lao text, designs and fonts, automatically and without asking. Use another font (for example Phetsarath OT or Noto Serif Lao) only when the user, an official template or a brand guide asks for it.

Inspect the actual file and rendered output when available. Distinguish a content concern from a rendering defect and a stylistic preference. Do not claim visual verification from source code alone.

## Checks

- Confirm Lao-capable fonts, required glyphs, real font weights, and a rendering engine that positions vowel and tone marks correctly. Inspect complex-script font settings in document formats that have separate font slots.
- Check upper and lower marks, tall consonants, mixed Lao/Latin lines, and text at final output size. Look for clipping, collisions, detached marks, missing glyphs, and unwanted fallback.
- Use the project's defaults as a starting point: body line height 1.5 or greater, headings about 1.4 or greater, zero letter-spacing, left alignment, no synthetic italic or bold. Judge actual fit and the user's design requirements rather than treating numbers as proof of correctness.
- Check that line wrapping and truncation preserve text clusters and intended syllables. Do not insert spaces between every Lao word to make a layout fit.
- Inspect unintended Thai characters in Lao runs without flagging legitimate Thai passages. Check consistent numbers, dates, currency, and language tags where supported.
- For PDF export, inspect the exported pages and test text extraction or copy-paste. For web output, check narrow widths and zoom when tools permit.

Report significant findings with severity, file/page/element location, evidence, and proposed repair. A rendering review does not certify spelling or meaning. If fixes are requested, preserve wording and edit only the relevant layout or technical settings; keep originals unless editing in place is authorized. Finish with checks performed and any unverified aspects.
