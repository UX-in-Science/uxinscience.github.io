from pathlib import Path
from html import escape
from textwrap import wrap

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "docs" / "brand-assets" / "logos"
INDIVIDUAL_DIR = OUT_DIR / "individual"
PDF_PATH = OUT_DIR / "ux-logo-explorations.pdf"

COLORS = {
    "jade": "#4CB944",
    "sky": "#00A7E1",
    "amethyst": "#34113F",
    "saffron": "#E3B505",
    "mint": "#F7FFF6",
    "dark_bg": "#010A00",
    "dark_jade": "#4DBA45",
    "dark_sky": "#1FC7FF",
    "dark_saffron": "#FACE1E",
    "border": "#D9E5D8",
    "muted": "#596057",
}

STYLE = f"""
  .ux-word {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 156px;
    font-weight: 800;
    letter-spacing: 0;
    fill: {COLORS["amethyst"]};
  }}
  .sheet-title {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 54px;
    font-weight: 800;
    letter-spacing: 0;
    fill: {COLORS["amethyst"]};
  }}
  .sheet-body {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 23px;
    font-weight: 400;
    letter-spacing: 0;
    fill: #202320;
  }}
  .card-title {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 29px;
    font-weight: 750;
    letter-spacing: 0;
    fill: {COLORS["amethyst"]};
  }}
  .card-copy {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 17px;
    font-weight: 400;
    letter-spacing: 0;
    fill: #202320;
  }}
  .card-muted {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 15px;
    font-weight: 400;
    letter-spacing: 0;
    fill: {COLORS["muted"]};
  }}
  .tag {{
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0;
    fill: {COLORS["amethyst"]};
  }}
  .thin {{
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
  }}
"""


CONCEPTS = [
    {
        "slug": "orbit-lab",
        "title": "Orbit Lab",
        "activity": "Human-centered systems, motion, discovery",
        "best_for": "Website mastheads, favicon seed, section dividers",
        "description": "A user-centered orbit suggests research systems, people in motion, and iterative inquiry.",
    },
    {
        "slug": "microscope-ux",
        "title": "Microscope UX",
        "activity": "Observation, researchers, usability sessions",
        "best_for": "Scientific audiences, workshop decks, research reports",
        "description": "The microscope is paired with participant cues to connect lab observation with human experience.",
    },
    {
        "slug": "helix-interface",
        "title": "Helix Interface",
        "activity": "Biology, computation, human factors",
        "best_for": "Cross-domain science programs and grant-facing material",
        "description": "The helix becomes a human-centered ladder, linking science, iteration, and people.",
    },
    {
        "slug": "experiment-loop",
        "title": "Experiment Loop",
        "activity": "Testing, synthesis, collaborative lab work",
        "best_for": "Friendly teaching material, event badges, slide title pages",
        "description": "A beaker, feedback loop, and two collaborators connect experimentation with team-based UX work.",
    },
    {
        "slug": "data-field",
        "title": "Data Field",
        "activity": "Measurement, participants, evidence",
        "best_for": "Reports, dashboards, evaluation summaries",
        "description": "People-as-data points make the mark evidence-led while keeping the human source of insight visible.",
    },
    {
        "slug": "molecular-network",
        "title": "Molecular Network",
        "activity": "Teams, collaboration, scientific networks",
        "best_for": "Community programs, navigation marks, small-size usage",
        "description": "The molecular network is revised as a team network, emphasizing connection and collaboration.",
    },
]


def svg_document(width, height, body, background=None):
    bg = f'<rect width="100%" height="100%" fill="{background}"/>' if background else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
<defs>
<style>
{STYLE}
</style>
</defs>
{bg}
{body}
</svg>
"""


def person_svg(x, y, scale=1, head=COLORS["amethyst"], stroke=COLORS["amethyst"], fill="none", width=4):
    r = 7 * scale
    shoulder = 20 * scale
    top = y + 14 * scale
    bottom = y + 28 * scale
    return f"""
