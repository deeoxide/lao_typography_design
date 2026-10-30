#!/usr/bin/env python3
"""Rebuild every generated artifact in this repo from the sources, and check them.

  python3 bin/build_plugin.py

Sources                                       Generated
  lao_typography_design/                   ->  lao_typography_design.skill        (upload to Claude; top folder lao-typography-design/)
  lao-font-studio/                         ->  lao-font-studio.skill              (top folder lao-font-studio/)
  lao_typography_design/references/*.md    ->  chatgpt/lao-typography-knowledge.md
  the two skills above, Package/skills/*,
  Agents/*.md, plugin-src/                 ->  plugins/lao-typography/            (the plugin: Claude Code, Codex, Agent manifests)
                                               lao-typography-plugin.zip          (the whole plugin, all manifests at the top level)
                                               lao-typography-chatgpt.zip         (ChatGPT / OpenAI upload: Codex manifest, skills, icons only)
                                               .claude-plugin/marketplace.json    (Claude Code marketplace)
                                               .agents/plugins/marketplace.json   (Codex marketplace)

What goes where
  Claude (.claude-plugin/plugin.json): skills, 10 subagents (agents/), a PostToolUse hook that runs lao_check.py
    after Claude writes a text file with Lao (claude/hooks.json + scripts/lao_hook.py), icon and listing URLs.
  Agent Plugins 1.0.0 (plugin.json at the plugin root, copied to .agent-plugin/plugin.json): the open portable
    manifest. Closed schema, $schema required; skills come from ./skills/. Codex reads it first.
  Codex / ChatGPT (.codex-plugin/plugin.json): read by Codex as an overlay on the root manifest, and by ChatGPT's
    uploader. Skills, per-skill agents/openai.yaml display names, and the interface block (name, subtitle, colours,
    icons, starter prompts). No hooks: the Codex validator rejects a "hooks" field.

Archives are reproducible (sorted entries, fixed timestamps). The build stops on any rule it can check offline:
skill names and descriptions, OpenAI listing limits (display name and subtitle 30 characters, three starter
prompts of 128 characters, category list, colour contrast, square icons), and archive limits.
Also run `claude plugin validate plugins/lao-typography` when Claude Code is installed.
"""
import json, os, re, shutil, struct, sys, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN_NAME = "lao-typography"
OUT = os.path.join(ROOT, "plugins", PLUGIN_NAME)
VERSION = "1.2.0"
REPO = "https://github.com/deeoxide/lao_typography_design"
FIXED_TIME = (2026, 10, 30, 0, 0, 0)
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")

DESCRIPTION = ("Lao (ພາສາລາວ) language, typography and font design for professional work: translation, proofreading "
               "and typesetting with Noto Sans Lao by default, Unicode and font fixes, OCR, spoken and written voice, "
               "web and graphic design, alphabet teaching, a Lao text checker, and a font studio that builds working "
               "TTF/WOFF2 fonts from a prompt.")

COMMON = {
    "name": PLUGIN_NAME,
    "version": VERSION,
    "description": DESCRIPTION,
    "author": {"name": "Deeoxide", "url": "https://github.com/deeoxide"},
    "homepage": REPO + "#readme",
    "repository": REPO,
    "license": "MIT",
    "keywords": ["lao", "laos", "ພາສາລາວ", "typography", "fonts", "unicode", "translation", "ocr", "design",
                 "noto-sans-lao"],
}

CLAUDE_MANIFEST = dict(COMMON, **{
    "displayName": "Lao Typography",
    "icon": "./assets/logo.png",
    "documentationUrl": REPO + "#readme",
    "supportUrl": REPO + "/issues",
    "hooks": "./claude/hooks.json",
})

