---
name: Pastel Ledger
colors:
  surface: '#f9f9ff'
  surface-dim: '#cfdaf2'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  surface-container: '#e7eeff'
  surface-container-high: '#dee8ff'
  surface-container-highest: '#d8e3fb'
  on-surface: '#111c2d'
  on-surface-variant: '#494454'
  inverse-surface: '#263143'
  inverse-on-surface: '#ecf1ff'
  outline: '#7b7486'
  outline-variant: '#cbc3d7'
  surface-tint: '#6d3bd7'
  primary: '#6b38d4'
  on-primary: '#ffffff'
  primary-container: '#8455ef'
  on-primary-container: '#fffbff'
  inverse-primary: '#d0bcff'
  secondary: '#00668a'
  on-secondary: '#ffffff'
  secondary-container: '#40c2fd'
  on-secondary-container: '#004d6a'
  tertiary: '#006947'
  on-tertiary: '#ffffff'
  tertiary-container: '#00855b'
  on-tertiary-container: '#f5fff6'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e9ddff'
  primary-fixed-dim: '#d0bcff'
  on-primary-fixed: '#23005c'
  on-primary-fixed-variant: '#5516be'
  secondary-fixed: '#c4e7ff'
  secondary-fixed-dim: '#7bd0ff'
  on-secondary-fixed: '#001e2c'
  on-secondary-fixed-variant: '#004c69'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f9f9ff'
  on-background: '#111c2d'
  surface-variant: '#d8e3fb'
typography:
  headline-xl:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
  headline-xl-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
  code-amount:
    fontFamily: JetBrains Mono
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter-xs: 0.25rem
  gutter-sm: 0.5rem
  gutter-md: 1rem
  gutter-lg: 1.5rem
  gutter-xl: 2rem
  gutter-2xl: 3rem
  card-padding-sm: 1rem
  card-padding-md: 1.5rem
  card-padding-lg: 2rem
---

## Brand & Style

This design system establishes a warm, delightful, and hyper-organized aesthetic tailored for an intelligent receipt and expense processing agent. The interface balances calm productivity with playful charm—transforming tedious administrative overhead into an inviting, tactile interaction. 

The aesthetic is anchored in **Soft Tactile Paper & Modern Pastel**:
- **Character:** Friendly, precise, approachable, and soothing without sacrificing high-density data utility.
- **Atmosphere:** Clean paper stationery, soft daylight illumination, creamy base tones, and pill-shaped structural accents.
- **Tone:** Crisp charcoal typography guarantees legibility, while purposeful pastel tones tag, classify, and elevate receipt metadata with zero visual aggression or harsh neon saturations.

## Colors

The palette pairs high-contrast text with soft, candy-tinted surfaces. Backgrounds drift between warm pearl white and creamy buttermilk, avoiding harsh sterile hex codes.

### Palette Architecture
- **Base Canvas (`#FBFBFE` / `#F8FAFC`):** Soft buttermilk pearl provides an easy-on-the-eyes backdrop that makes pure white (`#FFFFFF`) card containers feel layered and physical.
- **Primary Accent (`#8B5CF6` / Container `#EDE9FE`):** Soft electric lavender. Represents AI extraction, primary actions, and system suggestions.
- **Secondary Sky (`#38BDF8` / Container `#E0F2FE`):** Powder and sky blue. Used for status indicators, active filters, and payment method indicators.
- **Tertiary Mint (`#10B981` / Container `#D1FAE5`):** Pastel pistachio. Applied to verified totals, matched transactions, and tax deductions.
- **Accent Coral / Melon (`#FB7185` / Container `#FFE4E6`):** Soft blush coral. Reserved for attention requirements, duplicate flags, and non-reimbursable notices.
- **Neutral Typography (`#1E293B`):** Deep warm slate charcoal. Used for all primary numbers, headers, and essential metadata to preserve crisp legibility across low-contrast pastels.
- **Subtle Borders (`#F1F5F9` & `#E2E8F0`):** Hairline outlines grounding floating elements onto the canvas.

## Typography

The typography couples the rounded, geometric warmth of **Plus Jakarta Sans** with the structural precision of **JetBrains Mono** for financial digits and currency amounts.

- **Plus Jakarta Sans:** Drives all headlines, navigational anchors, and body copy. Its friendly curves mirror the roundedness of the physical card components.
- **JetBrains Mono:** Dedicated exclusively to transaction figures, merchant codes, VAT rates, and extracted receipt timestamps to enable vertical tabular alignment.
- **Weights:** Maintain tight constraints: 400 (Regular) for descriptions and secondary text, 600 (SemiBold) for interactive labels and titles, and 700 (Bold) for ledger totals and primary headings.

## Layout & Spacing

A fluid grid architecture engineered for multi-column receipt parsing, split-screen viewing (receipt preview alongside extracted ledger tables), and cross-device responsive reflow.

