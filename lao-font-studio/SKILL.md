---
name: lao-font-studio
description: Design and build original Lao (ພາສາລາວ) fonts from a text prompt. Use when the user asks to create, generate, design or freestyle a Lao typeface or Lao lettering as a working TTF/WOFF2 font, or to change an earlier generated Lao font.
---

# Lao Font Studio

Turn a style brief into a real, installable Lao font (TTF, optional WOFF2) with correct vowel and tone-mark stacking, plus a specimen image. Lao only: no Latin letters. The fonts include Latin digits 0–9.

## How it works

- `scripts/lao_skeletons.py` holds the letter skeletons: stroke centrelines for every Lao consonant, vowel, tone mark and digit, with loop points (`heads`) and loopless extras (`sans`).
- `scripts/build_font.py` strokes the skeletons with a pen described by a **style recipe** (JSON), adds loops or not, applies slant, width and roughness, then builds the TTF with GDEF/GPOS mark positioning (mark, mkmk) for Lao.
- `scripts/proof.py` renders a specimen with HarfBuzz shaping and reports missing glyphs.
- `presets/` holds starting recipes: `classic-looped`, `modern-sans`, `calligraphic`, `handwritten`, `bold-display`, plus one `like-*` recipe for each reference font (`like-chanthavy`, `like-dokkham`, `like-handwriting14`, `like-handwriting17`, `like-samakhee`, `like-warnjai`).
- `assets/reference-fonts/` holds six Lao fonts the user provided (Chanthavy, Dokkham, Handwriting14, Handwriting17, Samakhee, PB Warnjai Bold). Use them as mood references and benchmarks, and as ready-made fonts when no new design is needed. Read `references/reference-fonts.md` before using them.
- `references/lao-letterform-guide.md` covers which letter features must never change, what is free to change, how brief wording maps to recipe values, and the generator's limits. **Read it before designing.**

If the `scripts/` folder is missing next to this file, get it from the user's repo:
`git clone --depth 1 https://github.com/deeoxide/lao_typography_design /tmp/ltd` and use `/tmp/ltd/lao-font-studio/`.

Requirements: `pip install --break-system-packages fonttools shapely uharfbuzz pillow brotli` (Pillow needs RAQM for the specimen; check with `python3 -c "from PIL import features; print(features.check('raqm'))"`).

## Workflow

1. **Read the brief.** Note the mood, use (headline, body text, logo, signage), weight, and looped or loopless. If the user gives no direction, pick a bold interpretation instead of asking; a font is quick to rebuild.
2. **Write the recipe.** If the user names or describes one of the reference fonts ("like Dokkham", "bold and slanted like Warnjai"), start from its `like-*` preset. Otherwise start from the nearest preset and change values using the vocabulary table in the guide. Give the font a family name that fits the brief (for example "Cupfee Lao Round"). All recipe keys are documented at the top of `build_font.py`.
3. **Freestyle the letters when the brief calls for it.** In the recipe you can:
   - `glyphs`: replace a letter's skeleton completely. Copy its entry from `lao_skeletons.py` and edit the paths. Path commands: `M L C Q` (absolute, y up, baseline 0, x-height 500, tall stems 760) and `O cx cy r` for a circle.
   - `extra_strokes`: add ornament strokes to a letter, such as a swash, inline or dot.
   - `transform`: nudge one letter (`sx sy dx dy`).
   Keep every distinguishing feature from the guide's pair table.
4. **Build and proof:**
   ```bash
   python3 scripts/build_font.py recipe.json --out out/ --woff2
   python3 scripts/proof.py out/<Name>.ttf --out out/specimen.png --text "<the user's own Lao words>"
   # optional: compare against a reference font (grey line under each generated line)
   python3 scripts/proof.py out/<Name>.ttf --out out/compare.png --compare assets/reference-fonts/Lao_Dokkham.ttf
   ```
5. **Look at the specimen image yourself** (Read the PNG). Check for: closed loop holes, closed counters, marks colliding or floating, uneven weight between letters, and letters that look like their pair. Fix the recipe or skeleton and rebuild. Do at least one look-and-fix pass before delivering.
6. **Deliver** the TTF (plus WOFF2 for web), the specimen PNG and the recipe JSON, so the design can be rebuilt or changed later. Mention any limits from the guide that affect their use (for example, no Latin letters).

## Developing the skill over time

The skill improves as it is used. When the user approves a design or corrects a letter:
- Save the recipe to `presets/<name>.json` so it can be reused.
- If a skeleton correction should apply to every future font (a letter shape was wrong, not just stylistic), edit `scripts/lao_skeletons.py`. Rebuild two presets to check nothing else broke, then commit to the user's repo (`deeoxide/lao_typography_design`, folder `lao-font-studio/`) on a branch with a pull request.
- Note the change in one line in `references/changelog.md`.

## Rules

- A native Lao reader should confirm a new skeleton shape before it goes into `lao_skeletons.py`.
- Never trace or copy outlines from an existing font, including the bundled reference fonts. Skeletons are original; reference fonts may be viewed and compared, not copied.
- The bundled reference fonts carry their publishers' copyright. Check the terms before giving the files to clients or using them in paid work.
- Fonts made here belong to the user. Set `designer` in the recipe to the name they want credited.
