# AGENTS.md — lao_typography_design

Instructions for any coding agent that reads `AGENTS.md` (Codex, Claude Code, and others) when producing, editing, proofreading, translating, or typesetting Lao (ພາສາລາວ) text. This applies to documents, slides, spreadsheets, PDFs, web pages, design files, and artwork, including bilingual Lao/Thai/English work.

## Read first

Open the reference that matches the task before you write or typeset. Load only what you need.

| Task | File |
|---|---|
| Script basics, consonant names, tone classes, digraphs | `references/lao-alphabet.md` |
| Vowel forms, positions, short/long pairs, diphthongs, the carrier ອ, syllable types | `references/lao-vowels.md` |
| Fonts, size, line height, alignment, line breaking, mixed scripts, numerals, per-format settings, QA checklist | `references/lao-typography.md` |
| Consonant and vowel charts (French-language images) | `references/images/langue-lao-consonnes.gif`, `references/images/langue-lao-voyelles.gif` |

## Hard rules

1. Lao is a complex script. Render it with a font that has OpenType shaping (default: Noto Sans Lao, used automatically unless the user names another font) and a shaping-capable engine (Chromium, LibreOffice, WeasyPrint, XeTeX/LuaTeX). Do not use ReportLab, FPDF, or PIL text drawing for Lao.
2. Use Lao codepoints (U+0E80–U+0EFF) only. Never put Thai codepoints (U+0E00–U+0E7F) inside Lao text.
3. Files are UTF-8. HTML gets `<meta charset="utf-8">` and `lang="lo"`. Tag Thai as `th` and English as `en`.
4. Body text: line-height 1.5 or more, letter-spacing 0, left-aligned, true bold only. Lao has no italic tradition, so use bold, color, or size for emphasis unless the user asks for a slant.
5. Prefixed vowels (ເ ແ ໂ ໄ ໃ) are written before the consonant but read after it. Never reorder them.
6. Never split a vowel sign or tone mark from its consonant. Never cut or wrap in the middle of a syllable. Truncate by grapheme cluster, not by byte or code unit.
7. Set a font for each script (Lao, Thai, Latin). Do not rely on fallback.
8. Use one numeral system per document (໐–໙ or 0–9). Dates are `ວັນທີ 26 ຕຸລາ 2026`. Currency is `1,500,000 ກີບ`.
9. Vowel spelling has many exceptions, especially ໃ- words and short diphthongs. Do not invent spellings. Mark anything uncertain for review by a native speaker.

## Decorative headlines and artwork

When the user asks for a styled Lao title (stroke, shadow, slant, gradient):

- Build it in HTML/CSS and render to PNG with headless Chromium. Do not draw Lao text with PIL or SVG paths.
- Use Noto Sans Lao weight 900 (for example the `@fontsource/noto-sans-lao` npm package).
- Stroke: `-webkit-text-stroke` with `paint-order: stroke fill`. Stack duplicate spans (shadow layer, outline layer, fill layer) for a double outline.
- Shadow: a hard offset shadow plus a soft blur, for example `12px 14px 0 #020b1d, 20px 26px 28px rgba(0,0,0,.5)`.
- Slant (only when requested): `transform: skewX(-10deg)`. This is a synthetic slant, not a real italic.
- Gradient fill: `background-clip: text` with `color: transparent`.
- Keep `line-height` at 1.5 or more and `letter-spacing: 0` so tone marks and lower vowels do not clip.
- Measure the text with `getBoundingClientRect()` and scale the font size to fit the column. Do not guess.
- Render at 2x or more of the delivery size. Export a transparent PNG as well when the title will go over photos.

## Verify before delivery

1. Open the rendered image or PDF and look at it. Check for boxes (□), floating tone marks, and overlapping vowels.
2. Zoom into tall clusters (a consonant with a vowel above and a tone mark, such as ມື້ ທ້າຍ ແລ້ວ ຮຶ).
3. Confirm no text is clipped at any edge.
4. Confirm the right font was applied and embedded (PDF) or loaded (web).
5. Report any text you could not confirm.
