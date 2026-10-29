#!/usr/bin/env python3
"""Redesign an existing Lao font (one of the provided fonts) from a recipe (lao-font-studio).

Unlike build_font.py (which draws new letters from skeletons), this takes the real
outlines of a base font and transforms them, keeping its character set, ligatures
(GSUB) and mark positioning (GPOS, anchors adjusted to the new shapes).

Usage:
  python3 derive_font.py RECIPE.json --out OUTDIR [--woff2]

RECIPE.json keys:
  base        path to the base font, or a bare file name looked up in assets/reference-fonts/
  family      new family name (required); style_name (default "Regular")
  designer    credit (default "Deeoxide with Claude")
  wght, wdth  for variable bases (Noto Sans Lao, Noto Serif Lao): pick the instance first.
              wght 100-900 (default 400), wdth 62.5-100 (default 100). Then the effects below apply.
  weight      make strokes heavier (+) or lighter (-), in units per 1000 em (e.g. +25, -10)
  width       horizontal scale of letters and spacing (default 1.0)
  slant       slant in degrees, positive leans right (default 0)
  round       round off corners, radius per 1000 em (default 0)
  outline     hollow outline letters: outline stroke width per 1000 em (default 0 = off)
  inline      white line inside the strokes: {"inset": 18, "line": 8} per 1000 em
  shadow      extruded drop shadow: {"dx": 30, "dy": -30, "gap": 10} per 1000 em
  roughness   hand-cut wobble amplitude per 1000 em (default 0); seed (default 7)
  tracking    extra spacing per 1000 em added to every spacing glyph (default 0)
  only        optional string of characters to transform; other glyphs are copied as-is
"""
import argparse, copy, json, math, os, random, re, sys

from shapely.geometry import Polygon, MultiPolygon, GeometryCollection, LineString, Point
from shapely.ops import unary_union, polygonize
from shapely import affinity
from shapely.geometry.polygon import orient
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.fontBuilder import FontBuilder

HERE = os.path.dirname(os.path.abspath(__file__))
REF_DIR = os.path.join(HERE, "..", "assets", "reference-fonts")

DEFAULTS = dict(style_name="Regular", designer="Deeoxide with Claude", weight=0, width=1.0, slant=0,
                round=0, outline=0, inline=None, shadow=None, roughness=0, seed=7, tracking=0, only=None)

# ------------------------------------------------------------------ outline extraction
class FlatPen(BasePen):
    """Flattens a glyph (TrueType or CFF, components decomposed) into closed polylines."""
    def __init__(self, glyphSet, steps=12):
        super().__init__(glyphSet); self.contours = []; self.cur = []; self.steps = steps
    def _moveTo(self, p): self.cur = [p]
    def _lineTo(self, p): self.cur.append(p)
    def _curveToOne(self, a, b, c):
        p0 = self.cur[-1]; n = self.steps
        for i in range(1, n + 1):
            t = i / n; u = 1 - t
            self.cur.append((u**3*p0[0] + 3*u*u*t*a[0] + 3*u*t*t*b[0] + t**3*c[0],
                             u**3*p0[1] + 3*u*u*t*a[1] + 3*u*t*t*b[1] + t**3*c[1]))
    def _qCurveToOne(self, a, b):
        p0 = self.cur[-1]; n = self.steps
        for i in range(1, n + 1):
            t = i / n; u = 1 - t
            self.cur.append((u*u*p0[0] + 2*u*t*a[0] + t*t*b[0], u*u*p0[1] + 2*u*t*a[1] + t*t*b[1]))
    def _closePath(self):
        if len(self.cur) > 2: self.contours.append(self.cur)
        self.cur = []
    _endPath = _closePath

def signed_area(pts):
    return 0.5 * sum(pts[i][0]*pts[i-1][1] - pts[i-1][0]*pts[i][1] for i in range(len(pts)))

def contours_to_geom(contours):
    """Exact non-zero winding fill of the contours as a shapely geometry."""
    rings = [c for c in contours if abs(signed_area(c)) > 1e-6]
    if not rings: return Polygon()
    polys = [(Polygon(c).buffer(0), 1 if signed_area(c) > 0 else -1) for c in rings]
    if len(rings) == 1: return polys[0][0]
    lines = unary_union([LineString(list(c) + [c[0]]) for c in rings])
    keep = []
    for face in polygonize(lines):
        pt = face.representative_point()
        wn = sum(s for p, s in polys if p.contains(pt))
        if wn != 0: keep.append(face)
    return unary_union(keep).buffer(0) if keep else Polygon()

