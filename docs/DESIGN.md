# UX in Science Website Design System

## Purpose

This document defines the visual, interaction, accessibility, and implementation rules for a responsive UX in Science website built with semantic HTML and modern CSS.

In this specification, "responsible" means that the site is also:

- accessible to WCAG 2.2 AA;
- usable from small phones through large desktop displays;
- fast on slow networks and modest hardware;
- privacy-respecting, with no unnecessary tracking or third-party requests;
- progressively enhanced, so core content and navigation work without JavaScript.

The source of truth for brand colors and contrast is [`brand-assets/pdf/ux-in-science-brand-guide.md`](brand-assets/pdf/ux-in-science-brand-guide.md). If this document conflicts with the brand guide, the brand guide wins.

## Experience principles

The site should feel precise, evidence-driven, calm, and approachable.

1. **Lead with the evidence.** Use clear headings, short summaries, directly labeled data, and links to methods or sources.
2. **Make the next step obvious.** Each page should have one primary action and a small number of secondary actions.
3. **Let content breathe.** Use generous space and strong hierarchy instead of decoration to organize a page.
4. **Use bright color for wayfinding.** Jade, Sky, and Saffron are accents. Dark Amethyst and Mint Cream carry most reading surfaces.
5. **Never encode meaning in color alone.** Pair color with text, an icon, a shape, a pattern, or position.
6. **Design for interruption and uncertainty.** Plain language, descriptive labels, visible status, and forgiving forms matter more than visual novelty.

## Brand foundations

### Color roles

| Role | Light theme | Dark theme | Use |
|---|---:|---:|---|
| Page background | `#F7FFF6` | `#010A00` | Primary canvas |
| Surface | `#FFFFFF` | `#34113F` | Cards, forms, tables |
| Text | `#34113F` | `#F7FFF6` | Body copy and headings |
| Link | `#00698C` | `#1FC7FF` | Persistent underlined links |
| Primary accent | `#4CB944` | `#4DBA45` | Progress, success, selected accents |
| Information | `#00A7E1` | `#1FC7FF` | Informational graphics and highlights |
| Highlight | `#E3B505` | `#FACE1E` | Warnings, notes, key findings |
| Focus | `#34113F` | `#FACE1E` | Keyboard focus ring |

Accessible text and chart variants on light backgrounds:

- Jade text: `#30742B`
- Sky link/line: `#00698C` (preferred) or `#007EA8` (minimum)
- Saffron text/line: `#705A02` (preferred) or `#8D7103` (minimum)

Do not use base Jade, Fresh Sky, or Saffron as small text on Mint Cream or white. Do not place white text on those three base accents.

### CSS tokens

Keep components semantic: a component consumes `--color-link`, not `--sky`.

```css
@layer reset, tokens, base, layout, components, utilities;

@layer tokens {
  :root {
    color-scheme: light dark;

    --color-bg: #f7fff6;
    --color-surface: #ffffff;
    --color-text: #34113f;
    --color-link: #00698c;
    --color-primary: #4cb944;
    --color-primary-text: #34113f;
    --color-info: #00a7e1;
    --color-highlight: #e3b505;
    --color-success-text: #30742b;
    --color-warning-text: #705a02;
    --color-border: #34113f;
    --color-focus: #34113f;

    --font-sans: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
      "Segoe UI", sans-serif;
    --font-mono: ui-monospace, "SFMono-Regular", Consolas, monospace;

    --step--1: clamp(0.875rem, 0.84rem + 0.14vw, 0.95rem);
    --step-0: clamp(1rem, 0.96rem + 0.2vw, 1.125rem);
    --step-1: clamp(1.25rem, 1.14rem + 0.5vw, 1.55rem);
    --step-2: clamp(1.6rem, 1.35rem + 1vw, 2.2rem);
    --step-3: clamp(2.1rem, 1.6rem + 2vw, 3.4rem);
    --step-4: clamp(2.75rem, 1.9rem + 3.4vw, 5rem);

    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.5rem;
    --space-6: 2rem;
    --space-7: 3rem;
    --space-8: 4.5rem;
    --space-section: clamp(3.5rem, 8vw, 7rem);

    --measure: 68ch;
    --container: 76rem;
    --radius-sm: 0.35rem;
    --radius-md: 0.75rem;
    --radius-lg: 1.25rem;
    --border-control: 2px;
    --shadow-card: 0 0.4rem 1.4rem rgb(52 17 63 / 10%);
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --color-bg: #010a00;
      --color-surface: #34113f;
      --color-text: #f7fff6;
      --color-link: #1fc7ff;
      --color-primary: #4dba45;
      --color-primary-text: #010a00;
      --color-info: #1fc7ff;
      --color-highlight: #face1e;
      --color-success-text: #4dba45;
      --color-warning-text: #face1e;
      --color-border: #f7fff6;
      --color-focus: #face1e;
      --shadow-card: none;
    }
  }
}
```