<g>
  <circle cx="{x}" cy="{y}" r="{r}" fill="{head}"/>
  <path d="M{x - shoulder} {bottom} C{x - 14 * scale} {top} {x + 14 * scale} {top} {x + shoulder} {bottom} Z" fill="{stroke}"/>
</g>
"""


def mark_orbit_lab():
    return f"""
<g>
  <ellipse class="thin" cx="357" cy="112" rx="116" ry="43" transform="rotate(-24 357 112)" stroke="{COLORS["sky"]}" stroke-width="9"/>
  <ellipse class="thin" cx="351" cy="116" rx="86" ry="28" transform="rotate(28 351 116)" stroke="{COLORS["jade"]}" stroke-width="5" opacity="0.85"/>
  <text class="ux-word" x="54" y="175">UX</text>
  <circle cx="250" cy="151" r="13" fill="{COLORS["jade"]}"/>
  <circle cx="432" cy="62" r="12" fill="{COLORS["saffron"]}"/>
  {person_svg(383, 105, 1.0, COLORS["mint"], COLORS["amethyst"], width=5)}
</g>
"""


def mark_microscope_ux():
    return f"""
<g>
  <text class="ux-word" x="48" y="175">UX</text>
  <g class="thin" stroke="{COLORS["sky"]}" stroke-width="10">
    <path d="M362 54 L424 116"/>
    <path d="M347 71 L382 36"/>
    <path d="M411 111 L438 84"/>
    <path d="M371 124 C346 135 331 157 327 188"/>
    <path d="M303 190 H449"/>
    <path d="M329 212 C356 229 405 229 438 212"/>
  </g>
  <rect x="383" y="88" width="52" height="20" rx="6" transform="rotate(45 409 98)" fill="{COLORS["amethyst"]}"/>
  {person_svg(368, 174, 0.68, COLORS["saffron"], COLORS["amethyst"], width=5)}
  {person_svg(420, 174, 0.6, COLORS["jade"], COLORS["amethyst"], width=5)}
</g>
"""


def mark_helix_interface():
    return f"""
<g>
  <text class="ux-word" x="48" y="175">UX</text>
  <g transform="translate(350 32)">
    <path class="thin" d="M44 0 C-12 42 -12 78 44 120 C100 162 100 198 44 240" stroke="{COLORS["jade"]}" stroke-width="8"/>
    <path class="thin" d="M44 0 C100 42 100 78 44 120 C-12 162 -12 198 44 240" stroke="{COLORS["sky"]}" stroke-width="8"/>
    <g class="thin" stroke="{COLORS["saffron"]}" stroke-width="4" opacity="0.9">
      <path d="M20 36 H68"/>
      <path d="M11 78 H77"/>
      <path d="M20 162 H68"/>
      <path d="M12 204 H76"/>
    </g>
    <circle cx="44" cy="0" r="8" fill="{COLORS["saffron"]}"/>
    <circle cx="44" cy="120" r="18" fill="{COLORS["amethyst"]}"/>
    {person_svg(44, 112, 0.55, COLORS["mint"], COLORS["mint"], width=4)}
    <circle cx="44" cy="240" r="8" fill="{COLORS["saffron"]}"/>
  </g>
</g>
"""


def mark_experiment_loop():
    return f"""
<g>
  <text class="ux-word" x="48" y="175">UX</text>
  <g transform="translate(337 48)">
    <path class="thin" d="M47 0 H116" stroke="{COLORS["amethyst"]}" stroke-width="10"/>
    <path class="thin" d="M66 6 V54 L22 153 C16 168 27 183 44 183 H123 C140 183 151 168 145 153 L101 54 V6" stroke="{COLORS["sky"]}" stroke-width="9"/>
    <path d="M42 139 C70 118 102 158 130 134 L143 164 C145 173 137 180 124 180 H43 C31 180 23 173 26 164 Z" fill="{COLORS["saffron"]}" opacity="0.95"/>
    <circle cx="67" cy="90" r="7" fill="{COLORS["jade"]}"/>
    <circle cx="104" cy="111" r="5" fill="{COLORS["amethyst"]}"/>
    <path class="thin" d="M158 75 C188 97 185 144 151 160" stroke="{COLORS["jade"]}" stroke-width="7"/>
    <path d="M151 160 L170 162 L160 145 Z" fill="{COLORS["jade"]}"/>
    {person_svg(9, 62, 0.64, COLORS["saffron"], COLORS["amethyst"], width=5)}
    {person_svg(171, 50, 0.64, COLORS["jade"], COLORS["amethyst"], width=5)}
  </g>
