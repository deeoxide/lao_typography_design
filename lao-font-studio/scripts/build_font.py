#!/usr/bin/env python3
"""Build a Lao TTF from skeletons + a style recipe (lao-font-studio).

Usage:
  python3 build_font.py STYLE.json --out OUTDIR [--woff2]

STYLE.json keys (all optional except family):
  family        Font family name, e.g. "Deeoxide Lao Round"
  style_name    "Regular" | "Bold" | ... (default Regular)
  designer      Designer credit (default "Deeoxide with Claude")
  xheight       consonant body height in font units (default 520, UPM 1000)
  weight        stroke width in font units (default 80; 40 hairline .. 160 black)
  contrast      pen minor/major axis ratio, 1 = monoline (default 1.0)
  pen_angle     nib angle in degrees for contrast pens (default 30)
  cap           "round" | "flat" | "square" (default round)
  join          "round" | "mitre" | "bevel" (default round)
  width         horizontal scale of letter skeletons (default 1.0)
  slant         italic slant in degrees, positive leans right (default 0)
  loops         "ring" | "solid" | "none" (default ring)  -> looped vs loopless Lao
  loop_size     loop centreline radius in skeleton units (default 50)
  loop_weight   loop stroke width as a fraction of weight (default 0.85)
  mark_weight   stroke width of vowel/tone marks as a fraction of weight (default 0.8)
  mark_scale    size of vowel/tone marks (default 1.0)
  roughness     hand-drawn wobble amplitude in font units (default 0)
  seed          random seed for roughness (default 7)
  sidebearing   space each side of a letter in font units (default 45)
  tracking      extra advance added to every spacing glyph (default 0)
  glyphs        per-character overrides: {"ກ": {"w":..,"s":[..],"heads":[..],"sans":[..]}}
                (same format as lao_skeletons.py; replaces that glyph)
  extra_strokes per-character additions: {"ກ": ["M ...", ...]} drawn on top of the skeleton
  transform     per-character affine tweak: {"ກ": {"sx":1,"sy":1,"dx":0,"dy":0}}
"""
import argparse, json, math, os, random, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lao_skeletons as LS

from shapely.geometry import LineString, Point, Polygon, MultiPolygon, GeometryCollection
from shapely.ops import unary_union
from shapely import affinity
from shapely.geometry.polygon import orient
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString

DEFAULTS = dict(family="Lao Studio", style_name="Regular", designer="Deeoxide with Claude",
                xheight=520, weight=80, contrast=1.0, pen_angle=30, cap="round", join="round",
                width=1.0, slant=0, loops="ring", loop_size=50, loop_weight=0.85, mark_weight=0.8, mark_scale=1.0, roughness=0,
                seed=7, sidebearing=45, tracking=0, glyphs={}, extra_strokes={}, transform={})

CAP = {"round": 1, "flat": 2, "square": 3}
JOIN = {"round": 1, "mitre": 2, "bevel": 3}

# ------------------------------------------------------------------ path parsing
TOKEN = re.compile(r"[MLCQO]|-?\d+(?:\.\d+)?")

def parse(path, steps=24):
    """Return list of (points, closed) polylines in skeleton units."""
    toks = TOKEN.findall(path)
    out, cur, i = [], [], 0
    def num():
        nonlocal i
        v = float(toks[i]); i += 1; return v
    while i < len(toks):
        c = toks[i]; i += 1
        if c == "M":
            if len(cur) > 1: out.append((cur, False))
            cur = [(num(), num())]
        elif c == "L":
            cur.append((num(), num()))
        elif c == "C":
            p0 = cur[-1]; a = (num(), num()); b = (num(), num()); p = (num(), num())
            for k in range(1, steps + 1):
                t = k / steps; u = 1 - t
                cur.append((u*u*u*p0[0] + 3*u*u*t*a[0] + 3*u*t*t*b[0] + t*t*t*p[0],
                            u*u*u*p0[1] + 3*u*u*t*a[1] + 3*u*t*t*b[1] + t*t*t*p[1]))
        elif c == "Q":
            p0 = cur[-1]; a = (num(), num()); p = (num(), num())
            for k in range(1, steps + 1):
                t = k / steps; u = 1 - t
                cur.append((u*u*p0[0] + 2*u*t*a[0] + t*t*p[0], u*u*p0[1] + 2*u*t*a[1] + t*t*p[1]))
        elif c == "O":
            cx, cy, r = num(), num(), num()
            if len(cur) > 1: out.append((cur, False))
            cur = []
            out.append(([(cx + r*math.cos(2*math.pi*k/48), cy + r*math.sin(2*math.pi*k/48)) for k in range(49)], True))
        else:
            raise ValueError("bad token %r in %r" % (c, path))
    if len(cur) > 1: out.append((cur, False))
    return out