INTERFACE = {
    "displayName": "Lao Typography",
    "shortDescription": "Lao language, type and fonts",
    "longDescription": (
        "Professional Lao (ພາສາລາວ) work in one plugin. Translate between Lao and English; proofread and typeset "
        "Lao in Word, PowerPoint, Excel, PDF and web pages with Noto Sans Lao by default; fix boxes, floating "
        "tone marks, Thai letters mixed into Lao, and legacy fonts; read Lao from images; prepare voiceover "
        "scripts and subtitles; design posters and brands with live Lao text; teach the alphabet; and build new "
        "Lao fonts from a prompt. Includes a checker that finds common Lao text errors in files, and tested "
        "recipes for every common format."),
    "developerName": "Deeoxide",
    "category": "Productivity",
    "capabilities": ["Interactive", "Write"],
    "websiteURL": REPO,
    "supportURL": REPO + "/issues",
    "defaultPrompt": [
        "Translate this English text into natural Lao",
        "Make a Lao price list as a Word file and a PDF",
        "Design a Lao headline font for a festival poster",
    ],
    "brandColor": "#1B3F8B",
    "brandColorDark": "#7FA6F5",
    "composerIcon": "./assets/icon.png",
    "logo": "./assets/logo.png",
}
OPENAI_MANIFEST = dict(COMMON, skills="./skills/", interface=INTERFACE)

# Agent Plugins 1.0.0 (https://agent-plugins.org): the open, vendor-neutral manifest. It lives at the plugin root as
# plugin.json, its schema is closed (only these fields), and skills are always discovered from ./skills/. Codex
# reads it first and then layers .codex-plugin/plugin.json on top for the listing (interface, icons, prompts).
AGENT_PLUGINS_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
AGENT_PLUGINS_FIELDS = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license",
                        "keywords", "extensions"}
AGENT_MANIFEST = dict({"$schema": AGENT_PLUGINS_SCHEMA},
                      **{k: v for k, v in COMMON.items() if k in AGENT_PLUGINS_FIELDS})

# Display name and subtitle per skill, for ChatGPT and Codex (skills/<name>/agents/openai.yaml)
SKILL_UI = {
    "lao-typography-design": ("Lao Typography", "Lao script, fonts, layout rules and checker"),
    "lao-font-studio": ("Lao Font Studio", "Build Lao fonts from a prompt"),
    "english-lao-translator": ("English to Lao", "Translate English into natural Lao"),
    "lao-english-translator": ("Lao to English", "Translate Lao into clear English"),
    "lao-font-designer": ("Lao Font Designer", "Choose, pair and review Lao typefaces"),
    "lao-graphic-designer": ("Lao Graphic Design", "Posters, packaging and brands with Lao text"),
    "lao-letter-professor": ("Lao Alphabet Teacher", "Lessons and quizzes for the Lao script"),
    "lao-ocr-reader": ("Lao OCR", "Read Lao text from images and scans"),
    "lao-typography-checker": ("Lao Typography Check", "Audit files for Lao typography problems"),
    "lao-unicode-font-engineer": ("Lao Unicode Fixer", "Fix boxes, broken marks and encodings"),
    "lao-voice-specialist": ("Lao Voice", "Voiceover, TTS, subtitles and register"),
    "lao-web-designer": ("Lao Web Design", "CSS, webfonts and layout for Lao pages"),
}

AGENT_FOOTER = ("\n\n## Use the plugin's core skill\n\n"
                "Before you produce or check Lao output, load the `lao-typography-design` skill from this plugin. "
                "It has the core rules, tested recipes for each file format, and `scripts/lao_check.py`. Run the "
                "checker on every file you produce, and report what you could not verify.\n")

KNOWLEDGE_ORDER = ["lao-alphabet.md", "lao-vowels.md", "lao-typography.md", "unicode.md", "recipes.md", "fonts.md"]
OPENAI_CATEGORIES = {"Productivity", "Creativity", "Developer Tools", "Business & Operations", "Data & Analytics",
                     "Communication", "Education & Research", "Security", "Finance", "Healthcare", "Travel",
                     "Entertainment", "Other"}


def fail(msg):
    sys.exit("build: " + msg)


