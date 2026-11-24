#!/usr/bin/env python3
"""og.png 1200x630 — Salty Jax Seafood Co. — "butter & brine" poster.
Navy ink, clam-shell cream, butter-gold bun rules, bayou red buoy. Shop identity only."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

INK = (11, 37, 54); INK2 = (18, 50, 72); CREAM = (246, 241, 229); BUTTER = (224, 170, 62)
BAY = (178, 58, 47); SAND = (150, 166, 178); TEAL = (23, 97, 91)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except Exception: pass
    return ImageFont.load_default()

serif = lambda s: font(["Iowan Old Style.ttc", "Palatino.ttc", "Georgia.ttf", "Times New Roman.ttf"], s)
sans = lambda s: font(["Futura.ttc", "HelveticaNeue.ttc", "HelveticaNeue.ttc", "Arial.ttf"], s)

img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)

# subtle vertical band (ink2) lower third — like a horizon of brine
d.rectangle([0, 470, W, H], fill=INK2)
# butter rules top and bottom edges
d.rectangle([0, 0, W, 6], fill=BUTTER)
d.rectangle([0, H-6, W, H], fill=BUTTER)

def center(text, f, y, fill, tracking=0):
    if tracking:
        widths = [d.textbbox((0,0), ch, font=f)[2]-d.textbbox((0,0), ch, font=f)[0] for ch in text]
        tw = sum(widths) + tracking*(len(text)-1)
        x = (W-tw)/2
        for ch,w in zip(text,widths):
            bb = d.textbbox((0,0), ch, font=f)
            d.text((x - bb[0], y), ch, font=f, fill=fill)
            x += w + tracking
        return tw
    bb = d.textbbox((0,0), text, font=f)
    d.text(((W-(bb[2]-bb[0]))/2 - bb[0], y), text, font=f, fill=fill)
    return bb[2]-bb[0]

# kicker
center("OCEAN SPRINGS  ·  MISSISSIPPI GULF COAST", sans(24), 52, BUTTER, tracking=6)

# brand
center("SALTY JAX", serif(118), 108, CREAM)
center("S E A F O O D   C O .", sans(34), 250, SAND, tracking=8)

# double bun rule under brand
d.rectangle([W/2-140, 320, W/2+140, 323], fill=BUTTER)
d.rectangle([W/2-140, 329, W/2+140, 332], fill=BUTTER)

# line
center("New England-style lobster rolls.", serif(48), 352, CREAM)
center("Gulf Coast heart.", serif(48), 412, BUTTER)

# buoy + awards strip (on the brine band)
bx, by = 130, 512
d.ellipse([bx-26, by-26, bx+26, by+26], outline=BUTTER, width=9)
d.ellipse([bx-9, by-9, bx+9, by+9], fill=BAY)
center("Best Food Truck 2024 + 2025 · WXXV VCA's   —   Sun Herald Best of Coastal Mississippi 2025", sans(23), 494, CREAM)
center("Lobster Bisque  ·  Clam Chowder  ·  Bang Bang Tacos  ·  Queso Fries", sans(23), 530, TEAL if False else (122, 179, 170))
center("Now serving at The Shoppes at Washington Avenue — 6835 Washington Ave, Ocean Springs, MS", sans(21), 572, SAND)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
