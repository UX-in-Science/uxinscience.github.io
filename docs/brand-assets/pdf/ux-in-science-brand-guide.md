# UX in Science Brand Guide

Practical color and accessibility guidance for web pages, interface components, data graphics, and presentation slides.

## Brand posture

UX in Science should feel precise, evidence-driven, calm, and approachable. Use the bright colors to create momentum and wayfinding, but let Dark Amethyst and Mint Cream carry most reading surfaces.

## Core palette

| Color | Hex | RGB | HSL | Role | Accessible note |
|---|---:|---:|---:|---|---|
| Jade Green | `#4CB944` | `76, 185, 68` | `116, 46%, 50%` | Primary accent, positive states, progress | Do not use as small text on light backgrounds. Use as a fill with Dark Amethyst or black text, or use darker text variant `#30742B`. |
| Fresh Sky | `#00A7E1` | `0, 167, 225` | `195, 100%, 44%` | Secondary accent, links, information | Do not use as small text on light backgrounds. Use darker link variants `#007EA8` or `#00698C`. |
| Dark Amethyst | `#34113F` | `52, 17, 63` | `286, 58%, 16%` | Primary text, headings, strong surfaces | Works with Mint Cream, white, Jade, Sky, and Saffron. |
| Saffron | `#E3B505` | `227, 181, 5` | `48, 96%, 45%` | Highlight, warning, callout | Use for emphasis, not body text on light backgrounds. Use `#8D7103` or `#705A02` for text. |
| Mint Cream | `#F7FFF6` | `247, 255, 246` | `113, 100%, 98%` | Main light background, quiet panels | Pair with Dark Amethyst or black text. |

## Theme tokens

### Light

| Token | Hex | Usage |
|---|---:|---|
| Background | `#F7FFF6` | Page or slide canvas |
| Text | `#34113F` | Body copy, headings, captions |
| Primary | `#4CB944` | Primary accent and positive action |
| Info | `#00A7E1` | Information accent and chart series |
| Highlight | `#E3B505` | Callouts, notes, and attention |

### Dark

| Token | Hex | Usage |
|---|---:|---|
| Background | `#010A00` | Dark page or slide canvas |
| Text | `#F7FFF6` | Body copy, headings, captions |
| Primary | `#4DBA45` | Primary accent and positive action |
| Info | `#1FC7FF` | Links, focus, information accent |
| Amethyst accent | `#E3BFEE` | Secondary emphasis |
| Highlight | `#FACE1E` | Callouts, notes, and attention |

## Contrast rules

Target WCAG 2.2 AA:

- Normal text: at least `4.5:1`.
- Large text and meaningful UI/graphic boundaries: at least `3:1`.
- Color must not be the only cue for meaning.

| Combination | Ratio | Result | Guidance |
|---|---:|---|---|
| Dark Amethyst text on Mint Cream | `15.86:1` | AAA | Use for body copy and headings in light theme. |
| Black text on Mint Cream | `20.59:1` | AAA | Use for dense labels, tables, and code. |
| Jade text on Mint Cream | `2.47:1` | Fail | Use `#30742B` when green text is required. |
| Fresh Sky text on Mint Cream | `2.70:1` | Fail | Use `#007EA8` minimum, `#00698C` preferred. |
| Saffron text on Mint Cream | `1.89:1` | Fail | Use `#8D7103` minimum, `#705A02` preferred. |
| Mint Cream text on Dark Amethyst | `15.86:1` | AAA | Use for dark cards, banners, and title slides. |
| Dark Amethyst text on Jade Green | `6.42:1` | AA | Passes for buttons and badges. |
| Dark Amethyst text on Fresh Sky | `5.87:1` | AA | Passes for buttons and badges. |
| Dark Amethyst text on Saffron | `8.38:1` | AAA | Passes for buttons, tags, and callouts. |
| Dark Jade on `#010A00` | `8.06:1` | AAA | Passes for dark-mode text, icons, and chart marks. |
| Dark Sky on `#010A00` | `10.21:1` | AAA | Passes for dark-mode links, focus, and chart marks. |
| Dark Saffron on `#010A00` | `13.32:1` | AAA | Passes for dark-mode highlights. |

## Accessible variants from the shade scale

| Variant | Hex | Contrast on Mint Cream | Use |
|---|---:|---:|---|
| Jade text | `#30742B` | `5.63:1` | Success labels, status text, data labels |
| Sky link | `#007EA8` | `4.53:1` | Minimum AA link color on light backgrounds |
| Sky strong link | `#00698C` | `6.06:1` | Preferred blue link and chart line |
| Saffron text | `#8D7103` | `4.58:1` | Minimum AA warning text |
| Saffron strong text | `#705A02` | `6.53:1` | Preferred warning text and chart line |

