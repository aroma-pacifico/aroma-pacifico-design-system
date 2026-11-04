#!/usr/bin/env python3
"""Build tokens/tokens.json, tokens/tokens.css and tokens/contrast-report.md.

This script is the single source of the design tokens. It computes every
WCAG 2.2 contrast ratio from the sRGB values (relative luminance, formula of
WCAG 2.2 section 1.4.3), writes the ratio and the level reached next to each
pair, and fails if a pair misses the minimum its rule requires.

Usage:
  python3 scripts/build-tokens.py          write the three files
  python3 scripts/build-tokens.py --check  fail if the files are out of date
"""

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "tokens"
EXT = "org.aromapacifico"

# ---------------------------------------------------------------------------
# Palette (raw values). Every other color token is an alias of one of these.
# ---------------------------------------------------------------------------
BRAND = {
    "primary": {  # Pacific teal
        "900": "#0A3A41", "700": "#0E4C55", "500": "#13707C",
        "100": "#DCEFF0", "50": "#EEF7F7",
    },
    "coffee": {"700": "#6B4226", "500": "#8C5A36", "100": "#F1E6DC"},
    "parchment": {"400": "#C8963E", "100": "#F7EBD3"},
}
NEUTRAL = {
    "0": "#FFFFFF", "50": "#F6F2EC", "100": "#ECE6DE", "200": "#D9D1C7",
    "400": "#A39A8F", "600": "#6B655E", "700": "#4A4540", "900": "#1A1714",
    "1000": "#000000",
}
HUES = {
    "amber": {"700": "#5C3D00", "500": "#A86B00", "300": "#F2B33D", "100": "#FBF1DC"},
    "blue": {"800": "#0B3A6E", "700": "#0B4F8A", "500": "#1F63B5", "100": "#E3EEFB"},
    "green": {"800": "#0F4D22", "700": "#175A2B", "500": "#23803F", "100": "#E2F3E6"},
    "red": {"800": "#7A1610", "700": "#9E1C14", "500": "#C0281C", "100": "#FBE4E2"},
}

# Minimum ratios. OUTDOOR applies to every field app (farmer, transporter,
# collection-center logistics) and to the public lookup, which is read at the
# port and in the open: text and meaningful icons reach WCAG AAA (7:1).
# Boundaries and state borders reach WCAG 1.4.11 (3:1).
MIN_TEXT_OUTDOOR = 7.0
MIN_NON_TEXT = 3.0


def ref(path):
    return "{" + path + "}"


# Semantic colors: name -> alias path.
SEMANTIC = {
    "text": {
        "primary": "color.neutral.900",
        "secondary": "color.neutral.700",
        "inverse": "color.neutral.0",
        "brand": "color.brand.primary.700",
        "disabled": "color.neutral.600",
    },
    "surface": {
        "default": "color.neutral.0",
        "subtle": "color.neutral.50",
        "sunken": "color.neutral.100",
        "brand": "color.brand.primary.700",
        "brand-strong": "color.brand.primary.900",
    },
    "border": {
        "subtle": "color.neutral.200",
        "strong": "color.neutral.600",
        "focus": "color.brand.primary.700",
    },
    "action": {
        "primary": "color.brand.primary.700",
        "primary-pressed": "color.brand.primary.900",
        "on-primary": "color.neutral.0",
        "secondary": "color.neutral.0",
        "on-secondary": "color.brand.primary.700",
        "danger": "color.hue.red.700",
        "on-danger": "color.neutral.0",
        "disabled": "color.neutral.100",
        "on-disabled": "color.neutral.600",
    },
}

# The four sack badges of case statement point 7. Each badge is a tinted fill,
# dark text and icon in the same hue, and a 2 px border in the strong hue.
SACK = {
    "in-preparation": ("amber", "100", "700", "500"),
    "in-transit": ("blue", "100", "800", "500"),
    "accepted": ("green", "100", "800", "500"),
    "rejected": ("red", "100", "800", "500"),
}

