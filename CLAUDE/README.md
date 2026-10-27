# Lao Typography and Language Skills

A set of Claude subagents and reference data for professional work in **Lao (ພາສາລາວ)**: script, Unicode, translation, typography, fonts, web, graphic design, OCR, teaching, and voice. Built for bilingual Lao / Thai / English production in Lao PDR.

Author: **Deeoxide** · License: **MIT** · Year: 2026

## Why

Lao is a complex script. Vowels and tone marks attach to consonants and need real OpenType shaping, generous line spacing, and the right fonts. AI image generators draw Lao text badly, and Lao is easily confused with Thai. These skills encode the rules that keep Lao text correct, readable, and professional.

## What is included

| File | What it does |
|---|---|
| `lao-english-translator.md` | Translates Lao to English |
| `english-lao-translator.md` | Translates English to natural, correctly spelled Lao |
| `lao-font-designer.md` | Designs, specifies, and reviews Lao typefaces and glyph coverage |
| `lao-typography-checker.md` | Audits Lao typography in documents, slides, spreadsheets, PDFs, web, and design files |
| `lao-letter-professor.md` | Teaches the Lao alphabet, vowels, tone marks, and reading |
| `lao-unicode-font-engineer.md` | Unicode, encoding, OpenType shaping, legacy fonts, font license checks |
| `lao-web-designer.md` | CSS, webfonts, language tags, and responsive layout for Lao sites |
| `lao-graphic-designer.md` | Posters, packaging, and branding with real overlaid Lao text |
| `lao-ocr-reader.md` | Reads and transcribes Lao text from images, scans, and PDFs |
| `lao-voice-specialist.md` | Lao spoken voice and writing voice: register, voiceover, TTS, subtitles, voice profiles |
| `lao_letter.json` | Structured Lao letter data: 27 consonants, digraphs, vowels, tone marks, digits |
| `CLAUDE.md` | Project guidance and rules for Claude |
| `LICENSE`, `AUTHORS.md` | MIT license and authorship |

Every agent also carries a short "Lao voice (spoken and writing)" section so voice features work across the whole set.

## Install

1. Copy the agent files (the ten `.md` files whose names start with `lao-` or `english-lao-`) into your project's `.claude/agents/` folder, or into `~/.claude/agents/` to use them everywhere.
2. Keep `CLAUDE.md` at the project root so Claude loads the shared Lao rules.
3. Optional: keep `lao_letter.json` in the project as reference data for apps, flashcards, and quizzes.

Check the current Claude documentation for the exact agent folder and format your version expects.

## Use

Ask for the work in plain language, or name an agent:

- "Translate this proposal from Lao to English." → `lao-english-translator`
- "Check the Lao typography in this PDF before I send it." → `lao-typography-checker`
- "Why do the tone marks float in this Word file?" → `lao-unicode-font-engineer`
- "Build a landing page with Lao and English." → `lao-web-designer`
- "Design a coffee cup sleeve with a Lao headline." → `lao-graphic-designer`
- "Transcribe the Lao text in this photo." → `lao-ocr-reader`
- "Teach me the mid-class consonants." → `lao-letter-professor`
- "Write a Lao voiceover script and a voice profile for this brand." → `lao-voice-specialist`

## Core rules in one list

1. Lao text uses Lao codepoints only (U+0E80–U+0EFF); never Thai codepoints.
2. Lao on artwork is always real, live text over text-free images; never AI-generated.
3. Line height 1.5 or more, letter-spacing 0, no italic, no uppercase, true bold, left-aligned.
4. Use a shaping-capable font and engine (Phetsarath OT, Noto Sans Lao, Noto Serif Lao; Chrome, LibreOffice, WeasyPrint, XeTeX for PDF).
5. One numeral, date, and currency system per document.
6. Prefixed vowels are stored before the consonant and read after it; never split a syllable.
7. Verify fonts' licenses, tools' Lao support, and have a native Lao reader review official or published work.

## Limits

- Agents give technical guidance, not legal advice or linguistic certification.
- Pronunciation, tone pitch, and audio quality cannot be judged by the agents; use a tone chart and native speakers.
- Lao support in speech and OCR tools varies and changes; the agents are told to check current support before relying on any tool.
- Example words and romanizations are approximate and should be confirmed by a native speaker before publishing teaching material.

## Third-party material

The MIT License covers only the original text in this project. Fonts (such as Noto and Phetsarath OT), software, and trademarks mentioned here keep their own licenses. Read each license before embedding, redistributing, or using them commercially.

## Credit

If you reuse or adapt this work, keep the copyright notice and license text, and credit:

> Deeoxide, Lao typography and language skills, 2026.
