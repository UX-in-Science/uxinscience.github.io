from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "docs" / "brand-assets" / "pdf"
PDF_PATH = OUT_DIR / "ux-in-science-brand-guide.pdf"
MD_PATH = OUT_DIR / "ux-in-science-brand-guide.md"


CORE = [
    {
        "name": "Jade Green",
        "hex": "#4CB944",
        "rgb": "76, 185, 68",
        "hsl": "116, 46%, 50%",
        "role": "Primary accent, positive states, progress",
    },
    {
        "name": "Fresh Sky",
        "hex": "#00A7E1",
        "rgb": "0, 167, 225",
        "hsl": "195, 100%, 44%",
        "role": "Secondary accent, links, information",
    },
    {
        "name": "Dark Amethyst",
        "hex": "#34113F",
        "rgb": "52, 17, 63",
        "hsl": "286, 58%, 16%",
        "role": "Primary text, headings, strong surfaces",
    },
    {
        "name": "Saffron",
        "hex": "#E3B505",
        "rgb": "227, 181, 5",
        "hsl": "48, 96%, 45%",
        "role": "Highlight, warnings, callouts",
    },
    {
        "name": "Mint Cream",
        "hex": "#F7FFF6",
        "rgb": "247, 255, 246",
        "hsl": "113, 100%, 98%",
        "role": "Main light background, quiet panels",
    },
]

THEMES = {
    "Light": {
        "Background": "#F7FFF6",
        "Text": "#34113F",
        "Primary": "#4CB944",
        "Info": "#00A7E1",
        "Highlight": "#E3B505",
    },
    "Dark": {
        "Background": "#010A00",
        "Text": "#F7FFF6",
        "Primary": "#4DBA45",
        "Info": "#1FC7FF",
        "Amethyst accent": "#E3BFEE",
        "Highlight": "#FACE1E",
    },
}

TEXT_VARIANTS = [
    ("Jade text", "#30742B", "5.63 on Mint Cream"),
    ("Sky link", "#007EA8", "4.53 on Mint Cream"),
    ("Sky strong link", "#00698C", "6.06 on Mint Cream"),
    ("Saffron text", "#8D7103", "4.58 on Mint Cream"),
    ("Saffron strong text", "#705A02", "6.53 on Mint Cream"),
]

WCAG_REFERENCES = [
    "WCAG 2.2 SC 1.4.3 Contrast (Minimum): https://www.w3.org/TR/WCAG22/#contrast-minimum",
    "WCAG 2.2 SC 1.4.11 Non-text Contrast: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html",
    "WCAG 2.2 SC 1.4.1 Use of Color: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html",
]


def hex_color(value):
    return colors.HexColor(value)


def rel_channel(pair):
    value = int(pair, 16) / 255.0
    if value <= 0.04045:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def luminance(hex_value):
    value = hex_value.replace("#", "")
    return (
        0.2126 * rel_channel(value[0:2])
        + 0.7152 * rel_channel(value[2:4])
        + 0.0722 * rel_channel(value[4:6])
    )