# Crop alert severities. "solid" is the banner (strong fill, text, and a 2 px
# border that carries the 3:1 boundary when the fill is light, as for caution);
# "subtle" is the card and list item (tint, dark text, strong border).
ALERT = {
    "critical": {"solid": ("color.hue.red.700", "color.neutral.0", "color.hue.red.700"),
                 "subtle": ("color.hue.red.100", "color.hue.red.800", "color.hue.red.700")},
    "caution": {"solid": ("color.hue.amber.300", "color.neutral.900", "color.hue.amber.700"),
                "subtle": ("color.hue.amber.100", "color.hue.amber.700", "color.hue.amber.500")},
    "notice": {"solid": ("color.hue.blue.700", "color.neutral.0", "color.hue.blue.700"),
               "subtle": ("color.hue.blue.100", "color.hue.blue.800", "color.hue.blue.500")},
    "resolved": {"solid": ("color.hue.green.700", "color.neutral.0", "color.hue.green.700"),
                 "subtle": ("color.hue.green.100", "color.hue.green.800", "color.hue.green.500")},
    "no-data": {"solid": ("color.neutral.700", "color.neutral.0", "color.neutral.700"),
                "subtle": ("color.neutral.100", "color.neutral.900", "color.neutral.600")},
}

ALERT_MEANING = {
    "critical": "Open crop or drying alert: a reading left its alert range (episode open).",
    "caution": "Reading inside the alert range but outside the recommended band; displayed, never notified (ASM-134).",
    "notice": "Drying lot closure notice: coffee moisture reached the closure value (ASM-059); not an alert.",
    "resolved": "Episode closed: the variable is back in range.",
    "no-data": "Node not heard from; the farm status shows the last time it was heard (no alert to the farmer).",
}
SACK_MEANING = {
    "in-preparation": "Badge 'en preparacion': state in_preparation.",
    "in-transit": "Badge 'en viaje': states in_transit_to_center and in_transit_to_port.",
    "accepted": "Badge 'aceptado': states at_center_accepted and delivered_at_port_accepted.",
    "rejected": "Badge 'rechazado': states at_center_rejected and delivered_at_port_rejected.",
}

# ---------------------------------------------------------------------------
# Typography, spacing, sizes, grid.
# ---------------------------------------------------------------------------
FONT_FAMILY = {
    "sans": ["Roboto", "Noto Sans", "system-ui", "-apple-system", "Segoe UI", "Helvetica Neue", "Arial", "sans-serif"],
    "mono": ["Roboto Mono", "Noto Sans Mono", "ui-monospace", "SFMono-Regular", "Menlo", "Consolas", "monospace"],
}
FONT_WEIGHT = {"regular": 400, "medium": 500, "semibold": 600, "bold": 700}

# name: (family, size px, weight, line height px, letter spacing px)
TYPE_PHONE = {
    "display": ("sans", 32, "bold", 40, 0),
    "title": ("sans", 24, "bold", 32, 0),
    "heading": ("sans", 20, "semibold", 28, 0),
    "body-large": ("sans", 18, "regular", 26, 0),
    "body": ("sans", 16, "regular", 24, 0),
    "label": ("sans", 16, "semibold", 20, 0.2),
    "caption": ("sans", 14, "medium", 20, 0.2),
    "value": ("sans", 28, "bold", 34, 0),
    "code": ("mono", 20, "bold", 28, 1),
}
TYPE_WEB = {
    "display": ("sans", 36, "bold", 44, 0),
    "title": ("sans", 28, "bold", 36, 0),
    "heading": ("sans", 20, "semibold", 28, 0),
    "body": ("sans", 16, "regular", 24, 0),
    "label": ("sans", 14, "semibold", 20, 0.2),
    "caption": ("sans", 14, "regular", 20, 0),
    "value": ("sans", 24, "bold", 32, 0),
    "code": ("mono", 22, "bold", 30, 1),
}
# Web lookup scale above the md breakpoint.
TYPE_WEB_WIDE = {"display": 44, "title": 32, "value": 28}