# ------------------------------------------------------------------ skill checks
def frontmatter(skill_dir):
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        fail("%s has no SKILL.md" % skill_dir)
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        fail("%s/SKILL.md has no closed frontmatter" % skill_dir)
    fm = {}
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if sep and not line.startswith(" "):
            fm[k.strip()] = v.strip()
    if not m.group(2).strip():
        fail("%s/SKILL.md has an empty body" % skill_dir)
    return fm


def check_skill(skill_dir, expected_name=None):
    fm = frontmatter(skill_dir)
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        fail("%s: name %r must be lowercase letters, digits and hyphens" % (skill_dir, name))
    if expected_name and name != expected_name:
        fail("%s: name %r != folder %r" % (skill_dir, name, expected_name))
    if not desc or len(desc) > 1024:
        fail("%s: description missing or over 1024 characters (%d)" % (skill_dir, len(desc)))
    if len("%s:%s" % (PLUGIN_NAME, name)) > 64:
        fail("%s: plugin-name:skill-name is over 64 characters" % name)
    nested = [os.path.join(dp, f) for dp, _, fs in os.walk(skill_dir) for f in fs
              if f == "SKILL.md" and os.path.join(dp, f) != os.path.join(skill_dir, "SKILL.md")]
    if nested:
        fail("%s: extra SKILL.md files are rejected on upload: %s" % (skill_dir, nested))
    return name


# ------------------------------------------------------------------ OpenAI listing checks
def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        fail("%s is not a PNG" % path)
    return struct.unpack(">II", head[16:24])


def luminance(hex_colour):
    c = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def check_openai(manifest, plugin_dir):
    i = manifest["interface"]
    one_line = lambda s: "\n" not in s and "\r" not in s
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", manifest["name"]):
        fail("plugin name format")
    if not re.fullmatch(r"\d+\.\d+\.\d+([-+][0-9A-Za-z.-]+)?", manifest["version"]):
        fail("version must be semver")
    if not 0 < len(manifest["description"]) <= 1024:
        fail("description length")
    if not (0 < len(i["displayName"]) <= 30 and one_line(i["displayName"])):
        fail("interface.displayName must be one line, 30 characters or fewer (directory rule)")
    if not (0 < len(i["shortDescription"]) <= 30 and one_line(i["shortDescription"])):
        fail("interface.shortDescription must be one line, 30 characters or fewer (directory rule): %r" % i["shortDescription"])
    if not 0 < len(i["longDescription"]) <= 4000:
        fail("interface.longDescription length")
    if i["category"] not in OPENAI_CATEGORIES:
        fail("interface.category %r is not an allowed value" % i["category"])
    caps = i["capabilities"]
    if len(caps) > 20 or any(not c or len(c) > 120 for c in caps):
        fail("interface.capabilities")
    prompts = i["defaultPrompt"]
    norm = [" ".join(p.split()).casefold() for p in prompts]
    if len(prompts) > 3 or len(set(norm)) != len(norm) or any(not p or len(p) > 128 or not one_line(p) or "@" in p for p in prompts):
        fail("interface.defaultPrompt: at most 3 unique one-line prompts of 128 characters, no @mentions")
    for key, against in (("brandColor", "#FFFFFF"), ("brandColorDark", "#212121")):
        col = i.get(key)
        if col and (not re.fullmatch(r"#[0-9A-Fa-f]{6}", col) or contrast(col, against) < 2):
            fail("interface.%s %s needs 2:1 contrast against %s" % (key, col, against))
    for key in ("composerIcon", "logo"):
        rel = i[key]
        if not rel.startswith("./"):
            fail("interface.%s must start with ./" % key)
        w, h = png_size(os.path.join(plugin_dir, rel[2:]))
        if w != h or w < 48 or w > 4096:
            fail("interface.%s must be square, 48 to 4096 px (is %dx%d)" % (key, w, h))
    for key in ("websiteURL", "supportURL"):
        if key in i and not i[key].startswith("https://"):
            fail("interface.%s must be https" % key)


