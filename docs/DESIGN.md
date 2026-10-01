---
name: Fluent Institutional Green
colors:
  surface: '#f7f9ff'
  surface-dim: '#d0dbe8'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#ecf4ff'
  surface-container: '#e4effc'
  surface-container-high: '#dee9f6'
  surface-container-highest: '#d8e4f1'
  on-surface: '#121d26'
  on-surface-variant: '#3f4a38'
  inverse-surface: '#27323b'
  inverse-on-surface: '#e7f2ff'
  outline: '#6f7b66'
  outline-variant: '#becbb3'
  surface-tint: '#226d00'
  primary: '#226d00'
  on-primary: '#ffffff'
  primary-container: '#39a900'
  on-primary-container: '#0c3400'
  inverse-primary: '#6fdf43'
  secondary: '#3a5f94'
  on-secondary: '#ffffff'
  secondary-container: '#9fc2fe'
  on-secondary-container: '#294f83'
  tertiary: '#006e2d'
  on-tertiary: '#ffffff'
  tertiary-container: '#44a65a'
  on-tertiary-container: '#003412'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#8afd5d'
  primary-fixed-dim: '#6fdf43'
  on-primary-fixed: '#052100'
  on-primary-fixed-variant: '#185200'
  secondary-fixed: '#d5e3ff'
  secondary-fixed-dim: '#a7c8ff'
  on-secondary-fixed: '#001b3c'
  on-secondary-fixed-variant: '#1f477b'
  tertiary-fixed: '#94f8a2'
  tertiary-fixed-dim: '#79db88'
  on-tertiary-fixed: '#002109'
  on-tertiary-fixed-variant: '#005320'
  background: '#f7f9ff'
  on-background: '#121d26'
  surface-variant: '#d8e4f1'
  sena-green-bright: '#39A900'
  sena-green-deep: '#007832'
  institutional-navy: '#003366'
  institutional-slate: '#0B3553'
  fluent-acrylic-bg: '#FFFFFFCC'
  fluent-mica-tint: '#F3F7F4'
  badge-open-bg: '#EBF8E8'
  badge-open-text: '#007832'
  badge-closing-bg: '#FFF4E5'
  badge-closing-text: '#B25E00'
typography:
  display:
    fontFamily: Work Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  display-mobile:
    fontFamily: Work Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Work Sans
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Work Sans
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Work Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Work Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  title-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  title-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 22px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.03em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system serves the Escuela Nacional de Instructores (ENI) within SENA, orchestrating official faculty development calls, pedagogic training programs, and academic career pathways. The brand personality embodies institutional trust, vocational prestige, pedagogical innovation, and accessible public service. 

The aesthetic harmonizes Microsoft Fluent Design principles with the vibrant institutional identity of SENA Colombia. Key characteristics include:
- **Acrylic & Mica Translucency**: Restrained, calibrated backdrop filters (`backdrop-blur-md`, subtle alpha layering) reflecting Fluent's layered depth without sacrificing institutional readability or performance.
- **Subtle Layered Depth**: Elevation built through multi-layered ambient light, delicate perimeter highlights (1px translucent inner borders), and surface elevation rather than harsh drop shadows.
- **Structured Precision**: Systematic typography, generous whitespace, and balanced informational hierarchy that elevates functional administrative data into an inviting professional experience.

## Colors

The color palette anchors on the distinctive SENA green paired with Colombia's traditional public education navy blues, refined into Fluent-style surface tokens:

- **Primary (`#39A900`)**: The iconic, energetic SENA green. Reserved for primary calls-to-action, key progress highlights, active navigational state markers, and signature accents.
- **Secondary (`#003366`)**: Deep institutional navy. Provides authority, grounding header bars, section headings, and primary contrast elements.
- **Tertiary (`#007832`)**: Deep leaf green. Emphasizes secondary affirmative states, verified credentials, and high-contrast accessible text pairings where `#39A900` needs darker anchor support.
- **Neutral (`#5A6570`)**: Balanced slate-gray controlling structural borders, muted metadata, sub-labels, and background surface gradations.

### Surface System
- **Canvas Base**: `#F8FAF8` tinted neutral off-white mimicking Windows Mica material.
- **Acrylic Glass**: `#FFFFFFE6` with 16px background blur and `1px solid rgba(255, 255, 255, 0.6)` inner inset borders.
- **Card Surface**: High-purity `#FFFFFF` resting on mica tint with subtle 1px border `rgba(0, 51, 102, 0.08)`.

## Typography

The typographic hierarchy pairs **Work Sans** for executive, forward-looking headlines with **Inter** for crisp, utilitarian UI readability.

- **Work Sans** brings structural balance and contemporary legibility to program titles, portal headers, and dashboard summaries. It provides structural kinship with institutional identity while preventing visual fatigue.
- **Inter** handles data-dense tables, application rubrics, multi-field metadata tags (e.g., *Horas*, *Sede*, *Cupos*), and form inputs with high legibility down to 11px.
- Numerical figures (e.g., convocatoria codes, dates, hours) utilize tabular figures (`tnum`) for aligned scanning across lists and cards.

## Layout & Spacing

The layout adopts an adaptive 12-column grid system tuned for productivity software and administrative portal environments.