SPACE = {"0": 0, "1": 4, "2": 8, "3": 12, "4": 16, "5": 24, "6": 32, "7": 48, "8": 64}
RADIUS = {"sm": 4, "md": 8, "lg": 12, "pill": 999}
BORDER_WIDTH = {"thin": 1, "state": 2, "focus": 3}
SIZE = {
    "touch-target-min": 48,
    "touch-target-gloved": 56,
    "touch-gap-min": 8,
    "icon-sm": 20,
    "icon-md": 24,
    "icon-lg": 32,
    "top-bar": 56,
    "bottom-nav": 64,
    "content-max-lookup": 640,
    "content-max-web": 1200,
}
BREAKPOINT = {"sm": 0, "md": 600, "lg": 1024, "xl": 1440}
GRID = {
    "phone": {"columns": 4, "gutter": 16, "margin": 16, "from": "sm"},
    "tablet": {"columns": 8, "gutter": 24, "margin": 24, "from": "md"},
    "desktop": {"columns": 12, "gutter": 24, "margin": 32, "from": "lg"},
}


# ---------------------------------------------------------------------------
# Helpers.
# ---------------------------------------------------------------------------
def channel(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_value):
    h = hex_value.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def level(ratio, kind):
    if kind == "text":
        if ratio >= 7:
            return "AAA"
        if ratio >= 4.5:
            return "AA"
        if ratio >= 3:
            return "AA large text only"
        return "fail"
    return "pass (3:1 non-text)" if ratio >= 3 else "fail"


def color_value(hex_value):
    h = hex_value.lstrip("#")
    comps = [round(int(h[i:i + 2], 16) / 255, 4) for i in (0, 2, 4)]
    return {"colorSpace": "srgb", "components": comps, "hex": "#" + h.lower()}


def dim(px):
    return {"value": px, "unit": "px"}


RAW = {}


def raw_tokens():
    group = {"brand": {}, "neutral": {}, "hue": {}}
    for fam, steps in BRAND.items():
        group["brand"][fam] = {}
        for step, hx in steps.items():
            RAW[f"color.brand.{fam}.{step}"] = hx
            group["brand"][fam][step] = {"$value": color_value(hx)}
    for step, hx in NEUTRAL.items():
        RAW[f"color.neutral.{step}"] = hx
        group["neutral"][step] = {"$value": color_value(hx)}
    for fam, steps in HUES.items():
        group["hue"][fam] = {}
        for step, hx in steps.items():
            RAW[f"color.hue.{fam}.{step}"] = hx
            group["hue"][fam][step] = {"$value": color_value(hx)}
    group["brand"]["parchment"]["400"]["$description"] = (
        "Decorative only (isotype bean, illustration accents); never text or a state indicator."
    )
    return group


def pair(fg, bg, kind, rule, minimum):
    ratio = contrast(RAW[fg], RAW[bg])
    entry = {
        "foreground": ref(fg),
        "background": ref(bg),
        "ratio": round(ratio, 2),
        "level": level(ratio, kind),
        "kind": kind,
        "rule": rule,
        "minimum": minimum,
    }
    PAIRS.append(entry)
    return entry


PAIRS = []


