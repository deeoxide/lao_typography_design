# Project utilities

`inspect-project.ps1` reads `Package/manifest.json` and reports whether each listed source file exists, along with its size. It also checks the three file references that were missing when the inventory was created and lists the unavailable knowledge document titles.

Run from the main folder:

```powershell
.\bin\inspect-project.ps1
```

The script resolves paths from its own location, so it also works when invoked by full path from another directory. It only reads files and requires no external modules. A missing inventoried source file causes an error; previously documented gaps are reported separately.