Use the system font stack by default. It is readable, fast, and avoids an external font request. A future brand typeface must be self-hosted, subsetted, and tested for layout shift before it replaces this stack.

### Logo

The current workspace contains multiple logo explorations, so the final identity still requires stakeholder selection. Until then:

- use the text `UX in Science` as the accessible site name;
- if a provisional mark is needed, use the static simplified Team Orbit SVG appropriate to the theme;
- use the horizontal mark in the site header and the icon-only mark only for square contexts;
- preserve the SVG aspect ratio and do not recolor, rotate, crop, outline, or add effects;
- provide useful `alt` text when the image conveys the organization name; use `alt=""` when adjacent text already names it;
- avoid the animated logo in primary navigation. If used elsewhere, honor `prefers-reduced-motion`.

Provisional assets:

- Light header: `../src/assets/logos/ux-team-orbit-simple-primary.svg`
- Dark header: `../src/assets/logos/ux-team-orbit-simple-dark.svg`
- Compact icon: `../src/assets/logos/ux-team-orbit-simple-icon.svg`

## Information architecture

For a public-facing content site, use this initial top-level structure:

- **Home** - concise value proposition, featured work, evidence, and next step
- **Approach** - methods, principles, and how UX supports scientific work
- **Projects** - case studies with problem, method, result, and evidence
- **Resources** - articles, tools, templates, and talks
- **About** - team, partners, contact, and governance

Keep the primary navigation to five or fewer items. Put legal, accessibility, privacy, and secondary organizational links in the footer. Labels must describe destinations; avoid vague items such as “Learn” or “Explore.”

## Page anatomy

### Global shell

Every page follows this order:

1. Skip link
2. Site header and primary navigation
3. One `main` landmark with a unique `h1`
4. Page-specific sections with ordered heading levels
5. Site footer

The content container has a maximum width of `76rem` and inline padding of `clamp(1rem, 4vw, 2rem)`. Reading text is capped at `68ch`; do not stretch paragraphs across the full container.

### Home page

1. **Hero:** outcome-led `h1`, a two-to-three sentence explanation, one primary CTA, and one text link.
2. **Proof strip:** two or three concrete facts, outcomes, or partner signals. Do not use unsupported vanity metrics.
3. **What UX changes:** three cards covering usability, collaboration, and research impact.
4. **Featured case study:** problem, method, measurable result, and link to the full evidence.
5. **How we work:** a short, numbered process with explicit inputs and outputs.
6. **Resources:** three recent or foundational resources with content type and reading time.
7. **Closing CTA:** one focused invitation on a Dark Amethyst surface.

Use a single-column flow on small screens. At wider widths, the hero may become a `minmax(0, 1.2fr) minmax(18rem, 0.8fr)` grid and card groups may use two or three columns.

### Article and case-study pages

- Place title, summary, author/date, and content type before the body.
- Use an optional table of contents only for long pages; it must remain ordinary links in source order.
- Keep the main narrative at `68ch`.
- Use wide figures outside the text measure only when their labels remain readable.
- Each case study should identify the context, question, participants or data, method, findings, limitations, and outcome.
- Cite sources near claims and describe uncertainty plainly.

## Responsive layout

Use mobile-first CSS and let content determine when a layout changes. Reference ranges are:

| Range | Typical layout |
|---|---|
| Below `42rem` | One column, compact header, stacked actions |
| `42rem` to `63.99rem` | Two-column cards where useful |
| `64rem` and above | Full navigation, split hero, three-column cards |
| Above `80rem` | More outer whitespace; content does not keep expanding |

