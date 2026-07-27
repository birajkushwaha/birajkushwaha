from pathlib import Path
from PIL import Image

INPUT = Path("assets/photo-ready1.png")
OUTPUT = Path("portrait.svg")

GLYPHS = " '.,:;~+*xXO#"

WIDTH = 80
FONT_SIZE = 8
LINE_HEIGHT = 10

# ----------------------------
# Load image WITH alpha channel
# ----------------------------

img = Image.open(INPUT).convert("RGBA")

aspect = img.height / img.width
HEIGHT = int(WIDTH * aspect * 0.55)

img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

pixels = img.load()

rows = []

for y in range(HEIGHT):

    line = ""

    for x in range(WIDTH):

        r, g, b, a = pixels[x, y]

        # Transparent background -> empty space
        if a < 10:
            line += " "
            continue

        # Convert RGB to grayscale
        gray = int(0.299 * r + 0.587 * g + 0.114 * b)

        # Gamma correction
        gray = int((gray / 255) ** 0.8 * 255)

        index = int((255 - gray) / 255 * (len(GLYPHS) - 1))
        index = max(0, min(index, len(GLYPHS) - 1))

        line += GLYPHS[index]

    # pyrefly: ignore [parse-error]
    rows.append(line)

svg_width = WIDTH * FONT_SIZE
svg_height = HEIGHT * LINE_HEIGHT

svg = []

svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{svg_width}"
height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}">
''')

svg.append("""
<style>

svg{
background:#0d1117;
}

text{
font-family:Consolas,monospace;
font-size:8px;
fill:#7df9ff;
white-space:pre;
}

</style>
""")

for i, row in enumerate(rows):

    clip = f"clip{i}"

    svg.append(f'''
<clipPath id="{clip}">
<rect x="0" y="{i*LINE_HEIGHT}" width="0" height="{LINE_HEIGHT}">
<animate
attributeName="width"
from="0"
to="{svg_width}"
begin="{i*0.04}s"
dur="0.25s"
fill="freeze"/>
</rect>
</clipPath>
''')

    svg.append(f'''
<text
x="0"
y="{(i+1)*LINE_HEIGHT}"
clip-path="url(#{clip})">{row}</text>
''')

svg.append("</svg>")

OUTPUT.write_text("".join(svg), encoding="utf-8")

print("Saved -> portrait.svg")