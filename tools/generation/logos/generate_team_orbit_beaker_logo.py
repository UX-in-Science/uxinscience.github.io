from pathlib import Path
from math import cos, pi, radians, sin, tan
from textwrap import wrap

from PIL import Image, ImageDraw
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "docs" / "brand-assets" / "logos" / "team-orbit-simple"
SVG_PRIMARY = OUT_DIR / "ux-team-orbit-simple-primary.svg"
SVG_ICON = OUT_DIR / "ux-team-orbit-simple-icon.svg"
SVG_ICON_ANIMATED = OUT_DIR / "ux-team-orbit-simple-icon-animated.svg"
GIF_ICON_ANIMATED = OUT_DIR / "ux-team-orbit-simple-icon-animated.gif"
HTML_ANIMATED_PREVIEW = OUT_DIR / "ux-team-orbit-simple-icon-animated-preview.html"
SVG_DARK = OUT_DIR / "ux-team-orbit-simple-dark.svg"
SVG_GREYSCALE = OUT_DIR / "ux-team-orbit-simple-greyscale.svg"
SVG_BW = OUT_DIR / "ux-team-orbit-simple-black-white.svg"
SVG_ICON_GREYSCALE = OUT_DIR / "ux-team-orbit-simple-icon-greyscale.svg"
SVG_ICON_BW = OUT_DIR / "ux-team-orbit-simple-icon-black-white.svg"
SVG_STACKED = OUT_DIR / "ux-team-orbit-simple-stacked.svg"
SVG_BOARD = OUT_DIR / "ux-team-orbit-simple-board.svg"
PDF_PROOF = OUT_DIR / "ux-team-orbit-simple-proof.pdf"
MD_NOTES = OUT_DIR / "ux-team-orbit-simple-notes.md"


COLORS = {
    "jade": "#4CB944",
    "sky": "#00A7E1",
    "amethyst": "#34113F",
    "saffron": "#E3B505",
    "mint": "#F7FFF6",
    "dark_bg": "#010A00",
    "dark_sky": "#1FC7FF",
    "dark_jade": "#4DBA45",
    "dark_saffron": "#FACE1E",
    "line": "#D9E5D8",
    "text": "#202320",
    "grey_900": "#111111",
    "grey_700": "#555555",
    "grey_500": "#808080",
    "grey_300": "#B8B8B8",
    "white": "#FFFFFF",
    "black": "#000000",
}


STYLE = f"""
  .wordmark {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 110px;
    font-weight: 820;
    letter-spacing: 0;
    fill: {COLORS["amethyst"]};
  }}
  .wordmark-dark {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 110px;
    font-weight: 820;
    letter-spacing: 0;
    fill: {COLORS["mint"]};
  }}
  .small-label {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 25px;
    font-weight: 700;
    letter-spacing: 0;
    fill: {COLORS["amethyst"]};
  }}
  .body {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 21px;
    font-weight: 400;
    letter-spacing: 0;
    fill: {COLORS["text"]};
  }}
  .caption {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0;
    fill: {COLORS["amethyst"]};
  }}
  .thin {{
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
  }}
  .motion-copy {{
    opacity: 1;
  }}
  .motion-static {{
    opacity: 0;
  }}
  @media (prefers-reduced-motion: reduce) {{
    .motion-copy {{
      opacity: 0;
    }}
    .motion-static {{
      opacity: 1;
    }}
  }}
"""


def svg_document(width, height, body, background=None):
    bg = f'<rect width="100%" height="100%" fill="{background}"/>' if background else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
