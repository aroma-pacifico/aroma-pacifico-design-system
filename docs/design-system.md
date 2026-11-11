# Aroma Pacífico Design System Specification

## 1. Executive Summary and Architecture Grounding

The Aroma Pacífico design system is the visual and interaction standard for the 2026 coffee traceability pilot across Cauca, Huila, and Tolima. It satisfies point 7 of the academic DevOps challenge statement ("Sistema de diseño") and maps directly to the operational flows defined in [`docs/architecture.md`](https://github.com/aroma-pacifico/aroma-pacifico-architecture/blob/main/docs/architecture.md#9-point-7-design-system) of the architecture repository.

In strict adherence to the case statement, no manual or visual style is inherited from the 2020 pilot. The design system provides a cohesive, field-tested experience across three distinct applications:

1. **Coffee Grower Application (Farmer PWA)**: An offline-first mobile progressive web application featuring simplified workflows for wet-mill sack weighing, QR batch label binding, drying lot confirmation, and real-time/delayed crop alert monitoring.
2. **Transporter Application (Logistics Custody)**: A ruggedized mobile tracking interface capturing GNSS coordinates at 5-minute intervals, managing custody transfers across transit legs, and confirming delivery handovers at collection centers and the Port of Buenaventura.
3. **Public Sack Traceability Portal (Buyer View)**: A responsive, unauthenticated web interface allowing specialty coffee buyers, cooperatives, and exporters to verify sack origin, processing dates, custody status, and drying telemetry with strict privacy and data minimization.

---

## 2. Requirements Traceability Matrix

The design system addresses each requirement from point 7 of the case statement and the corresponding architectural inputs:

| Case Requirement | Architecture Input | Design System Deliverable | Verification Status |
|---|---|---|---|
| Main logo, isotype, single-ink and negative versions | Brand identity standard | [`brand/`](../brand/README.md) containing `logo.svg`, `isotype.svg`, `logo-mono.svg`, `isotype-mono.svg`, `logo-negative.svg`, `isotype-negative.svg` | Verified in [`examples/brand-sheet.html`](../examples/brand-sheet.html) and [`previews/brand.png`](../previews/brand.png) |
| Color palette covering sack statuses and crop alerts | Point 7, PD-154, ASM-096 | [`tokens/tokens.json`](../tokens/tokens.json) and [`tokens/tokens.css`](../tokens/tokens.css): 4 sack badges and 5 alert severities | Verified in [`tokens/contrast-report.md`](../tokens/contrast-report.md) (48 pairs checked, 0 failures) |
| Typography for phone and web lookup, spacing and grid | 8-unit spatial system | Responsive type scale, font family tokens, 4-column phone and 12-column web grid definitions | Verified in [`tokens/tokens.css`](../tokens/tokens.css) |
| Base components: button, field, alert, sack card, badge | Point 7 base components | [`components/components.css`](../components/components.css) and [`components/README.md`](../components/README.md) | Verified in [`examples/design-sheet.html`](../examples/design-sheet.html) |
| Outdoor contrast rules | High ambient sunlight glare | OUTDOOR-1 to OUTDOOR-8 rules; Level AAA (7:1) contrast; `data-contrast="outdoor"` mode | Verified in [`tokens/contrast-report.md`](../tokens/contrast-report.md) |
| Understandable icons without a long manual | Point 7 iconography | [`icons/`](../icons/README.md): 15 universal outline SVG icons (24x24 grid, 2px stroke) | Verified in [`icons/`](../icons/README.md) |
| Buyer view without excess data | Point 7, ASM-096 | [`examples/buyer-lookup.html`](../examples/buyer-lookup.html): exactly 4 data groups, zero personal data | Verified in [`previews/buyer-lookup-desktop.png`](../previews/buyer-lookup-desktop.png) |
| Applied in a sheet or document (no app code) | Academic delivery boundary | [`examples/design-sheet.html`](../examples/design-sheet.html) and [`previews/design-sheet.png`](../previews/design-sheet.png) | Verified via headless Chrome rendering |

---

## 3. Brand Architecture and Geometry

The brand visual language conveys high-altitude coffee cultivation in southwestern Colombia reaching Pacific maritime export at Buenaventura:

- **Isotype Geometry**: A coffee bean nested over two rhythmic ocean wave crests inside a circular containment disc. In single-ink and negative variants, the bean and wave paths are cut out using SVG clipping geometry, allowing the mounting background surface to show through without requiring white raster fills.
- **Outlined Typography**: The wordmark letters ("AROMA PACÍFICO") are outlines drawn from open-licensed Noto Sans Bold, ensuring consistent rendering across environments without embedding web font files or making remote HTTP calls.
- **Clear Space**: A minimum boundary equal to 25% of the mark's height must remain clear of text, borders, or other graphics on all sides.
- **Minimum Reproduction Size**: The complete logo maintains legibility down to 48 px on screens (15 mm in print); below 48 px, the isotype alone is used, with a minimum size of 24 px (8 mm in print).

---

## 4. Tokens and Color System

Color tokens are authored in W3C Design Tokens Community Group format (`tokens/tokens.json`) and compiled alongside CSS custom properties (`tokens/tokens.css`) by `scripts/build-tokens.py`.

### 4.1 Core Palette

| Palette Group | Token Token Path | Primary Hex | Outdoor Role |
|---|---|---|---|
| Primary Brand | `color.brand.primary.700` | `#0E4C55` | Primary buttons, active state headers, brand text (9.62:1 contrast on white). |
| Deep Brand | `color.brand.primary.900` | `#0A3A41` | Navigation headers, sack codes, high-emphasis text (12.39:1 contrast). |
| Coffee Neutral | `color.brand.coffee.700` | `#6B4226` | Earthy secondary brand elements, dry parchment accents. |
| Background Neutral | `color.surface.default` | `#FFFFFF` | Primary card and application background for high sunlight reflectance. |
| Warm Parchment | `color.surface.subtle` | `#F6F2EC` | Subtle secondary backgrounds and card grouping areas. |
| Dark Body Text | `color.text.primary` | `#1A1714` | Primary high-contrast typography (17.85:1 contrast on white). |

### 4.2 Sack Status Badges (PD-154 Mapping)

The seven operational states of the sack lifecycle defined in Part C of the case statement map to four clear status badges:

| Public Badge | Lifecycle States | Background | Border | Text & Icon | Outdoor Ratio |
|---|---|---|---|---|---|
| En preparación | `in_preparation` | `#FBF1DC` | `#A86B00` | `#5C3D00` | 8.82:1 (AAA) |
| En viaje | `in_transit_to_center`, `in_transit_to_port` | `#E3EEFB` | `#1F63B5` | `#0B3A6E` | 9.70:1 (AAA) |
| Aceptado | `at_center_accepted`, `delivered_at_port_accepted` | `#E2F3E6` | `#23803F` | `#0F4D22` | 8.64:1 (AAA) |
| Rechazado | `at_center_rejected`, `delivered_at_port_rejected` | `#FBE4E2` | `#C0281C` | `#7A1610` | 8.87:1 (AAA) |

### 4.3 Crop Alert Severities

Alerts use standardized color tokens that convey severity without relying on color alone:

| Severity | Background Tint | Border (2 px) | Text & Icon | Outdoor Ratio | Operational Meaning |
|---|---|---|---|---|---|
| Critical | `#FBE4E2` | `#9E1C14` | `#7A1610` | 8.87:1 (AAA) | Urgent agronomic threshold breach (broca, rust) triggering drone flight. |
| Caution | `#FBF1DC` | `#A86B00` | `#5C3D00` | 8.82:1 (AAA) | Environmental variable trending out of bounds (prolonged high humidity). |
| Notice | `#E3EEFB` | `#1F63B5` | `#0B3A6E` | 9.70:1 (AAA) | Scheduled mission notifications, driver dispatch updates. |
| Resolved | `#E2F3E6` | `#23803F` | `#0F4D22` | 8.64:1 (AAA) | Variable stabilized or inspection verified. |
| No-Data | `#ECE6DE` | `#6B655E` | `#1A1714` | 14.40:1 (AAA) | Sensor node silent for more than 24 hours (case statement section 6). |

---

## 5. Outdoor Usability and Contrast Rules

Direct equatorial sunlight in coffee plantations and maritime ports creates extreme glare. The design system enforces eight outdoor usability rules:

- **OUTDOOR-1**: Minimum 7.0:1 (WCAG Level AAA) relative luminance contrast for all text and meaningful iconography.
- **OUTDOOR-2**: Minimum 3.0:1 non-text boundary contrast (WCAG 1.4.11) for input borders, cards, and interactive elements.
- **OUTDOOR-3**: Touch target sizing: 48x48 px standard touch targets, expanding to 56x56 px for gloved field operations.
- **OUTDOOR-4**: High-reflectance light backgrounds (`#FFFFFF`, `#F6F2EC`) by default; dark mode is prohibited in outdoor daylight to prevent glossy screen mirror reflections.
- **OUTDOOR-5**: Redundant encoding: every status or alert pairs color with a distinct SVG icon and text label (WCAG 1.4.1).
- **OUTDOOR-6**: Visible focus states: 3 px solid high-contrast focus rings with 2 px offset.
- **OUTDOOR-7**: Arm's length readability: minimum 16 px base font on mobile devices, with critical numerical values (scale mass, moisture) displayed at 24-32 px bold.
- **OUTDOOR-8**: High-Contrast Outdoor Mode (`[data-contrast="outdoor"]`): switches body copy and borders to pure solid black (`#000000`) on solid white (`#FFFFFF`), delivering an absolute 21.0:1 contrast ratio.

---

## 6. Public Lookup and Data Minimization (Buyer View)

Conforming to ASM-096 and Colombian statutory privacy compliance (Ley 1581 de 2012), the public sack lookup returns strictly four data groups:

1. **Origin**: Alphanumeric sack code, department (Cauca, Huila, Tolima), and municipality.
2. **Processing Dates**: Calendar dates only for drying start, drying completion, and 60 kg sack packaging (no exact times of day).
3. **Status**: Current Part C custody state (e.g. "Entregado en Puerto Aceptado").
4. **Drying Variables**: Aggregate lot statistics (final moisture percentage, minimum grain temperature, mean grain temperature, maximum grain temperature).

Data strictly omitted to protect personal privacy and commercial confidentiality:
- Farmer name and cédula cafetera
- Farm name and cadastral registration number
- Exact GNSS farm coordinates and boundary polygons
- Transport vehicle license plates and driver identifiers
- Intermediate stop coordinates and transit itineraries
- Purchase prices, margins, and commercial contract terms

---

## 7. Verification Procedures

The design system repository includes comprehensive automated verification scripts:

1. **Token Contrast Audit**: `python3 scripts/build-tokens.py --check` recalculates relative luminance across all 48 semantic token pairs and verifies zero failures against Level AAA requirements.
2. **Headless Chrome Previews**: `bash scripts/render-previews.sh` renders full-resolution PNG previews of the brand sheet, master design sheet, buyer lookup (phone and desktop), and alert cards.
3. **Zero-Emoji Enforcement**: `grep -rnP '[\x{1F300}-\x{1FAD6}\x{2600}-\x{27BF}]' .` verifies that zero emojis exist across code, styles, documentation, and assets.