def to_polys(g):
    if g is None or g.is_empty: return []
    if isinstance(g, Polygon): return [g]
    if isinstance(g, (MultiPolygon, GeometryCollection)): return [p for x in g.geoms for p in to_polys(x)]
    return []

def wobble_geom(g, amp, rnd):
    if amp <= 0 or g.is_empty: return g
    ph = [rnd.uniform(0, 6.28) for _ in range(4)]; fr = [rnd.uniform(0.01, 0.03) for _ in range(2)]
    def shake(coords):
        out = []
        for x, y in coords:
            out.append((x + amp*math.sin(fr[0]*y + ph[0] + 0.7*math.sin(fr[1]*x + ph[2])),
                        y + amp*math.sin(fr[1]*x + ph[1] + 0.7*math.sin(fr[0]*y + ph[3]))))
        return out
    res = []
    for p in to_polys(g.segmentize(amp * 2 + 4)):
        res.append(Polygon(shake(p.exterior.coords), [shake(r.coords) for r in p.interiors]).buffer(0))
    return unary_union(res)

# ------------------------------------------------------------------ GPOS adjustment
def adjust_gpos(table, fx, fy_shear, dx):
    """Apply x' = x*fx + y*fy_shear + dx to every anchor; scale x values in value records."""
    seen = set()
    def visit(o):
        if o is None or id(o) in seen: return
        seen.add(id(o))
        name = type(o).__name__
        if name == "Anchor":
            x, y = o.XCoordinate, o.YCoordinate
            o.XCoordinate = int(round(x*fx + y*fy_shear + dx)); return
        if name == "ValueRecord":
            for k in ("XPlacement", "XAdvance"):
                if hasattr(o, k): setattr(o, k, int(round(getattr(o, k)*fx)))
            return
        if isinstance(o, (list, tuple)):
            for x in o: visit(x)
            return
        if hasattr(o, "__dict__"):
            for v in vars(o).values():
                if isinstance(v, (list, tuple)) or hasattr(v, "__dict__"): visit(v)
    visit(table)