<defs>
<style>
{STYLE}
</style>
</defs>
{bg}
{body}
</svg>
"""


def icon_palette(dark=False, variant="color"):
    if variant == "greyscale":
        return {
            "sky": COLORS["grey_500"],
            "jade": COLORS["grey_700"],
            "saffron": COLORS["grey_300"],
            "amethyst": COLORS["grey_900"],
        }
    if variant == "black-white":
        tone = COLORS["white"] if dark else COLORS["black"]
        return {
            "sky": tone,
            "jade": tone,
            "saffron": tone,
            "amethyst": tone,
        }
    return {
        "sky": COLORS["dark_sky"] if dark else COLORS["sky"],
        "jade": COLORS["dark_jade"] if dark else COLORS["jade"],
        "saffron": COLORS["dark_saffron"] if dark else COLORS["saffron"],
        "amethyst": COLORS["mint"] if dark else COLORS["amethyst"],
    }


def team_people_svg(palette):
    jade = palette["jade"]
    saffron = palette["saffron"]
    amethyst = palette["amethyst"]
    sky = palette["sky"]
    return f"""
  <path class="thin" d="M151 173 C165 117 204 94 220 94 C236 94 275 117 289 173" stroke="{amethyst}" stroke-width="10"/>
  <circle cx="220" cy="65" r="23" fill="none" stroke="{amethyst}" stroke-width="8"/>

  <path class="thin" d="M80 195 C94 142 130 124 146 124 C164 124 196 144 206 195" stroke="{jade}" stroke-width="9"/>
  <circle cx="146" cy="100" r="21" fill="none" stroke="{jade}" stroke-width="7"/>

  <path class="thin" d="M234 195 C246 144 279 124 298 124 C317 124 350 144 362 195" stroke="{saffron}" stroke-width="9"/>
  <circle cx="298" cy="100" r="21" fill="none" stroke="{saffron}" stroke-width="7"/>

  <circle cx="188" cy="213" r="8" fill="{jade}"/>
  <circle cx="220" cy="204" r="8" fill="{saffron}"/>
  <circle cx="252" cy="213" r="8" fill="{sky}"/>
"""


def rotate_point(x, y, cx, cy, angle_degrees):
    angle = radians(angle_degrees)
    dx = x - cx
    dy = y - cy
    return (
        cx + dx * cos(angle) - dy * sin(angle),
        cy + dx * sin(angle) + dy * cos(angle),
    )


def fmt_point(x, y):
    return f"{x:.3f}".rstrip("0").rstrip("."), f"{y:.3f}".rstrip("0").rstrip(".")


def rotated_ellipse_path(cx, cy, rx, ry, angle_degrees, reverse=False):
    step = -90 if reverse else 90
    angles = [radians(value) for value in range(0, step * 4 + step, step)]
    parts = []
    start_x = cx + rx * cos(angles[0])
    start_y = cy + ry * sin(angles[0])
    start_x, start_y = rotate_point(start_x, start_y, cx, cy, angle_degrees)
    sx, sy = fmt_point(start_x, start_y)
    parts.append(f"M {sx} {sy}")

    for start, end in zip(angles, angles[1:]):
        delta = end - start
        k = 4 / 3 * tan(delta / 4)
        x0 = cx + rx * cos(start)
        y0 = cy + ry * sin(start)
        x3 = cx + rx * cos(end)
        y3 = cy + ry * sin(end)
        dx0 = -rx * sin(start)
        dy0 = ry * cos(start)
        dx3 = -rx * sin(end)
        dy3 = ry * cos(end)
        x1 = x0 + k * dx0
        y1 = y0 + k * dy0
        x2 = x3 - k * dx3
        y2 = y3 - k * dy3
        points = [
            rotate_point(x1, y1, cx, cy, angle_degrees),
            rotate_point(x2, y2, cx, cy, angle_degrees),
            rotate_point(x3, y3, cx, cy, angle_degrees),
        ]
        formatted = [fmt_point(x, y) for x, y in points]
        parts.append(
            "C "
            + " ".join(f"{x} {y}" for x, y in formatted)
        )
    parts.append("Z")
    return " ".join(parts)


def ellipse_point(cx, cy, rx, ry, angle_degrees, phase):
    angle = 2 * pi * phase
    x = cx + rx * cos(angle)
    y = cy + ry * sin(angle)
    return rotate_point(x, y, cx, cy, angle_degrees)


def hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in range(0, 6, 2))


def cubic_points(p0, p1, p2, p3, steps=36):
    points = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1 - t
        x = mt ** 3 * p0[0] + 3 * mt ** 2 * t * p1[0] + 3 * mt * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = mt ** 3 * p0[1] + 3 * mt ** 2 * t * p1[1] + 3 * mt * t ** 2 * p2[1] + t ** 3 * p3[1]
        points.append((x, y))
    return points


def two_cubic_points(start, first, second, steps=36):
    return cubic_points(start, first[0], first[1], first[2], steps) + cubic_points(first[2], second[0], second[1], second[2], steps)[1:]


def transformed(points, offset=(34, 28), scale=1):
    return [((x + offset[0]) * scale, (y + offset[1]) * scale) for x, y in points]


def draw_round_line(draw, points, color, width):
    draw.line(points, fill=color, width=width, joint="curve")
    radius = width / 2
    for point in (points[0], points[-1]):
        draw.ellipse((point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius), fill=color)


def draw_circle(draw, cx, cy, r, fill, scale=1, offset=(34, 28), outline=None, width=1):
    x = (cx + offset[0]) * scale
    y = (cy + offset[1]) * scale
    rr = r * scale
    box = (x - rr, y - rr, x + rr, y + rr)
    if outline:
        draw.ellipse(box, fill=fill, outline=outline, width=max(1, round(width * scale)))
    else:
        draw.ellipse(box, fill=fill)


def draw_rotated_ellipse(draw, cx, cy, rx, ry, angle_degrees, color, width, scale=1, offset=(34, 28), steps=220):
    points = []
    for i in range(steps + 1):
        phase = i / steps
        points.append(ellipse_point(cx, cy, rx, ry, angle_degrees, phase))
    draw.line(transformed(points, offset, scale), fill=color, width=max(1, round(width * scale)), joint="curve")


def draw_people_gif(draw, palette, scale=1, offset=(34, 28)):
    jade = hex_rgb(palette["jade"])
    saffron = hex_rgb(palette["saffron"])
    amethyst = hex_rgb(palette["amethyst"])
    sky = hex_rgb(palette["sky"])

    center = two_cubic_points(
        (151, 173),
        ((165, 117), (204, 94), (220, 94)),
        ((236, 94), (275, 117), (289, 173)),
    )
    draw_round_line(draw, transformed(center, offset, scale), amethyst, round(10 * scale))
    draw_circle(draw, 220, 65, 23, None, scale, offset, outline=amethyst, width=8)

    left = two_cubic_points(
        (80, 195),
        ((94, 142), (130, 124), (146, 124)),
        ((164, 124), (196, 144), (206, 195)),
    )
    draw_round_line(draw, transformed(left, offset, scale), jade, round(9 * scale))
    draw_circle(draw, 146, 100, 21, None, scale, offset, outline=jade, width=7)

    right = two_cubic_points(
        (234, 195),
        ((246, 144), (279, 124), (298, 124)),
        ((317, 124), (350, 144), (362, 195)),
    )
    draw_round_line(draw, transformed(right, offset, scale), saffron, round(9 * scale))
    draw_circle(draw, 298, 100, 21, None, scale, offset, outline=saffron, width=7)

    draw_circle(draw, 188, 213, 8, jade, scale, offset)
    draw_circle(draw, 220, 204, 8, saffron, scale, offset)
    draw_circle(draw, 252, 213, 8, sky, scale, offset)


def team_icon_svg(x=0, y=0, scale=1, dark=False, variant="color"):
    palette = icon_palette(dark, variant)
    sky = palette["sky"]
    jade = palette["jade"]
    saffron = palette["saffron"]
    orbit_opacity = "0.92"
    return f"""