# ------------------------------------------------------------------ geometry
class Pen:
    def __init__(self, st, width_scale=1.0):
        w = st["weight"] * width_scale
        c = max(0.05, min(1.0, st["contrast"]))
        th = math.radians(st["pen_angle"])
        a, b = w / 2, w * c / 2
        # A = R(th) * diag(a, b)
        self.A = (math.cos(th)*a, -math.sin(th)*b, math.sin(th)*a, math.cos(th)*b)
        det = self.A[0]*self.A[3] - self.A[1]*self.A[2]
        self.Ai = (self.A[3]/det, -self.A[1]/det, -self.A[2]/det, self.A[0]/det)
        self.cap = CAP[st["cap"]]; self.join = JOIN[st["join"]]

    def stroke(self, pts, closed=False):
        if len(pts) < 2: return None
        geom = LineString(pts)
        a, b, c, d = self.Ai
        g2 = affinity.affine_transform(geom, [a, b, c, d, 0, 0])
        g2 = g2.buffer(1.0, quad_segs=12, cap_style=self.cap if not closed else 1,
                       join_style=self.join, mitre_limit=3.0)
        a, b, c, d = self.A
        return affinity.affine_transform(g2, [a, b, c, d, 0, 0])

def wobble(pts, amp, rnd):
    if amp <= 0: return pts
    ph = [rnd.uniform(0, 6.28) for _ in range(4)]
    fr = [rnd.uniform(0.004, 0.012) for _ in range(4)]
    out, s = [], 0.0
    for i, (x, y) in enumerate(pts):
        if i: s += math.hypot(x - pts[i-1][0], y - pts[i-1][1])
        out.append((x + amp*math.sin(fr[0]*s + ph[0]) * 0.7 + amp*0.3*math.sin(fr[2]*s*2.3 + ph[2]),
                    y + amp*math.sin(fr[1]*s + ph[1]) * 0.7 + amp*0.3*math.sin(fr[3]*s*1.9 + ph[3])))
    return out

def to_polys(geom):
    if geom is None or geom.is_empty: return []
    if isinstance(geom, Polygon): return [geom]
    if isinstance(geom, (MultiPolygon, GeometryCollection)):
        return [p for gg in geom.geoms for p in to_polys(gg)]
    return []