</g>
"""


def mark_data_field():
    return f"""
<g>
  <text class="ux-word" x="48" y="175">UX</text>
  <g transform="translate(322 48)">
    <rect x="0" y="0" width="190" height="150" rx="10" fill="{COLORS["mint"]}" stroke="{COLORS["amethyst"]}" stroke-width="7"/>
    <g class="thin" stroke="{COLORS["border"]}" stroke-width="3">
      <path d="M38 10 V140"/>
      <path d="M76 10 V140"/>
      <path d="M114 10 V140"/>
      <path d="M152 10 V140"/>
      <path d="M12 38 H178"/>
      <path d="M12 76 H178"/>
      <path d="M12 114 H178"/>
    </g>
    <polyline class="thin" points="18,119 54,92 88,105 124,50 168,72" stroke="{COLORS["jade"]}" stroke-width="9"/>
    <polyline class="thin" points="18,119 54,92 88,105 124,50 168,72" stroke="{COLORS["amethyst"]}" stroke-width="3" opacity="0.45"/>
    <circle cx="18" cy="119" r="8" fill="{COLORS["sky"]}"/>
    <circle cx="54" cy="92" r="8" fill="{COLORS["saffron"]}"/>
    <circle cx="88" cy="105" r="8" fill="{COLORS["sky"]}"/>
    <circle cx="124" cy="50" r="10" fill="{COLORS["saffron"]}"/>
    <circle cx="168" cy="72" r="8" fill="{COLORS["sky"]}"/>
    {person_svg(40, 164, 0.52, COLORS["sky"], COLORS["amethyst"], width=5)}
    {person_svg(85, 164, 0.52, COLORS["jade"], COLORS["amethyst"], width=5)}
    {person_svg(130, 164, 0.52, COLORS["saffron"], COLORS["amethyst"], width=5)}
  </g>
</g>
"""


def mark_molecular_network():
    return f"""
<g>
  <text class="ux-word" x="48" y="175">UX</text>
  <g transform="translate(340 35)">
    <g class="thin" stroke="{COLORS["sky"]}" stroke-width="8">
      <path d="M75 96 L23 39"/>
      <path d="M75 96 L135 28"/>
      <path d="M75 96 L145 164"/>
      <path d="M75 96 L25 172"/>
      <path d="M23 39 L135 28"/>
      <path d="M25 172 L145 164"/>
    </g>
    <circle cx="75" cy="96" r="23" fill="{COLORS["amethyst"]}"/>
    <circle cx="23" cy="39" r="18" fill="{COLORS["jade"]}"/>
    <circle cx="135" cy="28" r="16" fill="{COLORS["saffron"]}"/>
    <circle cx="145" cy="164" r="18" fill="{COLORS["sky"]}"/>
    <circle cx="25" cy="172" r="15" fill="{COLORS["mint"]}" stroke="{COLORS["amethyst"]}" stroke-width="6"/>
    {person_svg(75, 88, 0.58, COLORS["mint"], COLORS["mint"], width=5)}
    {person_svg(23, 34, 0.34, COLORS["amethyst"], COLORS["amethyst"], width=5)}
    {person_svg(135, 24, 0.32, COLORS["amethyst"], COLORS["amethyst"], width=5)}
    {person_svg(145, 158, 0.34, COLORS["amethyst"], COLORS["amethyst"], width=5)}
  </g>
