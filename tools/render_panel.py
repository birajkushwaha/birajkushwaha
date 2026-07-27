from pathlib import Path

OUTPUT = Path("sysinfo.svg")

# ==========================================
# CONFIG
# ==========================================

ROWS = [

    ("Host", "Biraj Kushwaha"),
    ("Role", "Java Backend Developer"),
    ("Language", "Java • Python"),
    ("Framework", "Spring Boot"),
    ("Database", "MongoDB • MySQL"),
    ("Security", "Spring Security • JWT"),
    ("Messaging", "Kafka • Redis"),
    ("Architecture", "Microservices"), 
    ("Cloud", "AWS • IBM Cloud"),
    ("Testing", "JUnit • Mockito"),
    ("Tools", "Git • Maven • Docker"),
    ("Core CS", "DSA • OOP"),
    ("AI", "IBM watsonx • LLM APIs"),     

]

WIDTH = 560
HEIGHT = 490

BACKGROUND = "#0d1117"
BORDER = "#30363d"

TITLE = "#ffffff"

GREEN = "#39d353"

LABEL = "#7ee787"

VALUE = "#c9d1d9"

FONT = "Consolas, Menlo, monospace"

svg = []

# ==========================================
# SVG START
# ==========================================

svg.append(f"""<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">
""")

svg.append(f"""
<defs>

<filter id="glow">
    <feGaussianBlur stdDeviation="1.5" result="blur"/>
    <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
    </feMerge>
</filter>

</defs>

<style>

svg{{
background:{BACKGROUND};
}}

text{{
font-family:{FONT};
}}

.title{{
fill:{TITLE};
font-size:15px;
font-weight:bold;
}}

.command{{
fill:{GREEN};
font-size:18px;
font-weight:bold;
filter:url(#glow);
}}

.label{{
fill:{LABEL};
font-size:16px;
font-weight:bold;
}}

.value{{
fill:{VALUE};
font-size:16px;
}}

</style>
""")

# ==========================================
# WINDOW
# ==========================================

svg.append(f"""
<rect
x="1"
y="1"
width="{WIDTH-2}"
height="{HEIGHT-2}"
rx="12"
fill="{BACKGROUND}"
stroke="{BORDER}"
stroke-width="1.5"/>
""")

# macOS buttons

svg.append("""
<circle cx="22" cy="22" r="6" fill="#ff5f56"/>
<circle cx="42" cy="22" r="6" fill="#ffbd2e"/>
<circle cx="62" cy="22" r="6" fill="#27c93f"/>
""")

# Window title

svg.append("""
<text
x="90"
y="27"
class="title">
Backend Developer
</text>
""")

# Divider

svg.append(f"""
<line
x1="0"
y1="42"
x2="{WIDTH}"
y2="42"
stroke="{BORDER}"/>
""")



y = 112
# ==========================================
# ROWS
# ==========================================

for i, (label, value) in enumerate(ROWS):

    delay = i * 0.18

    svg.append(f"""
<g opacity="0">

<animate
attributeName="opacity"
from="0"
to="1"
begin="{delay:.2f}s"
dur="0.25s"
fill="freeze"/>

<text
x="25"
y="{y}"
class="label">

{label}

</text>

<text
x="175"
y="{y}"
class="value">

: {value}

</text>

</g>
""")

    y += 26

# ==========================================
# FOOTER
# ==========================================

svg.append(f"""
<line
x1="20"
y1="{HEIGHT-50}"
x2="{WIDTH-20}"
y2="{HEIGHT-50}"
stroke="{BORDER}"/>
""")

svg.append(f"""
<text
x="20"
y="{HEIGHT-18}"
class="value"
font-size="12">

Open to Java Backend Opportunities

</text>
""")
# ==========================================
# BLINKING CURSOR
# ==========================================

svg.append("""
<text
x="20"
y="72"
class="command">

<tspan>biraj@github:~$ fastfetch --logo none </tspan>

<tspan opacity="1">█
    <animate
        attributeName="opacity"
        values="1;0;1"
        dur="1s"
        repeatCount="indefinite"/>
</tspan>

</text>
""")

# ==========================================
# SAVE SVG
# ==========================================

svg.append("</svg>")

OUTPUT.write_text(
    "".join(svg),
    encoding="utf-8"
)

print(f"Saved -> {OUTPUT}")