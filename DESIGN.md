---
name: Tack-Black Tactical System
colors:
  surface: '#10131a'
  surface-dim: '#10131a'
  surface-bright: '#363940'
  surface-container-lowest: '#0b0e14'
  surface-container-low: '#191c22'
  surface-container: '#1d2026'
  surface-container-high: '#272a31'
  surface-container-highest: '#32353c'
  on-surface: '#e1e2eb'
  on-surface-variant: '#e2bfb9'
  inverse-surface: '#e1e2eb'
  inverse-on-surface: '#2e3037'
  outline: '#a98984'
  outline-variant: '#5a413d'
  surface-tint: '#ffb4a8'
  primary: '#ffb4a8'
  on-primary: '#690000'
  primary-container: '#800000'
  on-primary-container: '#ff8371'
  inverse-primary: '#b22b1d'
  secondary: '#c3c6cf'
  on-secondary: '#2d3138'
  secondary-container: '#454951'
  on-secondary-container: '#b5b8c1'
  tertiary: '#c2c6d1'
  on-tertiary: '#2c3139'
  tertiary-container: '#383d46'
  on-tertiary-container: '#a3a7b2'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad4'
  primary-fixed-dim: '#ffb4a8'
  on-primary-fixed: '#410000'
  on-primary-fixed-variant: '#8f0f07'
  secondary-fixed: '#dfe2ec'
  secondary-fixed-dim: '#c3c6cf'
  on-secondary-fixed: '#181c22'
  on-secondary-fixed-variant: '#43474e'
  tertiary-fixed: '#dee2ed'
  tertiary-fixed-dim: '#c2c6d1'
  on-tertiary-fixed: '#171c24'
  on-tertiary-fixed-variant: '#424750'
  background: '#10131a'
  on-background: '#e1e2eb'
  surface-variant: '#32353c'
typography:
  headline-xl:
    fontFamily: Montserrat
    fontSize: 40px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: 0.01em
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.08em
  data-display:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: '1.2'
    letterSpacing: 0.02em
  headline-lg-mobile:
    fontFamily: Montserrat
    fontSize: 20px
    fontWeight: '700'
    lineHeight: '1.2'
spacing:
  unit: 4px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 32px
  max-width: 1440px
---

## Brand & Style

The design system is engineered for high-stakes digital navigation and automation. It targets power users, developers, and security-conscious operators who require an interface that feels like a mission-critical tactical overlay. The brand personality is authoritative, precise, and uncompromisingly technical.

The style is a fusion of **Tactical Futurism** and **Minimalist Dark Mode**. It leverages deep blacks to eliminate distraction, using surgical strikes of glowing maroon to draw attention to actionable intelligence. The UI should evoke the feeling of a heads-up display (HUD), prioritizing data density and system transparency through a rigorous grid-based architecture.

## Colors

The palette is anchored in `#0B0E14` (Deep Black) to provide a non-reflective, infinite canvas. 

- **Primary:** `#800000` (Maroon) is used for critical call-to-actions, active states, and system alerts.
- **Secondary:** `#2A2E35` (Dark Gray) serves as the primary border color and surface-tier 1.
- **Interactive Accents:** A brighter `#FF0000` is reserved for low-opacity glows and pulsing "active" status indicators.
- **Typography:** Pure `#FFFFFF` (Stark White) ensures maximum legibility against the dark void.

## Typography

This design system utilizes a dual-font strategy to balance high-level navigation with granular technical data.

- **Montserrat** (Headlines): Used for structural headers and primary navigation. Its geometric weight provides the "futuristic" anchor for the UI.
- **Inter** (Body): Used for tooltips, descriptions, and long-form content to maintain high readability.
- **JetBrains Mono** (Technical/Labels): Every interactive label, status badge, and log entry must use JetBrains Mono. This reinforces the "agent" persona and the feeling of direct machine interaction.
- **Case Styling:** Headlines and labels should be frequently set in `UPPERCASE` to reinforce the tactical tone.

## Layout & Spacing

The layout follows a **Rigid Grid** philosophy. Every element must align to a 4px baseline grid. 

- **Grid Model:** 12-column fluid grid for desktop with 1px thin borders separating primary sections (Sidebar, Main Terminal, Inspector).
- **Tactical Borders:** Avoid heavy padding; use thin `#2A2E35` borders to define zones.
- **Density:** Information density should be high. Use "Compact" spacing for data tables and logs, and "Default" spacing for configuration panels.
- **Mobile:** Elements reflow into a single column stack. The sidebar collapses into a bottom-anchored tactical dock.

## Elevation & Depth

Depth is conveyed through **Tonal Layering** and **Luminescent Accents** rather than traditional shadows.

- **Base Layer:** `#0B0E14` (The Void).
- **Surface Layer:** `#151921` (Raised panels/Cards).
- **Tactical Glow:** Active elements use a `0px 0px 8px` outer glow in `#800000` at 40% opacity. 
- **Backdrop:** Use a slight `blur(10px)` on any overlaying modals to maintain the sense of a unified HUD, with a semi-transparent black fill.

## Shapes

The design system uses **Sharp (0px)** corners for all primary containers, buttons, and inputs to emphasize a professional, military-grade precision. 

Occasional 45-degree "clipped corners" (dog-ear style) can be used for status badges or high-level navigation tabs to reinforce the futuristic military aesthetic. Never use rounded corners or "pills" as they detract from the tactical narrative.

## Components

### Buttons & Controls
- **Primary Button:** Solid `#800000` fill, white JetBrains Mono text (all caps). No border. On hover, add a 1px white inner border.
- **Ghost Button:** 1px border of `#2A2E35`. Text in white. On hover, border changes to `#800000` with a subtle outer glow.
- **Active State:** Elements like "Recording" or "Agent Processing" must feature a 2-second pulse animation using the Primary Maroon color.

### Inputs & Terminal
- **Input Fields:** Dark background (`#05070A`) with a bottom-only 1px border. Focus state turns the border Maroon with a blinking cursor.
- **Terminal Log:** Sequential lines of JetBrains Mono text. Timestamps in Tertiary Gray. Success messages in Dim Green; Errors in Primary Maroon.

### Navigation & Status
- **Tactical Tabs:** Rectangular blocks. Active tab has a top 2px Maroon border.
- **Status Chips:** Small, rectangular labels with a low-opacity Maroon background and bright Maroon text.
- **Data Cards:** 1px `#2A2E35` border. Use thin crosshair icons in the corners to simulate a targeting system or HUD frame.