</g>
"""


MARKS = {
    "orbit-lab": mark_orbit_lab,
    "microscope-ux": mark_microscope_ux,
    "helix-interface": mark_helix_interface,
    "experiment-loop": mark_experiment_loop,
    "data-field": mark_data_field,
    "molecular-network": mark_molecular_network,
}


def individual_svg(concept):
    mark = MARKS[concept["slug"]]()
    title = concept["title"]
    body = f"""
<title>UX logo concept - {title}</title>
<desc>{concept["description"]}</desc>
<rect x="0" y="0" width="560" height="260" fill="none"/>
{mark}
"""
    return svg_document(560, 260, body)


def svg_text_block(x, y, text, width_chars, class_name, line_height, max_lines=None):
    lines = wrap(text, width=width_chars)
    if max_lines:
        lines = lines[:max_lines]
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        tspans.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    return f'<text class="{class_name}" x="{x}" y="{y}">{"".join(tspans)}</text>'


def card(concept, x, y):
    mark = MARKS[concept["slug"]]()
    return f"""
<g transform="translate({x} {y})">
  <rect x="0" y="0" width="700" height="500" rx="22" fill="#FFFFFF" stroke="{COLORS["border"]}" stroke-width="3"/>
  <g transform="translate(54 54) scale(0.92)">
    {mark}
  </g>
  <text class="card-title" x="44" y="310">{concept["title"]}</text>
  <text class="tag" x="44" y="344">{concept["activity"]}</text>
  {svg_text_block(44, 382, concept["description"], 65, "card-copy", 23, max_lines=3)}
  <text class="tag" x="44" y="456">BEST FOR</text>
  {svg_text_block(135, 456, concept["best_for"], 55, "card-muted", 20, max_lines=2)}
</g>
"""


def sheet_svg():
    positions = [(80, 295), (820, 295), (80, 830), (820, 830), (80, 1365), (820, 1365)]
    cards = "\n".join(card(concept, x, y) for concept, (x, y) in zip(CONCEPTS, positions))
    swatches = []
    for i, (name, value) in enumerate(
        [
            ("Jade", COLORS["jade"]),
            ("Sky", COLORS["sky"]),
            ("Amethyst", COLORS["amethyst"]),
            ("Saffron", COLORS["saffron"]),
            ("Mint", COLORS["mint"]),
        ]
    ):
        x = 80 + i * 142
        swatches.append(
            f'<g><rect x="{x}" y="208" width="118" height="38" rx="12" fill="{value}" stroke="{COLORS["border"]}" stroke-width="2"/>'
            f'<text class="tag" x="{x + 132}" y="232">{name} {value}</text></g>'
        )
    body = f"""
<title>UX in Science logo explorations</title>
<rect width="1600" height="1960" fill="{COLORS["mint"]}"/>
<text class="sheet-title" x="80" y="95">UX in Science Logo Explorations</text>
{svg_text_block(80, 144, "Six editable vector directions using the brand guide colors. Each keeps UX explicit and adds simple human/team and science cues.", 96, "sheet-body", 32, max_lines=2)}
{"".join(swatches)}
{cards}
<text class="tag" x="80" y="1908">Guidance: keep Dark Amethyst as the main wordmark color; keep human cues simple enough for favicon, slide, and header sizes.</text>
"""
    return svg_document(1600, 1960, body)


def markdown_brief():
    rows = "\n".join(
        f"| {c['title']} | {c['activity']} | {c['best_for']} | `{INDIVIDUAL_DIR / (c['slug'] + '.svg')}` |"
        for c in CONCEPTS
    )
    return f"""# UX in Science Logo Explorations

These are early vector directions that use the brand guide palette and keep the text `UX` explicit. This pass adds human/team cues to each science activity mark while keeping the geometry simple enough for web headers, slide footers, and potential favicons.

## Concept directions

| Direction | Science cue | Best fit | File |
|---|---|---|---|
{rows}

## Selection criteria

