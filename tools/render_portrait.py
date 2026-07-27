from pathlib import Path
from PIL import Image

INPUT = Path("assets/photo-ready1.png")
OUTPUT = Path("portrait.svg")

GLYPHS = " '.,:;~+*xXO#"

# ==========================================
# CANVAS CONFIG (Matches sysinfo.svg aspect 340x490 @ 2x = 680x980)
# ==========================================
CANVAS_W = 680
CANVAS_H = 980

BACKGROUND = "#0d1117"
BORDER = "#30363d"
TITLE = "#ffffff"

# ==========================================
# ASCII GRID CONFIG
# ==========================================
# Content box inside window frame:
# Header takes y=0..84. Content Y from 95 to 960 (height ~865px, width ~640px)
CONTENT_X = 20
CONTENT_Y = 95
CONTENT_W = 640
CONTENT_H = 865

# Character sizing
FONT_SIZE = 11
LINE_HEIGHT = 12.5
CHAR_WIDTH = 6.6  # Approx width of Consolas at 11px font-size

COLS = int(CONTENT_W / CHAR_WIDTH)   # ~96 columns
ROWS = int(CONTENT_H / LINE_HEIGHT)  # ~69 rows

# ----------------------------
# Process Image
# ----------------------------
img = Image.open(INPUT).convert("RGBA")

# Crop tight alpha bounding box
alpha = img.split()[-1]
bbox = alpha.getbbox()
if bbox:
    img = img.crop(bbox)

# Resize to ASCII grid dimensions
img_resized = img.resize((COLS, ROWS), Image.Resampling.LANCZOS)
pixels = img_resized.load()

rows = []
for y in range(ROWS):
    line = ""
    for x in range(COLS):
        r, g, b, a = pixels[x, y]
        if a < 10:
            line += " "
            continue

        gray = int(0.299 * r + 0.587 * g + 0.114 * b)
        index = int(gray / 255 * (len(GLYPHS) - 1))
        index = max(0, min(index, len(GLYPHS) - 1))
        line += GLYPHS[index]

    rows.append(line)

# Calculate exact ASCII rendered box to center it horizontally and vertically inside content area
ascii_render_w = COLS * CHAR_WIDTH
ascii_render_h = ROWS * LINE_HEIGHT

start_x = CONTENT_X + (CONTENT_W - ascii_render_w) / 2
start_y = CONTENT_Y + (CONTENT_H - ascii_render_h) / 2

# ----------------------------
# Generate SVG
# ----------------------------
svg = []
svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{CANVAS_W}"
height="{CANVAS_H}"
viewBox="0 0 {CANVAS_W} {CANVAS_H}">
''')

svg.append(f'''
<defs>
<filter id="glow">
    <feGaussianBlur stdDeviation="2" result="blur"/>
    <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
    </feMerge>
</filter>
</defs>

<style>
svg {{
    background: {BACKGROUND};
}}

text {{
    font-family: Consolas, Menlo, monospace;
}}

.title {{
    fill: {TITLE};
    font-size: 20px;
    font-weight: bold;
}}

.ascii-text {{
    font-size: {FONT_SIZE}px;
    fill: #39d353;
    white-space: pre;
}}
</style>
''')

# Outer Window Card Frame
svg.append(f'''
<rect
x="2"
y="2"
width="{CANVAS_W-4}"
height="{CANVAS_H-4}"
rx="24"
fill="{BACKGROUND}"
stroke="{BORDER}"
stroke-width="3"/>
''')

# macOS Window Buttons
svg.append('''
<circle cx="36" cy="42" r="10" fill="#ff5f56"/>
<circle cx="68" cy="42" r="10" fill="#ffbd2e"/>
<circle cx="100" cy="42" r="10" fill="#27c93f"/>
''')

# Window Title
svg.append('''
<text
x="140"
y="49"
class="title">
Portrait
</text>
''')

# Window Header Divider
svg.append(f'''
<line
x1="0"
y1="84"
x2="{CANVAS_W}"
y2="84"
stroke="{BORDER}"
stroke-width="2"/>
''')

# ASCII Portrait Rows with Animation
for i, row in enumerate(rows):
    clip_id = f"clip{i}"
    row_y = start_y + (i + 1) * LINE_HEIGHT
    
    svg.append(f'''
<clipPath id="{clip_id}">
<rect x="{start_x}" y="{start_y + i * LINE_HEIGHT}" width="0" height="{LINE_HEIGHT}">
<animate
attributeName="width"
from="0"
to="{ascii_render_w}"
begin="{i * 0.03:.2f}s"
dur="0.25s"
fill="freeze"/>
</rect>
</clipPath>

<text
x="{start_x}"
y="{row_y}"
class="ascii-text"
clip-path="url(#{clip_id})">{row}</text>
''')

svg.append("</svg>")

OUTPUT.write_text("".join(svg), encoding="utf-8")
print(f"Saved -> {OUTPUT}")