# Troubleshooting Log

This log records operational friction points, edge cases, root causes, and resolutions encountered during the implementation and verification of the Aroma Pacífico design system.

---

## Entry 1: Headless Google Chrome Preview Rendering Pipeline

### Context & Symptom
During initial verification of visual artifact rendering via `scripts/render-previews.sh`, executing `google-chrome --headless` without newer container flags resulted in intermittent blank raster outputs or process hangs when capturing high-resolution full-page screenshots.

### Root Cause
Modern headless Chromium requires the `--headless=new` rendering engine flag to accurately evaluate CSS layout grids, CSS custom property inheritance, SVG clipping masks, and web font fallbacks in off-screen framebuffers. Legacy headless modes failed to render complex SVG masks and multi-column grid layouts.

### Resolution Applied
Updated `scripts/render-previews.sh` to execute Google Chrome with explicit headless flags:
```bash
"$chrome" --headless=new --disable-gpu --hide-scrollbars \
  --allow-file-access-from-files --force-device-scale-factor=1 \
  --window-size="$width,$height" \
  --screenshot="$out/$name.png" "file://$root/$page"
```

### Preventive Architecture
All visual preview generation relies strictly on `scripts/render-previews.sh`. Rendering scripts must specify explicit viewport dimensions, disable GPU compositing, and force device pixel scale factor to ensure identical raster outputs across Linux development containers and CI/CD runners.

---

## Entry 2: Mobile Safari and Android Chrome Form Input Auto-Zoom

### Context & Symptom
When testing mobile phone input fields for 60 kg sack weighing scale measurements and code entry, focusing the input field on iOS Safari and mobile Chrome triggered an automatic viewport zoom, obscuring surrounding form labels and field hints.

### Root Cause
Mobile WebKit and Blink browsers enforce an automatic zoom behavior on input focus whenever the declared `font-size` of the form control is less than 16 px (e.g. 14 px or 15 px).

### Resolution Applied
Configured `--ap-typography-phone-body-size` and `.ap-input` to an explicit minimum of 16 px (`1rem`), with 48 px minimum control height. For high-prominence numerical entries such as scale gross mass, font size is increased to 20 px bold.

### Preventive Architecture
Base component styles in `components/components.css` enforce a strict rule that no `<input>`, `<select>`, or `<textarea>` element may declare a font size below 16 px on viewports under 600 px width.

---

## Entry 3: WCAG AAA Relative Luminance Contrast Thresholds for Outdoor Use

### Context & Symptom
Standard accessible web palettes targeting WCAG Level AA (4.5:1 for normal text) exhibited noticeable degradation under direct sunlight simulation (high ambient glare and screen reflection). In particular, amber caution alerts and subtle gray borders became virtually indistinguishable from white surfaces.

### Root Cause
Ambient illuminance in tropical coffee drying patios frequently exceeds 50,000 lux. Under direct sunlight, surface reflections reduce the effective perceived contrast ratio by more than 50%, transforming a 4.5:1 ratio into an unreadable wash.

### Resolution Applied
Elevated the project-wide outdoor text contrast mandate (OUTDOOR-1) to WCAG Level AAA (7.0:1 minimum). For amber alerts, replaced pale yellow text with dark amber hue token `#5C3D00`, achieving an 8.82:1 ratio. For subtle borders, introduced dark neutral `#6B655E` with 5.76:1 ratio, and formulated OUTDOOR-8 high-contrast mode (`data-contrast="outdoor"`) providing pure black on pure white (21.0:1 ratio).

### Preventive Architecture
Automated script `scripts/build-tokens.py` calculates relative luminance across all 48 semantic token pairs and triggers a build failure if any pair falls below 7.0:1 for text or 3.0:1 for non-text boundaries.