def check_agent_plugins(manifest):
    """Agent Plugins 1.0.0 plugin.schema.json: closed object, required $schema and name, name pattern, typed fields."""
    extra = set(manifest) - AGENT_PLUGINS_FIELDS
    if extra:
        fail("Agent Plugins manifest has fields outside the closed schema: %s" % sorted(extra))
    if manifest.get("$schema") != AGENT_PLUGINS_SCHEMA:
        fail("Agent Plugins $schema must be %s" % AGENT_PLUGINS_SCHEMA)
    if not re.fullmatch(r"(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", manifest["name"]) or len(manifest["name"]) > 64:
        fail("Agent Plugins name %r is invalid" % manifest["name"])
    for k in ("version", "description", "homepage", "repository", "license"):
        if k in manifest and not isinstance(manifest[k], str):
            fail("Agent Plugins %s must be a string" % k)
    if set(manifest.get("author", {})) - {"name", "email", "url"}:
        fail("Agent Plugins author may only have name, email, url")
    if not all(isinstance(k, str) for k in manifest.get("keywords", [])):
        fail("Agent Plugins keywords must be strings")


def check_archive(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        infos = z.infolist()
        total = sum(x.file_size for x in infos)
        if len(infos) > 5000 or os.path.getsize(zip_path) > 100 * 1024 * 1024 or total > 512 * 1024 * 1024:
            fail("%s exceeds upload limits" % zip_path)
        names = [x.filename for x in infos]
        if any(n.count("/") >= 20 or "\\" in n or ".." in n.split("/") for n in names):
            fail("%s has an invalid path" % zip_path)
        if not any(n in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".agent-plugin/plugin.json")
                   for n in names):
            fail("%s has no manifest at the top level" % zip_path)
        if not any(re.fullmatch(r"skills/[^/.][^/]*/SKILL\.md", n) for n in names):
            fail("%s has no skills/<name>/SKILL.md" % zip_path)
    return len(names), os.path.getsize(zip_path)


# ------------------------------------------------------------------ writers
def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def files_under(base, top_filter=None):
    for dp, dn, fn in os.walk(base):
        rel_dir = os.path.relpath(dp, base)
        if rel_dir == "." and top_filter is not None:
            dn[:] = sorted(d for d in dn if d in top_filter)
            fn = [f for f in fn if f in top_filter]
        else:
            dn[:] = sorted(d for d in dn if d != "__pycache__")
        for f in sorted(fn):
            if f.endswith(".pyc") or f == ".DS_Store":
                continue
            yield os.path.join(dp, f)


def write_zip(zip_path, base, prefix="", top_filter=None):
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files_under(base, top_filter):
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
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(parts))
    return path


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)       # a JSON string is a valid YAML scalar


