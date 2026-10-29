#!/usr/bin/env python3
"""Build the lao-typography plugin folder and zip from the skill sources in this repo.

  python3 bin/build_plugin.py            # rebuild lao-typography-plugin/ and lao-typography-plugin.zip

Sources:
  lao_typography_design/   -> skills/lao-typography-design/
  lao-font-studio/         -> skills/lao-font-studio/
  Package/skills/<name>/   -> skills/<name>/      (the ten specialist skills)
The plugin root (manifests at the top level) is what gets zipped.
"""
import json, os, shutil, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "lao-typography-plugin")
VERSION = "1.0.0"
MANIFEST = {
    "name": "lao-typography",
    "version": VERSION,
    "description": "Lao (ພາສາລາວ) language, typography and font design for professional work: translation, typesetting, "
                   "OCR, voice, web/graphic design, and a Lao font studio that builds working TTF/WOFF2 fonts from a prompt.",
    "author": {"name": "Deeoxide"},
    "license": "MIT",
    "keywords": ["lao", "typography", "fonts", "unicode", "translation", "design"],
    "skills": "./skills/",
}

INTERFACE = {
    "displayName": "Lao Typography",
    "shortDescription": "Lao language, typography and a font studio that builds Lao fonts from a prompt.",
    "longDescription": "Skills for professional Lao (ພາສາລາວ) work: Lao/English translation, proofreading and typesetting "
                       "to Lao typography rules, OCR, spoken and written voice, web and graphic design, Unicode and font "
                       "engineering, alphabet teaching, and a Lao font studio that creates new Lao fonts or redesigns "
                       "bundled Lao fonts into working TTF/WOFF2 files.",
    "developerName": "Deeoxide",
    "category": "Productivity",
    "capabilities": ["Read", "Write"],
    "websiteURL": "https://github.com/deeoxide/lao_typography_design",
    "defaultPrompt": ["Design a Lao font for a coffee shop menu, friendly and handmade."],
}

def copy(src, dst):
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))

if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "skills"))
copy(os.path.join(ROOT, "lao_typography_design"), os.path.join(OUT, "skills", "lao-typography-design"))
copy(os.path.join(ROOT, "lao-font-studio"), os.path.join(OUT, "skills", "lao-font-studio"))
pk = os.path.join(ROOT, "Package", "skills")
for n in sorted(os.listdir(pk)):
    if os.path.isdir(os.path.join(pk, n)): copy(os.path.join(pk, n), os.path.join(OUT, "skills", n))

for d in (".claude-plugin", ".codex-plugin", ".agent-plugin"):
    os.makedirs(os.path.join(OUT, d))
    m = dict(MANIFEST)
    if d != ".claude-plugin":      # Codex and Agent manifests require an interface block
        m["interface"] = INTERFACE
    with open(os.path.join(OUT, d, "plugin.json"), "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2); f.write("\n")
shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(OUT, "LICENSE"))
with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
    f.write("# lao-typography plugin\n\nSkills for Lao language, typography and font design. "
            "See `skills/*/SKILL.md`. Rebuilt from the repo sources with `bin/build_plugin.py`.\n\n"
            "Skills: " + ", ".join(sorted(os.listdir(os.path.join(OUT, "skills")))) + "\n")

zp = os.path.join(ROOT, "lao-typography-plugin.zip")
if os.path.exists(zp): os.remove(zp)
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for dp, dn, fn in os.walk(OUT):
        for x in sorted(fn):
            p = os.path.join(dp, x); z.write(p, os.path.relpath(p, OUT))
print("built", OUT, "and", zp)
