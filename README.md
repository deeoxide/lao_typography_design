# Lao Typography and Language Skills

Instructions, tools and reference notes that let Claude, ChatGPT and other coding agents work with Lao (ພາສາລາວ) correctly: translation, typography review, Unicode and fonts, teaching, web and graphic design, OCR, and spoken and written voice. It contains Markdown guidance, GIF charts, bundled Lao fonts, and two small scripts (a Lao text checker and a font installer).

## Use it where you work

| Where | What to use | How |
| --- | --- | --- |
| **Claude** (claude.ai, Claude Desktop) | [`lao_typography_design.skill`](lao_typography_design.skill) | Upload it in Claude's Skills settings. It contains `SKILL.md`, the references, the scripts and the bundled fonts. |
| **Claude Code** | The plugin: 12 skills, 10 subagents, and an automatic Lao check after every edit | `/plugin install lao-typography --marketplace deeoxide/lao_typography_design` (Claude Code 2.1.275 or later), or `/plugin marketplace add deeoxide/lao_typography_design`, then `/plugin install lao-typography@deeoxide-lao` |
| **ChatGPT plugin upload** | [`lao-typography-chatgpt.zip`](lao-typography-chatgpt.zip) | Upload this zip, not the full plugin zip and not a GitHub "Download ZIP". It has only the Codex manifest, the 12 skills and the icons. |
| **ChatGPT** (Custom GPT, Project, or one chat) | [`chatgpt/`](chatgpt/README.md) | Paste the instructions, upload the knowledge file, `lao_check.py` and the Noto Sans Lao font, turn on Code Interpreter. |
| **Codex** | The plugin | `codex plugin marketplace add deeoxide/lao_typography_design`, then `codex plugin add lao-typography@deeoxide-lao` |
| **Other agents that read `AGENTS.md`** | [`lao_typography_design/AGENTS.md`](lao_typography_design/AGENTS.md) | Copy it to your repository root with `references/`, `scripts/` and `assets/` beside it. |

## Folder map

| Location | Contents and purpose |
| --- | --- |
| [lao_typography_design/](lao_typography_design/) | The main skill. `SKILL.md` (Claude), `AGENTS.md` (Codex and others), `references/` (alphabet, vowels, typography, Unicode, recipes, fonts, charts), `scripts/` (`lao_check.py`, `setup_fonts.sh`), `assets/fonts/` (Noto Sans Lao and six display fonts). |
| [lao_typography_design.skill](lao_typography_design.skill) | The same folder as an upload archive (top folder `lao-typography-design/`). Generated. |
| [chatgpt/](chatgpt/) | Custom GPT instructions, setup guide, and a single knowledge file generated from the references. |
| [lao-font-studio/](lao-font-studio/) and [lao-font-studio.skill](lao-font-studio.skill) | The Lao font studio skill, which builds working TTF/WOFF2 fonts from a prompt, and its upload archive. |
| [Agents/](Agents/) | Ten specialist agent definitions, each with metadata and working instructions. |
| [Package/](Package/) | Package context, source inventory, and ten separate Lao skills. |
| [CLAUDE/](CLAUDE/) | Original project overview and shared Claude guidance. |
| [Image_consonnes_voyelles/](Image_consonnes_voyelles/) | Two reference charts: Lao consonants and vowels. |
| [plugins/lao-typography/](plugins/lao-typography/) | The installable plugin. Generated. Manifests: `.claude-plugin/plugin.json` (Claude), `plugin.json` at the root (the open Agent Plugins 1.0.0 standard, also copied to `.agent-plugin/`), `.codex-plugin/plugin.json` (Codex and ChatGPT listing: name, subtitle, colours, icons, starter prompts). |
| [lao-typography-plugin.zip](lao-typography-plugin.zip) | The whole plugin, all manifests at the top level. Generated. |
| [lao-typography-chatgpt.zip](lao-typography-chatgpt.zip) | The ChatGPT upload: Codex manifest, skills and icons only. Generated. |
| [plugin-src/](plugin-src/) | Plugin-only sources: icons, the Claude hook and its script, the plugin README. |
| [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json), [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json) | Marketplace files for Claude Code and Codex. Generated. |
| [bin/](bin/) | `build_plugin.py` rebuilds and checks every generated file; `inspect-project.ps1` inspects the inventory. |

## What the main skill adds beyond the notes

- **A workflow** every agent follows: read the matching reference, set up the font, produce real text, run the checker, look at a render, report what was not verified.
- **`scripts/lao_check.py`** finds common Lao text errors in text, HTML, Word, PowerPoint, Excel and PDF files: Thai letters mixed into Lao words, vowel signs and tone marks with no consonant, prefixed vowels (ເ ແ ໂ ໄ ໃ) typed in reading order, doubled tone marks, zero-width spaces inside a syllable, broken characters, mixed digits, missing Word and PowerPoint complex-script settings, and (with `--font`) characters a font cannot draw. It checks structure only, not spelling or meaning.
- **`scripts/setup_fonts.sh`** installs the bundled fonts without network access, which sandboxes need.
- **`references/unicode.md`** covers codepoints, Thai look-alikes, why NFKC must not be applied to Lao, and a tested truncation helper.
- **`references/recipes.md`** has working code for HTML to PDF, Word (including the `w:bCs` bold fix), PowerPoint, Excel and Pillow. The Word, PowerPoint and WeasyPrint recipes were run and the output viewed.
- **A section on how AI models go wrong with Lao** (retyping the user's text, slipping Thai letters in, inventing spellings) and how to avoid it.

## Start here

Read [Package/README.md](Package/README.md) for a summary and agent directory, then [CLAUDE/CLAUDE.md](CLAUDE/CLAUDE.md) for the source project's working rules. The original setup instructions are in [CLAUDE/README.md](CLAUDE/README.md). For the ten separate skills, start with the [skill priority guide](Package/skills/README.md).

To check a file for Lao errors:

```bash
python3 lao_typography_design/scripts/lao_check.py report.docx --font lao_typography_design/assets/fonts/NotoSansLao-VariableFont_wdthwght.ttf
```

To check the inventory from PowerShell in this folder:

```powershell
.\bin\inspect-project.ps1
```

## Rebuilding generated files

`lao_typography_design.skill`, `lao-font-studio.skill`, `chatgpt/lao-typography-knowledge.md`, `plugins/lao-typography/`, both plugin zips and both marketplace files are generated. After you change any source, run:

```bash
python3 bin/build_plugin.py
claude plugin validate plugins/lao-typography --strict    # if Claude Code is installed
```

The build checks each skill (name, description length, one `SKILL.md`), the ChatGPT listing limits (30-character name and subtitle, three starter prompts of 128 characters, category, colour contrast, square icons), the Agent Plugins schema and the upload limits, then rebuilds everything reproducibly. Do not edit the generated files by hand.

## Gaps in this copy

The original documentation mentions `lao_letter.json` and `AUTHORS.md`, but these files are absent. The knowledge documents titled `Lao alphabet`, `Lao vowel`, and `Lao typography` are in [lao_typography_design/references/](lao_typography_design/references/). The GIF charts are present, but have not been transcribed into structured letter data.

The project is released under the MIT license (see [LICENSE](LICENSE)); the license covers this project's original text and scripts. Bundled fonts and other third-party material keep their own licenses; see [lao_typography_design/references/fonts.md](lao_typography_design/references/fonts.md).

The original folders remain the source of truth. `Package` indexes their contents and holds standalone skill adaptations; the teaching skill includes copies of the reference charts. `bin` contains utilities, not discarded files.

See [CHANGELOG.md](CHANGELOG.md) for what changed in each version.
