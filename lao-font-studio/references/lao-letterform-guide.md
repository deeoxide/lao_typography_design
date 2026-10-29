# Lao letterform guide for freestyle design

Read this before changing glyph skeletons or inventing a new style. It lists what must stay fixed so the text stays readable Lao, and what is free to change.

## What a Lao reader needs (never break these)

1. **Pairs that differ by one feature.** Keep the difference clear in every style:

| Pair | The only difference |
|---|---|
| ບ / ປ | ປ has a tall right stem above the x-height |
| ພ / ຟ | ຟ has a tall right stem |
| ຜ / ຝ | ຜ has a short hooked right stem; ຝ has a tall straight stem |
| ຍ / ຢ | ຢ has a tall right stem |
| ດ / ຕ | ຕ has a dip in the middle of the top |
| ກ / ຖ | ຖ's right stem goes below the baseline |
| ຂ / ຊ | ຊ's final stroke goes below the baseline |
| ຣ / ຮ | ຮ has an extra hook rising at the top right |
| ລ / ສ | ສ has a horizontal oval loop over the top |
| ວ / ອ | ອ has an inner stroke crossing the middle |
| ນ / ບ | ນ has a tail at the lower left |
| ມ / ນ | ມ's left stem is separate and ends in a loop or foot at the bottom |
| ຄ / ດ | ຄ has a notch (ε shape) on the left |
| ິ / ີ | ີ has a tail extending right |
| ຶ / ື | same as ິ / ີ, with the inner circle |
| ັ / ົ | ັ curls down then runs along the bottom; ົ curls up then runs along the top |
| ຸ / ູ | ຸ is a single hook; ູ is a small U |

2. **Heights.** All consonants share one x-height. Only ປ ຝ ຟ ຢ and the vowels ໂ ໃ ໄ rise above it. Only ງ ຊ ຖ ຽ ໆ go below the baseline. Do not let decoration add false ascenders or descenders.
3. **Loops.** In looped (traditional) styles, the loop is where the hand starts the letter. Loops must stay open (a visible hole) at text sizes. Never add a loop where the skeleton has no `heads` entry, because that can turn one letter into another.
4. **Marks.** Above vowels, tone marks and below vowels are zero-width and positioned by the font's mark tables. Tones sit above any above vowel. Keep marks lighter than the base letters so stacks stay readable.
5. **Spacing vowels.** ເ ແ ໂ ໃ ໄ come before the consonant, and ະ າ ຳ ຽ come after. They need the same stroke weight as consonants.

## What is free to change

- Stroke weight, contrast and pen angle (monoline, calligraphic broad nib, high-contrast display).
- Terminals: round, flat, square, ball (solid loops), open loops, or no loops (modern loopless).
- Proportions: width, x-height, sidebearings, tracking.
- Slant (up to about 12°) and hand-drawn roughness.
- The curve shapes inside each skeleton, as long as the features in the table above stay.
- Ornament added with `extra_strokes` (dots, swashes, inline strokes) on display fonts, as long as it doesn't touch neighbouring letters or the mark zone.

## Style vocabulary to recipe

| Brief says | Recipe direction |
|---|---|
| traditional, formal, government, temple | `loops: ring`, weight 70 to 90, contrast 1.0, no slant |
| modern, tech, startup, clean, minimal | `loops: none`, weight 60 to 80, cap round |
| brand headline, poster, bold, strong | weight 110 to 130, `loops: solid` or `none`, cap square, width 1.1 |
| elegant, wedding, luxury | contrast 0.2 to 0.35, pen_angle 30 to 40, cap flat, slant 6 to 10, ring loops |
| friendly, kids, cafe, handmade | roughness 6 to 12, weight 55 to 75, slant 2 to 5, ring loops 55 to 65 |
| retro sign painting | weight 100, contrast 0.5, cap flat, slant 8 |
| condensed, narrow | width 0.8 to 0.9, sidebearing 30 |
| airy, light | weight 40 to 55, sidebearing 55 |

## Limits of the generator

- Weight above about 140 closes the counters of ຄ ຕ ໜ ໝ. Lower `width` or `weight` if a counter closes.
- Outlines are polygons made of many short straight segments. They render smoothly at display and text sizes, but they are heavier than hand-drawn Bezier fonts. To finish a font for professional sale, open the TTF in a font editor (FontForge, Glyphs) for cleanup.
- Coverage: the 27 consonants, ໜ ໝ, all vowels and tone marks, Lao digits, ຯ ໆ ₭, basic punctuation and Latin digits 0–9. Pali/Sanskrit letters (ຆ ຉ ...) and Latin letters are not included. Pair the font with a Latin font for English text.
