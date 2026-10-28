# Lao Typography and Language Skills

This folder is a collection of Claude agent instructions and reference images for Lao language work. It covers translation, typography review, Unicode and fonts, teaching, web and graphic design, OCR, and spoken and written voice. It contains Markdown guidance and GIF charts; no application or compiled program is included.

## Folder map

| Location | Contents and purpose |
| --- | --- |
| [Agents/](Agents/) | Ten specialist agent definitions, each with metadata and working instructions. |
| [CLAUDE/](CLAUDE/) | Original project overview and shared Claude guidance. |
| [Image_consonnes_voyelles/](Image_consonnes_voyelles/) | Two reference charts: Lao consonants and vowels. |
| [Package/](Package/) | Package context, source inventory, and ten separate Lao skills. |
| [bin/](bin/) | A PowerShell utility to inspect the inventory and report missing files. |
| [lao_typography_design/](lao_typography_design/) | The `lao_typography_design` skill: `SKILL.md` for Claude, `AGENTS.md` for Codex and other coding agents, and the `Lao alphabet`, `Lao vowel`, and `Lao typography` reference notes. |
| [lao_typography_design.skill](lao_typography_design.skill) | The same folder packaged as a zip, ready to upload as a skill. |

## Start here

Read [Package/README.md](Package/README.md) for a summary and agent directory, then [CLAUDE/CLAUDE.md](CLAUDE/CLAUDE.md) for the source project's working rules. The original setup instructions are in [CLAUDE/README.md](CLAUDE/README.md).

For the separate skills, start with the [skill priority guide](Package/skills/README.md). It organizes ten standalone skills into foundation, production, and specialist groups.

To check the contents from PowerShell in this folder:

```powershell
.\bin\inspect-project.ps1
```

## Gaps in this copy

The original documentation mentions `lao_letter.json`, `LICENSE`, and `AUTHORS.md`, but these files are absent. The knowledge documents titled `Lao alphabet`, `Lao vowel`, and `Lao typography` are now in [lao_typography_design/references/](lao_typography_design/references/). The GIF charts are present, but have not been transcribed into structured letter data.

The original README credits Deeoxide (2026) and states MIT licensing. The actual license file is not included in this copy. See the source documentation for its authorship and third-party material notes.

The original folders remain the source of truth. `Package` indexes their contents and holds standalone skill adaptations; the teaching skill includes copies of the reference charts. `bin` contains utilities, not discarded files.
