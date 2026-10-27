# Package context

This package collects instructions for professional Lao language and typography work, including bilingual Lao, Thai, and English projects. Its main assets are ten specialist Claude agent definitions and two alphabet reference images.

Ten separate skill adaptations are available in [skills/](skills/README.md), with a priority guide and a `SKILL.md` in each skill folder. These are workspace package sources, not a global installation.

## Agent directory

| Agent file in `../Agents/` | Main responsibility |
| --- | --- |
| `english-lao-translator.md` | English-to-Lao translation and Lao editing. |
| `lao-english-translator.md` | Lao/English translation, with emphasis on Lao-to-English work. |
| `lao-font-designer.md` | Typeface design, glyph coverage, and font review. |
| `lao-graphic-designer.md` | Posters, packaging, branding, and real Lao text over artwork. |
| `lao-letter-professor.md` | Alphabet, vowels, tone marks, reading, and learning materials. |
| `lao-ocr-reader.md` | Transcription of Lao text from images and scanned documents. |
| `lao-typography-checker.md` | Typography reviews across documents, layouts, and websites. |
| `lao-unicode-font-engineer.md` | Encoding, shaping, legacy fonts, and font license checks. |
| `lao-voice-specialist.md` | Spoken scripts, writing register, subtitles, and voice profiles. |
| `lao-web-designer.md` | Lao webfonts, CSS, language tags, and responsive layouts. |

## Shared guidance

The source instructions emphasize correct Lao Unicode, keeping Thai and Lao text distinct, preserving vowel and tone-mark clusters, using fonts and rendering engines that support Lao shaping, and allowing adequate line spacing. They require real font-set Lao text in artwork and consistent numeral, date, and currency styles. They also call for native-reader review where appropriate and verification of tool support and font licensing.

These are summaries of the supplied instructions, not an independent linguistic or technical review. Read [the full guidance](../CLAUDE/CLAUDE.md) before applying it.

## Reference material

- [Consonant chart](../Image_consonnes_voyelles/langue-lao-consonnes.gif)
- [Vowel chart](../Image_consonnes_voyelles/langue-lao-voyelles.gif)
- [Original README](../CLAUDE/README.md)

## Manifest

[`manifest.json`](manifest.json) lists the 14 original files with their roles. All paths are relative to the main project folder, one level above this folder. It also records references that are absent from this copy. Newly added organizational files are not counted as original package assets.

Keep the manifest current when adding or removing source assets, and run `../bin/inspect-project.ps1` to check listed paths. This folder contains package metadata and skill source folders; it is not a built archive or a global skill installation.