def contrast(a, b):
    l1, l2 = sorted([luminance(a), luminance(b)], reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def pass_label(ratio, normal_text=True):
    if normal_text:
        if ratio >= 7:
            return "AAA"
        if ratio >= 4.5:
            return "AA"
        return "Fail"
    if ratio >= 4.5:
        return "AAA large"
    if ratio >= 3:
        return "AA large/UI"
    return "Fail"


def readable_text_for_bg(hex_value):
    return colors.white if contrast("#FFFFFF", hex_value) >= contrast("#000000", hex_value) else colors.black


def p(text, style):
    return Paragraph(text, style)


class ColorBand(Flowable):
    def __init__(self, swatches, height=0.9 * inch, gap=0.06 * inch):
        super().__init__()
        self.swatches = swatches
        self.height = height
        self.gap = gap

    def wrap(self, avail_width, avail_height):
        self.width = avail_width
        return avail_width, self.height

    def draw(self):
        count = len(self.swatches)
        width = (self.width - self.gap * (count - 1)) / count
        for index, (name, hex_value) in enumerate(self.swatches):
            x = index * (width + self.gap)
            self.canv.setFillColor(hex_color(hex_value))
            self.canv.roundRect(x, 0, width, self.height, 8, fill=1, stroke=0)
            self.canv.setFillColor(readable_text_for_bg(hex_value))
            self.canv.setFont("Helvetica-Bold", 8.5)
            self.canv.drawString(x + 8, 12, hex_value.upper())
            self.canv.setFont("Helvetica", 7)
            self.canv.drawString(x + 8, 25, name)


def build_styles():
    base = getSampleStyleSheet()
    styles = {
        "Title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=32,
            textColor=hex_color("#34113F"),
            spaceAfter=10,
            alignment=TA_LEFT,
        ),
        "Subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=12,
            leading=17,
            textColor=hex_color("#34113F"),
            spaceAfter=12,
        ),
        "H1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=hex_color("#34113F"),
            spaceBefore=4,
            spaceAfter=8,
        ),
        "H2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=hex_color("#34113F"),
            spaceBefore=6,
            spaceAfter=4,
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=12.5,
            textColor=hex_color("#222222"),
            spaceAfter=5,
        ),
        "Small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.4,
            leading=9.5,
            textColor=hex_color("#333333"),
        ),
        "SmallCenter": ParagraphStyle(
            "SmallCenter",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.4,
            leading=9.5,
            textColor=hex_color("#333333"),
            alignment=TA_CENTER,
        ),
        "TableHead": ParagraphStyle(
            "TableHead",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.4,
            leading=9.2,
            textColor=colors.white,
        ),
        "TableCell": ParagraphStyle(
            "TableCell",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.3,
            leading=9.1,
            textColor=hex_color("#222222"),
        ),
        "Code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7,
            leading=9,
            textColor=hex_color("#111111"),
            backColor=hex_color("#F1F5F1"),
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=6,
        ),
    }
    return styles


def bullets(items, styles):
    return ListFlowable(
        [
            ListItem(p(item, styles["Body"]), leftIndent=10, bulletColor=hex_color("#34113F"))
            for item in items
        ],
        bulletType="bullet",
        start="circle",
        leftIndent=12,
        bulletFontName="Helvetica",
        bulletFontSize=7,
    )