These are not device targets. A component should wrap or stack before its content collides.

```css
.container {
  width: min(100% - clamp(2rem, 8vw, 4rem), var(--container));
  margin-inline: auto;
}

.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  align-items: center;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr));
  gap: var(--space-5);
}

img,
svg,
video {
  display: block;
  max-width: 100%;
  height: auto;
}
```

- Avoid fixed heights for text containers.
- Allow controls and headings to wrap at 200% zoom.
- Never create horizontal page scrolling at a viewport width of `320px`.
- Tables that cannot reflow belong in a labeled horizontal scroll region with keyboard access and a visible overflow cue.
- Prefer container queries for reusable components when their behavior depends on available component width rather than viewport width.

## Typography and content

- Body text uses `--step-0` with a line height of `1.6`.
- Headings use Dark Amethyst/Mint Cream, a line height between `1.05` and `1.2`, and balanced wrapping where supported.
- Use sentence case for headings and controls.
- Use no more than three heading sizes in a typical view.
- Use bold selectively for scan points; do not bold full paragraphs.
- Use the mono stack only for code, identifiers, and literal values.
- Left-align prose. Do not justify text or center paragraphs longer than two short lines.
- Prefer “Use,” “Compare,” and “Download” over generic labels such as “Click here.”
- Expand acronyms on first use and explain specialist terms for interdisciplinary readers.

## Components

### Header and navigation

- The header uses the page background or surface color with a strong bottom border.
- The logo/site name links to the home page.
- The active page is indicated by text/`aria-current="page"` plus a visual treatment.
- At small widths, allow navigation to wrap into a clearly labeled second row. A disclosure menu may be added later, but it requires JavaScript and must use a real button with correct expanded state.
- Keep touch targets at least `44px` in each dimension where practical.

### Buttons and links

- Primary button: Dark Amethyst fill with Mint Cream text in light mode.
- Alternate primary button: Jade fill, Dark Amethyst text, and a `2px` Dark Amethyst border.
- Secondary button: transparent background, current text color, and a `2px` border.
- Links use the accessible Sky link token and remain underlined outside navigation.
- Hover is an enhancement; every control must be understandable without it.
- Disabled appearance is never the only explanation for why an action is unavailable.

### Cards

- Use white surfaces in light mode and Dark Amethyst surfaces in dark mode.
- Keep the full card readable in source order: type/eyebrow, heading, summary, metadata, action.
- Avoid making the entire card an invisible nested link. Use one descriptive primary link, optionally stretched with CSS only when no other interactive element exists.
- Prefer border and spacing over shadow. Use `--shadow-card` sparingly.

### Callouts and status

- Informational callout: Sky strip or icon, descriptive heading, and ordinary body text.
- Success: Jade accent plus “Success” or a specific outcome label.
- Warning: Saffron strip/icon with Dark Amethyst text in light mode.
- Error: do not invent an inaccessible red-only state. Use an error icon, an explicit “Error” label, clear correction text, and a tested high-contrast border/text color.
- Place status messages near the affected content and announce dynamic messages appropriately if JavaScript is introduced.

### Forms

- Use visible labels above controls; placeholders are optional examples, never labels.
- White fields sit on Mint Cream with a `1.5px` to `2px` Dark Amethyst border.
- Group related controls with `fieldset` and `legend`.
- Put requirements and accepted formats before the field.
- Put errors next to fields and summarize them at the top after submission.
- Use the correct input type and autocomplete token.
- Preserve entered values after validation errors.

### Data and scientific figures

Light-theme series use Dark Amethyst `#34113F`, Jade text variant `#30742B`, strong Sky `#00698C`, and strong Saffron `#705A02`. Dark-theme series use Mint Cream `#F7FFF6`, Jade `#4DBA45`, Sky `#1FC7FF`, and Saffron `#FACE1E`.

- Directly label lines and bars where possible.
- Combine color with marker shape, line style, label, or pattern.
- Include a text summary and an accessible data table when a figure carries substantive evidence.
- Avoid text over busy scientific images. If unavoidable, place text on an opaque or near-opaque Dark Amethyst panel.
- Every figure needs a useful caption, units, sample size where applicable, and source/method context.

