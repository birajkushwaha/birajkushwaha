from pathlib import Path
from html import escape

OUTPUT = Path("terminal.svg")

# ==========================
# TERMINAL CONFIG
# ==========================

WIDTH = 920
HEIGHT = 760

FONT_SIZE = 16
LINE_HEIGHT = 24

PADDING_X = 20
PADDING_Y = 70

# GitHub Dark Theme

BACKGROUND = "#0d1117"
BORDER = "#30363d"

TEXT = "#c9d1d9"

GREEN = "#39d353"

TITLE = "#ffffff"

# ==========================
# PROJECTS
# ==========================

PROJECTS = [

    (
        "Journal-Management-System",
        [
            "Java",
            "Spring Boot",
            "Spring Security",
            "JWT",
            "MongoDB",
            "REST API",
        ],
    ),

    (
        "URL-Shortener",
        [
            "Java",
            "Spring Boot",
            "Docker",
            "MySQL",
            "REST API",
        ],
    ),

    (
        "Signify-AI",
        [
            "Python",
            "TensorFlow",
            "OpenCV",
            "MediaPipe",
        ],
    ),

]

# ==========================
# TECH STACK
# ==========================

STACK = [

    "Java 21",

    "Spring Boot",

    "Spring Security",

    "MongoDB",

    "MySQL",

    "Kafka",

    "Redis",

    "Docker",

    "AWS",

    "IBM Cloud",

    "Git",

    "Maven",

    "JUnit",

    "Mockito",

    "LLM APIs",

]

svg = []
# ==========================
# SVG START
# ==========================

svg.append(f"""<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">
""")

svg.append(f"""
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

svg{{
background:{BACKGROUND};
}}

text{{
font-family:Consolas,Menlo,monospace;
font-size:{FONT_SIZE}px;
fill:{TEXT};
white-space:pre;
}}

.prompt{{
fill:{GREEN};
font-weight:bold;
filter:url(#glow);
}}

.header{{
fill:{TITLE};
font-size:15px;
font-weight:bold;
}}

.command{{
fill:{GREEN};
}}

.cursor{{
fill:{GREEN};
}}

@keyframes blink{{
0%{{opacity:1;}}
50%{{opacity:0;}}
100%{{opacity:1;}}
}}

.blink{{
animation:blink 1s infinite;
}}

</style>
""")

# ==========================
# TERMINAL WINDOW
# ==========================

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

# macOS window buttons

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
class="header">
biraj@github: ~/profile
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

# Cursor position

current_y = PADDING_Y

# ==========================
# Helper Function
# ==========================

def add_line(text, cls="", delay=0):

    global current_y

    svg.append(f'''
<text
x="{PADDING_X}"
y="{current_y}"
class="{cls}"
style="opacity:0">

<animate
attributeName="opacity"
from="0"
to="1"
begin="{delay}s"
dur="0.25s"
fill="freeze"/>

{escape(text)}

</text>
''')

    current_y += LINE_HEIGHT

# ==========================
# PROJECT TREE
# ==========================

delay = 0

add_line("biraj@github:~$ tree", "prompt", delay)
delay += 0.3

add_line(".", "", delay)
delay += 0.15

for index, (project, tech) in enumerate(PROJECTS):

    last = index == len(PROJECTS) - 1

    branch = "└──" if last else "├──"

    add_line(f"{branch} {project}", "", delay)
    delay += 0.15

    indent = "    " if last else "│   "

    add_line(
        f"{indent}└── {' • '.join(tech)}",
        "",
        delay
    )

    delay += 0.15

    if not last:
        add_line("│", "", delay)
        delay += 0.08

current_y += 12
# ==========================
# TECH STACK
# ==========================

add_line("", "", delay)
delay += 0.15

add_line("biraj@github:~$ cat skills.txt", "prompt", delay)
delay += 0.30

for tech in STACK:

    add_line(tech, "", delay)

    delay += 0.10

current_y += 15
# ==========================
# FINAL PROMPT
# ==========================

add_line("", "", delay)
delay += 0.20

prompt_y = current_y

svg.append(f"""
<text
x="{PADDING_X}"
y="{prompt_y}"
class="prompt">

biraj@github:~$

</text>
""")

# Blinking Cursor

svg.append(f"""
<rect
x="175"
y="{prompt_y-13}"
width="10"
height="18"
fill="{GREEN}"
class="blink"/>
""")

# ==========================
# FOOTER
# ==========================

svg.append(f"""
<text
x="{WIDTH-20}"
y="{HEIGHT-18}"
text-anchor="end"
fill="#7d8590"
font-size="12">

Java Backend Developer • Open to Opportunities

</text>
""")

# ==========================
# SAVE SVG
# ==========================

svg.append("</svg>")

OUTPUT.write_text(

    "".join(svg),

    encoding="utf-8"

)

print(f"Saved -> {OUTPUT}")