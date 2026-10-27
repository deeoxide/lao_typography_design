# CLAUDE.md

Guidance for Claude when working in this project: **Lao typography and language skills** (author: Deeoxide, MIT License).

## Purpose

Help Claude understand Lao (ພາສາລາວ) language, typography, and voice for professional work: documents, slides, spreadsheets, PDFs, web pages, design files, artwork, and audio scripts, including bilingual Lao/Thai/English work.

## Project layout

| File | Role |
|---|---|
| `lao-english-translator.md` | Lao to English translation |
| `english-lao-translator.md` | English to Lao translation |
| `lao-font-designer.md` | Lao typeface and font design |
| `lao-typography-checker.md` | Audits Lao typography in files and layouts |
| `lao-letter-professor.md` | Teaches the Lao alphabet and writing system |
| `lao-unicode-font-engineer.md` | Unicode, encoding, OpenType shaping, legacy fonts, font licenses |
| `lao-web-designer.md` | CSS, webfonts, language tags, responsive layout |
| `lao-graphic-designer.md` | Posters, packaging, branding with real overlaid text |
| `lao-ocr-reader.md` | Reads Lao text from images and scans |
| `lao-voice-specialist.md` | Lao spoken voice and writing voice (register, TTS, voiceover, subtitles) |
| `lao_letter.json` | Structured data: consonants, digraphs, vowels, tone marks, digits |
| `LICENSE`, `AUTHORS.md` | MIT license and authorship |

The project knowledge documents are `Lao alphabet`, `Lao vowel`, and `Lao typography`, plus two chart images (consonants and vowels). Read them before answering questions about Lao script or typography; they are the source for the rules below.

Agent files are subagent definitions (YAML frontmatter plus instructions). To use them, copy them into `.claude/agents/`.

## Which agent to use

- Translating Lao to English: `lao-english-translator`. English to Lao: `english-lao-translator`.
- Checking a finished file or layout that contains Lao: `lao-typography-checker`.
- Broken, garbled, or boxed Lao text, Unicode, shaping, legacy fonts, font licenses: `lao-unicode-font-engineer`.
- Choosing, specifying, or reviewing a Lao typeface: `lao-font-designer`.
- Web pages and CSS with Lao: `lao-web-designer`.
- Posters, packaging, logos, brand guidelines: `lao-graphic-designer`.
- Reading Lao from images, scans, and photos: `lao-ocr-reader`.
- Teaching or quizzing the Lao alphabet: `lao-letter-professor`.
- Voiceover, text-to-speech, transcripts, subtitles, tone and register, voice profiles: `lao-voice-specialist`.

## Non-negotiable Lao rules

1. **Lao script only for Lao text** (U+0E80–U+0EFF), in UTF-8. Never use Thai codepoints (U+0E00–U+0E7F) in Lao text. Keep Lao and Thai in separate blocks, tagged `lang="lo"` and `lang="th"`.
2. **Real text, never generated.** Lao text on artwork, posters, packaging, and logos is always live text set in a Lao font and overlaid. Never let an image generator draw Lao letters. Generate artwork without text.
3. **Vowel order.** Prefixed vowels (ເ ແ ໂ ໄ ໃ) are stored before the consonant and read after it. Keep tone marks and vowel signs attached to their consonant. Never split a syllable when wrapping or truncating.
4. **No spaces between words.** Spaces only mark phrases or sentence ends. Use U+200B for allowed breaks and U+2060 to keep names together.
5. **Typography:** line height 1.5 or more (1.4 or more for headings), letter-spacing 0, no italic, no uppercase, true bold only, left-aligned, Lao about 1–2 pt larger than Latin. Fonts: Phetsarath OT for formal Word/Excel, Noto Sans Lao for web and cross-platform, Noto Serif Lao for long print text. Always define a fallback stack.
6. **Numerals, dates, currency:** one system per document. Western digits for business and finance; Lao digits (໐–໙) for formal or ceremonial use. Dates like `ວັນທີ 26 ຕຸລາ 2026` (CE unless told to use Buddhist Era). One currency format (`1,500,000 ກີບ`).
7. **Tools:** set the complex-script font and language (lo-LA) in Word and PowerPoint; generate PDFs only with shaping-capable engines (Chrome, LibreOffice, WeasyPrint, XeTeX). Avoid ReportLab and FPDF for Lao.
8. **Voice:** apply the register the audience needs; prepare spoken content with numbers written as spoken and a pronunciation list; never clone a real person's voice without written consent; never claim to hear or grade audio.

## Working rules

- **Never overwrite originals.** Write corrected or translated copies next to the source and say exactly what changed.
- **Do not rewrite, translate, or "correct" Lao wording unless asked.** Flag suspected spelling or phrasing issues as "possible".
- **Verify, don't assume.** Inspect real files and codepoints with scripts. Read font license text before embedding or redistributing a font; if a license cannot be found, mark it unknown. Check current Lao support before relying on any speech engine.
- **Do not state tone pitch values from memory.** Use a tone chart and recommend native confirmation.
- **Say what you could not verify** (rendering, spelling, meaning, licenses, audio) and recommend review by a native Lao reader for official, legal, financial, or published material. You are not a lawyer or a certified linguist.
- **Third-party material keeps its own license** (fonts, tools, trademarks). The MIT license covers only this project's original text.

## Output conventions

- Reviews: summary verdict, findings table (Severity High / Medium / Low, Location, Problem, Fix), checklist, and a "Not verified" list.
- Translations: output first, then a short "Notes" section only for real ambiguities.
- Transcriptions: verbatim text with uncertainty marks (`[?x]`, `[…]`), then an uncertainty list.
- Files with Lao: tell the user which font is needed and to view a preview before delivery.

## Editing this project

- Keep each agent file self-contained, with `name`, `description`, `tools`, and `model` in the frontmatter.
- Keep rules consistent across agents. If a shared rule changes (for example the font list or line height), update every agent file, `lao_letter.json` if relevant, and this file.
- Keep `lao_letter.json` valid JSON in UTF-8. Validate it after edits.
- Update `AUTHORS.md` when agents are added or removed.
