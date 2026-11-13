#!/usr/bin/env python3
"""Build the 1200x630 Open Graph / social card for pointly.scottdavis.uk.

Usage:  python3 tools/make-og-image.py [output.png|output.jpg]
Needs:  Pillow, and the two variable TTFs in tools/fonts.
Fonts are the OFL-licensed Outfit and Plus Jakarta Sans faces the site uses.

The card committed at the repo root (og-image.png, 1734x907) was supplied by
Scott, not produced here. This script renders an alternative and deliberately
defaults to og-image-generated.png so a run cannot overwrite the real asset.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG_TOP = (4, 8, 15)
BG_BOT = (7, 16, 28)
GREEN = (52, 211, 153)
AMBER = (251, 191, 36)
WHITE = (255, 255, 255)
MUTED = (148, 163, 184)
SOFT = (203, 213, 225)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.environ.get("OG_FONT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts"))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "og-image-generated.png")
SHOT = next(
    (p for p in (os.path.join(HERE, "app-screenshot.jpg"), os.path.join(HERE, "v2", "app-screenshot.jpg"))
     if os.path.exists(p)),
    os.path.join(HERE, "app-screenshot.jpg"),
)


def font(name, size, weight=None):
    f = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def gradient():
    img = Image.new("RGB", (W, H), BG_TOP)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        d.line(
            [(0, y), (W, y)],
            fill=tuple(round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOT)),
        )
    return img


def glow(img, cx, cy, radius, colour, peak=70):
    """Soft radial glow, drawn additively on an L mask."""
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    steps = 90
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(peak * (1 - i / steps) ** 2)
        md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
    layer = Image.new("RGB", (W, H), colour)
    img.paste(Image.composite(layer, img, mask), (0, 0))


def rings(img):
    """Reticle rings behind the phone, clipped so they never cross the copy."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    cx, cy = 1010, 315
    ld.ellipse([cx - 300, cy - 300, cx + 300, cy + 300], outline=(148, 163, 184, 70), width=2)
    ld.ellipse([cx - 255, cy - 255, cx + 255, cy + 255], outline=AMBER + (110,), width=3)
    ld.ellipse([cx - 210, cy - 210, cx + 210, cy + 210], outline=GREEN + (200,), width=4)
    # keep the rings on the right-hand third of the card
    clip = Image.new("L", (W, H), 0)
    ImageDraw.Draw(clip).rectangle([815, 0, W, H], fill=255)
    layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", (W, H), 0), clip))
    img.alpha_composite(layer) if img.mode == "RGBA" else img.paste(
        Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0, 0)
    )


def phone(img, top=40, height=550):
    shot = Image.open(SHOT).convert("RGB")
    w = round(height * shot.width / shot.height)
    shot = shot.resize((w, height), Image.Resampling.LANCZOS)
    bezel = 8
    pw, ph = w + bezel * 2, height + bezel * 2
    px, py = 1180 - pw, top - bezel
    frame = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    fd = ImageDraw.Draw(frame)
    fd.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=34, fill=(2, 6, 23, 255))
    frame.paste(shot, (bezel, bezel))
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=34, fill=255)
    img.paste(frame, (px, py), mask)


def main():
    base = gradient().convert("RGBA")
    glow(base, 1010, 315, 420, (16, 90, 68), peak=95)
    glow(base, 120, 60, 380, (12, 40, 70), peak=60)
    rings(base)
    phone(base)
    img = base.convert("RGB")
    d = ImageDraw.Draw(img)

    # Brand row
    d.ellipse([76, 74, 118, 116], outline=GREEN, width=4)
    d.ellipse([88, 86, 106, 104], outline=GREEN, width=2)
    d.text((140, 95), "Pointly", font=font("outfit-var.ttf", 40, 800), fill=WHITE, anchor="lm")

    # Headline
    d.text((76, 214), "Point at your lamp.", font=font("outfit-var.ttf", 62, 800), fill=WHITE, anchor="ls")
    d.text((76, 288), "Tap to toggle.", font=font("outfit-var.ttf", 62, 800), fill=GREEN, anchor="ls")

    # Standfirst
    body = font("jakarta-var.ttf", 24, 400)
    d.text((76, 350), "A point-and-tap remote for Home Assistant.", font=body, fill=SOFT, anchor="ls")
    d.text((76, 386), "Aim your Android phone, tap once, the device fires.", font=body, fill=(170, 184, 202), anchor="ls")
    d.text((76, 422), "Runs on your own server. No cloud account.", font=body, fill=(170, 184, 202), anchor="ls")

    # Store line
    pill = [76, 470, 442, 522]
    d.rounded_rectangle(pill, radius=10, outline=GREEN, width=2)
    d.text((96, 496), "Free on Google Play  ·  Android 12+", font=font("jakarta-var.ttf", 20, 700), fill=GREEN, anchor="lm")

    if OUT.lower().endswith(".png"):
        img.save(OUT, optimize=True)
    else:
        img.save(OUT, quality=88, optimize=True, progressive=True)
    print(f"wrote {OUT} {img.size} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
