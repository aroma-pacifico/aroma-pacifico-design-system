# Aroma Pacífico Design System

Design system for the three Aroma Pacífico pilot applications: Coffee Grower (offline-first PWA), Transporter (mobile custody lookup), and Sack Traceability Portal (buyer view).

Part of the Aroma Pacífico pilot, the 2026 update of the coffee traceability pilot across Cauca, Huila, and Tolima. Backlog tasks are tracked in [aroma-pacifico-roadmap](https://github.com/aroma-pacifico/aroma-pacifico-roadmap) and on the [Aroma Pacífico Pilot board](https://github.com/orgs/aroma-pacifico/projects/1).

---

## What Lives Here

This repository provides the visual identity, W3C design tokens, CSS custom properties, base UI components, outline SVG icons, and responsive preview sheets for the three applications of the traceability pilot. In accordance with case statement point 7, no manual or style is inherited from the 2020 pilot, and the applications themselves are not constructed here.

### Repository Layout

```text
aroma-pacifico-design-system/
|-- brand/
|   |-- README.md                 # Brand manual, clear space, minimum reproduction sizes
|   |-- logo.svg                  # Full color logo on light surfaces
|   |-- logo-mono.svg             # Single ink logo for print and engraving (#1A1714)
|   |-- logo-negative.svg         # Negative white logo for dark surfaces
|   |-- isotype.svg               # Full color isotype (coffee bean over Pacific waves)
|   |-- isotype-mono.svg          # Single ink isotype
|   `-- isotype-negative.svg      # Negative white isotype
|-- components/
|   |-- README.md                 # Component specifications and OUTDOOR-1 to OUTDOOR-8 rules
|   `-- components.css            # Base styles: button, field, alert, sack card, badge
|-- docs/
|   |-- case/
|   |   `-- case-statement.pdf    # Source of project requirements
|   |-- decision-log.md           # Assigned ID block 240-249 (ASM-240 to ASM-244)
|   |-- design-system.md          # Comprehensive technical design system specification
|   `-- troubleshooting-log.md    # Living log of engineering friction and resolutions
|-- examples/
|   |-- alert-card.html           # Crop alerts and delayed timestamp store-and-forward demo
|   |-- brand-sheet.html          # Brand identity marks and clear space specimen
|   |-- buyer-lookup.html         # Public sack lookup with ASM-096 data minimization
|   `-- design-sheet.html         # Master unified design system sheet (1280x3600)
|-- icons/
|   |-- README.md                 # Iconography guide and visual metaphors
|   |-- alert-triangle.svg        # Warning / crop alerts
|   |-- calendar.svg              # Processing dates
|   |-- check-circle.svg          # Accepted status
|   |-- clock.svg                 # Preparation status and delayed timestamps
|   |-- droplet.svg               # Moisture percentage
|   |-- eye.svg                   # Inspection view
|   |-- location.svg              # Department and municipality origin
|   |-- package.svg               # Coffee sack container
|   |-- qr-code.svg               # Sack code scanning
|   |-- scale.svg                 # 60 kg gross mass scale weighing
|   |-- shield-check.svg          # Data minimization verification
|   |-- sun.svg                   # Outdoor high-contrast mode toggle
|   |-- thermometer.svg           # Grain drying temperatures
|   |-- truck.svg                 # Transit custody
|   `-- x-circle.svg              # Rejected status
|-- previews/
|   |-- alert-card.png            # Rendered alert card preview (390x900)
|   |-- brand.png                 # Rendered brand sheet preview (1200x1060)
|   |-- buyer-lookup-desktop.png  # Rendered desktop buyer lookup preview (1280x1000)
|   |-- buyer-lookup-phone.png    # Rendered mobile phone buyer lookup preview (390x1240)
|   `-- design-sheet.png          # Rendered master design sheet preview (1280x3600)
|-- scripts/
|   |-- build-brand.py            # Generates SVG brand marks from shared geometry
|   |-- build-tokens.py           # Builds tokens.json, tokens.css, contrast-report.md
|   `-- render-previews.sh        # Headless Google Chrome raster preview generator
|-- standards/                    # Synchronized engineering standards
|-- tokens/
|   |-- contrast-report.md        # Relative luminance report (48 checked, 0 failures)
|   |-- tokens.css                # CSS custom properties and outdoor mode definitions
|   `-- tokens.json               # W3C design tokens format
|-- AGENTS.md                     # Engineering constitution and zero-emoji mandate
|-- CLAUDE.md                     # Claude agent instructions
|-- CONTRIBUTING.md               # Contribution workflow
|-- GEMINI.md                     # Gemini agent instructions
`-- README.md                     # Repository documentation and index
```

---

## Core Deliverables Summary

| Area | Scope & Key Assets | Regulatory / Architectural Reference |
|---|---|---|
| Brand Identity | Logo, isotype, single-ink, and negative versions in pure SVG vector paths | Case statement point 7; [`brand/README.md`](brand/README.md) |
| Design Tokens | Primary teal, neutral, 4 sack badge colors, 5 crop alert severities | W3C Design Tokens Module 2025.10; [`tokens/tokens.json`](tokens/tokens.json) |
| Contrast Verification | Programmatic relative luminance check guaranteeing Level AAA (&ge; 7.0:1) outdoors | WCAG 2.2 Section 1.4.3 & 1.4.11; [`tokens/contrast-report.md`](tokens/contrast-report.md) |
| System Iconography | 15 outline vector icons on 24x24 grid with 2 px stroke and `currentColor` | Case statement point 7; [`icons/README.md`](icons/README.md) |
| Base UI Components | Button, field, alert, sack card, status badge | Case statement point 7; [`components/components.css`](components/components.css) |
| Outdoor Contrast | OUTDOOR-1 through OUTDOOR-8 rules, `data-contrast="outdoor"` 21:1 mode | [`components/README.md#outdoor-contrast-rules`](components/README.md#outdoor-contrast-rules) |
| Buyer View (Lookup) | Public sack lookup returning 4 data groups; zero personal data exposed | ASM-096; Ley 1581 de 2012; [`examples/buyer-lookup.html`](examples/buyer-lookup.html) |
| Master Design Sheet | Complete design system applied across the three pilot applications | Case statement point 7; [`examples/design-sheet.html`](examples/design-sheet.html) |

---

## Rebuilding and Verification

### Token Compilation and Contrast Audit

The single source of truth for design tokens is `scripts/build-tokens.py`. To recompile tokens and verify that all 48 color pairs satisfy outdoor contrast rules:

```bash
# Rebuild tokens.json, tokens.css, and contrast-report.md
python3 scripts/build-tokens.py

# Verify that committed files match the generator output
python3 scripts/build-tokens.py --check
```

### Visual Preview Generation

Raster previews in `previews/` are generated from HTML example sheets using headless Google Chrome:

```bash
bash scripts/render-previews.sh
```

### Zero-Emoji Policy Verification

All files and git logs must strictly comply with the zero-emoji mandate:

```bash
grep -rnP '[\x{1F300}-\x{1FAD6}\x{2600}-\x{27BF}]' .
```

---

## Tasks Delivered Here

- [A24](https://github.com/aroma-pacifico/aroma-pacifico-roadmap/issues/37): Build the design system for the 3 applications (Refs aroma-pacifico/aroma-pacifico-roadmap#37, Closes ALPH-18).
