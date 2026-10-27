# Separate Lao skills and priorities

Ten standalone skills adapted from the corresponding files in `Agents/` and shared guidance in `CLAUDE/CLAUDE.md`. Original materials credit Deeoxide (2026); the source license file is absent, as recorded in the package manifest.

Each folder contains an independent `SKILL.md` with a focused description and workflow. The teaching skill also includes copies of the two supplied reference charts. No skill requires the original agent files or another skill to operate.

## Priority guide

Priority means the recommended order of attention when several needs overlap. It is documentation, not a runtime priority setting, and does not override the user's request. Use only the skills relevant to the task.

| Priority | Skill | When to use |
| --- | --- | --- |
| P1 - Foundation | [lao-unicode-font-engineer](lao-unicode-font-engineer/SKILL.md) | Broken text, encoding, missing glyphs, detached marks, legacy conversions. |
| P1 - Foundation | [english-lao-translator](english-lao-translator/SKILL.md) | Translate English into Lao. |
| P1 - Foundation | [lao-english-translator](lao-english-translator/SKILL.md) | Translate Lao into English. |
| P1 - Foundation | [lao-typography-checker](lao-typography-checker/SKILL.md) | Review readability and rendering of a Lao deliverable. |
| P2 - Production | [lao-ocr-reader](lao-ocr-reader/SKILL.md) | Extract Lao from images and scanned documents. |
| P2 - Production | [lao-web-designer](lao-web-designer/SKILL.md) | Build or improve Lao web layouts. |
| P2 - Production | [lao-graphic-designer](lao-graphic-designer/SKILL.md) | Produce Lao posters, packaging, and visual layouts. |
| P3 - Specialist | [lao-font-designer](lao-font-designer/SKILL.md) | Develop Lao typefaces and integrate/test fonts in Adobe, Figma, and Canva. |
| P3 - Specialist | [lao-letter-professor](lao-letter-professor/SKILL.md) | Teach Lao script and reading. |
| P3 - Specialist | [lao-voice-specialist](lao-voice-specialist/SKILL.md) | Prepare spoken scripts, writing voice, and subtitles. |

## Resolve overlapping tasks

- For an image requiring translation, transcribe first, retain uncertainty markers, then translate.
- For garbled source text, diagnose encoding before translating; a font change alone cannot fix corrupted text.
- For a web page or poster, use the production skill to create the deliverable and check typography before handing it over. A full separate audit is needed only when requested or justified by a problem.
- For teaching or voice tasks, use that specialist directly. P3 does not make these tasks less important when they are the user's goal.

## Packaging status

These are skill source folders in the workspace, not a global installation. Package placement alone does not activate them in an assistant. Keep each folder intact when importing it into the target assistant's supported skill location. No artificial `priority` field, Claude `model` setting, or fixed tool list is included in the skill frontmatter.

The original 14-file inventory remains in `../manifest.json`; it intentionally tracks source assets separately from these adaptations.
