# Base Components and Outdoor Contrast Rules

This document specifies the five base components mandated by case statement point 7 ("Componentes base: botón, campo, alerta, tarjeta de saco y distintivo de estado") and defines the eight outdoor contrast and usability rules (OUTDOOR-1 through OUTDOOR-8).

The components are implemented in [`components.css`](components.css) and wired directly to the W3C design tokens in [`tokens/tokens.css`](../tokens/tokens.css).

---

## Base Component Specifications

### 1. Button (`.ap-button`)

The button component provides primary, secondary, and destructive actions across phone and web viewports.

| Variant / State | CSS Class | Visual Styling | Minimum Contrast Ratio | WCAG Compliance |
|---|---|---|---|---|
| Primary | `.ap-button--primary` | Background `--ap-color-action-primary` (`#0E4C55`), text white (`#FFFFFF`) | 9.62:1 | Level AAA (OUTDOOR-1) |
| Secondary | `.ap-button--secondary` | Background white (`#FFFFFF`), text and border `--ap-color-action-primary` (`#0E4C55`) | 9.62:1 | Level AAA (OUTDOOR-1) |
| Danger | `.ap-button--danger` | Background `--ap-color-action-danger` (`#9E1C14`), text white (`#FFFFFF`) | 7.98:1 | Level AAA (OUTDOOR-1) |
| Focus Indicator | `:focus-visible` | 3 px solid `--ap-color-border-focus` (`#0E4C55`), 2 px offset | 9.62:1 on white | WCAG 2.4.7 / 2.4.11 |
| Disabled | `:disabled` | Background `--ap-color-action-disabled` (`#ECE6DE`), text `--ap-color-neutral-600` (`#6B655E`) | 4.64:1 | Level AA (exempt 1.4.3) |
| Field Target | `.ap-button--large` | 56 px minimum height, 24 px padding, 18 px text | 9.62:1 | OUTDOOR-3 |

### 2. Form Field and Input (`.ap-field`, `.ap-input`)

Designed for quick, accurate data entry by farmers weighing sacks at wet mills and drivers verifying loads in transit.

| Element | Specification | Rationale |
|---|---|---|
| Field Label | 14 px bold semibold (`--ap-typography-web-label-size`), `#1A1714` text | High-contrast label placed directly above inputs prevents ambiguity under sunlight glare. |
| Input Container | 48 px minimum height, 16 px base font size, 2 px solid border (`#6B655E`) | 16 px font size prevents mobile Safari/Chrome auto-zoom on touch focus; 5.76:1 border contrast. |
| Code Input | `.ap-input--code`: monospace font (`--ap-font-family-mono`), uppercase, bold | Distinguishes alphanumeric characters (e.g. `O` vs `0`, `I` vs `1`) when typing sack codes. |
| Scale Mass Input | `.ap-input--numeric`: right-aligned, 20 px bold, fixed suffix unit (`kg`) | Optimizes scale weight verification with prominent numerals visible at arm's length. |
| Focus State | 3 px border (`--ap-color-border-focus`), subtle focus ring | Meets non-text contrast requirement (OUTDOOR-2). |
| Error State | `.ap-field--error`: 2 px red border (`#9E1C14`), red tinted background (`#FBE4E2`) | Accompanied by inline error message and alert triangle icon (never color alone). |

### 3. Crop Alert Banner (`.ap-alert`)

Displays agronomic and telemetric alerts across five standardized severity levels. Each alert includes an icon, title, description, and dual timestamp metadata.