- Keep `UX` legible at small sizes before evaluating the science cue.
- Keep the human/team cue recognizable as a secondary signal, not the dominant shape.
- Prefer Dark Amethyst as the wordmark color for light backgrounds.
- Use Jade, Fresh Sky, and Saffron as accents, not as the primary text color.
- Check final candidates in one-color, grayscale, light theme, and dark theme.
- For slides, avoid detailed marks smaller than 0.45 in wide; use a simplified icon-only variant when needed.

## Palette used

- Jade Green: `#4CB944`
- Fresh Sky: `#00A7E1`
- Dark Amethyst: `#34113F`
- Saffron: `#E3B505`
- Mint Cream: `#F7FFF6`
"""


PAGE_W = 11 * inch
PAGE_H = 17 * inch


def pdf_color(hex_value):
    return colors.HexColor(hex_value)


class PdfMark:
    def __init__(self, canv, x, y, scale):
        self.c = canv
        self.x = x
        self.y = y
        self.s = scale

    def px(self, value):
        return self.x + value * self.s

    def py(self, value):
        return PAGE_H - (self.y + value * self.s)

    def text(self, x, y, content, size=156, fill=COLORS["amethyst"], font="Helvetica-Bold"):
        self.c.setFillColor(pdf_color(fill))
        self.c.setFont(font, size * self.s)
        self.c.drawString(self.px(x), self.py(y), content)

    def line(self, x1, y1, x2, y2, stroke, width):
        self.c.setStrokeColor(pdf_color(stroke))
        self.c.setLineWidth(width * self.s)
        self.c.setLineCap(1)
        self.c.line(self.px(x1), self.py(y1), self.px(x2), self.py(y2))

    def polyline(self, points, stroke, width):
        self.c.setStrokeColor(pdf_color(stroke))
        self.c.setLineWidth(width * self.s)
        self.c.setLineCap(1)
        self.c.setLineJoin(1)
        path = self.c.beginPath()
        path.moveTo(self.px(points[0][0]), self.py(points[0][1]))
        for x, y in points[1:]:
            path.lineTo(self.px(x), self.py(y))
        self.c.drawPath(path, stroke=1, fill=0)

    def bezier(self, points, stroke, width):
        self.c.setStrokeColor(pdf_color(stroke))
        self.c.setLineWidth(width * self.s)
        self.c.setLineCap(1)
        self.c.setLineJoin(1)
        self.c.bezier(
            self.px(points[0][0]),
            self.py(points[0][1]),
            self.px(points[1][0]),
            self.py(points[1][1]),
            self.px(points[2][0]),
            self.py(points[2][1]),
            self.px(points[3][0]),
            self.py(points[3][1]),
        )

    def circle(self, x, y, r, fill, stroke=None, width=1):
        self.c.setFillColor(pdf_color(fill))
        self.c.setStrokeColor(pdf_color(stroke or fill))
        self.c.setLineWidth(width * self.s)
        self.c.circle(self.px(x), self.py(y), r * self.s, stroke=1 if stroke else 0, fill=1)

    def person(self, x, y, scale=1, head=COLORS["amethyst"], stroke=COLORS["amethyst"], width=4):
        self.circle(x, y, 7 * scale, head)
        body = self.c.beginPath()
        body.moveTo(self.px(x - 20 * scale), self.py(y + 28 * scale))
        body.curveTo(
            self.px(x - 14 * scale),
            self.py(y + 14 * scale),
            self.px(x + 14 * scale),
            self.py(y + 14 * scale),
            self.px(x + 20 * scale),
            self.py(y + 28 * scale),
        )
        body.close()
        self.c.setFillColor(pdf_color(stroke))
        self.c.drawPath(body, stroke=0, fill=1)

    def round_rect(self, x, y, w, h, r, fill, stroke=None, width=1):
        self.c.setFillColor(pdf_color(fill))
        self.c.setStrokeColor(pdf_color(stroke or fill))
        self.c.setLineWidth(width * self.s)
        self.c.roundRect(self.px(x), self.py(y + h), w * self.s, h * self.s, r * self.s, stroke=1 if stroke else 0, fill=1)

    def rotated_ellipse(self, cx, cy, rx, ry, angle, stroke, width):
        self.c.saveState()
        self.c.translate(self.px(cx), self.py(cy))
        self.c.rotate(-angle)
        self.c.scale(rx * self.s, ry * self.s)
        self.c.setStrokeColor(pdf_color(stroke))
        self.c.setLineWidth(width / max(rx, ry))
        self.c.circle(0, 0, 1, stroke=1, fill=0)
        self.c.restoreState()

    def fluid_path(self):
        path = self.c.beginPath()
        path.moveTo(self.px(42), self.py(139))
        path.curveTo(self.px(70), self.py(118), self.px(102), self.py(158), self.px(130), self.py(134))
        path.lineTo(self.px(143), self.py(164))
        path.curveTo(self.px(145), self.py(173), self.px(137), self.py(180), self.px(124), self.py(180))
        path.lineTo(self.px(43), self.py(180))
        path.curveTo(self.px(31), self.py(180), self.px(23), self.py(173), self.px(26), self.py(164))
        path.close()
        self.c.setFillColor(pdf_color(COLORS["saffron"]))
        self.c.drawPath(path, stroke=0, fill=1)


def pdf_orbit_lab(draw):
    draw.rotated_ellipse(357, 112, 116, 43, -24, COLORS["sky"], 9)
    draw.rotated_ellipse(351, 116, 86, 28, 28, COLORS["jade"], 5)
    draw.text(54, 175, "UX")
    draw.circle(250, 151, 13, COLORS["jade"])
    draw.circle(432, 62, 12, COLORS["saffron"])
    draw.person(383, 105, 1.0, COLORS["mint"], COLORS["amethyst"], 5)


def pdf_microscope_ux(draw):
    draw.text(48, 175, "UX")
    for line in [(362, 54, 424, 116), (347, 71, 382, 36), (411, 111, 438, 84), (303, 190, 449, 190)]:
        draw.line(*line, COLORS["sky"], 10)
    draw.bezier([(371, 124), (346, 135), (331, 157), (327, 188)], COLORS["sky"], 10)
    draw.bezier([(329, 212), (356, 229), (405, 229), (438, 212)], COLORS["sky"], 10)
    draw.line(383, 88, 435, 140, COLORS["amethyst"], 16)
    draw.person(368, 174, 0.68, COLORS["saffron"], COLORS["amethyst"], 5)
    draw.person(420, 174, 0.6, COLORS["jade"], COLORS["amethyst"], 5)


def pdf_helix_interface(draw):
    draw.text(48, 175, "UX")
    d = PdfMark(draw.c, draw.x + 350 * draw.s, draw.y + 32 * draw.s, draw.s)
    d.bezier([(44, 0), (-12, 42), (-12, 78), (44, 120)], COLORS["jade"], 8)
    d.bezier([(44, 120), (100, 162), (100, 198), (44, 240)], COLORS["jade"], 8)
    d.bezier([(44, 0), (100, 42), (100, 78), (44, 120)], COLORS["sky"], 8)
    d.bezier([(44, 120), (-12, 162), (-12, 198), (44, 240)], COLORS["sky"], 8)
    for y, x1, x2 in [(36, 20, 68), (78, 11, 77), (162, 20, 68), (204, 12, 76)]:
        d.line(x1, y, x2, y, COLORS["saffron"], 4)
    d.circle(44, 0, 8, COLORS["saffron"])
    d.circle(44, 120, 18, COLORS["amethyst"])
    d.person(44, 112, 0.55, COLORS["mint"], COLORS["mint"], 4)
    d.circle(44, 240, 8, COLORS["saffron"])


def pdf_experiment_loop(draw):
    draw.text(48, 175, "UX")
    d = PdfMark(draw.c, draw.x + 337 * draw.s, draw.y + 48 * draw.s, draw.s)
    d.line(47, 0, 116, 0, COLORS["amethyst"], 10)
    for line in [(66, 6, 66, 54), (101, 6, 101, 54), (66, 54, 22, 153), (101, 54, 145, 153)]:
        d.line(*line, COLORS["sky"], 9)
    d.bezier([(22, 153), (16, 168), (27, 183), (44, 183)], COLORS["sky"], 9)
    d.line(44, 183, 123, 183, COLORS["sky"], 9)
    d.bezier([(123, 183), (140, 183), (151, 168), (145, 153)], COLORS["sky"], 9)
    d.fluid_path()
    d.circle(67, 90, 7, COLORS["jade"])
    d.circle(104, 111, 5, COLORS["amethyst"])
    d.bezier([(158, 75), (188, 97), (185, 144), (151, 160)], COLORS["jade"], 7)
    d.circle(160, 154, 4, COLORS["jade"])
    d.person(9, 62, 0.64, COLORS["saffron"], COLORS["amethyst"], 5)
    d.person(171, 50, 0.64, COLORS["jade"], COLORS["amethyst"], 5)


def pdf_data_field(draw):
    draw.text(48, 175, "UX")
    d = PdfMark(draw.c, draw.x + 322 * draw.s, draw.y + 48 * draw.s, draw.s)
    d.round_rect(0, 0, 190, 150, 10, COLORS["mint"], COLORS["amethyst"], 7)
    for gx in [38, 76, 114, 152]:
        d.line(gx, 10, gx, 140, COLORS["border"], 3)
    for gy in [38, 76, 114]:
        d.line(12, gy, 178, gy, COLORS["border"], 3)
    pts = [(18, 119), (54, 92), (88, 105), (124, 50), (168, 72)]
    d.polyline(pts, COLORS["jade"], 9)
    for x, y, fill, r in [(18, 119, COLORS["sky"], 8), (54, 92, COLORS["saffron"], 8), (88, 105, COLORS["sky"], 8), (124, 50, COLORS["saffron"], 10), (168, 72, COLORS["sky"], 8)]:
        d.circle(x, y, r, fill)
    d.person(40, 164, 0.52, COLORS["sky"], COLORS["amethyst"], 5)
    d.person(85, 164, 0.52, COLORS["jade"], COLORS["amethyst"], 5)
    d.person(130, 164, 0.52, COLORS["saffron"], COLORS["amethyst"], 5)


def pdf_molecular_network(draw):
    draw.text(48, 175, "UX")
    d = PdfMark(draw.c, draw.x + 340 * draw.s, draw.y + 35 * draw.s, draw.s)
    for line in [(75, 96, 23, 39), (75, 96, 135, 28), (75, 96, 145, 164), (75, 96, 25, 172), (23, 39, 135, 28), (25, 172, 145, 164)]:
        d.line(*line, COLORS["sky"], 8)
    d.circle(75, 96, 23, COLORS["amethyst"])
    d.circle(23, 39, 18, COLORS["jade"])
    d.circle(135, 28, 16, COLORS["saffron"])
    d.circle(145, 164, 18, COLORS["sky"])
    d.circle(25, 172, 15, COLORS["mint"], COLORS["amethyst"], 6)
    d.person(75, 88, 0.58, COLORS["mint"], COLORS["mint"], 5)
    d.person(23, 34, 0.34, COLORS["amethyst"], COLORS["amethyst"], 5)
    d.person(135, 24, 0.32, COLORS["amethyst"], COLORS["amethyst"], 5)
    d.person(145, 158, 0.34, COLORS["amethyst"], COLORS["amethyst"], 5)


PDF_MARKS = {
    "orbit-lab": pdf_orbit_lab,
    "microscope-ux": pdf_microscope_ux,
    "helix-interface": pdf_helix_interface,
    "experiment-loop": pdf_experiment_loop,
    "data-field": pdf_data_field,
    "molecular-network": pdf_molecular_network,
}


def pdf_text(canv, x, y, content, size, fill=COLORS["amethyst"], font="Helvetica"):
    canv.setFillColor(pdf_color(fill))
    canv.setFont(font, size)
    canv.drawString(x, PAGE_H - y, content)


def pdf_wrapped(canv, x, y, text, width_chars, size=10.5, leading=14, fill="#202320"):
    canv.setFillColor(pdf_color(fill))
    canv.setFont("Helvetica", size)
    current_y = y
    for line in wrap(text, width=width_chars):
        canv.drawString(x, PAGE_H - current_y, line)
        current_y += leading
    return current_y


def build_pdf_sheet():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("UX in Science Logo Explorations")
    c.setAuthor("UX in Science")
    c.setFillColor(pdf_color(COLORS["mint"]))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    pdf_text(c, 48, 70, "UX in Science Logo Explorations", 34, font="Helvetica-Bold")
    pdf_wrapped(
        c,
        48,
        100,
        "Six editable vector directions using the brand guide colors. Each keeps UX explicit and adds simple human/team and science cues.",
        95,
        12,
        16,
    )
    swatch_x = 48
    for name, value in [("Jade", COLORS["jade"]), ("Sky", COLORS["sky"]), ("Amethyst", COLORS["amethyst"]), ("Saffron", COLORS["saffron"]), ("Mint", COLORS["mint"])]:
        c.setFillColor(pdf_color(value))
        c.roundRect(swatch_x, PAGE_H - 158, 44, 22, 7, fill=1, stroke=0)
        pdf_text(c, swatch_x + 51, 152, f"{name} {value}", 7.5, COLORS["amethyst"], "Helvetica-Bold")
        swatch_x += 142

    positions = [(48, 190), (420, 190), (48, 505), (420, 505), (48, 820), (420, 820)]
    for concept, (x, y) in zip(CONCEPTS, positions):
        c.setFillColor(colors.white)
        c.setStrokeColor(pdf_color(COLORS["border"]))
        c.setLineWidth(1.2)
        c.roundRect(x, PAGE_H - y - 285, 324, 285, 14, fill=1, stroke=1)
        mark = PdfMark(c, x + 18, y + 20, 0.48)
        PDF_MARKS[concept["slug"]](mark)
        pdf_text(c, x + 20, y + 170, concept["title"], 17, COLORS["amethyst"], "Helvetica-Bold")
        pdf_text(c, x + 20, y + 193, concept["activity"], 8.5, COLORS["amethyst"], "Helvetica-Bold")
        pdf_wrapped(c, x + 20, y + 213, concept["description"], 56, 8.5, 11, "#202320")
        pdf_text(c, x + 20, y + 264, "BEST FOR", 7, COLORS["amethyst"], "Helvetica-Bold")
        pdf_wrapped(c, x + 77, y + 264, concept["best_for"], 38, 7.5, 9.5, COLORS["muted"])

    pdf_text(
        c,
        48,
        1156,
        "Guidance: keep Dark Amethyst as the main wordmark color; keep human cues simple enough for favicon, slide, and header sizes.",
        8.5,
        COLORS["amethyst"],
        "Helvetica-Bold",
    )
    c.save()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    INDIVIDUAL_DIR.mkdir(parents=True, exist_ok=True)
    for concept in CONCEPTS:
        (INDIVIDUAL_DIR / f"{concept['slug']}.svg").write_text(individual_svg(concept), encoding="utf-8")
    (OUT_DIR / "ux-logo-explorations.svg").write_text(sheet_svg(), encoding="utf-8")
    (OUT_DIR / "ux-logo-explorations.md").write_text(markdown_brief(), encoding="utf-8")
    build_pdf_sheet()
    print(OUT_DIR / "ux-logo-explorations.svg")
    print(OUT_DIR / "ux-logo-explorations.md")
    print(PDF_PATH)
    for concept in CONCEPTS:
        print(INDIVIDUAL_DIR / f"{concept['slug']}.svg")


if __name__ == "__main__":
    main()
