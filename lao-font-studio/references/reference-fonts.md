# Reference fonts (provided by Deeoxide)

Six Lao fonts are bundled in `assets/reference-fonts/`. They have three jobs in this skill:

1. **Mood references.** When a user says "like Dokkham" or "in the style of Warnjai", start from the matching `like-*` preset, build, and compare side by side:
   `python3 scripts/proof.py out/<Name>.ttf --out compare.png --compare assets/reference-fonts/<file>`
   The generated line is black and the reference is grey under it. Match weight, slant, width, loop size and overall colour on the page.
2. **Benchmarks.** Proof a new design against the closest reference to judge whether its weight, x-height and spacing are in a normal range for Lao display type.
3. **Ready-made fonts.** If the user just needs a font and not a new design, one of these may already fit. Hand over the file and say which one it is.

`specimens/reference-matches.png` shows each reference next to its `like-*` recipe.

| File | Family name | Look | Loops | Slant | Starting preset |
|---|---|---|---|---|---|
| `Lao_Chanthavy.otf` | Lao_Chanthavy | Heavy, rounded, compact headline | small | upright | `like-chanthavy` |
| `Lao_Dokkham.ttf` | Lao_Dokkham | Heavy, festive, wide, slight contrast | yes | about 12° | `like-dokkham` |
| `Lao_Handwriting14.ttf` | Lao_Handwriting14 | Pen-written, upright, thick verticals | yes | upright | `like-handwriting14` |
| `Lao_Handwriting17.ttf` | Lao_Handwriting17 | Casual fast script, light, uneven | no | about 15° | `like-handwriting17` |
| `Lao_Samakhee.otf` | Lao_Samakhee | Heavy, bouncy, slanted | yes | about 10° | `like-samakhee` |
| `PB-Warnjai-Bold.ttf` | PB Warnjai | Bold, rounded, modern, slanted | small | about 10° | `like-warnjai` |

## Rules for using them

- **Reference only, never copy.** Do not trace, extract, convert or reuse their outlines, glyph data or metrics tables in a generated font. Generated fonts are built only from this skill's own skeletons. Looking at them and matching mood is fine.
- **Licensing.** Five are from Free Lao Fonts Online; Lao_Chanthavy and Lao_Handwriting17 say "All rights reserved". PB Warnjai is "Copyright 2022 Souliphong. All Rights Reserved." Check the publisher's terms before handing one of these files to a client or using it in paid work.
- **Coverage gaps.** None of them has Thai letters. All lack some rare Pali/Sanskrit letters (ຆ ຠ ຨ and others). Chanthavy, Handwriting17, Samakhee and Warnjai also lack ◌໎, and Warnjai lacks the Pali virama ◌຺. Modern everyday Lao is fully covered.
- **When a generated font replaces one of them** in a project, note which reference it was matched to in the recipe's `description` or the delivery message, so the design history is clear.