| Severity | Subtle Background | Border (2 px) | Text Color | Ratio | Meaning |
|---|---|---|---|---|---|
| Critical | `#FBE4E2` (`red.100`) | `#9E1C14` (`red.700`) | `#7A1610` (`red.800`) | 8.87:1 AAA | Immediate crop hazard requiring agronomist inspection or drone confirmation. |
| Caution | `#FBF1DC` (`amber.100`) | `#A86B00` (`amber.500`) | `#5C3D00` (`amber.700`) | 8.82:1 AAA | Telemetry parameter trending out of optimal agronomic range. |
| Notice | `#E3EEFB` (`blue.100`) | `#1F63B5` (`blue.500`) | `#0B3A6E` (`blue.800`) | 9.70:1 AAA | Scheduled flight window notification, logistics dispatch update. |
| Resolved | `#E2F3E6` (`green.100`) | `#23803F` (`green.500`) | `#0F4D22` (`green.800`) | 8.64:1 AAA | Microclimate variable stabilized, inspection task verified. |
| No-Data | `#ECE6DE` (`neutral.100`) | `#6B655E` (`neutral.600`) | `#1A1714` (`neutral.900`) | 14.40:1 AAA | Farm sensor node silent for more than 24 hours (case statement section 6). |

Dual timestamp feature: When store-and-forward telemetry is delayed due to mountainous terrain or lack of network connectivity, the alert displays both the sampling time ("Medido: 06:15") and the drained delivery time ("Recibido: 08:30"), ensuring farmers understand when the reading actually occurred.

### 4. Sack Card (`.ap-sack-card`)

Presents individual sack details in mobile list views (farmer inventory, driver cargo manifests, and warehouse receiving docks).

| Card Region | Visual Elements | Token & Contrast |
|---|---|---|
| Card Header | Alphanumeric sack code and status badge | Code set in bold monospace (`--ap-color-brand-primary-900`, 17.85:1 contrast). |
| Primary Metric | 60 kg gross scale mass | 24 px bold display typography with attached unit suffix (`kg`). |
| Origin Metadata | Department and municipality names | Clean typography paired with location pin icon. |
| Lot Reference | Drying lot identifier and date stamp | High-contrast secondary text (`#4A4540`, 9.47:1 contrast on white). |
| Card Border | 2 px solid `--ap-color-border-strong` (`#6B655E`) | 5.76:1 non-text boundary contrast against light background. |

### 5. Status Badge (`.ap-badge`)

Maps the seven internal platform states of the sack lifecycle (Part C of the case statement) into four public status badges (PD-154):

| Public Badge | Mapped Lifecycle States | Background & Border | Text & Icon Color | Contrast Ratio |
|---|---|---|---|---|
| En preparación | `in_preparation` | `#FBF1DC` / `#A86B00` border | `#5C3D00` (`amber.700`) | 8.82:1 (AAA) |
| En viaje | `in_transit_to_center`, `in_transit_to_port` | `#E3EEFB` / `#1F63B5` border | `#0B3A6E` (`blue.800`) | 9.70:1 (AAA) |
| Aceptado | `at_center_accepted`, `delivered_at_port_accepted` | `#E2F3E6` / `#23803F` border | `#0F4D22` (`green.800`) | 8.64:1 (AAA) |
| Rechazado | `at_center_rejected`, `delivered_at_port_rejected` | `#FBE4E2` / `#C0281C` border | `#7A1610` (`red.800`) | 8.87:1 (AAA) |

---

## Outdoor Contrast Rules

Field testing in the coffee landscapes of Cauca, Huila, and Tolima and on the maritime docks of Buenaventura presents extreme environmental constraints: direct equatorial sunlight, high ambient glare, variable weather, and tactile usage with soiled or gloved hands. The following eight rules are binding across all application layouts.

### OUTDOOR-1: Minimum 7:1 (WCAG AAA) Contrast for Text and Meaningful Icons

All body copy, headers, numerical measurements, status labels, and functional iconography must achieve a minimum relative luminance contrast ratio of 7.0:1 against their immediate background surface.

Standard Web Content Accessibility Guidelines (WCAG) Level AA specifies 4.5:1 for normal text. However, ambient outdoor illuminance in coffee drying patios frequently exceeds 50,000 lux, causing glare that washes out subtle contrast. Requiring 7.0:1 (WCAG Level AAA) ensures legibility even when direct sunlight strikes phone screens.

