---
name: lao-web-designer
description: Build or improve web interfaces containing Lao text, including webfonts, language tags, responsive layout, and text wrapping. Use for Lao web implementation; do not activate for unrelated web work or translation alone.
---

# Lao web design

Work within the user's framework and existing design system. Preserve supplied Lao wording unless copy changes are requested.

## Implementation

- Declare UTF-8 and the correct page language. Tag Lao, Thai, and English passages with their own language where appropriate; do not mark every page as Lao merely because one label is Lao.
- Use a font with verified Lao coverage and shaping, plus Lao-capable fallbacks. Check exact font licensing before bundling or hosting. Preserve shaping tables when subsetting.
- Start Lao body text near `line-height: 1.7`, with `letter-spacing: 0`, normal font style, and left alignment. Adjust apparent size against Latin text by inspection. Load actual weights and avoid synthetic styles that obscure marks.
- Use flexible heights and padding for stacked marks. Avoid fixed-height clipping, `word-break: break-all`, and truncation by byte or UTF-16 code unit. Prefer dictionary-aware wrapping; test any emergency wrapping or ellipsis on real Lao content.
- Keep text selectable and accessible. Put Lao headlines over artwork as real HTML text. Preserve semantic labels, keyboard access, and meaningful language metadata.
- Do not force word spaces into Lao or normalize stored text merely to solve a layout issue.

## Verification

Inspect real Lao strings with upper/lower vowels and tone marks at narrow and wide widths and with zoom. Check long labels, form input, tables, and font fallback. Test exported or printed output if it is part of the request. Verify current platform behavior when making compatibility claims.

Deliver the implementation and a concise account of checks performed, font dependencies, and any rendering or language review still needed.
