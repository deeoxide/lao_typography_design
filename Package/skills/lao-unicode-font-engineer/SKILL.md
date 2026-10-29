---
name: lao-unicode-font-engineer
description: Diagnose and repair Lao encoding, missing glyphs, detached vowel or tone marks, and legacy font conversions. Use for broken Lao text or technical font inspection, not ordinary translation or visual styling.
---

# Lao Unicode and font engineering

> **Default font:** unless the user names a font, use **Noto Sans Lao** for all Lao text, designs and fonts, automatically and without asking. Use another font (for example Phetsarath OT or Noto Serif Lao) only when the user, an official template or a brand guide asks for it.

Inspect the actual text and font before choosing a repair. Distinguish corrupted bytes, legacy encoding, missing glyphs, incorrect character sequences, and shaping or layout failures.

## Workflow

1. Inspect bytes, codepoints, the selected font, and the application or export path. Record file and text locations. Lao is U+0E80-U+0EFF; Thai is U+0E00-U+0E7F. Investigate Thai characters in intended Lao runs without treating legitimate bilingual text, Latin digits, punctuation, or the kip sign U+20AD as corruption.
2. Check replacement characters, private-use characters, unexpected invisible controls, and detached marks. Preserve prefixed vowel order and base/mark clusters. Do not infer correct spelling from a range check alone.
3. For encoding repair, establish the original encoding from evidence and verify a sample before applying it broadly. For legacy fonts, identify the exact font and obtain its mapping; never invent a Latin-to-Lao or Thai-to-Lao substitution table.
4. Inspect font coverage and shaping behavior. When relevant, inspect cmap, GSUB/GPOS, mark attachment, and vertical metrics. Test actual rendering; table presence alone does not prove correct output.
5. Use UTF-8 for new text files. Avoid compatibility normalization or automatic mark reordering without a demonstrated need and a comparison of the result. Preserve source files unless the user requested edits in place.

When embedding or redistributing a font, read the license for that exact file and intended use; record unknown terms as unknown. Verify current application support instead of relying on historical engine limitations.

Return the diagnosis, evidence, changes made, and remaining uncertainties. Confirm extraction or copy-paste as well as visual rendering when repairing a PDF. Keep linguistic corrections separate from technical repairs.