<g transform="translate({x} {y}) scale({scale})">
  <ellipse class="thin" cx="220" cy="156" rx="196" ry="70" transform="rotate(-22 220 156)" stroke="{sky}" stroke-width="11" opacity="{orbit_opacity}"/>
  <ellipse class="thin" cx="220" cy="156" rx="152" ry="53" transform="rotate(24 220 156)" stroke="{jade}" stroke-width="7" opacity="{orbit_opacity}"/>
  <circle cx="384" cy="77" r="14" fill="{saffron}"/>
  <circle cx="66" cy="209" r="14" fill="{jade}"/>
{team_people_svg(palette)}
</g>
"""


def primary_svg():
    body = f"""
<title>UX in Science logo with simplified scientific team and atomic orbit</title>
<desc>Primary logo lockup showing UX in Science text beside a simplified scientific team with atomic orbit paths.</desc>
<text class="wordmark" x="54" y="211">UX in Science</text>
{team_icon_svg(790, 42, 0.82)}
"""
    return svg_document(1200, 340, body)


def icon_svg():
    body = f"""
<title>UX in Science scientific team icon with atomic orbit</title>
<desc>Icon-only mark showing a simplified scientific team with atomic orbit paths.</desc>
{team_icon_svg(34, 28, 1)}
"""
    return svg_document(500, 370, body)


def animated_icon_svg():
    palette = icon_palette()
    sky = palette["sky"]
    jade = palette["jade"]
    saffron = palette["saffron"]
    sky_path = rotated_ellipse_path(220, 156, 196, 70, -22)
    jade_path = rotated_ellipse_path(220, 156, 152, 53, 24)
    jade_motion_path = rotated_ellipse_path(220, 156, 152, 53, 24, reverse=True)
    body = f"""
