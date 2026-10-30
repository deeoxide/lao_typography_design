---
name: lao-font-designer
description: Design, select, develop, and test Lao typefaces, including font setup and typography workflows in Adobe Illustrator, InDesign, Photoshop, Figma, and Canva. Use for glyph design, font integration, reusable text styles, and rendering checks; not translation or unrelated layout work.
---

# Lao typeface design

> **Default font:** unless the user names a font, use **Noto Sans Lao** for all Lao text, designs and fonts, automatically and without asking. Use another font (for example Phetsarath OT or Noto Serif Lao) only when the user, an official template or a brand guide asks for it.

Establish the target use, sizes, style, weights, and rendering environments from the brief. Distinguish a design specification from an implemented font; do not describe a written brief as a working font file.

## Choose the workflow

- **Build a new or restyled font from a prompt:** use the `lao-font-studio` skill. It builds from Noto Sans Lao automatically when no font is named.

- **Create or modify a font:** develop glyph outlines, character mapping, spacing, anchors, shaping, and metrics in an available font-authoring toolchain. Artwork drawn in an external design app is an input to this process; exporting SVG or PDF does not by itself create a usable OTF or TTF font. Build and validate the font before testing it in target apps.
- **Use a font in an external app:** establish the exact app, version, desktop/browser environment, and font file or family. Read the relevant section of [external-apps.md](references/external-apps.md) for Adobe, Figma, or Canva setup, text styles, and export checks. Preserve the user's chosen application.
- **Evaluate compatibility:** compare the same supplied Lao text and font version in the editor and requested exports. Distinguish missing font access from unsupported glyphs, incorrect shaping, and clipped layout.

When suitable connected tools are available, inspect the document and perform the requested work through them. Otherwise prepare the font specification, setup instructions, style values, or importable artifacts the user can apply. A skill is assistant guidance, not an Adobe/Figma/Canva extension; do not claim direct application control, successful installation, or in-app validation without evidence. Font upload and shared-library changes must stay within the user's authorized task.

## Design and review

- Derive the required glyph repertoire from the intended text and language scope. Include needed consonants, vowels, tone marks, digits, special consonant forms, punctuation, and mixed-language characters. The kip sign U+20AD is outside the Lao block.
- Preserve recognizable Lao letterforms and differences between similar vowel signs. Evaluate small sizes as well as display sizes. Do not substitute Thai glyphs or use generated image text as a font master.
- Design mark-to-base and mark-to-mark positioning for upper vowels, tone marks, lower vowels, and tall consonants. Inspect shaping behavior in actual text; an inventory of font tables alone is insufficient.
- Set vertical metrics to accommodate stacks without clipping or interline collisions. Test real weights and avoid relying on synthetic bold or italic.
- Compare apparent size and stroke weight with the intended Latin companion. Keep spacing from separating combining marks.
- Inspect the license for each source or candidate font before modification, subsetting, embedding, or redistribution. Do not infer rights from a font name.

Provide a specimen covering required glyphs, stacked marks, lower vowels, numbers, currency, mixed-language lines, and real supplied phrases. Distinguish synthetic stress strings from meaningful Lao words. Compare target engines and sizes where available.

Deliver the requested brief, recommendation, font changes, or review with evidence by glyph or string. State which rendering environments, licensing terms, and linguistic readings remain unverified.

For external-app work, include the exact font family/version and weights, relevant text-style settings, editable artifact or setup steps, export results, and unresolved compatibility issues. Keep live text in the working master; make outlined or rasterized delivery copies only when the requested workflow needs them.
