---
name: lao-typography-design
description: lao_typography_design. Use whenever producing, editing, proofreading, translating, or typesetting Lao (ພາສາລາວ) text — documents, slides, spreadsheets, PDFs, web pages, or design files, artwork — including bilingual Lao/Thai/English work. Covers the script, Unicode, grammar and register, formal document conventions, font and layout rules, and per-format technical handling.
---

# Lao typography and language (lao_typography_design)

Use this skill for any work that produces, edits, proofreads, translates, or typesets Lao (ພາສາລາວ) text, including bilingual Lao/Thai/English work.

## How to use the reference files

Read the reference that matches the task before writing or typesetting. Load only what you need.

| Task | Read |
|---|---|
| Script basics, consonant names, tone classes, digraphs | `references/lao-alphabet.md` |
| Vowel forms, positions, short/long pairs, diphthongs, the carrier ອ, syllable types | `references/lao-vowels.md` |
| Fonts, size, line height, alignment, line breaking, mixed scripts, numerals, per-format settings, QA checklist | `references/lao-typography.md` |
| Visual charts of the consonants and vowels (French-language charts) | `references/images/langue-lao-consonnes.gif`, `references/images/langue-lao-voyelles.gif` |

## Core rules (always apply)

1. Lao is a complex script. Use a font with proper OpenType shaping (Phetsarath OT, Noto Sans Lao) and a shaping-capable tool.
2. Line height 1.5 or more. Letter-spacing 0. No italic or faux bold. Prefer left alignment.
3. Never split a vowel sign or tone mark from its consonant, and never cut text in the middle of a syllable.
4. Prefixed vowels (ເ ແ ໂ ໄ ໃ) are written before the consonant but read after it.
5. Use Lao codepoints (U+0E80–U+0EFF), never Thai codepoints (U+0E00–U+0E7F), inside Lao text.
6. Tag languages (`lo`, `th`, `en`) and set a font per script. Use one numeral system per document.
7. Before delivery, view a preview image or PDF and check for boxes (□), floating marks, and overlapping vowels.
8. Vowel spelling has many exceptions. Have a native speaker confirm important text.
