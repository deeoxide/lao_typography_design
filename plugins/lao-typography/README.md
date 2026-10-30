# Lao Typography plugin

Skills, agents and an automatic check for professional Lao (ພາສາລາວ) work: translation, proofreading and typesetting, Unicode and font fixes, OCR, spoken and written voice, web and graphic design, alphabet teaching, and a font studio that builds working Lao fonts from a prompt. Noto Sans Lao is the default font everywhere unless you name another.

## Install

- **Claude Code:** `/plugin install lao-typography --marketplace deeoxide/lao_typography_design` (Claude Code 2.1.275 or later). On older versions: `/plugin marketplace add deeoxide/lao_typography_design`, then `/plugin install lao-typography@deeoxide-lao`.
- **Claude (claude.ai, Desktop):** upload `lao-typography-plugin.zip` where your plan allows plugin uploads, or upload the single skill `lao_typography_design.skill`.
- **ChatGPT:** upload `lao-typography-chatgpt.zip` (Codex manifest, skills and icons only).
- **Codex:** add this repository as a plugin marketplace; Codex reads `.agents/plugins/marketplace.json`.

## What you get in each app

| | Claude Code | Claude (claude.ai, Desktop) | ChatGPT | Codex |
|---|---|---|---|---|
| 12 skills | yes | yes | yes | yes |
| 10 specialist subagents (`agents/`) | yes | where agents are supported | no | no |
| Automatic Lao check after every file edit (hook) | yes | where hooks are supported | no | no |
| Listing icon, colours, starter prompts | `icon` | `icon` | `interface` | `interface` |

## Skills

| Skill | Use it for |
|---|---|
| `lao-typography-design` | The core: script, vowels, Unicode, font and layout rules, tested recipes for Word, PowerPoint, Excel, PDF and HTML, and `lao_check.py`. Load it for any Lao output. |
| `lao-font-studio` | Build new Lao fonts (TTF, WOFF2) from a prompt, or restyle the bundled fonts. |
| `english-lao-translator`, `lao-english-translator` | Translation in each direction. |
| `lao-typography-checker` | Audit a finished file for Lao typography problems. |
| `lao-unicode-font-engineer` | Boxes, floating marks, Thai mix-ups, legacy fonts, font licences. |
| `lao-font-designer` | Choose, pair and review Lao typefaces. |
| `lao-web-designer` | CSS, webfonts, language tags and responsive layout for Lao pages. |
| `lao-graphic-designer` | Posters, packaging and brands with live Lao text. |
| `lao-ocr-reader` | Read Lao from images, scans and PDFs. |
| `lao-letter-professor` | Teach and quiz the Lao alphabet. |
| `lao-voice-specialist` | Voiceover scripts, TTS, subtitles, register. |

## The automatic check (Claude Code)

After Claude writes or edits a text file (`.md`, `.txt`, `.html`, `.css`, `.json`, `.csv`, `.srt`, `.vtt` and similar) that contains Lao, the plugin runs `lao_check.py` on it. If it finds a High problem, such as Thai letters inside a Lao word, a vowel sign or tone mark with no consonant, a prefixed vowel typed in reading order, or a damaged character, Claude gets the list right away and fixes it in the same turn. Files without Lao are skipped in a few milliseconds. The check never blocks an edit. It needs `python3`; without it the hook does nothing. Turn it off by disabling the plugin's hooks in `/plugin`.

## Licence

MIT for this plugin's text and scripts. Bundled fonts keep their own licences: see `skills/lao-typography-design/references/fonts.md` and `skills/lao-font-studio/references/reference-fonts.md`.

Source and issues: https://github.com/deeoxide/lao_typography_design