## Interaction states

Every interactive component needs default, hover, focus-visible, active, disabled, loading, success, and error behavior where applicable.

```css
:where(a, button, input, select, textarea, summary):focus-visible {
  outline: 3px solid var(--color-focus);
  outline-offset: 3px;
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Do not remove outlines. Do not communicate an interactive state only by changing color. Motion must explain a state change, not decorate routine navigation.

## Semantic HTML rules

- Start with native elements: `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`, `button`, and `details`.
- Use a link for navigation and a button for an action.
- Keep DOM order identical to reading and keyboard order; CSS must not create a misleading visual reorder.
- Use one unique `h1`; do not skip heading levels for appearance.
- Give each navigation landmark an accessible name when more than one exists.
- Use `aria-*` only when native HTML cannot express the behavior.
- Decorative images use empty alt text. Complex figures get a concise alt description plus nearby detail or data.
- Set the page language and provide a descriptive, unique `title` for every page.

## CSS architecture

Organize styles in cascade layers:

1. `reset` - box sizing, margin normalization, media defaults
2. `tokens` - brand and scale custom properties
3. `base` - document typography and native element defaults
4. `layout` - container, stack, cluster, grid, sidebar primitives
5. `components` - header, buttons, cards, callouts, forms, footer
6. `utilities` - a small set of single-purpose helpers such as visually hidden text

Use low-specificity selectors and component classes. Avoid IDs for styling, `!important` except in deliberate accessibility overrides, deep nesting, and one-off pixel values where a token exists.

Suggested structure:

```text
/
├── index.html
├── approach.html
├── projects/
├── resources/
├── about.html
└── assets/
    ├── css/
    │   ├── tokens.css
    │   ├── base.css
    │   ├── layout.css
    │   └── components.css
    ├── images/
    └── logos/
```

## Responsible delivery

### Performance

- Target a fast first render on a mid-range phone over a constrained connection.
- Ship HTML and CSS needed for the first view without a framework runtime.
- Keep initial CSS small, remove unused rules, and avoid render-blocking third-party assets.
- Use SVG for logos and simple diagrams; use AVIF/WebP with dimensions and responsive `srcset` for photographs.
- Lazy-load below-the-fold images, but never the primary hero image.
- Avoid autoplaying media and background video.
- Reserve media dimensions to prevent layout shift.

### Privacy and resilience

- Do not add analytics, embeds, cookie banners, or third-party fonts by default.
- If measurement becomes necessary, collect the least data needed, document retention, and obtain appropriate consent.
- Prefer links to third-party media over surveillance-heavy embeds; load embeds only after clear user action.
- Core content, navigation, contact information, and downloads must work without JavaScript.
- Show a useful fallback when an enhancement or external service fails.

### Accessibility validation

Test with keyboard only, visible focus, browser zoom at 200% and 400%, reduced motion, light/dark preference, and high-contrast/forced-colors modes. Combine automated checks with manual review and screen-reader smoke testing.

## Definition of done

A page is ready when:

- it has valid, landmark-based semantic HTML and a logical heading outline;
- it works at `320px` wide without two-dimensional scrolling;
- prose remains readable and layouts survive 200% text zoom;
- normal text meets `4.5:1` contrast and meaningful boundaries meet `3:1`;
- focus order is logical and every interactive element has a visible focus indicator;
- color-coded information has a second cue;
- links are descriptive and persistently distinguishable from body text;
- images have correct dimensions, formats, and text alternatives;
- the page works without JavaScript for core tasks;
- dark mode uses the approved dark tokens and has been reviewed independently;
- reduced-motion preferences are honored;
- no unnecessary third-party request, tracker, or personal-data collection has been introduced;
- content states evidence, methods, limitations, ownership, and dates where relevant.

## Open decisions

The following choices should be confirmed before a production build:

1. Which logo exploration is the approved identity? This specification provisionally references Simplified Team Orbit.
2. What is the final content inventory and which top-level navigation labels match it?
3. Is automatic system dark mode desired, or should the future site include a persistent user-controlled theme toggle?
4. What evidence, project results, and partner marks are approved for public use?
5. What privacy, analytics, hosting, and content-governance policies apply?