- **Desktop (1200px+)**: 12 columns with 24px (`1.5rem`) gutters and a max content container of 1360px centered on screen. Left-hand sticky filter panel spans 3 columns; active call listings span 9 columns.
- **Tablet (768px - 1199px)**: 8 columns with 16px (`1rem`) gutters and 24px margins. Filters collapse into an off-canvas drawer or top horizontal filter chips.
- **Mobile (< 768px)**: 4 columns with 12px gutters and 16px outer margins (`margin-mobile`). Cards transition to a single-column stacked layout with full-width action strips.
- **Rhythm**: Standard spacing increments follow a strict 4px/8px scale, maintaining spatial alignment across cards, metadata clusters, and toolbar controls.

## Elevation & Depth

Depth in this system reflects the Microsoft Fluent material ethos, combining translucent acrylics, light-bleed surfaces, and ambient layered shadows:

- **Level 0 (Flat Canvas)**: Neutral surface (`#F8FAF8`) used for main page backdrop, providing subtle warmth behind cards.
- **Level 1 (Mica / Frosted Cards)**: Default state for convocatoria cards and interactive tiles. 
  - Background: `rgba(255, 255, 255, 0.88)` with `backdrop-filter: blur(12px)`.
  - Border: `1px solid rgba(0, 51, 102, 0.08)`.
  - Shadow: `0px 2px 4px rgba(11, 53, 83, 0.04), 0px 1px 2px rgba(11, 53, 83, 0.02)`.
- **Level 2 (Hover / Elevated Cards)**:
  - Transition: `all 200ms cubic-bezier(0.16, 1, 0.3, 1)`.
  - Transform: `translateY(-2px)`.
  - Border: `1px solid rgba(57, 169, 0, 0.35)`.
  - Shadow: `0px 8px 16px -4px rgba(0, 51, 102, 0.08), 0px 4px 8px -2px rgba(11, 53, 83, 0.04)`.
- **Level 3 (Acrylic Flyouts, Modals & Menus)**:
  - Background: `rgba(255, 255, 255, 0.94)` with `backdrop-filter: blur(20px)`.
  - Border: `1px solid rgba(255, 255, 255, 0.8)`.
  - Shadow: `0px 16px 32px -8px rgba(0, 51, 102, 0.14), 0px 4px 12px rgba(0, 0, 0, 0.04)`.

## Shapes

The geometric identity relies on soft, ergonomic corners (Level 2 roundedness), aligning with modern Fluent components:

- **Base Radius (8px / `0.5rem`)**: Applied to buttons, inputs, drop-downs, metadata tags, and segmented tabs.
- **Container Radius (12px / `0.75rem` - `rounded-lg`)**: Applied to convocatoria cards, preview panels, dialog containers, and elevated modules.
- **Surface Outer Radius (16px / `1rem` - `rounded-xl`)**: Applied to modal overlays, large visual banners, and dashboard hero summaries.
- **Capsule / Full Radius (`9999px`)**: Exclusively reserved for status pill badges (e.g., *Convocatoria Abierta*, *Cupos Agotados*) and icon-only floating action counters.

## Components

### Convocatoria Cards
- **Structure**: Multi-zone card featuring an acrylic header with an institutional tag and status indicator, a central body containing program title and competence code, and a bottom metadata grid (Modalidad, Sede/Regional, Fechas límite, Horas certificables).
- **Border**: Subtle 1px translucent perimeter with accent left border (`3px solid #39A900`) for priority calls.
- **Hover Microinteraction**: Seamless lift (`-2px`), shadow expansion, and slight illumination of the "Inscribirse / Ver detalles" button.

### Buttons
- **Primary**: Background `#39A900`, text `#FFFFFF`, font weight 600. On hover: `#007832` with gentle 150ms ease. Active state includes 0.98 scale micro-compression.
- **Secondary / Fluent Outline**: Background `transparent`, border `1.5px solid #003366`, text `#003366`. On hover: `rgba(0, 51, 102, 0.04)` fill.
- **Subtle / Ghost**: No border, text `#0B3553`, padding 8px 12px. On hover: `rgba(0, 51, 102, 0.06)` rounded to 8px.

### Chips & Metadata Tags
- **Area & Modality Chips**: Neutral tinted pills (`rgba(0, 51, 102, 0.05)` background, `#0B3553` text, `border: 1px solid rgba(0, 51, 102, 0.1)`).
- **Status Badges**:
  - *Abierta*: Background `#EBF8E8`, text `#007832`, with an optional pulsing 6px green status dot.
  - *Próxima*: Background `#F0F4F8`, text `#003366`.
  - *Cierre Inminente*: Background `#FFF4E5`, text `#B25E00`.

### Form Inputs & Search Filters
- **Fields**: Background `#FFFFFF`, height 40px, border `1px solid rgba(90, 101, 112, 0.3)`.
- **Focus State**: Accent bottom bar or 2px outline in `#39A900` with subtle outward glow (`box-shadow: 0 0 0 3px rgba(57, 169, 0, 0.15)`).

### Selection Controls
- **Checkboxes**: 18px rounded square (4px border radius). Checked state fills with `#39A900` and displays a crisp white checkmark.
- **Radio Buttons**: Dual-circle Fluent design. Selected state shows a `#39A900` ring encircling an 8px solid center dot.

### Lists & Data Grids
- Clean alternating rows with transparent and `rgba(0, 51, 102, 0.015)` fills. Dividers use hairline `rgba(0, 51, 102, 0.06)`. Hovering a row triggers a tinted `#F3F7F4` highlight.