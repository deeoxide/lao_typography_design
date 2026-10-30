# Changelog

## 1.1.0 (2026-10-30)

Better results for Claude and ChatGPT.

**Fixed**
- `lao_typography_design.skill` was out of date: it still said Phetsarath OT was the default and did not contain the Noto Sans Lao font that `SKILL.md` points to. `lao-font-studio.skill` was also behind its source. Both are now rebuilt from the sources, reproducibly, by `bin/build_plugin.py`.
- The skill archive's top folder now matches the skill name (`lao-typography-design/`), as the Agent Skills format requires.
- `references/lao-alphabet.md`: ຄ now shows its full name (ຄໍ ຄວາຍ); a note on ຣ versus ລ; tone-mark and digit tables added.
- `references/lao-typography.md`: truncating by grapheme cluster is not enough (a prefixed vowel can be stranded); Word bold needs `w:bCs`; month and weekday names added.
- `references/lao-vowels.md`: example words for ɯ / ɯɯ.
- Removed stray frontmatter from the three reference notes.

**Added**
- `SKILL.md` rewritten: sharper description and triggers, a six-step workflow, a section on how AI models go wrong with Lao, and notes for sandboxes (Claude's workspace, ChatGPT's code interpreter, Codex). `AGENTS.md` matches it.
- `scripts/lao_check.py`: checks text, HTML, CSS, Word, PowerPoint, Excel and PDF files for common Lao errors, and font files for missing glyphs and Lao shaping tables.
- `scripts/setup_fonts.sh`: installs the bundled fonts without network access.
- `references/unicode.md` and `references/recipes.md`.
- `chatgpt/`: Custom GPT instructions (under 8,000 characters), a setup guide, and a generated single-file knowledge bundle.
- `bin/build_plugin.py` now also builds both `.skill` archives and the ChatGPT knowledge file, and validates each skill first.
- Plugin version 1.1.0.
