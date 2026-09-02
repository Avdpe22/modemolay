#!/usr/bin/env python3
"""
Build the Missouri DeMolay lockups as vector SVG, in the DeMolay International style.

Mirrors the structure of the official DI mark: gold stars flanking a red shield, the
stylised "DeMOLAY" wordmark (navy fill, white gap, gold outline), and the jurisdiction
name in red -- MISSOURI in place of INTERNATIONAL.

Two lockups, because one ratio cannot serve both sizes:
  * stacked    (~3.1:1) full star row, for the footer and anywhere shown large
  * horizontal (~3.6:1) shield only, MISSOURI set larger so it stays legible in the
                        nav bar at ~46px tall

Letterforms are converted to SVG paths, so the marks never depend on a webfont
loading. Barlow (SIL OFL 1.1) is already the site's display face.

Usage: build_logo.py <Barlow-Bold.ttf> [outdir]
"""
import math
import os
import sys

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else "."

NAVY, GOLD, RED = "#1D3A63", "#FFC629", "#EE2737"
OUTLINE_R, GAP_R = 0.168, 0.090   # outline weights as a fraction of cap height
E_RATIO = 0.60                    # small "e" x-height as a fraction of cap height

font = TTFont(FONT)
upem = font["head"].unitsPerEm
CAP_R = font["OS/2"].sCapHeight / upem
XH_R = font["OS/2"].sxHeight / upem
glyphset = font.getGlyphSet()
cmap = font.getBestCmap()
hmtx = font["hmtx"]


def advance(text, size, tracking=0.0):
    if not text:
        return 0.0
    return sum(hmtx[cmap[ord(c)]][0] * size / upem + tracking for c in text) - tracking