<title>UX in Science animated scientific team icon with atomic orbit</title>
<desc>Animated icon-only mark showing two orbit balls moving along atomic tracks around a simplified scientific team. The animation visually falls back to static orbit balls when reduced motion is preferred.</desc>
<g transform="translate(34 28)">
  <path id="uxis-sky-orbit-motion" d="{sky_path}" fill="none" stroke="none" opacity="0"/>
  <path id="uxis-jade-orbit-motion" d="{jade_motion_path}" fill="none" stroke="none" opacity="0"/>
  <path class="thin" d="{sky_path}" stroke="{sky}" stroke-width="11" opacity="0.92"/>
  <path class="thin" d="{jade_path}" stroke="{jade}" stroke-width="7" opacity="0.92"/>

  <g class="motion-copy">
    <circle r="14" fill="{saffron}">
      <animateMotion dur="7.2s" begin="-0.8s" repeatCount="indefinite" calcMode="linear">
        <mpath href="#uxis-sky-orbit-motion" xlink:href="#uxis-sky-orbit-motion"/>
      </animateMotion>
    </circle>
    <circle r="14" fill="{jade}">
      <animateMotion dur="8.8s" begin="-4.1s" repeatCount="indefinite" calcMode="linear">
        <mpath href="#uxis-jade-orbit-motion" xlink:href="#uxis-jade-orbit-motion"/>
      </animateMotion>
    </circle>
  </g>

  <g class="motion-static">
    <circle cx="384" cy="77" r="14" fill="{saffron}"/>
    <circle cx="66" cy="209" r="14" fill="{jade}"/>
  </g>

{team_people_svg(palette)}
</g>
"""
    return svg_document(500, 370, body)


def animated_preview_html():
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>UX in Science Animated Icon</title>
  <style>
    html,
    body {{
      height: 100%;
      margin: 0;
    }}
    body {{
      display: grid;
      place-items: center;
      background: {COLORS["mint"]};
    }}
    img {{
      width: min(78vw, 640px);
      height: auto;
    }}
  </style>
</head>
<body>
  <img src="{SVG_ICON_ANIMATED.name}" alt="UX in Science animated scientific team icon">
</body>
</html>
"""


def draw_animated_gif():
    palette = icon_palette()
    scale = 3
    width = 500
    height = 370
    frame_count = 72
    frame_duration_ms = 83
    bg = hex_rgb(COLORS["mint"])
    sky = hex_rgb(palette["sky"])
    jade = hex_rgb(palette["jade"])
    saffron = hex_rgb(palette["saffron"])
    frames = []
    resampling = getattr(Image, "Resampling", Image).LANCZOS

    for frame_index in range(frame_count):
        progress = frame_index / frame_count
        image = Image.new("RGB", (width * scale, height * scale), bg)
        draw = ImageDraw.Draw(image)

        draw_rotated_ellipse(draw, 220, 156, 196, 70, -22, sky, 11, scale)
        draw_rotated_ellipse(draw, 220, 156, 152, 53, 24, jade, 7, scale)

        saffron_x, saffron_y = ellipse_point(220, 156, 196, 70, -22, progress)
        jade_x, jade_y = ellipse_point(220, 156, 152, 53, 24, (-2 * progress + 0.18) % 1)
        draw_circle(draw, saffron_x, saffron_y, 14, saffron, scale)
        draw_circle(draw, jade_x, jade_y, 14, jade, scale)

        draw_people_gif(draw, palette, scale)

        frames.append(image.resize((width, height), resampling))

    frames[0].save(
        GIF_ICON_ANIMATED,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration_ms,
        loop=0,
        optimize=True,
        disposal=2,
    )


def dark_svg():
    body = f"""
<title>UX in Science logo dark variant</title>
<desc>Dark background logo lockup showing UX in Science text beside a simplified scientific team with atomic orbit paths.</desc>
<rect width="1200" height="340" fill="{COLORS["dark_bg"]}"/>
<text class="wordmark-dark" x="54" y="211">UX in Science</text>
{team_icon_svg(790, 42, 0.82, dark=True)}
"""
    return svg_document(1200, 340, body)