# ------------------------------------------------------------------ main build
def build(st, outdir, woff2=False):
    X, W = st["xheight"], st["weight"]
    ky = (X - W) / 500.0
    kx = ky * st["width"]
    rnd = random.Random(st["seed"])
    pen = Pen(st)
    mark_pen = Pen(st, st["mark_weight"])
    km = X / 500.0 * st["mark_scale"]
    loop_pen = Pen(st, st["loop_weight"])
    looped = st["loops"] in ("ring", "solid")
    slant = math.tan(math.radians(st["slant"]))
    sb = st["sidebearing"]

    glyph_defs = dict(LS.S)
    for ch, gd in st["glyphs"].items():
        base = dict(w=400, s=[], heads=[], sans=[], tall=False, kind=glyph_defs.get(ch, {}).get("kind", "base"))
        base.update(gd); glyph_defs[ch] = base

    def mapper(kind):
        if kind.startswith("mark"):
            return lambda x, y: (x*km*st["width"], y*km)
        return lambda x, y: (W/2 + x*kx, W/2 + y*ky)

    def draw(ch, gd):
        m = mapper(gd["kind"])
        tf = st["transform"].get(ch, {})
        def M(x, y):
            x, y = m(x, y)
            return (x*tf.get("sx", 1) + tf.get("dx", 0), y*tf.get("sy", 1) + tf.get("dy", 0))
        shapes = []
        paths = list(gd["s"]) + list(st["extra_strokes"].get(ch, []))
        if not looped: paths += gd.get("sans", [])
        for p in paths:
            for pts, closed in parse(p):
                pts = wobble([M(*q) for q in pts], st["roughness"], rnd)
                shapes.append((mark_pen if gd["kind"].startswith("mark") else pen).stroke(pts, closed))
        if looped:
            # keep the loop's counter open: radius at least ~0.9 x the loop stroke width
            R = max(st["loop_size"] * ky, 1.2 * W * st["loop_weight"])
            for (hx, hy, dx, dy) in gd.get("heads", []):
                tx, ty = M(hx, hy)
                n = math.hypot(dx, dy) or 1
                if st["loops"] == "solid":
                    rad = 0.5*W + 0.4*st["loop_size"]*ky
                    off = rad - 0.3*W
                    shapes.append(Point(tx + off*dx/n, ty + off*dy/n).buffer(rad, quad_segs=16))
                else:
                    cx, cy = tx + R*dx/n, ty + R*dy/n
                    ring = [(cx + R*math.cos(2*math.pi*k/48), cy + R*math.sin(2*math.pi*k/48)) for k in range(49)]
                    shapes.append(loop_pen.stroke(wobble(ring, st["roughness"]*0.5, rnd), True))
        geom = unary_union([s for s in shapes if s is not None])
        if slant:
            geom = affinity.affine_transform(geom, [1, slant, 0, 1, -slant*X/2 if not gd["kind"].startswith("mark") else 0, 0])
        return geom

    # typical consonant advance, used to park marks over the previous letter
    ref = draw("ກ", glyph_defs["ກ"]); rb = ref.bounds
    avg_adv = (rb[2] - rb[0]) + 2*sb
    mark_dx = -avg_adv/2

    glyphs, order, cmap, metrics, anchors = {}, [".notdef"], {}, {}, {}
    def gname(ch):
        return "space" if ch == " " else "uni%04X" % ord(ch)

    def emit(name, polys, adv, lsb_shift):
        pen_ = TTGlyphPen(None)
        for poly in polys:
            poly = orient(poly.simplify(0.6, preserve_topology=True), sign=-1.0)
            for ring in [poly.exterior] + list(poly.interiors):
                pts = [(round(x + lsb_shift), round(y)) for x, y in ring.coords[:-1]]
                clean = [p for i, p in enumerate(pts) if p != pts[i-1]]
                if len(clean) < 3: continue
                pen_.moveTo(clean[0])
                for p in clean[1:]: pen_.lineTo(p)
                pen_.closePath()
        g_ = pen_.glyph()
        glyphs[name] = g_
        g_.recalcBounds(None) if hasattr(g_, "recalcBounds") and False else None
        metrics[name] = (int(round(adv)), 0)

    # .notdef box
    p = TTGlyphPen(None)
    for ring in ([(60, 0), (60, 700), (440, 700), (440, 0)], [(110, 50), (390, 50), (390, 650), (110, 650)]):
        p.moveTo(ring[0]); [p.lineTo(q) for q in ring[1:]]; p.closePath()
    glyphs[".notdef"] = p.glyph(); metrics[".notdef"] = (500, 60)

    above_marks, tone_marks, below_marks, bases = [], [], [], []
    for ch, gd in glyph_defs.items():
        name = gname(ch); order.append(name); cmap[ord(ch)] = name
        if gd["kind"] == "space":
            glyphs[name] = TTGlyphPen(None).glyph()
            metrics[name] = (int(gd["w"]*kx + st["tracking"]), 0); continue
        geom = draw(ch, gd); polys = to_polys(geom)
        if gd["kind"].startswith("mark"):
            emit(name, polys, 0, mark_dx)
            mb = geom.bounds
            anchors[name] = dict(kind=gd["kind"], at=(round(mark_dx), 0), top=(round(mark_dx), round(mb[3] + 0.05*X)))
            {"mark_above": above_marks, "mark_tone": tone_marks, "mark_below": below_marks}[gd["kind"]].append(name)
        else:
            b = geom.bounds
            shift = sb - b[0]
            adv = (b[2] - b[0]) + 2*sb + st["tracking"]
            emit(name, polys, adv, shift)
            x0, x1 = sb, sb + (b[2] - b[0])
            topx = x0 + (0.36 if gd.get("tall") else 0.55) * (x1 - x0)
            desc = b[1] < -0.05*X
            botx = x0 + (0.32 if desc else 0.5) * (x1 - x0)
            anchors[name] = dict(kind="base", top=(round(topx), round(X + 0.04*X)),
                                 bottom=(round(botx), round(min(0, b[1]) - 0.02*X) if desc else 0))
            bases.append(name)

    # ຳ = ໍ parked over previous letter + າ
    for ch, (mk, sp) in LS.COMPOSITES.items():
        name = gname(ch); order.append(name); cmap[ord(ch)] = name
        sp_geom = draw(sp, glyph_defs[sp]); b = sp_geom.bounds
        mk_geom = draw(mk, glyph_defs[mk])
        mk_geom = affinity.translate(mk_geom, mark_dx + sb - b[0] + (b[2]-b[0])*0.0, X + 0.04*X)
        sp_geom = affinity.translate(sp_geom, sb - b[0], 0)
        emit(name, to_polys(unary_union([mk_geom, sp_geom])), (b[2]-b[0]) + 2*sb + st["tracking"], 0)
        bases.append(name)
        anchors[name] = dict(kind="base", top=(round(sb), round(X*1.04)), bottom=(round(sb), 0))

    # ------------------------------------------------------------------ assemble font
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    glyf = fb.font["glyf"]
    hm = {}
    for n in order:
        gl = glyf[n]; gl.recalcBounds(glyf)
        hm[n] = (metrics[n][0], getattr(gl, "xMin", 0) if gl.numberOfContours else 0)
    fb.setupHorizontalMetrics(hm)
    ymax = max(getattr(glyf[n], "yMax", 0) for n in order)
    ymin = min(getattr(glyf[n], "yMin", 0) for n in order)
    asc, desc = max(ymax + 40, int(X*1.95)), min(ymin - 40, -int(X*0.75))
    fb.setupHorizontalHeader(ascent=asc, descent=desc, lineGap=0)
    family = st["family"]; sty = st["style_name"]
    ps = re.sub(r"[^A-Za-z0-9-]", "", family.replace(" ", "")) + "-" + re.sub(r"[^A-Za-z0-9]", "", sty)
    fb.setupNameTable(dict(familyName=family, styleName=sty, uniqueFontIdentifier=ps + "-1.0",
                           fullName=f"{family} {sty}", psName=ps, version="Version 1.000",
                           designer=st["designer"], manufacturer=st["designer"],
                           description="Lao typeface generated with the lao-font-studio skill"))
    bold = sty.lower() in ("bold", "black", "heavy")
    fb.setupOS2(sTypoAscender=asc, sTypoDescender=desc, sTypoLineGap=0, usWinAscent=asc, usWinDescent=-desc,
                sxHeight=X, sCapHeight=int(X*1.46), version=4, usWeightClass=700 if bold else 400, fsType=0,
                ulUnicodeRange3=(1 << (68 - 64)), achVendID="DEOX",
                fsSelection=(0x20 if bold else 0x40) | 0x80, ulCodePageRange1=1)
    fb.setupPost()
    fb.setupHead(unitsPerEm=1000)
    fb.font["head"].macStyle = 1 if bold else 0

    # ------------------------------------------------------------------ OpenType
    def A(p): return "<anchor %d %d>" % p
    fea = ["languagesystem DFLT dflt;", "languagesystem lao dflt;", ""]
    fea.append("@BASES = [%s];" % " ".join(bases))
    fea.append("@MARKS = [%s];" % " ".join(above_marks + tone_marks + below_marks))
    fea.append("table GDEF { GlyphClassDef @BASES, , @MARKS, ; } GDEF;")
    for n in above_marks + tone_marks:
        fea.append("markClass %s %s @TOP;" % (n, A(anchors[n]["at"])))
    for n in below_marks:
        fea.append("markClass %s %s @BOTTOM;" % (n, A(anchors[n]["at"])))
    for n in tone_marks:
        fea.append("markClass %s %s @TONE;" % (n, A(anchors[n]["at"])))
    fea.append("lookup mkTop { lookupflag 0;")
    for n in bases: fea.append("  pos base %s %s mark @TOP;" % (n, A(anchors[n]["top"])))
    fea.append("} mkTop;")
    fea.append("lookup mkBottom {")
    for n in bases: fea.append("  pos base %s %s mark @BOTTOM;" % (n, A(anchors[n]["bottom"])))
    fea.append("} mkBottom;")
    fea.append("lookup mkTone {")
    for n in above_marks: fea.append("  pos mark %s %s mark @TONE;" % (n, A(anchors[n]["top"])))
    fea.append("} mkTone;")
    fea.append("feature mark { script lao; lookup mkTop; lookup mkBottom; } mark;")
    fea.append("feature mkmk { script lao; lookup mkTone; } mkmk;")
    fea_text = "\n".join(fea)
    addOpenTypeFeaturesFromString(fb.font, fea_text)

    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, ps + ".ttf")
    fb.font.save(out)
    with open(os.path.join(outdir, ps + ".fea"), "w") as f: f.write(fea_text)
    res = [out]
    if woff2:
        from fontTools.ttLib import TTFont
        t = TTFont(out); t.flavor = "woff2"; o2 = out[:-4] + ".woff2"; t.save(o2); res.append(o2)
    return res

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("style"); ap.add_argument("--out", default="out"); ap.add_argument("--woff2", action="store_true")
    a = ap.parse_args()
    st = dict(DEFAULTS); st.update(json.load(open(a.style, encoding="utf-8")))
    for p in build(st, a.out, a.woff2): print(p)
