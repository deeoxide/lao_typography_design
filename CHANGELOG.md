# Changelog

## 1.2.0 (2026-10-30)

Plugin manifests rebuilt against each app's real format (Claude Code docs and `claude plugin validate`, OpenAI's plugin submission rules, Codex's manifest parser, and the Agent Plugins 1.0.0 schema).

**Fixed**
- ChatGPT upload: added the square `logo` and `composerIcon` images that OpenAI requires; shortened the display name and subtitle to 30 characters; added three starter prompts. New `lao-typography-chatgpt.zip` contains only what the uploader needs.
- `.agent-plugin/plugin.json` was a copy of the Codex manifest. It now follows the Agent Plugins 1.0.0 standard (`$schema`, closed field list), and the same manifest is at the plugin root as `plugin.json`, where the standard and Codex look for it.
- The plugin folder is now `plugins/lao-typography/`, matching the plugin name as Codex marketplaces require.

**Added**
- Claude Code: the 10 specialist subagents now ship in the plugin (`agents/`), each told to load the core skill; a hook runs `lao_check.py` after Claude writes a text file containing Lao and hands any High problems back to Claude to fix (about 70 ms, never blocks); `displayName`, icon, documentation and support links.
- Codex and ChatGPT: per-skill display names and subtitles (`skills/*/agents/openai.yaml`), brand colours checked for contrast, website and support links.
- Codex marketplace file `.agents/plugins/marketplace.json`. Tested: Codex 0.166 installs the plugin and loads all 12 skills.
- `bin/build_plugin.py` checks the ChatGPT listing limits, the Agent Plugins schema and upload limits on every build.
- `lao_check.py`: a box character (□) only counts when it touches Lao letters, and `+` is accepted in vowel-chart notation such as ໍ+າ.

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
