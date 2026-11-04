#!/usr/bin/env python3
"""Build the Aroma Pacifico brand SVGs in brand/.

The isotype is drawn from geometric primitives defined below. The wordmark
letters are converted to outlines from Noto Sans Bold (SIL Open Font License
1.1), so the published SVGs reference no font and embed no raster.

Requires fontTools (pip install fonttools) only to rebuild; the committed SVGs
need nothing.

Usage: python3 scripts/build-brand.py [--font PATH]
"""

import argparse
import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRAND = ROOT / "brand"
DEFAULT_FONT = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"

# Brand colors, mirrored from tokens/tokens.json (color.brand.*).
PRIMARY_700 = "#0E4C55"
COFFEE_700 = "#6B4226"
PARCHMENT_400 = "#C8963E"
INK_MONO = "#1A1714"
INK_NEGATIVE = "#FFFFFF"

# Isotype geometry on a 64 x 64 grid.
BEAN = 'cx="0" cy="0" rx="11.5" ry="17"'
BEAN_TRANSFORM = "translate(32 27) rotate(35)"
CREASE = "M0 -14.5 C -6 -6 6 6 0 14.5"
WAVES = (
    "M2 47 C 11 42.5 21 51.5 32 47 S 53 42.5 62 47",
    "M2 54.5 C 11 50 21 59 32 54.5 S 53 50 62 54.5",
)


def isotype_group(prefix, ink, bean_fill, crease_ink):
    """Return the isotype markup: ink disc with the bean and two waves cut out."""
    waves = "".join(
        f'<path d="{d}" fill="none" stroke="#000" stroke-width="2.6" '
        f'stroke-linecap="round"/>'
        for d in WAVES
    )
    bean_fill_markup = (
        f'<ellipse {BEAN} transform="{BEAN_TRANSFORM}" fill="{bean_fill}"/>'
        if bean_fill
        else ""
    )
    return (
        f'<mask id="{prefix}-cut" maskUnits="userSpaceOnUse" x="0" y="0" '
        f'width="64" height="64">'
        f'<rect width="64" height="64" fill="#fff"/>'
        f'<ellipse {BEAN} transform="{BEAN_TRANSFORM}" fill="#000"/>'
        f"{waves}</mask>"
        f'<circle cx="32" cy="32" r="30" fill="{ink}" mask="url(#{prefix}-cut)"/>'
        f"{bean_fill_markup}"
        f'<path d="{CREASE}" transform="{BEAN_TRANSFORM}" fill="none" '
        f'stroke="{crease_ink}" stroke-width="2.8" stroke-linecap="round"/>'
    )


def outline(font, text, cap_height, x0, baseline, tracking=0.0):
    """Return (svg path data, advance width) for text set at cap_height."""
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    cap = font["OS/2"].sCapHeight
    scale = cap_height / cap
    pen = SVGPathPen(glyph_set)
    x = x0
    for i, ch in enumerate(text):
        name = cmap[ord(ch)]
        glyph = glyph_set[name]
        tpen = TransformPen(pen, (scale, 0, 0, -scale, x, baseline))
        glyph.draw(tpen)
        x += glyph.width * scale
        if i < len(text) - 1:
            x += tracking
    return pen.getCommands(), x - x0


def svg(width, height, title, desc, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.2f} {height}" '
        f'width="{width:.2f}" height="{height}" role="img" '
        f'aria-labelledby="t d">'
        f'<title id="t">{title}</title><desc id="d">{desc}</desc>'
        f"{body}</svg>\n"
    )


def build(font_path):
    font = TTFont(font_path)
    BRAND.mkdir(exist_ok=True)

    # Wordmark: AROMA over PACIFICO (with the accent of the proper name),
    # PACIFICO tracked out so both lines share one width.
    x0 = 78
    top_path, top_w = outline(font, "AROMA", 23, x0, 30)
    raw_path, raw_w = outline(font, "PACÍFICO", 12.5, x0, 53)
    tracking = (top_w - raw_w) / (len("PACÍFICO") - 1)
    bottom_path, bottom_w = outline(font, "PACÍFICO", 12.5, x0, 53, tracking)
    width = x0 + max(top_w, bottom_w) + 2

    variants = {
        "": ("Full color", PRIMARY_700, PARCHMENT_400, PRIMARY_700, PRIMARY_700, COFFEE_700),
        "-mono": ("Single ink", INK_MONO, None, INK_MONO, INK_MONO, INK_MONO),
        "-negative": ("Negative, white on dark", INK_NEGATIVE, None, INK_NEGATIVE, INK_NEGATIVE, INK_NEGATIVE),
    }
    for suffix, (label, ink, bean, crease, top_ink, bottom_ink) in variants.items():
        iso = isotype_group(f"ap-iso{suffix or '-color'}", ink, bean, crease)
        (BRAND / f"isotype{suffix}.svg").write_text(
            svg(
                64,
                64,
                "Aroma Pacifico isotype",
                f"{label}: a coffee bean over two Pacific waves inside a disc.",
                iso,
            ),
            encoding="utf-8",
        )
        logo_iso = isotype_group(f"ap-logo{suffix or '-color'}", ink, bean, crease)
        body = (
            f"{logo_iso}"
            f'<path d="{top_path}" fill="{top_ink}"/>'
            f'<path d="{bottom_path}" fill="{bottom_ink}"/>'
        )
        (BRAND / f"logo{suffix}.svg").write_text(
            svg(
                width,
                64,
                "Aroma Pacifico logo",
                f"{label}: isotype and the wordmark AROMA PACIFICO.",
                body,
            ),
            encoding="utf-8",
        )
    print(f"logo width {width:.2f}, PACIFICO tracking {tracking:.3f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--font", default=DEFAULT_FONT)
    build(parser.parse_args().font)