## Web usage guidelines

- Light theme: use Mint Cream as the page canvas and Dark Amethyst as the default text color. White may be used for cards, tables, and form fields.
- Buttons and controls: borderless Jade, Sky, and Saffron components do not meet the 3:1 boundary rule on Mint Cream. Add a 2 px Dark Amethyst border, use a darker shade, or use a Dark Amethyst fill.
- Links: do not use base Fresh Sky for small link text on light backgrounds. Use `#007EA8` minimum, `#00698C` preferred, and keep underlines or another persistent cue.
- Focus states: use a 2-3 px Dark Amethyst focus ring on light backgrounds. Use dark-theme Sky or Saffron on `#010A00`.
- Color meaning: pair status color with text, icon shape, pattern, or placement.
- Dark theme: `#010A00` background with Mint Cream text is the default. The dark-theme accent colors are strong enough for text, icons, charts, and focus rings.

```css
:root {
  --ux-bg: #F7FFF6;
  --ux-surface: #FFFFFF;
  --ux-text: #34113F;
  --ux-link: #00698C;
  --ux-primary: #4CB944;
  --ux-primary-text: #34113F;
  --ux-info: #00A7E1;
  --ux-highlight: #E3B505;
  --ux-focus: #34113F;
}

@media (prefers-color-scheme: dark) {
  :root {
    --ux-bg: #010A00;
    --ux-surface: #34113F;
    --ux-text: #F7FFF6;
    --ux-link: #1FC7FF;
    --ux-primary: #4DBA45;
    --ux-primary-text: #010A00;
    --ux-info: #1FC7FF;
    --ux-highlight: #FACE1E;
    --ux-focus: #FACE1E;
  }
}
```

## Component recipes

| Component | Recommended color treatment | Avoid |
|---|---|---|
| Primary CTA | Dark Amethyst fill with Mint Cream text, or Jade fill with Dark Amethyst text and Dark Amethyst border | White text on Jade, Sky, or Saffron |
| Status badge | Jade/Sky/Saffron fill, Dark Amethyst text, explicit label, and icon or shape cue | Color-only status dots |
| Form field | White field on Mint Cream with Dark Amethyst label, 1.5-2 px border, clear focus ring | Pale border that is the only field boundary |
| Alert/callout | Saffron header strip or icon with Dark Amethyst text; include alert title and actionable copy | Saffron paragraph text on light background |

## Slides and data graphics

- Default slide: Mint Cream background, Dark Amethyst title and body text. Use one accent color per slide unless the content is a chart.
- Dark title slide: `#010A00` background with Mint Cream title and dark-theme accents. Keep dense body copy off dark slides.
- Text scale: titles `34-44 pt`, body `24-28 pt`, annotations at least `18 pt`.
- Scientific images: avoid text directly over busy images. If overlay is necessary, use an opaque or near-opaque Dark Amethyst or `#010A00` panel with Mint Cream text.
- Projector safety: test slides in grayscale and on a low-brightness display. Saffron and Mint Cream can wash out as thin marks.

### Chart palette

| Purpose | Light background | Dark background | Guidance |
|---|---:|---:|---|
| Primary series | `#34113F` | `#F7FFF6` | Anchor series or baseline |
| Green series | `#30742B` | `#4DBA45` | Use darker Jade for lines/markers on light slides |
| Blue series | `#00698C` | `#1FC7FF` | Preferred for links, methods, secondary datasets |
| Yellow series | `#705A02` | `#FACE1E` | Use with labels or patterns; avoid thin base Saffron lines on light backgrounds |
| Accessible category cue | Color plus marker shape, line style, label, or pattern | Color plus marker shape, line style, label, or pattern | Do not rely on hue alone |

## Production checklist

- Normal web text reaches at least `4.5:1`; large text and meaningful graphics/UI boundaries reach at least `3:1`.
- Interactive controls have visible boundaries and focus indicators that meet `3:1` against adjacent colors.
- Every color-coded status, chart series, or required field has a second cue: text, icon, shape, pattern, or direct label.
- Bright base accents are not used as paragraph text on Mint Cream or white.
- Dark-mode pages use `#010A00` background, Mint Cream text, and the dark-theme accent tokens from the theme image.
- Slides remain readable in grayscale and at projector brightness; charts have direct labels and sufficient line weight.

## References

- WCAG 2.2 SC 1.4.3 Contrast (Minimum): https://www.w3.org/TR/WCAG22/#contrast-minimum
- WCAG 2.2 SC 1.4.11 Non-text Contrast: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- WCAG 2.2 SC 1.4.1 Use of Color: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html

Contrast ratios were computed from the supplied hex values using the WCAG relative luminance formula. The light/dark theme values come from `Themes-LightDark.png`.