def greyscale_svg():
    body = f"""
<title>UX in Science logo greyscale variant</title>
<desc>Greyscale logo lockup showing UX in Science text beside a simplified scientific team with atomic orbit paths.</desc>
<text class="wordmark" x="54" y="211" style="fill:{COLORS["grey_900"]};">UX in Science</text>
{team_icon_svg(790, 42, 0.82, variant="greyscale")}
"""
    return svg_document(1200, 340, body)


def black_white_svg():
    body = f"""
<title>UX in Science logo black and white variant</title>
<desc>One-color black logo lockup showing UX in Science text beside a simplified scientific team with atomic orbit paths.</desc>
<text class="wordmark" x="54" y="211" style="fill:{COLORS["black"]};">UX in Science</text>
{team_icon_svg(790, 42, 0.82, variant="black-white")}
"""
    return svg_document(1200, 340, body)


def icon_greyscale_svg():
    body = f"""
<title>UX in Science greyscale scientific team icon with atomic orbit</title>
<desc>Greyscale icon-only mark showing a simplified scientific team with atomic orbit paths.</desc>
{team_icon_svg(34, 28, 1, variant="greyscale")}
"""
    return svg_document(500, 370, body)


def icon_black_white_svg():
    body = f"""
<title>UX in Science black and white scientific team icon with atomic orbit</title>
<desc>One-color black icon-only mark showing a simplified scientific team with atomic orbit paths.</desc>
{team_icon_svg(34, 28, 1, variant="black-white")}
"""
    return svg_document(500, 370, body)


def stacked_svg():
    body = f"""
<title>UX in Science logo stacked variant</title>
<desc>Stacked logo lockup with UX in Science text above a simplified scientific team with atomic orbit paths.</desc>
<text class="wordmark" x="72" y="144" style="font-size:78px;">UX in Science</text>
{team_icon_svg(150, 182, 0.8)}
"""
    return svg_document(720, 520, body)


def text_block(x, y, text, width_chars, class_name, line_height):
    lines = wrap(text, width=width_chars)
    tspans = []
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else line_height
        tspans.append(f'<tspan x="{x}" dy="{dy}">{line}</tspan>')
    return f'<text class="{class_name}" x="{x}" y="{y}">{"".join(tspans)}</text>'


def board_svg():
    body = f"""
<title>UX scientific team logo proof board</title>
<rect width="1600" height="1380" fill="{COLORS["mint"]}"/>
<text class="wordmark" x="70" y="140" style="font-size:62px;">UX in Science Scientific Team Logo</text>
{text_block(72, 188, "Focused revision: the beaker has been removed. The icon is now a simplified scientific team with atomic orbit paths wrapping the group.", 108, "body", 30)}

<rect x="72" y="260" width="700" height="300" rx="22" fill="#FFFFFF" stroke="{COLORS["line"]}" stroke-width="3"/>
<text class="small-label" x="110" y="322">Primary horizontal</text>
<g transform="translate(112 355) scale(0.68)">
  <text class="wordmark" x="0" y="156" style="font-size:68px;">UX in Science</text>
  {team_icon_svg(382, 22, 0.62)}
</g>

<rect x="828" y="260" width="700" height="300" rx="22" fill="{COLORS["dark_bg"]}" stroke="{COLORS["line"]}" stroke-width="3"/>
<text class="small-label" x="866" y="322" style="fill:{COLORS["mint"]};">Dark variant</text>
<g transform="translate(868 355) scale(0.68)">
  <text class="wordmark-dark" x="0" y="156" style="font-size:68px;">UX in Science</text>
  {team_icon_svg(382, 22, 0.62, dark=True)}
</g>

<rect x="72" y="600" width="700" height="300" rx="22" fill="#FFFFFF" stroke="{COLORS["line"]}" stroke-width="3"/>
<text class="small-label" x="110" y="662" style="fill:{COLORS["grey_900"]};">Greyscale</text>
<g transform="translate(112 695) scale(0.68)">
  <text class="wordmark" x="0" y="156" style="font-size:68px; fill:{COLORS["grey_900"]};">UX in Science</text>
  {team_icon_svg(382, 22, 0.62, variant="greyscale")}
</g>

<rect x="828" y="600" width="700" height="300" rx="22" fill="#FFFFFF" stroke="{COLORS["line"]}" stroke-width="3"/>
<text class="small-label" x="866" y="662" style="fill:{COLORS["black"]};">Black and white</text>
<g transform="translate(868 695) scale(0.68)">
  <text class="wordmark" x="0" y="156" style="font-size:68px; fill:{COLORS["black"]};">UX in Science</text>
  {team_icon_svg(382, 22, 0.62, variant="black-white")}
</g>

<rect x="72" y="940" width="700" height="300" rx="22" fill="#FFFFFF" stroke="{COLORS["line"]}" stroke-width="3"/>
<text class="small-label" x="110" y="1002">Icon-only mark</text>
<g transform="translate(238 1028) scale(0.7)">
  {team_icon_svg(0, 0, 1)}
</g>

<rect x="828" y="940" width="700" height="300" rx="22" fill="#FFFFFF" stroke="{COLORS["line"]}" stroke-width="3"/>
<text class="small-label" x="866" y="1002">Stacked lockup</text>
<g transform="translate(974 1006) scale(0.64)">
  <text class="wordmark" x="-84" y="112" style="font-size:78px;">UX in Science</text>
  {team_icon_svg(0, 152, 0.78)}
</g>

<text class="caption" x="72" y="1318">Brand role: teamwork is primary, science is explicit, and UX in Science remains the readable wordmark. Use full color where possible; use greyscale for neutral print and black/white for one-color reproduction.</text>
"""
    return svg_document(1600, 1380, body)


