---
name: lao-font-studio
description: Design and build Lao (ພາສາລາວ) fonts from a text prompt, either as new letters drawn from scratch or as redesigns of the user's own provided Lao fonts (Chanthavy, Dokkham, Handwriting14, Handwriting17, Samakhee, PB Warnjai, Noto Sans Lao, Noto Serif Lao). Use when asked to create, generate, design, freestyle or restyle a Lao typeface as a working TTF/WOFF2 font.
---

# Lao Font Studio

Turn a style brief into a real, installable Lao font (TTF, optional WOFF2) with correct vowel and tone-mark stacking, plus a specimen image.

## Two ways to design

| Mode | Use when the prompt… | Script | Result |
|---|---|---|---|
| **Derive** (from a provided font) | names one of the provided fonts, or asks for a font "in/as/from/based on" Dokkham, Warnjai, Noto Serif, etc. | `scripts/derive_font.py` | The provided font's real letter shapes, restyled: heavier or lighter, wider, slanted, rounded, outline, inline, shadow, rough. Keeps its full character set, ligatures and mark positioning. |
| **Create** (from scratch) | asks for a new or original Lao font, or describes a style without naming a provided font | `scripts/build_font.py` | New letters drawn from this skill's own skeletons in any style. Lao letters only, plus Latin digits. |

If the prompt is unclear, prefer **Derive** when one provided font is clearly close to the brief, because those fonts are complete and polished. Use **Create** for styles none of them fit.

## What's in the skill

- `assets/reference-fonts/`: the eight provided Lao fonts (six display fonts plus the variable Noto Sans Lao and Noto Serif Lao). See `references/reference-fonts.md` for what each looks like and its licence notes.
- `scripts/derive_font.py`: redesigns a provided font. Recipe keys are documented at the top of the script.
- `scripts/build_font.py` + `scripts/lao_skeletons.py`: creates fonts from skeletons. Recipe keys are at the top of `build_font.py`.
- `scripts/proof.py`: specimen image + HarfBuzz missing-glyph check; `--compare FONT` puts a second font in grey under each line.
- `presets/derive/`: example derive recipes (`dokkham-outline`, `chanthavy-shadow`, `handwriting14-heavy`, `handwriting17-rough`, `samakhee-inline`, `warnjai-soft-wide`, `noto-sans-black`, `noto-sans-outline-slant`, `noto-serif-light-narrow`, `noto-serif-shadow`).
- `presets/`: create recipes (`classic-looped`, `modern-sans`, `calligraphic`, `handwritten`, `bold-display`, and `like-*` look-alikes of each provided font).
- `references/lao-letterform-guide.md`: letter features that must stay distinct, brief→recipe vocabulary, limits. Read it before Create mode, and before strong Derive effects.
- `specimens/`: example output.

If `scripts/` is missing next to this file, get the tools from the user's repo:
`git clone --depth 1 https://github.com/deeoxide/lao_typography_design /tmp/ltd` and use `/tmp/ltd/lao-font-studio/`.

Requirements: `pip install --break-system-packages fonttools shapely uharfbuzz pillow brotli` (Pillow needs RAQM for the specimen; check with `python3 -c "from PIL import features; print(features.check('raqm'))"`).

## Workflow

1. **Read the brief and pick the mode** (table above). Note the mood, use (headline, body text, logo, signage) and any provided font named. If the user gives no direction, choose boldly instead of asking; a font rebuilds in seconds.
2. **Write the recipe JSON.** Give the new font its own family name (for example "Dokkham Festival Outline").
   - Derive: set `base` to the font file name, then add effects. Typical values per 1000 em: `weight` −25 to +50, `width` 0.85–1.2, `slant` −8 to 12, `round` 5–20, `outline` 15–30, `inline` `{"inset": 15–25, "line": 6–12}`, `shadow` `{"dx": 20–40, "dy": −20 to −40, "gap": 6–12}`, `roughness` 3–10. Use `only` to restyle just some characters. For the variable Noto fonts, set `wght` (100–900) and `wdth` (62.5–100) first.
   - Create: start from the nearest preset (a `like-*` one if the brief describes a provided font's look without asking to use it), then use the guide's vocabulary table. You can redraw letters with `glyphs`, add ornaments with `extra_strokes` and nudge single letters with `transform`.
3. **Build:**
   ```bash
   python3 scripts/derive_font.py recipe.json --out out/ --woff2     # Derive
   python3 scripts/build_font.py  recipe.json --out out/ --woff2     # Create
   ```
4. **Proof:**
   ```bash
   python3 scripts/proof.py out/<Name>.ttf --out out/specimen.png --text "<the user's own Lao words>"
   python3 scripts/proof.py out/<Name>.ttf --out out/compare.png --compare assets/reference-fonts/<base>   # Derive: before/after
   ```
5. **Look at the specimen yourself** (Read the PNG). Check: tone marks and vowels sit correctly and don't collide; counters and loops are still open (heavy weight, inline and outline can close them); letters still look different from their pairs (ບ/ປ, ດ/ຕ, ຣ/ຮ, ວ/ອ, ິ/ີ …); nothing clips at the top or bottom. Fix the recipe and rebuild. Do at least one look-and-fix pass. A missing-glyph warning only matters if the original font has that character (for example, PB Warnjai has no ₭).
6. **Deliver** the TTF (plus WOFF2 for web), the specimen PNG and the recipe JSON. For Derive, say which provided font it is based on.

## Developing the skill over time

When the user approves a design or corrects something:
- Save the recipe to `presets/` (Create) or `presets/derive/` (Derive) so it can be reused.
- If a skeleton letter shape was wrong, fix `scripts/lao_skeletons.py`, rebuild two presets to check, and note it.
- Commit changes to the user's repo (`deeoxide/lao_typography_design`, folder `lao-font-studio/`) on a branch with a pull request, and add one line to `references/changelog.md`.

## Rules

- Derive mode is for the provided fonts. Derived fonts keep the original copyright notice in their name table (the script does this automatically). The two Noto fonts are open licensed (SIL OFL 1.1), so derived versions can be shared and used commercially if the licence text stays with the font. Several of the other fonts say "All rights reserved", so remind the user once to check the publisher's terms before selling or giving such a derived font to a client.
- In Create mode, never trace or copy outlines from any existing font. Skeletons are original.
- A native Lao reader should confirm new skeleton shapes before they go into `lao_skeletons.py`.
- Set `designer` in the recipe to the name the user wants credited.
