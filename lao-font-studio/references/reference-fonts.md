# Provided fonts (from Deeoxide)

Six Lao fonts are bundled in `assets/reference-fonts/`. They have four uses in this skill:

1. **Base fonts for Derive mode.** When the user asks for a font "as", "in", "from" or "based on" one of these, `scripts/derive_font.py` restyles that font's real letter shapes (weight, width, slant, rounding, outline, inline, shadow, roughness). The output keeps the font's characters, ligatures and mark positioning. Examples are in `presets/derive/` and `specimens/derived-examples.png`.
2. **Look-alike starting points for Create mode.** If the user wants an original font that only feels like one of these, start from its `like-*` preset (see `specimens/reference-matches.png`).
3. **Benchmarks.** Proof any new design against the closest one with `proof.py --compare` to judge weight, size and spacing.
4. **Ready-made fonts.** If the user just needs a font, one of these may already fit. Hand over the file and say which one it is.

| File | Family name | Look | Loops | Slant | Derive example | Create look-alike |
|---|---|---|---|---|---|---|
| `Lao_Chanthavy.otf` | Lao_Chanthavy | Heavy, rounded, compact headline | small | upright | `chanthavy-shadow` | `like-chanthavy` |
| `Lao_Dokkham.ttf` | Lao_Dokkham | Heavy, festive, wide, slight contrast | yes | about 12° | `dokkham-outline` | `like-dokkham` |
| `Lao_Handwriting14.ttf` | Lao_Handwriting14 | Pen-written, upright, thick verticals | yes | upright | `handwriting14-heavy` | `like-handwriting14` |
| `Lao_Handwriting17.ttf` | Lao_Handwriting17 | Casual fast script, light, uneven | no | about 15° | `handwriting17-rough` | `like-handwriting17` |
| `Lao_Samakhee.otf` | Lao_Samakhee | Heavy, bouncy, slanted | yes | about 10° | `samakhee-inline` | `like-samakhee` |
| `PB-Warnjai-Bold.ttf` | PB Warnjai | Bold, rounded, modern, slanted | small | about 10° | `warnjai-soft-wide` | `like-warnjai` |

All six also contain Latin letters and punctuation, which Derive mode restyles along with the Lao.

## Derive tips per font

- **Heavy fonts (Chanthavy, Dokkham, Samakhee):** they take outline, inline and shadow well. Avoid `weight` above about +20, or ຄ ຕ ໜ ໝ close up.
- **Handwriting14:** has room to go much bolder (+40 to +50) and still reads well.
- **Handwriting17:** thin, so inline and outline don't work; use weight, width, slant and roughness.
- **PB Warnjai:** already bold and slanted. Use `slant` −4 to −10 to straighten it, and negative `weight` for a lighter version.

## Licensing and coverage

- Five are from Free Lao Fonts Online; Lao_Chanthavy and Lao_Handwriting17 say "All rights reserved". PB Warnjai is "Copyright 2022 Souliphong. All Rights Reserved."
- Derived fonts keep the original copyright text in their name table plus "Modified version of …". Remind the user to check the publisher's terms before selling a derived font or giving it to a client.
- None of them has Thai letters. All lack some rare Pali/Sanskrit letters (ຆ ຠ ຨ and others). Chanthavy, Handwriting17, Samakhee and Warnjai also lack ◌໎, and Warnjai lacks ◌຺ and ₭. Modern everyday Lao is fully covered.
