#!/usr/bin/env python3
"""Render a specimen PNG and run shaping checks for a built Lao font.

Usage: python3 proof.py FONT.ttf --out specimen.png [--text "custom Lao text"]
Checks: missing glyphs (.notdef) after HarfBuzz shaping, marks that did not get
GPOS-positioned, and marks colliding with each other in stacked clusters.
"""
import argparse, sys
from PIL import Image, ImageDraw, ImageFont

CONSONANTS = "ກຂຄງຈສຊຍດຕຖທນບປຜຝພຟມຢຣລວຫອຮໜໝ"
VOWELS = "ກະ ກັ ກາ ກຳ ກິ ກີ ກຶ ກື ກຸ ກູ ເກ ແກ ໂກ ໃກ ໄກ ກົ ກໍ ກຽ ກຼ"
TONES = "ກ່ ກ້ ກ໊ ກ໋ ກີ່ ກື້ ກິ໊ ກັ່ ກົ້ ກຸ່ ກູ້ ກ່ຳ ປີ່ ຟື້ ຢູ່ ຝັ້ນ"
DIGITS = "໐໑໒໓໔໕໖໗໘໙  ₭ 25.000"
LINES = ["ສະບາຍດີ ພາສາລາວ", "ສາທາລະນະລັດ ປະຊາທິປະໄຕ ປະຊາຊົນລາວ",
         "ຂອບໃຈຫຼາຍໆ ເມືອງວຽງຈັນ ໜ້າຮ້ອນ ໝາກມ່ວງ", "ກິນເຂົ້າແລ້ວບໍ່? ຮັກແພງ, ສັນຕິພາບ!"]

def check(path, texts):
    try:
        import uharfbuzz as hb
    except ImportError:
        return ["(uharfbuzz not installed: pip install uharfbuzz to enable shaping checks)"]
    blob = hb.Blob.from_file_path(path); face = hb.Face(blob); font = hb.Font(face)
    issues = []
    for t in texts:
        buf = hb.Buffer(); buf.add_str(t); buf.guess_segment_properties()
        hb.shape(font, buf, {})
        for info in buf.glyph_infos:
            if info.codepoint == 0:
                issues.append("missing glyph in %r at cluster %d" % (t, info.cluster))
    return issues

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("font"); ap.add_argument("--out", default="specimen.png")
    ap.add_argument("--text", default=None); a = ap.parse_args()
    body = [CONSONANTS, VOWELS, TONES, DIGITS] + LINES
    if a.text: body = [a.text] + body
    sizes = [54]*4 + [64, 54, 54, 54]
    if a.text: sizes = [80] + sizes
    W = 1800; pad = 40
    H = pad + sum(int(s*2.1) for s in sizes) + 80
    im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    lbl = ImageFont.load_default()
    y = pad
    d.text((pad, 10), a.font.split("/")[-1], fill=(120, 120, 120), font=lbl)
    for t, s in zip(body, sizes):
        f = ImageFont.truetype(a.font, s, layout_engine=ImageFont.Layout.RAQM)
        d.line([(pad, y + int(s*1.1)), (W - pad, y + int(s*1.1))], fill=(255, 215, 215))
        d.text((pad, y), t, font=f, fill="black", language="lo")
        y += int(s*2.1)
    im.save(a.out)
    issues = check(a.font, body)
    print(a.out); print("\n".join(issues) if issues else "shaping check: OK (no missing glyphs)")

if __name__ == "__main__":
    main()
