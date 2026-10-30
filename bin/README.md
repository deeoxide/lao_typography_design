# Project utilities

## build_plugin.py

Rebuilds every generated file from the skill sources: `lao_typography_design.skill`, `lao-font-studio.skill`, `chatgpt/lao-typography-knowledge.md`, `lao-typography-plugin/` and `lao-typography-plugin.zip`. It checks each skill first (name, description length, one `SKILL.md`) and produces identical bytes when the sources have not changed. Needs only Python 3.

```bash
python3 bin/build_plugin.py
```

## inspect-project.ps1

`inspect-project.ps1` reads `Package/manifest.json` and reports whether each listed source file exists, along with its size. It also checks the three file references that were missing when the inventory was created and lists the unavailable knowledge document titles.

Run from the main folder:

```powershell
.\bin\inspect-project.ps1
```

The script resolves paths from its own location, so it also works when invoked by full path from another directory. It only reads files and requires no external modules. A missing inventoried source file causes an error; previously documented gaps are reported separately.