Verification: All 48 semantic token pairs are programmatically checked by `scripts/build-tokens.py` and validated in `tokens/contrast-report.md`. Zero token pairs fail this threshold.

### OUTDOOR-2: Minimum 3:1 Non-Text Boundary Contrast (WCAG 1.4.11)

All component perimeters, input borders, active focus indicators, and status badge edges must maintain at least a 3.0:1 contrast ratio against the surrounding container surface.

Buttons and input fields must remain identifiable as interactive elements even under harsh surface reflections. Thin 1 px gray borders are prohibited outdoors; interactive boundaries use 2 px solid borders with dark neutral or saturated brand tokens.

### OUTDOOR-3: Touch Target Ergonomics and Finger Spacing

All interactive components (buttons, camera triggers, list selections, and navigation tabs) must adhere to the following physical dimensions:

| Operation Mode | Minimum Target Box | Minimum Spacing Between Targets | Primary Use Case |
|---|---|---|---|
| Standard Mobile | 48 x 48 px | 8 px | Single-hand thumb navigation in dry conditions. |
| Field / Gloved Mode | 56 x 56 px | 12 px | Wet-mill sack weighing, harvest handling, and vehicle dock loading. |

### OUTDOOR-4: Direct Sunlight Glare Mitigation and Surface Hierarchy

1. Surfaces default to crisp white (`--ap-color-surface-default`, `#FFFFFF`) or light warm parchment (`--ap-color-surface-subtle`, `#F6F2EC`).
2. Dark mode is prohibited as the default field UI theme because glossy screen glass transforms dark screens into mirrors reflecting direct sunlight.
3. Shadows and diffuse elevation blurs are prohibited for defining card bounds. Structural separation is achieved through explicit 2 px solid borders and neutral background shifts.

### OUTDOOR-5: Redundant Semantic Encoding (Zero Color-Alone)

Color must never serve as the sole mechanism for conveying status, severity, or operational outcomes.

1. Status badges must pair the hue token with a distinct SVG icon (`clock.svg`, `truck.svg`, `check-circle.svg`, `x-circle.svg`) and uppercase descriptive text.
2. Form validation errors must combine red borders with an inline warning icon and text explanation.
3. Crop alert levels must include severity titles (e.g., "Alerta Crítica", "Precaución") alongside color styling.

### OUTDOOR-6: High-Visibility Focus and Active States

1. Interactive focus states render a 3 px solid focus ring using `--ap-color-border-focus` (`#0E4C55`, 9.62:1 contrast against white) with a 2 px outer offset.
2. Pressed states (`:active`) darken button surfaces to provide immediate visual tactile feedback without reliance on micro-animations.

### OUTDOOR-7: Arm's Length Legibility and Scale Typography

1. Body text on phone viewports must never render below 16 px (`--ap-typography-phone-body-size`).
2. Primary metrics (gross scale mass in kg, drying moisture percentage, and grain temperature) must render at minimum 24 px bold display typography (`--ap-typography-phone-value-size`).
3. Alphanumeric sack codes must render in monospace font with wide letter spacing (0.05 em) to allow legibility at arm's length while handling 60 kg sacks.

### OUTDOOR-8: Dedicated High-Contrast Mode (`[data-contrast="outdoor"]`)

The design system incorporates an automatic or user-activated extreme outdoor mode triggered via the attribute `[data-contrast="outdoor"]`.

When active:
- Primary and secondary text becomes pure solid black (`#000000`, `--ap-color-neutral-1000`) on solid white (`#FFFFFF`, `--ap-color-neutral-0`), achieving an absolute maximum 21.0:1 contrast ratio.
- All button borders, input borders, and card boundaries increase to 3 px solid black.
- Status badges and alert containers keep their semantic background tints but gain 3 px solid black perimeters, ensuring complete clarity under extreme glare conditions.
