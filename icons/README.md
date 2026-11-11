# System Icons

This directory provides the official SVG icon set for the Aroma Pacífico design system across the three applications: the Coffee Grower offline-first PWA, the Transporter custody app, and the Public Sack Traceability Portal.

Case statement point 7 mandates understandable icons that do not require extensive training manuals ("iconos entendibles sin un manual largo"). The icon set relies on universal physical metaphors (scales, thermometers, water droplets, calendar sheets, map markers, and delivery trucks) to ensure immediate comprehension by rural farmers, logistics drivers, warehouse workers, and international coffee buyers.

## Icon Inventory

| Icon | File | Visual Metaphor | Target Application & Semantic Use |
|---|---|---|---|
| QR Code | [`qr-code.svg`](qr-code.svg) | Square 2D barcode matrix | Sack registration scanning, printed label verification, public lookup code camera input. |
| Scale | [`scale.svg`](scale.svg) | Balance scale with central pivot | Wet-mill scale weighing input, tare adjustment, and gross 60 kg sack mass confirmation. |
| Droplet | [`droplet.svg`](droplet.svg) | Clean water drop contour | Moisture percentage indicator, crop humidity telemetry, and grain drying moisture target (10-12%). |
| Thermometer | [`thermometer.svg`](thermometer.svg) | Liquid bulb thermometer column | Ambient crop temperature telemetry, solar drying bed temperature, and grain heating alerts. |
| Calendar | [`calendar.svg`](calendar.svg) | Wall calendar page with rings | Processing dates: drying start date, drying completion date, and 60 kg sack packaging date. |
| Location | [`location.svg`](location.svg) | Map coordinate pin with inner aperture | Geographic origin indicator: department (Cauca, Huila, Tolima) and municipality names. |
| Package | [`package.svg`](package.svg) | Folded 3D isometric carton container | 60 kg burlap coffee sack inventory, batch aggregation, and warehouse stacking. |
| Truck | [`truck.svg`](truck.svg) | Commercial cargo vehicle profile | Transporter custody transfer, overland transit legs, and Buenaventura port freight movement. |
| Check Circle | [`check-circle.svg`](check-circle.svg) | Enclosed verification check stroke | Accepted sack state (`aceptado`), resolved crop alert, and successful GNSS custody handshake. |
| Alert Triangle | [`alert-triangle.svg`](alert-triangle.svg) | Equilateral warning triangle with marker | Caution and critical crop variable breaches, weight tolerance warnings, and connectivity gaps. |
| Cross Circle | [`x-circle.svg`](x-circle.svg) | Enclosed cancellation cross stroke | Rejected sack state (`rechazado`), invalid QR code format, and failed telemetry sync. |
| Clock | [`clock.svg`](clock.svg) | Circular analog clock face | Sack in preparation state (`en preparación`), delayed alert transit timestamp, and telemetry cadence. |
| Sun | [`sun.svg`](sun.svg) | Solar disc surrounded by ray ticks | Outdoor direct sunlight mode toggle (`data-contrast="outdoor"`), solar exposure level. |
| Shield Check | [`shield-check.svg`](shield-check.svg) | Armored crest with verification check | Buyer view data minimization assurance, cryptographic provenance seal, and privacy compliance. |
| Eye | [`eye.svg`](eye.svg) | Open visual iris contour | Public lookup inspection mode, previewing sack journey details, and telemetry audit viewing. |

## Technical Specification

All icons conform strictly to the following construction parameters:

| Parameter | Specification | Engineering Rationale |
|---|---|---|
| Coordinate Grid | 24 x 24 units (`viewBox="0 0 24 24"`) | Aligns with the 8-unit spatial layout grid and scales cleanly to 16, 24, 32, and 48 px. |
| Stroke Geometry | Outline stroke only, 2.0 unit uniform width | Outlined vectors maintain sharpness on low-DPI displays and retain contrast under glaring outdoor sunlight. |
| Line Joins and Caps | `stroke-linecap="round"` and `stroke-linejoin="round"` | Softened terminal joints eliminate visual distortion at low rendering resolutions. |
| Color Binding | `stroke="currentColor" fill="none"` | Icons dynamically inherit semantic text and badge tokens without requiring duplicate asset files. |
| Zero External Rasters | Pure vector XML path coordinates | Guarantees zero HTTP round-trips, sub-millisecond parsing, and complete offline availability. |

## Sizing and Spatial Rules

| Context | Visual Box | Surrounding Padding | Minimum Touch Target |
|---|---|---|---|
| Status Badge Icon | 16 x 16 px | 0 px (inline with text) | Governed by parent badge height (32 px) |
| Form Input Prefix/Suffix | 20 x 20 px | 8 px horizontal | Governed by input field height (48 px) |
| Standard Button Icon | 20 x 20 px | 8 px right margin | Governed by button height (48 px) |
| Standalone Interactive Icon | 24 x 24 px | 12 px uniform | 48 x 48 px touch target (WCAG 2.5.5 Level AAA) |
| Outdoor Field Action Target | 24 x 24 px | 16 px uniform | 56 x 56 px touch target (optimized for gloved hands) |

## Semantic Rules and Usage Directives

1. Icons must always be paired with explicit text labels in informative contexts. In accordance with WCAG 2.2 Success Criterion 1.4.1 (Use of Color), an icon and its color token must never be the sole mechanism for conveying critical status or severity.
2. In interactive standalone buttons, provide an accessible description via `aria-label` or visually hidden text (`.ap-visually-hidden`).
3. Decorative icons accompanying redundant text must include `aria-hidden="true"` to prevent duplicate screen reader announcements.
4. Emojis and bitmap pictograms are strictly prohibited across all application layouts, code comments, and documentation.