def notes_md():
    return f"""# UX in Science Simplified Team Orbit Logo

Focused revision requested: make the people outlines only.

## Files

- Primary horizontal SVG: `{SVG_PRIMARY}`
- Icon-only SVG: `{SVG_ICON}`
- Animated icon-only SVG: `{SVG_ICON_ANIMATED}`
- Shareable animated GIF: `{GIF_ICON_ANIMATED}`
- Animated icon HTML preview: `{HTML_ANIMATED_PREVIEW}`
- Dark variant SVG: `{SVG_DARK}`
- Greyscale horizontal SVG: `{SVG_GREYSCALE}`
- Black and white horizontal SVG: `{SVG_BW}`
- Greyscale icon-only SVG: `{SVG_ICON_GREYSCALE}`
- Black and white icon-only SVG: `{SVG_ICON_BW}`
- Stacked SVG: `{SVG_STACKED}`
- Proof board SVG: `{SVG_BOARD}`
- Proof sheet PDF: `{PDF_PROOF}`
- Rendered PNG preview: `{OUT_DIR / "ux-team-orbit-simple-proof-preview-1.png"}`

## Design rationale

- The team is explicit: three outline-only human avatars with connected shoulders/arms around a shared work surface.
- The icon is simplified: the beaker has been removed, leaving the team and atomic orbit as the main symbols.
- The science cue is explicit: two orbit rings wrap around the full team composition.
- The wordmark stays explicit: `UX in Science` remains the dominant readable text.
- The palette follows the brand guide: Dark Amethyst anchors the mark; Fresh Sky, Jade Green, and Saffron are accents.
- The greyscale option supports neutral print or low-color slide contexts while preserving role contrast.
- The black and white option supports one-color reproduction, embossing, engraving, and high-contrast handouts.
- The animated icon uses native SVG motion paths so the orbit balls travel directly on the two atomic tracks; a reduced-motion media query swaps the moving balls for static positions.
- The shareable GIF uses the same icon geometry on a Mint background, with a seamless loop for social posts, email, and slide insertion.
"""


def pdf_color(value):
    return colors.HexColor(value)


PAGE_W = 11 * inch
PAGE_H = 8.5 * inch