def build_plugin(skills):
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "skills"))

    # skills, each with a ChatGPT/Codex display name
    for name, src in skills:
        dst = os.path.join(OUT, "skills", name)
        shutil.copytree(src, dst, ignore=IGNORE)
        if name not in SKILL_UI:
            fail("add %s to SKILL_UI" % name)
        disp, short = SKILL_UI[name]
        os.makedirs(os.path.join(dst, "agents"), exist_ok=True)
        with open(os.path.join(dst, "agents", "openai.yaml"), "w", encoding="utf-8", newline="\n") as f:
            f.write("interface:\n  display_name: %s\n  short_description: %s\npolicy:\n  allow_implicit_invocation: true\n"
                    % (yaml_str(disp), yaml_str(short)))

    # Claude subagents
    agents_src = os.path.join(ROOT, "Agents")
    os.makedirs(os.path.join(OUT, "agents"))
    for f in sorted(os.listdir(agents_src)):
        if f.endswith(".md"):
            text = open(os.path.join(agents_src, f), encoding="utf-8").read().rstrip("\n")
            if not re.match(r"^---\n(?:[^\n]*\n)*?name: [a-z0-9-]+\n(?:[^\n]*\n)*?---\n", text):
                fail("Agents/%s needs frontmatter with a name" % f)
            with open(os.path.join(OUT, "agents", f), "w", encoding="utf-8", newline="\n") as g:
                g.write(text + AGENT_FOOTER)

    # plugin-only files: icons, hook, README
    src = os.path.join(ROOT, "plugin-src")
    for d in ("assets", "scripts", "claude"):
        shutil.copytree(os.path.join(src, d), os.path.join(OUT, d), ignore=IGNORE)
    shutil.copy(os.path.join(src, "README.md"), os.path.join(OUT, "README.md"))
    shutil.copy(os.path.join(ROOT, "LICENSE"), os.path.join(OUT, "LICENSE"))

    # manifests
    write_json(os.path.join(OUT, ".claude-plugin", "plugin.json"), CLAUDE_MANIFEST)
    write_json(os.path.join(OUT, ".codex-plugin", "plugin.json"), OPENAI_MANIFEST)
    write_json(os.path.join(OUT, "plugin.json"), AGENT_MANIFEST)                       # Agent Plugins standard location
    write_json(os.path.join(OUT, ".agent-plugin", "plugin.json"), AGENT_MANIFEST)      # path OpenAI's uploader also accepts
    check_openai(OPENAI_MANIFEST, OUT)
    check_agent_plugins(AGENT_MANIFEST)

    # archives
    full = os.path.join(ROOT, "lao-typography-plugin.zip")
    write_zip(full, OUT)
    chat = os.path.join(ROOT, "lao-typography-chatgpt.zip")
    write_zip(chat, OUT, top_filter={".codex-plugin", "skills", "assets", "README.md", "LICENSE"})
    return [(os.path.basename(p),) + check_archive(p) for p in (full, chat)]


def build_marketplaces():
    rel = "./plugins/" + PLUGIN_NAME
    write_json(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), {
        "name": "deeoxide-lao",
        "owner": {"name": "Deeoxide", "url": "https://github.com/deeoxide"},
        "metadata": {"description": "Lao language, typography and font design plugins by Deeoxide."},
        "plugins": [{
            "name": PLUGIN_NAME,
            "source": rel,
            "displayName": "Lao Typography",
            "description": DESCRIPTION,
            "version": VERSION,
            "author": COMMON["author"],
            "homepage": COMMON["homepage"],
            "repository": REPO,
            "license": "MIT",
            "keywords": COMMON["keywords"],
            "category": "productivity",
        }],
    })
    write_json(os.path.join(ROOT, ".agents", "plugins", "marketplace.json"), {
        "name": "deeoxide-lao",
        "interface": {"displayName": "Deeoxide Lao"},
        "plugins": [{
            "name": PLUGIN_NAME,
            "source": {"source": "local", "path": rel},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        }],
    })


def main():
    skills = []
    for src in (os.path.join(ROOT, "lao_typography_design"), os.path.join(ROOT, "lao-font-studio")):
        skills.append((check_skill(src), src))
    pk = os.path.join(ROOT, "Package", "skills")
    for n in sorted(os.listdir(pk)):
        d = os.path.join(pk, n)
        if os.path.isdir(d):
            skills.append((check_skill(d, expected_name=n), d))

    for fname, (name, src) in (("lao_typography_design.skill", skills[0]), ("lao-font-studio.skill", skills[1])):
        write_zip(os.path.join(ROOT, fname), src, prefix=name)
    kb = build_knowledge()
    archives = build_plugin(skills)
    build_marketplaces()

    print("skills checked (%d): %s" % (len(skills), ", ".join(n for n, _ in skills)))
    print("plugin: %s (v%s)" % (os.path.relpath(OUT, ROOT), VERSION))
    for name, count, size in archives:
        print("  %-28s %4d files  %.1f MB" % (name, count, size / 1e6))
    print("also: lao_typography_design.skill, lao-font-studio.skill, %s, both marketplace files"
          % os.path.relpath(kb, ROOT))


if __name__ == "__main__":
    main()
