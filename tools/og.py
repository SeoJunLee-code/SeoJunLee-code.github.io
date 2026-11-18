# -*- coding: utf-8 -*-
"""Share image for og:image: a 1200x630 crop of the hero planet (assets/img/horizon.webp), no text rendered.
Deterministic. Run: python -I tools/og.py  -> assets/img/og.png (build.py adds the og:image tags when it exists)."""
import pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1200, 630
src = Image.open(ROOT / "assets/img/horizon.webp").convert("RGB")
scale = W / src.width                                   # full width, keep the crest of the planet in frame
im = src.resize((W, round(src.height * scale)), Image.LANCZOS)
top = max(0, min(im.height - H, round(im.height * 0.5) - H // 2))
im = im.crop((0, top, W, top + H))
im = im.quantize(colors=192, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
im.save(ROOT / "assets/img/og.png", optimize=True)
print("og.png", im.size, (ROOT / "assets/img/og.png").stat().st_size, "bytes")