def _round(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def draw(text, size, x, baseline, tracking=0.0):
    """Return (path data list, advance). Font space is Y-up, SVG is Y-down."""
    out, pen = [], x
    for ch in text:
        gn = cmap[ord(ch)]
        s = size / upem
        spen = SVGPathPen(glyphset, ntos=_round)
        glyphset[gn].draw(TransformPen(spen, Transform(s, 0, 0, -s, pen, baseline)))
        if spen.getCommands().strip():
            out.append(spen.getCommands())
        pen += hmtx[gn][0] * s + tracking
    return out, pen - x - (tracking if text else 0.0)


def solve_tracking(runs, target):
    natural = sum(advance(t, s) for t, s in runs)
    n = sum(len(t) for t, _ in runs)
    return (target - natural) / max(n - 1, 1)


def wordmark(cap_h, x, baseline, ink_w):
    """The DeMOLAY wordmark laid out to an exact ink width (outline included)."""
    cap_size, e_size = cap_h / CAP_R, (E_RATIO * cap_h) / XH_R
    runs = [("D", cap_size), ("e", e_size), ("MOLAY", cap_size)]
    gold_sw = cap_h * OUTLINE_R
    target = ink_w - gold_sw
    track = solve_tracking(runs, target)
    paths, cur = [], x + gold_sw / 2
    for text, size in runs:
        got, adv = draw(text, size, cur, baseline, track)
        paths.extend(got)
        cur += adv + track
    return paths, gold_sw, cap_h * GAP_R


def star(cx, cy, r, inner=0.40):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * inner
        pts.append(f"{cx + rad*math.cos(a):.2f},{cy + rad*math.sin(a):.2f}")
    return "M" + "L".join(pts) + "Z"


def shield(cx, top, w, h):
    hw = w / 2
    return (f"M{cx-hw:.2f},{top:.2f} L{cx+hw:.2f},{top:.2f} L{cx+hw:.2f},{top+h*0.46:.2f} "
            f"C{cx+hw:.2f},{top+h*0.78:.2f} {cx+hw*0.55:.2f},{top+h*0.94:.2f} {cx:.2f},{top+h:.2f} "
            f"C{cx-hw*0.55:.2f},{top+h*0.94:.2f} {cx-hw:.2f},{top+h*0.78:.2f} {cx-hw:.2f},{top+h*0.46:.2f} Z")


def emit_wordmark(paths, gold_sw, white_sw, mono):
    """Glyphs are defined once and referenced per outline layer, so the three
    stacked strokes cost three <use> tags rather than three copies of the paths."""
    p = ['<defs><g id="wm">']
    p += [f'<path d="{d}"/>' for d in paths]
    p.append('</g></defs>')
    layers = ([("#FFFFFF", 0)] if mono
              else [(GOLD, gold_sw), ("#FFFFFF", white_sw), (NAVY, 0)])
    for colour, sw in layers:
        if sw:
            p.append(f'<use href="#wm" fill="none" stroke="{colour}" '
                     f'stroke-width="{sw:.2f}" stroke-linejoin="round" stroke-linecap="round"/>')
        else:
            p.append(f'<use href="#wm" fill="{colour}"/>')
    return p


def head(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" '
            f'role="img" aria-label="{title}">')


# ---------------------------------------------------------------- stacked
def build_stacked(mono=False):
    W, H, CX = 1000.0, 322.0, 500.0
    SH_W, SH_H, SH_TOP = 54.0, 66.0, 2.0
    STAR_R, STAR_CY, STAR_GAP = 17.0, 30.0, 52.0
    CAP_H, BASE_Y, INK_W = 155.0, 246.0, 968.0
    SUB_CAP, SUB_BASE, SUB_W = 36.0, 316.0, 452.0

    wm, gold_sw, white_sw = wordmark(CAP_H, (W - INK_W) / 2, BASE_Y, INK_W)
    sub_size = SUB_CAP / CAP_R
    sub, _ = draw("MISSOURI", sub_size, (W - SUB_W) / 2, SUB_BASE,
                  solve_tracking([("MISSOURI", sub_size)], SUB_W))
    star_xs = [CX - SH_W / 2 - 20 - STAR_GAP * i for i in range(3)] + \
              [CX + SH_W / 2 + 20 + STAR_GAP * i for i in range(3)]

    p = [head(W, H, "Missouri DeMolay")]
    p.append(f'<g fill="{"#FFFFFF" if mono else GOLD}">')
    p += [f'<path d="{star(sx, STAR_CY, STAR_R)}"/>' for sx in star_xs]
    p.append('</g>')
    if mono:
        p.append(f'<path d="{shield(CX, SH_TOP, SH_W, SH_H)}" fill="none" '
                 f'stroke="#FFFFFF" stroke-width="7"/>')
        p.append(f'<path d="{star(CX, STAR_CY + 3, 12)}" fill="#FFFFFF"/>')
    else:
        p.append(f'<path d="{shield(CX, SH_TOP, SH_W, SH_H)}" fill="{RED}"/>')
        p.append(f'<path d="{star(CX, STAR_CY + 1, 15)}" fill="#FFFFFF"/>')
    p += emit_wordmark(wm, gold_sw, white_sw, mono)
    p.append(f'<g fill="{"#FFFFFF" if mono else RED}">')
    p += [f'<path d="{d}"/>' for d in sub]
    p.append('</g></svg>')
    return "\n".join(p)


# ------------------------------------------------------------- horizontal
def build_horizontal(mono=False):
    """Shield at left, wordmark over MISSOURI. Built to stay legible small."""
    W, H = 392.0, 100.0
    SH_CX, SH_TOP, SH_W, SH_H = 30.0, 17.0, 50.0, 66.0
    TEXT_X, TEXT_W = 74.0, 306.0
    CAP_H, BASE_Y = 44.0, 60.0
    SUB_CAP, SUB_BASE = 17.0, 91.0

    wm, gold_sw, white_sw = wordmark(CAP_H, TEXT_X, BASE_Y, TEXT_W)
    sub_size = SUB_CAP / CAP_R
    sub, _ = draw("MISSOURI", sub_size, TEXT_X + gold_sw / 2, SUB_BASE,
                  solve_tracking([("MISSOURI", sub_size)], TEXT_W - gold_sw))

    p = [head(W, H, "Missouri DeMolay")]
    if mono:
        p.append(f'<path d="{shield(SH_CX, SH_TOP, SH_W, SH_H)}" fill="none" '
                 f'stroke="#FFFFFF" stroke-width="6"/>')
        p.append(f'<path d="{star(SH_CX, SH_TOP + 27, 12)}" fill="#FFFFFF"/>')
    else:
        p.append(f'<path d="{shield(SH_CX, SH_TOP, SH_W, SH_H)}" fill="{RED}"/>')
        p.append(f'<path d="{star(SH_CX, SH_TOP + 25, 15)}" fill="#FFFFFF"/>')
    p += emit_wordmark(wm, gold_sw, white_sw, mono)
    p.append(f'<g fill="{"#FFFFFF" if mono else RED}">')
    p += [f'<path d="{d}"/>' for d in sub]
    p.append('</g></svg>')
    return "\n".join(p)


for name, svg in (
    ("logo-stacked.svg", build_stacked()),
    ("logo-stacked-white.svg", build_stacked(mono=True)),
    ("logo-horizontal.svg", build_horizontal()),
    ("logo-horizontal-white.svg", build_horizontal(mono=True)),
):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)
    print(f"{name:30s} {len(svg):>6,} bytes")