def build():
    PAIRS.clear()
    RAW.clear()
    tokens = {
        "$description": (
            "Aroma Pacifico design tokens for the farmer app, the transporter app, the "
            "collection-center logistics app and reports web, and the public sack lookup. "
            "Format: W3C Design Tokens Community Group, Format Module 2025.10. "
            "Generated by scripts/build-tokens.py; do not edit by hand."
        ),
        "color": {"$type": "color"},
    }
    color = tokens["color"]
    color.update(raw_tokens())

    # Semantic aliases.
    for grp, names in SEMANTIC.items():
        color[grp] = {name: {"$value": ref(path)} for name, path in names.items()}
        for name, path in names.items():
            RAW[f"color.{grp}.{name}"] = RAW[path]

    # Contrast of the general pairs.
    general = [
        pair("color.text.primary", "color.surface.default", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
        pair("color.text.primary", "color.surface.subtle", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
        pair("color.text.secondary", "color.surface.default", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
        pair("color.text.secondary", "color.surface.subtle", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
        pair("color.text.brand", "color.surface.default", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
        pair("color.text.inverse", "color.surface.brand", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
        pair("color.text.inverse", "color.surface.brand-strong", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
        pair("color.action.on-primary", "color.action.primary", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
        pair("color.action.on-secondary", "color.action.secondary", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
        pair("color.action.on-danger", "color.action.danger", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
        pair("color.action.on-disabled", "color.action.disabled", "text", "disabled (exempt, WCAG 1.4.3)", 4.5),
        pair("color.border.strong", "color.surface.default", "non-text", "OUTDOOR-2", MIN_NON_TEXT),
        pair("color.border.focus", "color.surface.default", "non-text", "OUTDOOR-2", MIN_NON_TEXT),
        pair("color.action.primary", "color.surface.default", "non-text", "OUTDOOR-2", MIN_NON_TEXT),
    ]
    color["$extensions"] = {EXT: {"contrast": general}}

    # Sack badges.
    color["sack"] = {}
    for name, (hue, bg, fg, border) in SACK.items():
        p_bg, p_fg, p_border = (f"color.hue.{hue}.{bg}", f"color.hue.{hue}.{fg}", f"color.hue.{hue}.{border}")
        for part, path in (("background", p_bg), ("text", p_fg), ("icon", p_fg), ("border", p_border)):
            RAW[f"color.sack.{name}.{part}"] = RAW[path]
        color["sack"][name] = {
            "$description": SACK_MEANING[name],
            "background": {"$value": ref(p_bg)},
            "text": {"$value": ref(p_fg)},
            "icon": {"$value": ref(p_fg)},
            "border": {"$value": ref(p_border)},
            "$extensions": {EXT: {"contrast": [
                pair(f"color.sack.{name}.text", f"color.sack.{name}.background", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
                pair(f"color.sack.{name}.text", "color.surface.default", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
                pair(f"color.sack.{name}.border", "color.surface.default", "non-text", "OUTDOOR-2", MIN_NON_TEXT),
            ]}},
        }

    # Crop alert severities.
    color["alert"] = {}
    for name, spec in ALERT.items():
        s_bg, s_fg, s_border = spec["solid"]
        t_bg, t_fg, t_border = spec["subtle"]
        mapping = {
            "solid-background": s_bg, "solid-text": s_fg, "solid-border": s_border,
            "subtle-background": t_bg, "subtle-text": t_fg, "subtle-border": t_border,
        }
        for part, path in mapping.items():
            RAW[f"color.alert.{name}.{part}"] = RAW[path]
        color["alert"][name] = {
            "$description": ALERT_MEANING[name],
            **{part: {"$value": ref(path)} for part, path in mapping.items()},
            "$extensions": {EXT: {"contrast": [
                pair(f"color.alert.{name}.solid-text", f"color.alert.{name}.solid-background", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
                pair(f"color.alert.{name}.subtle-text", f"color.alert.{name}.subtle-background", "text", "OUTDOOR-1", MIN_TEXT_OUTDOOR),
                pair(f"color.alert.{name}.subtle-border", "color.surface.default", "non-text", "OUTDOOR-2", MIN_NON_TEXT),
                pair(f"color.alert.{name}.solid-border", "color.surface.default", "non-text", "OUTDOOR-2", MIN_NON_TEXT),
            ]}},
        }

    # Outdoor high-contrast mode (data-contrast="outdoor"): pure black on white.
    RAW["color.outdoor.text"] = NEUTRAL["1000"]
    RAW["color.outdoor.surface"] = NEUTRAL["0"]
    RAW["color.outdoor.border"] = NEUTRAL["1000"]
    color["outdoor"] = {
        "$description": (
            "Outdoor high-contrast mode, switched on by the user or by the app in direct "
            "sunlight: text and borders become pure black on white; badge and alert fills keep "
            "their hue and gain a 3 px black border."
        ),
        "text": {"$value": ref("color.neutral.1000")},
        "surface": {"$value": ref("color.neutral.0")},
        "border": {"$value": ref("color.neutral.1000")},
        "$extensions": {EXT: {"contrast": [
            pair("color.outdoor.text", "color.outdoor.surface", "text", "OUTDOOR-8", MIN_TEXT_OUTDOOR),
            pair("color.outdoor.border", "color.outdoor.surface", "non-text", "OUTDOOR-8", MIN_NON_TEXT),
        ]}},
    }

    # Fonts and typography.
    tokens["font"] = {
        "family": {"$type": "fontFamily", **{k: {"$value": v} for k, v in FONT_FAMILY.items()}},
        "weight": {"$type": "fontWeight", **{k: {"$value": v} for k, v in FONT_WEIGHT.items()}},
    }

    def type_group(scale, desc):
        g = {"$type": "typography", "$description": desc}
        for name, (fam, size, weight, lh, ls) in scale.items():
            g[name] = {"$value": {
                "fontFamily": ref(f"font.family.{fam}"),
                "fontSize": dim(size),
                "fontWeight": ref(f"font.weight.{weight}"),
                "letterSpacing": dim(ls),
                "lineHeight": round(lh / size, 3),
            }}
        return g

    tokens["typography"] = {
        "phone": type_group(TYPE_PHONE, (
            "Farmer and transporter apps (Android and iOS). Sizes in px equal sp/pt at density 1 "
            "and scale with the system font size. No text under 14."
        )),
        "web": type_group(TYPE_WEB, (
            "Public sack lookup and the collection-center reports web, from the sm breakpoint. "
            "System fonts only: the lookup page loads no font file."
        )),
        "web-wide": {"$type": "dimension", "$description": "Font sizes that grow from the md breakpoint.",
                     **{k: {"$value": dim(v)} for k, v in TYPE_WEB_WIDE.items()}},
    }

    tokens["space"] = {"$type": "dimension", "$description": "4 px base scale.",
                       **{k: {"$value": dim(v)} for k, v in SPACE.items()}}
    tokens["radius"] = {"$type": "dimension", **{k: {"$value": dim(v)} for k, v in RADIUS.items()}}
    tokens["border-width"] = {"$type": "dimension", **{k: {"$value": dim(v)} for k, v in BORDER_WIDTH.items()}}
    tokens["size"] = {"$type": "dimension", **{k: {"$value": dim(v)} for k, v in SIZE.items()}}
    tokens["breakpoint"] = {"$type": "dimension", "$description": "Minimum viewport width of each range.",
                            **{k: {"$value": dim(v)} for k, v in BREAKPOINT.items()}}
    tokens["grid"] = {}
    for name, g in GRID.items():
        tokens["grid"][name] = {
            "$description": f"Layout grid from the {g['from']} breakpoint.",
            "columns": {"$type": "number", "$value": g["columns"]},
            "gutter": {"$type": "dimension", "$value": dim(g["gutter"])},
            "margin": {"$type": "dimension", "$value": dim(g["margin"])},
            "from": {"$type": "dimension", "$value": ref(f"breakpoint.{g['from']}")},
        }

    failures = [p for p in PAIRS if p["ratio"] < p["minimum"]]
    return tokens, failures


# ---------------------------------------------------------------------------
# CSS and report rendering.
# ---------------------------------------------------------------------------
def css_name(path):
    return "--ap-" + path.replace(".", "-")


def css_value(value):
    if isinstance(value, str) and value.startswith("{"):
        return f"var({css_name(value[1:-1])})"
    if isinstance(value, dict) and "hex" in value:
        return value["hex"].upper()
    if isinstance(value, dict) and "unit" in value:
        return f"{value['value']}{value['unit']}" if value["value"] else "0"
    if isinstance(value, list):
        return ", ".join(f'"{v}"' if " " in v else v for v in value)
    return str(value)


def walk(node, path, out):
    for key, val in node.items():
        if key.startswith("$"):
            continue
        p = f"{path}.{key}" if path else key
        if isinstance(val, dict) and "$value" in val:
            v = val["$value"]
            if isinstance(v, dict) and "fontSize" in v:
                for prop, css_prop in (("fontFamily", "family"), ("fontSize", "size"), ("fontWeight", "weight"),
                                       ("lineHeight", "line-height"), ("letterSpacing", "letter-spacing")):
                    out.append((f"{p}.{css_prop}", css_value(v[prop])))
            else:
                out.append((p, css_value(v)))
        elif isinstance(val, dict):
            walk(val, p, out)


def render_css(tokens):
    decls = []
    walk(tokens, "", decls)
    lines = [
        "/*",
        " * Aroma Pacifico design tokens as CSS custom properties.",
        " * Generated by scripts/build-tokens.py from the same source as tokens.json.",
        " * Do not edit by hand.",
        " */",
        "",
        ":root {",
    ]
    lines += [f"  {css_name(p)}: {v};" for p, v in decls]
    lines += ["}", ""]
    wide = [f"  --ap-typography-web-{k}-size: var(--ap-typography-web-wide-{k});" for k in TYPE_WEB_WIDE]
    lines += [f"@media (min-width: {BREAKPOINT['md']}px) {{", ":root {"] + wide + ["}", "}", ""]
    lines += [
        "/* OUTDOOR-8: outdoor high-contrast mode. */",
        '[data-contrast="outdoor"] {',
        "  --ap-color-text-primary: var(--ap-color-outdoor-text);",
        "  --ap-color-text-secondary: var(--ap-color-outdoor-text);",
        "  --ap-color-text-brand: var(--ap-color-outdoor-text);",
        "  --ap-color-surface-default: var(--ap-color-outdoor-surface);",
        "  --ap-color-surface-subtle: var(--ap-color-outdoor-surface);",
        "  --ap-color-border-subtle: var(--ap-color-outdoor-border);",
        "  --ap-color-border-strong: var(--ap-color-outdoor-border);",
    ]
    for name in SACK:
        lines.append(f"  --ap-color-sack-{name}-border: var(--ap-color-outdoor-border);")
    for name in ALERT:
        lines.append(f"  --ap-color-alert-{name}-subtle-border: var(--ap-color-outdoor-border);")
    lines += ["  --ap-border-width-state: var(--ap-border-width-focus);", "}", ""]
    return "\n".join(lines)


def render_report(failures):
    lines = [
        "# Contrast report",
        "",
        "Generated by `scripts/build-tokens.py`. Every ratio is computed from the sRGB values with the "
        "WCAG 2.2 relative luminance formula; none is estimated. OUTDOOR-1 requires 7:1 (AAA) for text "
        "and meaningful icons; OUTDOOR-2 requires 3:1 for boundaries and state borders (WCAG 1.4.11). "
        "Rules are defined in [`components/README.md`](../components/README.md#outdoor-contrast-rules).",
        "",
        "| Foreground | Background | Colors | Ratio | Level | Rule | Minimum | Result |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for p in PAIRS:
        fg, bg = p["foreground"][1:-1], p["background"][1:-1]
        result = "SUCCESS" if p["ratio"] >= p["minimum"] else "ERROR"
        lines.append(
            f"| `{fg}` | `{bg}` | {RAW[fg]} on {RAW[bg]} | {p['ratio']:.2f}:1 | {p['level']} | "
            f"{p['rule']} | {p['minimum']}:1 | {result} |"
        )
    lines += ["", f"Pairs checked: {len(PAIRS)}. Failures: {len(failures)}.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    tokens, failures = build()
    files = {
        OUT / "tokens.json": json.dumps(tokens, indent=2, ensure_ascii=False) + "\n",
        OUT / "tokens.css": render_css(tokens),
        OUT / "contrast-report.md": render_report(failures),
    }
    for p in failures:
        print(f"ERROR contrast {p['foreground']} on {p['background']}: {p['ratio']} < {p['minimum']}")

    if args.check:
        stale = [f for f, text in files.items() if not f.exists() or f.read_text(encoding="utf-8") != text]
        for f in stale:
            print(f"ERROR out of date: {f.relative_to(ROOT)}")
        if stale or failures:
            return 1
        print(f"SUCCESS tokens up to date; {len(PAIRS)} contrast pairs meet their minimum")
        return 0

    OUT.mkdir(exist_ok=True)
    for f, text in files.items():
        f.write_text(text, encoding="utf-8")
        print(f"wrote {f.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