- **Desktop (1024px+):** 12-column layout with 24px gutters and 32px margins. Allows a standard 5:7 split for side-by-side verification (5 columns for source paper document preview, 7 columns for editable parsed fields).
- **Tablet (768px - 1023px):** 8-column layout with 20px gutters. Slips into collapsible sidebar modes and toggleable document trays.
- **Mobile (< 768px):** 4-column layout with 16px margins and 12px gutters. Cards stack vertically with edge-to-edge scroll snapping for multi-item itemized slips.
- **Rhythm:** Spacing derives strictly from a 4px baseline, scaled primarily in multiples of 8px (8, 16, 24, 32) to reinforce a clean stationery feel.

## Elevation & Depth

Visual hierarchy emphasizes tactile card surfaces and layered paper sheets over deep artificial shadows:

- **Surface Layers:**
  - **Base Layer:** Canvas tone (`#FBFBFE`).
  - **Card Layer:** Pure white (`#FFFFFF`) with a 1px boundary stroke of `#F1F5F9`.
  - **Hover/Selected Layer:** Floats above other surfaces with a soft pastel-tinted atmospheric drop shadow.
- **Shadow Profile:**
  - *Resting Cards:* `0 2px 8px -2px rgba(30, 41, 59, 0.04), 0 1px 2px -1px rgba(30, 41, 59, 0.02)`.
  - *Hovered / Dragging Items:* `0 12px 24px -6px rgba(139, 92, 246, 0.12), 0 4px 8px -2px rgba(30, 41, 59, 0.04)`.
  - *Modals & Drawers:* `0 24px 48px -12px rgba(30, 41, 59, 0.08), 0 0 1px 1px rgba(226, 232, 240, 0.8)`.
- **Inner Depth:** Recessed components (such as upload drop-zones and form field interiors) use subtle background color drops (`#F8FAFC`) rather than inset shadows.

## Shapes

The form language relies on generous, soft radiuses to convey warmth while retaining architectural order:

- **Cards & Sheet Containers:** Standardized to `rounded-2xl` (16px/1rem radius) to evoke rounded cardstock and premium paper vouchers.
- **Chips, Badges, and Micro-actions:** Fully pill-shaped (`rounded-full` / 9999px) to produce soft touchpoints.
- **Input Fields & Text Areas:** Styled with `rounded-xl` (12px/0.75rem radius) to sit between pill buttons and structural card panels.

## Components

### Buttons
- **Primary:** Lavender solid (`#8B5CF6`), text white, `rounded-full`, 44px height for touch targets. Hover elevates with a soft violet halo: `0 4px 14px rgba(139, 92, 246, 0.35)`.
- **Secondary:** Lavender container (`#EDE9FE`), text `#7C3AED`, zero shadow, crisp 1px tone border (`#DDD6FE`).
- **Ghost:** Transparent, slate text (`#475569`), transitions to `#F1F5F9` on hover.

### Chips & Badges
- **Status Pills:** Pill-shaped (`rounded-full`), 24px height, horizontal padding 10px. 
  - *Processed/Valid:* Mint background (`#D1FAE5`), text `#065F46`, font `JetBrains Mono` 11px weight 600.
  - *Review Needed:* Melon background (`#FFE4E6`), text `#9F1239`.
  - *Categorizing:* Powder sky background (`#E0F2FE`), text `#0369A1`.
  - *AI Extraction:* Lavender background (`#EDE9FE`), text `#6D28D9`.

### Cards & Ledger Lists
- **Receipt Cards:** White paper cards (`#FFFFFF`) framed in `rounded-2xl` with a crisp 1px stroke of `#F1F5F9`. Features a subtle jagged receipt perforation tear line indicator when visualizing itemized splits.
- **List Rows:** Separated by 8px vertical gaps rather than single-pixel divider lines, creating a series of cleanly compartmentalized stacked pills.

### Input Fields & Selectors
- **Form Inputs:** Creamy tinted background (`#F8FAFC`), border 1.5px `#E2E8F0`, corner radius `12px`. Focus state shifts the border to `#8B5CF6` and produces a gentle 3px lavender outer ring (`rgba(139, 92, 246, 0.15)`).
- **Amount Inputs:** Prominent monospaced layout (`JetBrains Mono`), right-aligned, with currency denomination badges pinned softly inside the right margin.

### Checkboxes & Toggles
- **Checkboxes:** 20px boxes with `rounded-md` (6px radius), border 2px `#CBD5E1`. On check: fill `#8B5CF6` with a white custom tick.
- **Toggle Switch:** 24px height pill track (`#E2E8F0`), active fill `#10B981`. Thumb is pure white with a soft floating drop shadow.

### Receipt Inspector Drawer
- A sliding sheet anchored to the right viewport for granular item verification. Backed by frosted white paper (`backdrop-blur-md`, `rgba(255, 255, 255, 0.92)`), delivering clarity without losing workspace context.