#!/usr/bin/env python3
"""
Turn the official Missouri DeMolay trademark PDF into web-ready SVGs.

    sudo apt-get install -y poppler-utils
    python3 assets/brand/pdf-to-svg.py assets/brand/trademark.pdf assets

Emits, from the one supplied colour artwork:
    logo-missouri-demolay.svg        full colour, exactly as supplied
    logo-missouri-demolay-white.svg  all-white, for dark backgrounds
    logo-missouri-demolay-navy.svg   single-colour navy

The white and navy variants are the SAME vector paths with the ink recoloured, which
is what the supplied one-colour versions are. Nothing is redrawn, rescaled or
restructured -- the trademark geometry is used exactly as delivered.

If official vector files for the white or navy versions exist, prefer those: run this
on each and keep only its full-colour output.
"""
import re
import subprocess
import sys
from pathlib import Path

NAVY = "#0A1A2F"  # exact ink from the official single-colour "Dark" export

src = Path(sys.argv[1])
out = Path(sys.argv[2] if len(sys.argv) > 2 else ".")
out.mkdir(parents=True, exist_ok=True)

raw = out / "_raw.svg"
subprocess.run(["pdftocairo", "-svg", str(src), str(raw)], check=True)
svg = raw.read_text(encoding="utf-8")
svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)

# a colour token actually used as ink, i.e. preceded by fill:/stroke:
INK = re.compile(r'((?:fill|stroke)\s*(?::|=")\s*)(#[0-9a-fA-F]{6}|rgb\([^)]*\))')


def to_hex(c):
    """'#aabbcc' / 'rgb(10%,20%,30%)' / 'rgb(1,2,3)' -> '#rrggbb'. None if unparsable."""
    c = c.strip()
    if c.startswith("#"):
        return c.lower()
    nums = re.findall(r"[\d.]+%?", c)
    if len(nums) < 3:
        return None
    vals = []
    for n in nums[:3]:
        v = float(n.rstrip("%"))
        vals.append(max(0, min(255, round(v * 255 / 100) if n.endswith("%") else round(v))))
    return "#%02x%02x%02x" % tuple(vals)


def is_white(c):
    h = to_hex(c)
    if not h:
        return False
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    return min(r, g, b) >= 250          # tolerate 254,255,255 rounding out of the PDF


def recolour(text, target):
    """Map every non-white ink to `target`. Whites, 'none' and gradients are untouched."""
    return INK.sub(lambda m: m.group(0) if is_white(m.group(2)) else m.group(1) + target, text)


print("colours found in the artwork:")
for c in sorted({m.group(2).lower() for m in INK.finditer(svg)}):
    print(f"   {c}  ->  {to_hex(c)}")

(out / "logo-missouri-demolay.svg").write_text(svg, encoding="utf-8")
(out / "logo-missouri-demolay-white.svg").write_text(recolour(svg, "#FFFFFF"), encoding="utf-8")
(out / "logo-missouri-demolay-navy.svg").write_text(recolour(svg, NAVY), encoding="utf-8")
raw.unlink()

for p in sorted(out.glob("logo-missouri-demolay*.svg")):
    print(f"{p.name:36s} {p.stat().st_size:>8,} bytes")

print("\nNow LOOK at the white variant before shipping it. Whether the thin gap between")
print("each letter and its outline is painted white or left transparent decides whether")
print("you get proper knockout letters on the dark footer or a solid silhouette.")