class PdfDraw:
    def __init__(self, canv, x, y, scale=1, dark=False, variant="color"):
        self.c = canv
        self.x = x
        self.y = y
        self.s = scale
        self.dark = dark
        self.variant = variant

    def px(self, value):
        return self.x + value * self.s

    def py(self, value):
        return PAGE_H - (self.y + value * self.s)

    def path(self, items, fill=None, stroke=None, width=1):
        p = self.c.beginPath()
        for item in items:
            if item[0] == "M":
                p.moveTo(self.px(item[1]), self.py(item[2]))
            elif item[0] == "L":
                p.lineTo(self.px(item[1]), self.py(item[2]))
            elif item[0] == "C":
                p.curveTo(self.px(item[1]), self.py(item[2]), self.px(item[3]), self.py(item[4]), self.px(item[5]), self.py(item[6]))
            elif item[0] == "Z":
                p.close()
        if fill:
            self.c.setFillColor(pdf_color(fill))
        if stroke:
            self.c.setStrokeColor(pdf_color(stroke))
            self.c.setLineWidth(width * self.s)
        self.c.drawPath(p, stroke=1 if stroke else 0, fill=1 if fill else 0)

    def line(self, x1, y1, x2, y2, color, width):
        self.c.setStrokeColor(pdf_color(color))
        self.c.setLineWidth(width * self.s)
        self.c.setLineCap(1)
        self.c.line(self.px(x1), self.py(y1), self.px(x2), self.py(y2))

    def circle(self, x, y, r, fill, stroke=None, width=1):
        self.c.setFillColor(pdf_color(fill))
        if stroke:
            self.c.setStrokeColor(pdf_color(stroke))
            self.c.setLineWidth(width * self.s)
        self.c.circle(self.px(x), self.py(y), r * self.s, stroke=1 if stroke else 0, fill=1)

    def circle_outline(self, x, y, r, stroke, width=1):
        self.c.setStrokeColor(pdf_color(stroke))
        self.c.setLineWidth(width * self.s)
        self.c.circle(self.px(x), self.py(y), r * self.s, stroke=1, fill=0)

    def ellipse(self, cx, cy, rx, ry, angle, stroke, width):
        self.c.saveState()
        self.c.translate(self.px(cx), self.py(cy))
        self.c.rotate(-angle)
        self.c.scale(rx * self.s, ry * self.s)
        self.c.setStrokeColor(pdf_color(stroke))
        self.c.setLineWidth(width / max(rx, ry))
        self.c.circle(0, 0, 1, stroke=1, fill=0)
        self.c.restoreState()

    def text(self, x, y, text, size, fill, font="Helvetica-Bold"):
        self.c.setFillColor(pdf_color(fill))
        self.c.setFont(font, size * self.s)
        self.c.drawString(self.px(x), self.py(y), text)


def pdf_team_icon(d):
    palette = icon_palette(d.dark, d.variant)
    sky = palette["sky"]
    jade = palette["jade"]
    saffron = palette["saffron"]
    amethyst = palette["amethyst"]
    d.ellipse(220, 156, 196, 70, -22, sky, 11)
    d.ellipse(220, 156, 152, 53, 24, jade, 7)
    d.circle(384, 77, 14, saffron)
    d.circle(66, 209, 14, jade)

    d.path([("M", 151, 173), ("C", 165, 117, 204, 94, 220, 94), ("C", 236, 94, 275, 117, 289, 173)], stroke=amethyst, width=10)
    d.circle_outline(220, 65, 23, amethyst, 8)

    d.path([("M", 80, 195), ("C", 94, 142, 130, 124, 146, 124), ("C", 164, 124, 196, 144, 206, 195)], stroke=jade, width=9)
    d.circle_outline(146, 100, 21, jade, 7)
    d.path([("M", 234, 195), ("C", 246, 144, 279, 124, 298, 124), ("C", 317, 124, 350, 144, 362, 195)], stroke=saffron, width=9)
    d.circle_outline(298, 100, 21, saffron, 7)

    d.circle(188, 213, 8, jade)
    d.circle(220, 204, 8, saffron)
    d.circle(252, 213, 8, sky)