def make_table(data, col_widths, styles, header=True):
    table = Table(data, colWidths=col_widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("BOX", (0, 0), (-1, -1), 0.4, hex_color("#B9C7B8")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, hex_color("#D9E5D8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), hex_color("#34113F")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ]
        )
    table.setStyle(TableStyle(commands))
    return table


def swatch_cell(hex_value, label, styles):
    text_color = "#FFFFFF" if contrast("#FFFFFF", hex_value) >= contrast("#000000", hex_value) else "#000000"
    return Paragraph(
        f'<font color="{text_color}"><b>{label}</b><br/>{hex_value.upper()}</font>',
        styles["SmallCenter"],
    )


def build_pdf():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.62 * inch,
        bottomMargin=0.52 * inch,
        title="UX in Science Brand Guide",
        author="UX in Science",
    )
    styles = build_styles()
    story = []

    def add_footer(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(hex_color("#666666"))
        canvas.drawString(0.55 * inch, 0.32 * inch, "UX in Science Brand Guide")
        canvas.drawRightString(8.0 * inch, 0.32 * inch, f"{document.page}")
        canvas.restoreState()

    story.append(p("UX in Science Brand Guide", styles["Title"]))
    story.append(
        p(
            "A practical color and accessibility system for web pages, interface components, data graphics, and presentation slides.",
            styles["Subtitle"],
        )
    )
    story.append(ColorBand([(c["name"], c["hex"]) for c in CORE], height=1.15 * inch))
    story.append(Spacer(1, 0.2 * inch))
    story.append(p("Brand posture", styles["H1"]))
    story.append(
        p(
            "UX in Science should feel precise, evidence-driven, calm, and approachable. Use the bright colors to create momentum and wayfinding, but let Dark Amethyst and Mint Cream carry most reading surfaces.",
            styles["Body"],
        )
    )
    story.append(
        bullets(
            [
                "<b>Default voice:</b> clear, concise, research-literate, and human.",
                "<b>Visual rhythm:</b> generous whitespace, strong hierarchy, compact tables, and directly labeled data.",
                "<b>Accessibility stance:</b> color supports meaning; it never carries meaning alone.",
            ],
            styles,
        )
    )
    story.append(Spacer(1, 0.14 * inch))
    story.append(p("Source files", styles["H2"]))
    story.append(
        p(
            "Palette source: <font name='Courier'>palette.scss</font>, <font name='Courier'>palette.txt</font>, <font name='Courier'>UX in Science.pdf</font>, and <font name='Courier'>Themes-LightDark.png</font>.",
            styles["Small"],
        )
    )
    story.append(PageBreak())

    story.append(p("Core Palette", styles["H1"]))
    token_rows = [[p("Color", styles["TableHead"]), p("Values", styles["TableHead"]), p("Role", styles["TableHead"]), p("Accessible notes", styles["TableHead"])]]
    notes = {
        "Jade Green": "Do not use as small text on light backgrounds. Use as a fill with Dark Amethyst or black text, or use darker text variant #30742B.",
        "Fresh Sky": "Do not use as small text on light backgrounds. Use as accent fill, underlines, chart markers, or darker link variants #007EA8/#00698C.",
        "Dark Amethyst": "Primary light-theme text and strongest brand surface. Works with Mint Cream, white, Jade, Sky, and Saffron.",
        "Saffron": "Best for highlights and attention, not body text on light backgrounds. Use #8D7103 or #705A02 for text.",
        "Mint Cream": "Primary light canvas. Pair with Dark Amethyst or black text.",
    }
    for c in CORE:
        swatch = swatch_cell(c["hex"], c["name"], styles)
        values = p(f"<b>{c['hex']}</b><br/>RGB {c['rgb']}<br/>HSL {c['hsl']}", styles["TableCell"])
        token_rows.append([swatch, values, p(c["role"], styles["TableCell"]), p(notes[c["name"]], styles["TableCell"])])
    table = make_table(token_rows, [1.35 * inch, 1.45 * inch, 1.7 * inch, 2.9 * inch], styles)
    for i, c in enumerate(CORE, start=1):
        table.setStyle(TableStyle([("BACKGROUND", (0, i), (0, i), hex_color(c["hex"]))]))
    story.append(table)
    story.append(Spacer(1, 0.18 * inch))
    story.append(p("Light and dark theme tokens", styles["H2"]))
    theme_rows = [[p("Theme", styles["TableHead"]), p("Token", styles["TableHead"]), p("Hex", styles["TableHead"]), p("Usage", styles["TableHead"])]]
    theme_usage = {
        "Background": "Page or slide canvas.",
        "Text": "Body copy, headings, captions.",
        "Primary": "Primary accent and positive action.",
        "Info": "Information accent and chart series.",
        "Highlight": "Callouts, notes, and attention.",
        "Amethyst accent": "Dark-theme tint for secondary emphasis.",
    }
    for theme, tokens in THEMES.items():
        for token, hex_value in tokens.items():
            theme_rows.append(
                [
                    p(theme, styles["TableCell"]),
                    p(token, styles["TableCell"]),
                    swatch_cell(hex_value, hex_value, styles),
                    p(theme_usage[token], styles["TableCell"]),
                ]
            )
    theme_table = make_table(theme_rows, [0.8 * inch, 1.25 * inch, 1.35 * inch, 4.0 * inch], styles)
    row_index = 1
    for theme, tokens in THEMES.items():
        for token, hex_value in tokens.items():
            theme_table.setStyle(TableStyle([("BACKGROUND", (2, row_index), (2, row_index), hex_color(hex_value))]))
            row_index += 1
    story.append(theme_table)
    story.append(PageBreak())

    story.append(p("Accessibility Rules", styles["H1"]))
    story.append(
        p(
            "The guide targets WCAG 2.2 AA contrast: 4.5:1 for normal text, 3:1 for large text and meaningful graphics/UI boundaries, and an additional non-color cue wherever color conveys meaning.",
            styles["Body"],
        )
    )
    contrast_rows = [[p("Combination", styles["TableHead"]), p("Ratio", styles["TableHead"]), p("Result", styles["TableHead"]), p("Guidance", styles["TableHead"])]]
    contrast_cases = [
        ("Dark Amethyst text on Mint Cream", "#34113F", "#F7FFF6", "Use for body copy and headings in light theme."),
        ("Black text on Mint Cream", "#000000", "#F7FFF6", "Use for utilitarian tables, code, and dense labels."),
        ("Jade text on Mint Cream", "#4CB944", "#F7FFF6", "Fail for normal text; use #30742B if green text is required."),
        ("Fresh Sky text on Mint Cream", "#00A7E1", "#F7FFF6", "Fail for normal text; use #007EA8 or #00698C for links."),
        ("Saffron text on Mint Cream", "#E3B505", "#F7FFF6", "Fail for normal text; use #8D7103 or #705A02."),
        ("Mint Cream text on Dark Amethyst", "#F7FFF6", "#34113F", "Use for dark cards, banners, and title slides."),
        ("Dark Amethyst text on Jade Green", "#34113F", "#4CB944", "Pass for buttons and badges."),
        ("Dark Amethyst text on Fresh Sky", "#34113F", "#00A7E1", "Pass for buttons and badges."),
        ("Dark Amethyst text on Saffron", "#34113F", "#E3B505", "Pass for buttons, tags, and callouts."),
        ("Dark-theme Jade on #010A00", "#4DBA45", "#010A00", "Pass for dark-mode text, icons, and chart marks."),
        ("Dark-theme Sky on #010A00", "#1FC7FF", "#010A00", "Pass for dark-mode links, focus, and chart marks."),
        ("Dark-theme Saffron on #010A00", "#FACE1E", "#010A00", "Pass for dark-mode highlights."),
    ]
    for label, fg, bg, guidance in contrast_cases:
        ratio = contrast(fg, bg)
        contrast_rows.append(
            [
                p(label, styles["TableCell"]),
                p(f"{ratio:.2f}:1", styles["TableCell"]),
                p(pass_label(ratio), styles["TableCell"]),
                p(guidance, styles["TableCell"]),
            ]
        )
    story.append(make_table(contrast_rows, [2.3 * inch, 0.75 * inch, 0.8 * inch, 3.55 * inch], styles))
    story.append(Spacer(1, 0.16 * inch))
    story.append(p("Accessible text variants from the shade scale", styles["H2"]))
    variant_rows = [[p("Variant", styles["TableHead"]), p("Hex", styles["TableHead"]), p("Contrast on Mint Cream", styles["TableHead"]), p("Use", styles["TableHead"])]]
    variant_use = {
        "Jade text": "Success labels, status text, data labels.",
        "Sky link": "Minimum AA link color on light backgrounds.",
        "Sky strong link": "Preferred blue link and chart line.",
        "Saffron text": "Minimum AA warning text.",
        "Saffron strong text": "Preferred warning text and chart line.",
    }
    for name, hex_value, ratio in TEXT_VARIANTS:
        variant_rows.append(
            [
                p(name, styles["TableCell"]),
                swatch_cell(hex_value, hex_value, styles),
                p(ratio, styles["TableCell"]),
                p(variant_use[name], styles["TableCell"]),
            ]
        )
    variant_table = make_table(variant_rows, [1.4 * inch, 1.15 * inch, 1.5 * inch, 3.35 * inch], styles)
    for i, (_, hex_value, _) in enumerate(TEXT_VARIANTS, start=1):
        variant_table.setStyle(TableStyle([("BACKGROUND", (1, i), (1, i), hex_color(hex_value))]))
    story.append(variant_table)
    story.append(PageBreak())

    story.append(p("Web Usage Guidelines", styles["H1"]))
    story.append(
        bullets(
            [
                "<b>Light theme:</b> use Mint Cream as the page canvas and Dark Amethyst as the default text color. White may be used for cards, tables, and form fields.",
                "<b>Buttons and controls:</b> borderless Jade, Sky, and Saffron components do not meet the 3:1 boundary rule on Mint Cream. Add a 2 px Dark Amethyst border, use a darker shade, or use a Dark Amethyst fill.",
                "<b>Links:</b> do not use base Fresh Sky for small link text on light backgrounds. Use #007EA8 minimum, #00698C preferred, and keep underlines or another persistent cue.",
                "<b>Focus states:</b> use a 2-3 px Dark Amethyst focus ring on light backgrounds. Use dark-theme Sky or Saffron on #010A00.",
                "<b>Color meaning:</b> pair status color with text, icon shape, pattern, or placement. For example, do not communicate required fields or chart categories with color alone.",
                "<b>Dark theme:</b> #010A00 background with Mint Cream text is the default. The dark-theme accent colors are strong enough for text, icons, charts, and focus rings.",
            ],
            styles,
        )
    )
    story.append(Spacer(1, 0.08 * inch))
    story.append(p("Suggested CSS tokens", styles["H2"]))
    story.append(
        p(
            "--ux-bg: #F7FFF6;<br/>--ux-surface: #FFFFFF;<br/>--ux-text: #34113F;<br/>--ux-link: #00698C;<br/>--ux-primary: #4CB944;<br/>--ux-primary-text: #34113F;<br/>--ux-info: #00A7E1;<br/>--ux-highlight: #E3B505;<br/>--ux-focus: #34113F;<br/><br/>@media (prefers-color-scheme: dark) {<br/>&nbsp;&nbsp;--ux-bg: #010A00;<br/>&nbsp;&nbsp;--ux-surface: #34113F;<br/>&nbsp;&nbsp;--ux-text: #F7FFF6;<br/>&nbsp;&nbsp;--ux-link: #1FC7FF;<br/>&nbsp;&nbsp;--ux-primary: #4DBA45;<br/>&nbsp;&nbsp;--ux-primary-text: #010A00;<br/>&nbsp;&nbsp;--ux-info: #1FC7FF;<br/>&nbsp;&nbsp;--ux-highlight: #FACE1E;<br/>&nbsp;&nbsp;--ux-focus: #FACE1E;<br/>}",
            styles["Code"],
        )
    )
    story.append(Spacer(1, 0.08 * inch))
    story.append(p("Component recipes", styles["H2"]))
    recipe_rows = [[p("Component", styles["TableHead"]), p("Recommended color treatment", styles["TableHead"]), p("Avoid", styles["TableHead"])]]
    recipe_rows.extend(
        [
            [
                p("Primary CTA", styles["TableCell"]),
                p("Dark Amethyst fill with Mint Cream text, or Jade fill with Dark Amethyst text and Dark Amethyst border.", styles["TableCell"]),
                p("White text on Jade, Sky, or Saffron.", styles["TableCell"]),
            ],
            [
                p("Status badge", styles["TableCell"]),
                p("Jade/Sky/Saffron fill, Dark Amethyst text, explicit label, and icon or shape cue.", styles["TableCell"]),
                p("Color-only status dots.", styles["TableCell"]),
            ],
            [
                p("Form field", styles["TableCell"]),
                p("White field on Mint Cream with Dark Amethyst label, 1.5-2 px Dark Amethyst or neutral border, clear focus ring.", styles["TableCell"]),
                p("Pale border that is the only field boundary.", styles["TableCell"]),
            ],
            [
                p("Alert/callout", styles["TableCell"]),
                p("Saffron header strip or icon with Dark Amethyst text; include alert title and actionable copy.", styles["TableCell"]),
                p("Saffron paragraph text on light background.", styles["TableCell"]),
            ],
        ]
    )
    story.append(make_table(recipe_rows, [1.2 * inch, 4.0 * inch, 2.2 * inch], styles))
    story.append(PageBreak())

    story.append(p("Slides and Data Graphics", styles["H1"]))
    story.append(
        bullets(
            [
                "<b>Default slide:</b> Mint Cream background, Dark Amethyst title and body text. Use one accent color per slide unless the content is a chart.",
                "<b>Dark title slide:</b> #010A00 background with Mint Cream title and dark-theme accents. Keep dense body copy off dark slides.",
                "<b>Text scale:</b> titles 34-44 pt, body 24-28 pt, annotations at least 18 pt. Keep labels direct and avoid long paragraphs.",
                "<b>Scientific images:</b> avoid text directly over busy images. If overlay is necessary, use an opaque or near-opaque Dark Amethyst/#010A00 panel with Mint Cream text.",
                "<b>Projector safety:</b> test slides in grayscale and on a low-brightness display. Saffron and Mint Cream can wash out if used as thin marks.",
            ],
            styles,
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(p("Chart palette", styles["H2"]))
    chart_rows = [[p("Purpose", styles["TableHead"]), p("Light background", styles["TableHead"]), p("Dark background", styles["TableHead"]), p("Guidance", styles["TableHead"])]]
    chart_rows.extend(
        [
            [
                p("Primary series", styles["TableCell"]),
                swatch_cell("#34113F", "Dark Amethyst", styles),
                swatch_cell("#F7FFF6", "Mint Cream", styles),
                p("Use as the anchor series or baseline.", styles["TableCell"]),
            ],
            [
                p("Green series", styles["TableCell"]),
                swatch_cell("#30742B", "Jade -37.5%", styles),
                swatch_cell("#4DBA45", "Dark Jade", styles),
                p("Use darker Jade for lines/markers on light slides.", styles["TableCell"]),
            ],
            [
                p("Blue series", styles["TableCell"]),
                swatch_cell("#00698C", "Sky -37.5%", styles),
                swatch_cell("#1FC7FF", "Dark Sky", styles),
                p("Preferred for links, methods, secondary datasets.", styles["TableCell"]),
            ],
            [
                p("Yellow series", styles["TableCell"]),
                swatch_cell("#705A02", "Saffron -50%", styles),
                swatch_cell("#FACE1E", "Dark Saffron", styles),
                p("Use with labels or patterns; avoid thin base Saffron lines on light backgrounds.", styles["TableCell"]),
            ],
            [
                p("Accessible category cue", styles["TableCell"]),
                p("Color plus marker shape, line style, label, or pattern.", styles["TableCell"]),
                p("Color plus marker shape, line style, label, or pattern.", styles["TableCell"]),
                p("Do not rely on hue alone for categories or significance.", styles["TableCell"]),
            ],
        ]
    )
    chart_table = make_table(chart_rows, [1.25 * inch, 1.65 * inch, 1.65 * inch, 2.85 * inch], styles)
    chart_bg_map = {
        (1, 1): "#34113F",
        (2, 1): "#30742B",
        (3, 1): "#00698C",
        (4, 1): "#705A02",
        (1, 2): "#F7FFF6",
        (2, 2): "#4DBA45",
        (3, 2): "#1FC7FF",
        (4, 2): "#FACE1E",
    }
    for (row, col), hex_value in chart_bg_map.items():
        chart_table.setStyle(TableStyle([("BACKGROUND", (col, row), (col, row), hex_color(hex_value))]))
    story.append(chart_table)
    story.append(Spacer(1, 0.16 * inch))
    story.append(p("Slide layout patterns", styles["H2"]))
    story.append(
        bullets(
            [
                "Use a Dark Amethyst title bar or left rule when a slide needs more structure.",
                "Use Saffron sparingly for the single most important conclusion, not every annotation.",
                "Use Fresh Sky for methods, links, or navigation; use Jade for outcomes, progress, or success.",
                "For section dividers, use full-bleed Dark Amethyst or #010A00 with Mint Cream text and one accent line.",
            ],
            styles,
        )
    )
    story.append(PageBreak())

    story.append(p("Production Checklist", styles["H1"]))
    story.append(
        bullets(
            [
                "Normal web text reaches at least 4.5:1 contrast; large text and meaningful graphics/UI boundaries reach at least 3:1.",
                "Interactive controls have visible boundaries and focus indicators that meet 3:1 against adjacent colors.",
                "Every color-coded status, chart series, or required field has a second cue: text, icon, shape, pattern, or direct label.",
                "Bright base accents are not used as paragraph text on Mint Cream or white.",
                "Dark-mode pages use #010A00 background, Mint Cream text, and the dark-theme accent tokens from the theme image.",
                "Slides remain readable in grayscale and at projector brightness; charts have direct labels and sufficient line weight.",
            ],
            styles,
        )
    )
    story.append(Spacer(1, 0.16 * inch))
    story.append(p("References", styles["H2"]))
    for ref in WCAG_REFERENCES:
        story.append(p(ref, styles["Small"]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        p(
            "Contrast ratios in this guide were computed from the supplied hex values using the WCAG relative luminance formula. The light/dark theme values come from Themes-LightDark.png.",
            styles["Small"],
        )
    )

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)


def build_markdown():
    md = """# UX in Science Brand Guide

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
"""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MD_PATH.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    build_pdf()
    build_markdown()
    print(PDF_PATH)
    print(MD_PATH)