# ------------------------------------------------------------------ main
def derive(st, outdir, woff2=False):
    base = st["base"]
    if not os.path.exists(base): base = os.path.join(REF_DIR, base)
    src = TTFont(base)
    if "fvar" in src:
        from fontTools.varLib import instancer
        axes = {a.axisTag: a.defaultValue for a in src["fvar"].axes}
        for tag in ("wght", "wdth"):
            if tag in st: axes[tag] = st[tag]
        src = instancer.instantiateVariableFont(src, axes, inplace=False, updateFontNames=False)
    upm = src["head"].unitsPerEm; k = upm / 1000.0
    gs = src.getGlyphSet(); order = src.getGlyphOrder()
    cmap = src.getBestCmap()
    only = None
    if st.get("only"):
        only = {cmap[ord(c)] for c in st["only"] if ord(c) in cmap}
    d = st["weight"] * k / 2                      # buffer distance (half of the weight change)
    sx = st["width"]; sh = math.tan(math.radians(st["slant"]))
    rnd = random.Random(st["seed"])
    track = st["tracking"] * k
    shift = max(d, 0)                             # keep left sidebearing when emboldening

    glyphs, hm = {}, {}
    for gn in order:
        adv = src["hmtx"][gn][0]
        pen = FlatPen(gs); gs[gn].draw(pen)
        geom = contours_to_geom(pen.contours)
        if not geom.is_empty and (only is None or gn in only):
            if d: geom = geom.buffer(d, quad_segs=8, join_style=1) if d > 0 else geom.buffer(d, quad_segs=8)
            if st["round"]:
                r = st["round"] * k; geom = geom.buffer(-r, quad_segs=8).buffer(r, quad_segs=8)
            if st["inline"]:
                inset = st["inline"].get("inset", 18) * k; lw = st["inline"].get("line", 8) * k
                inner = geom.buffer(-inset)
                if not inner.is_empty: geom = geom.difference(inner.boundary.buffer(lw/2))
            if st["outline"]:
                o = st["outline"] * k / 2
                geom = geom.buffer(o).difference(geom.buffer(-o))
            if st["shadow"]:
                sdx = st["shadow"].get("dx", 30) * k; sdy = st["shadow"].get("dy", -30) * k
                gap = st["shadow"].get("gap", 10) * k
                n = max(1, int(math.hypot(sdx, sdy) / (6*k)))
                ext = unary_union([affinity.translate(geom, sdx*i/n, sdy*i/n) for i in range(1, n+1)])
                geom = unary_union([ext.difference(geom.buffer(gap)), geom])
            geom = wobble_geom(geom, st["roughness"] * k, rnd)
        if not geom.is_empty:
            geom = affinity.affine_transform(geom, [sx, sh, 0, 1, shift, 0])
        tp = TTGlyphPen(None)
        for poly in to_polys(geom):
            poly = orient(poly.simplify(0.4*k, preserve_topology=True), sign=-1.0)
            for ring in [poly.exterior] + list(poly.interiors):
                pts = [(round(x), round(y)) for x, y in ring.coords[:-1]]
                pts = [p for i, p in enumerate(pts) if p != pts[i-1]]
                if len(pts) < 3: continue
                tp.moveTo(pts[0]); [tp.lineTo(p) for p in pts[1:]]; tp.closePath()
        glyphs[gn] = tp.glyph()
        new_adv = int(round(adv*sx + (2*shift + track if adv > 0 else 0)))
        hm[gn] = new_adv

    fb = FontBuilder(upm, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    glyf = fb.font["glyf"]
    mets = {}
    for gn in order:
        gl = glyf[gn]; gl.recalcBounds(glyf)
        mets[gn] = (hm[gn], gl.xMin if gl.numberOfContours else 0)
    fb.setupHorizontalMetrics(mets)
    ymax = max((glyf[g].yMax for g in order if glyf[g].numberOfContours), default=upm)
    ymin = min((glyf[g].yMin for g in order if glyf[g].numberOfContours), default=0)
    sh_ = src["hhea"]
    asc = max(sh_.ascent, ymax); desc = min(sh_.descent, ymin)
    fb.setupHorizontalHeader(ascent=asc, descent=desc, lineGap=sh_.lineGap)

    family = st["family"]; sty = st["style_name"]
    ps = re.sub(r"[^A-Za-z0-9-]", "", family.replace(" ", "")) + "-" + re.sub(r"[^A-Za-z0-9]", "", sty)
    src_family = src["name"].getDebugName(1) or os.path.basename(base)
    src_copy = src["name"].getDebugName(0) or ""
    lic_text = src["name"].getDebugName(13); lic_url = src["name"].getDebugName(14)
    names = dict(copyright=(src_copy + " " if src_copy else "") +
                           f"Modified version of {src_family}.",
                           familyName=family, styleName=sty, uniqueFontIdentifier=ps + "-1.0",
                           fullName=f"{family} {sty}", psName=ps, version="Version 1.000",
                           designer=st["designer"], manufacturer=st["designer"],
                           description=f"Derived from {src_family} with the lao-font-studio skill")
    if lic_text: names["licenseDescription"] = lic_text   # keep the base font's licence text (e.g. SIL OFL)
    if lic_url: names["licenseInfoURL"] = lic_url
    fb.setupNameTable(names)
    os2 = copy.deepcopy(src["OS/2"])
    os2.usWinAscent = max(os2.usWinAscent, ymax); os2.usWinDescent = max(os2.usWinDescent, -ymin)
    if st["slant"]: os2.fsSelection = (os2.fsSelection | 0x01) & ~0x40
    fb.font["OS/2"] = os2
    fb.setupPost(keepGlyphNames=True, italicAngle=-st["slant"])
    fb.font["head"].macStyle = src["head"].macStyle | (2 if st["slant"] else 0)
    for tag in ("GDEF", "GSUB", "GPOS"):
        if tag in src: fb.font[tag] = copy.deepcopy(src[tag])
    if "GPOS" in fb.font:
        adjust_gpos(fb.font["GPOS"].table, sx, sh, shift)
    if "GDEF" in fb.font and getattr(fb.font["GDEF"].table, "LigCaretList", None):
        fb.font["GDEF"].table.LigCaretList = None

    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, ps + ".ttf"); fb.font.save(out)
    res = [out]
    if woff2:
        t = TTFont(out); t.flavor = "woff2"; o2 = out[:-4] + ".woff2"; t.save(o2); res.append(o2)
    return res

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("recipe"); ap.add_argument("--out", default="out"); ap.add_argument("--woff2", action="store_true")
    a = ap.parse_args()
    st = dict(DEFAULTS); st.update(json.load(open(a.recipe, encoding="utf-8")))
    for p in derive(st, a.out, a.woff2): print(p)