def draw_pdf_proof():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(PDF_PROOF), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("UX in Science Simplified Team Orbit Logo Proof")
    c.setAuthor("UX in Science")
    c.setFillColor(pdf_color(COLORS["mint"]))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(pdf_color(COLORS["amethyst"]))
    c.setFont("Helvetica-Bold", 29)
    c.drawString(0.5 * inch, PAGE_H - 0.55 * inch, "UX in Science Simplified Team Orbit Logo")
    c.setFillColor(pdf_color(COLORS["text"]))
    c.setFont("Helvetica", 10.5)
    c.drawString(0.5 * inch, PAGE_H - 0.82 * inch, "Focused mark: simplified scientific team and atomic orbit with the UX in Science wordmark.")

    cards = [
        (0.5 * inch, 1.15 * inch, 3.18 * inch, 2.48 * inch, "Primary", False, "color", "horizontal"),
        (3.91 * inch, 1.15 * inch, 3.18 * inch, 2.48 * inch, "Dark", True, "color", "horizontal"),
        (7.32 * inch, 1.15 * inch, 3.18 * inch, 2.48 * inch, "Greyscale", False, "greyscale", "horizontal"),
        (0.5 * inch, 4.05 * inch, 3.18 * inch, 2.48 * inch, "Black and white", False, "black-white", "horizontal"),
        (3.91 * inch, 4.05 * inch, 3.18 * inch, 2.48 * inch, "Icon-only", False, "color", "icon"),
        (7.32 * inch, 4.05 * inch, 3.18 * inch, 2.48 * inch, "Stacked", False, "color", "stacked"),
    ]

    for x, y, w, h, label, dark, variant, layout in cards:
        c.setFillColor(pdf_color(COLORS["dark_bg"] if dark else "#FFFFFF"))
        c.setStrokeColor(pdf_color(COLORS["line"]))
        c.setLineWidth(1)
        c.roundRect(x, PAGE_H - y - h, w, h, 14, fill=1, stroke=1)
        if dark:
            label_color = COLORS["mint"]
        elif variant == "greyscale":
            label_color = COLORS["grey_900"]
        elif variant == "black-white":
            label_color = COLORS["black"]
        else:
            label_color = COLORS["amethyst"]
        c.setFillColor(pdf_color(label_color))
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x + 0.22 * inch, PAGE_H - y - 0.25 * inch, label)

        text_color = label_color
        if layout == "horizontal":
            c.setFillColor(pdf_color(text_color))
            c.setFont("Helvetica-Bold", 18.5)
            c.drawString(x + 0.2 * inch, PAGE_H - y - 1.25 * inch, "UX in Science")
            d2 = PdfDraw(c, x + 1.9 * inch, y + 0.62 * inch, 0.2, dark, variant)
            pdf_team_icon(d2)
        elif layout == "icon":
            d = PdfDraw(c, x + 0.62 * inch, y + 0.45 * inch, 0.39, dark, variant)
            pdf_team_icon(d)
        else:
            c.setFillColor(pdf_color(text_color))
            c.setFont("Helvetica-Bold", 21)
            c.drawString(x + 0.42 * inch, PAGE_H - y - 0.97 * inch, "UX in Science")
            d = PdfDraw(c, x + 1.0 * inch, y + 1.07 * inch, 0.31, dark, variant)
            pdf_team_icon(d)

    c.setFillColor(pdf_color(COLORS["amethyst"]))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(0.5 * inch, 0.28 * inch, "Palette: use full color where possible; greyscale for neutral print; black and white for one-color production and high-contrast handouts.")
    c.save()


def write_outputs():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SVG_PRIMARY.write_text(primary_svg(), encoding="utf-8")
    SVG_ICON.write_text(icon_svg(), encoding="utf-8")
    SVG_ICON_ANIMATED.write_text(animated_icon_svg(), encoding="utf-8")
    HTML_ANIMATED_PREVIEW.write_text(animated_preview_html(), encoding="utf-8")
    draw_animated_gif()
    SVG_DARK.write_text(dark_svg(), encoding="utf-8")
    SVG_GREYSCALE.write_text(greyscale_svg(), encoding="utf-8")
    SVG_BW.write_text(black_white_svg(), encoding="utf-8")
    SVG_ICON_GREYSCALE.write_text(icon_greyscale_svg(), encoding="utf-8")
    SVG_ICON_BW.write_text(icon_black_white_svg(), encoding="utf-8")
    SVG_STACKED.write_text(stacked_svg(), encoding="utf-8")
    SVG_BOARD.write_text(board_svg(), encoding="utf-8")
    MD_NOTES.write_text(notes_md(), encoding="utf-8")
    draw_pdf_proof()
    print(SVG_PRIMARY)
    print(SVG_ICON)
    print(SVG_ICON_ANIMATED)
    print(GIF_ICON_ANIMATED)
    print(HTML_ANIMATED_PREVIEW)
    print(SVG_DARK)
    print(SVG_GREYSCALE)
    print(SVG_BW)
    print(SVG_ICON_GREYSCALE)
    print(SVG_ICON_BW)
    print(SVG_STACKED)
    print(SVG_BOARD)
    print(PDF_PROOF)
    print(MD_NOTES)


if __name__ == "__main__":
    write_outputs()
