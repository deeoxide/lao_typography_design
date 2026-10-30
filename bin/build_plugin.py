#!/usr/bin/env python3
"""Rebuild every generated artifact in this repo from the skill sources.

  python3 bin/build_plugin.py

Sources                                      Generated
  lao_typography_design/                  ->   lao_typography_design.skill      (upload to Claude; top folder lao-typography-design/)
  lao-font-studio/                        ->   lao-font-studio.skill            (top folder lao-font-studio/)
  lao_typography_design/references/*.md   ->   chatgpt/lao-typography-knowledge.md   (one file for a Custom GPT or Project)
  lao_typography_design/, lao-font-studio/,
  Package/skills/<name>/                  ->   lao-typography-plugin/ and lao-typography-plugin.zip
                                               (manifests for Claude, Codex and Agent; version also written to
                                               .claude-plugin/marketplace.json)

Archives are reproducible: entries are sorted and carry a fixed timestamp, so rebuilding unchanged sources gives
identical bytes. Each skill is checked first (SKILL.md present, name matches its archive folder, description length,
one SKILL.md per skill). Nothing outside the repo is touched.
"""
import json, os, re, shutil, sys, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "lao-typography-plugin")
VERSION = "1.1.0"
FIXED_TIME = (2026, 10, 30, 0, 0, 0)
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")

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

KNOWLEDGE_ORDER = ["lao-alphabet.md", "lao-vowels.md", "lao-typography.md", "unicode.md", "recipes.md", "fonts.md"]


def frontmatter(skill_dir):
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        sys.exit("build: %s has no SKILL.md" % skill_dir)
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        sys.exit("build: %s/SKILL.md has no frontmatter" % skill_dir)
    fm = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        if _ and not line.startswith(" "):
            fm[k.strip()] = v.strip()
    return fm


def check_skill(skill_dir, expected_name=None):
    fm = frontmatter(skill_dir)
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        sys.exit("build: %s: name %r must be lowercase letters, digits and hyphens" % (skill_dir, name))
    if expected_name and name != expected_name:
        sys.exit("build: %s: name %r != %r" % (skill_dir, name, expected_name))
    if not desc or len(desc) > 1024:
        sys.exit("build: %s: description missing or over 1024 characters (%d)" % (skill_dir, len(desc)))
    nested = [os.path.join(dp, f) for dp, _, fs in os.walk(skill_dir) for f in fs
              if f == "SKILL.md" and os.path.join(dp, f) != os.path.join(skill_dir, "SKILL.md")]
    if nested:
        sys.exit("build: %s: extra SKILL.md files are rejected on upload: %s" % (skill_dir, nested))
    return name


def files_under(base):
    for dp, dn, fn in os.walk(base):
        dn[:] = sorted(d for d in dn if d not in ("__pycache__",))
        for f in sorted(fn):
            if f.endswith(".pyc") or f == ".DS_Store":
                continue
            yield os.path.join(dp, f)


def write_zip(zip_path, base, prefix=""):
    """Zip every file under base, with `prefix/` in front, reproducibly."""
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files_under(base):
            arc = os.path.join(prefix, os.path.relpath(p, base)).replace(os.sep, "/")
            zi = zipfile.ZipInfo(arc, FIXED_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = (os.stat(p).st_mode & 0o777) << 16
            with open(p, "rb") as f:
                z.writestr(zi, f.read())


def demote_headings(md):
    out, fenced = [], False
    for line in md.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        out.append("#" + line if (not fenced and line.startswith("#")) else line)
    return "\n".join(out)


def build_knowledge():
    refs = os.path.join(ROOT, "lao_typography_design", "references")
    parts = [
        "# Lao typography knowledge bundle\n\n"
        "Generated from `lao_typography_design/references/` by `bin/build_plugin.py`. Do not edit this file; edit the "
        "sources and rebuild. Use it with `chatgpt/custom-gpt-instructions.md`.\n\n"
        "**Files in ChatGPT.** Files uploaded to a GPT or project are flat under `/mnt/data/`. Where these notes say "
        "`scripts/lao_check.py` use `/mnt/data/lao_check.py`; where they say `assets/fonts/X` use `/mnt/data/X`; "
        "`scripts/setup_fonts.sh` is not needed, copy the font file to `~/.fonts` and run `fc-cache -f` instead.\n"
    ]
    for name in KNOWLEDGE_ORDER:
        text = open(os.path.join(refs, name), encoding="utf-8").read().strip()
        parts.append("\n---\n\n" + demote_headings(text) + "\n")
    path = os.path.join(ROOT, "chatgpt", "lao-typography-knowledge.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(parts))
    return path


def build_plugin(skill_names_dirs):
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "skills"))
    for name, src in skill_names_dirs:
        shutil.copytree(src, os.path.join(OUT, "skills", name), ignore=IGNORE)
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
    write_zip(os.path.join(ROOT, "lao-typography-plugin.zip"), OUT)

    mp = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
    data = json.load(open(mp, encoding="utf-8"))
    for p in data.get("plugins", []):
        if p.get("name") == MANIFEST["name"]:
            p["version"] = VERSION
    with open(mp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2); f.write("\n")


def main():
    skills = []   # (skill name, source dir)
    for src in (os.path.join(ROOT, "lao_typography_design"), os.path.join(ROOT, "lao-font-studio")):
        skills.append((check_skill(src), src))
    pk = os.path.join(ROOT, "Package", "skills")
    for n in sorted(os.listdir(pk)):
        d = os.path.join(pk, n)
        if os.path.isdir(d):
            skills.append((check_skill(d, expected_name=n), d))

    # upload archives: the top folder is the skill name, as the Agent Skills format requires
    for fname, (name, src) in (("lao_typography_design.skill", skills[0]), ("lao-font-studio.skill", skills[1])):
        write_zip(os.path.join(ROOT, fname), src, prefix=name)
    kb = build_knowledge()
    build_plugin(skills)
    print("skills checked:", ", ".join(n for n, _ in skills))
    print("built: lao_typography_design.skill, lao-font-studio.skill, %s, lao-typography-plugin/, lao-typography-plugin.zip (v%s)"
          % (os.path.relpath(kb, ROOT), VERSION))


if __name__ == "__main__":
    main()
