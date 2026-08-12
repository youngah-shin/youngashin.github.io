"""
Lecture note SVG generator
--------------------------
Edit the CONFIG block, run, and the .svg files are written next to this script.
Runs in Colab as-is: paste into a cell, run, then use files.download('...').

No external packages required.
"""

import os

# ============================================================
# CONFIG - edit this part only
# ============================================================

OUT_DIR = "."
FONT = "Roboto, Arial, Helvetica, sans-serif"

# Section palettes. Add a new entry per section / per week.
PALETTE = {
    "blue":   dict(bg="#E6F1FB", tint="#F4F9FE", mid="#378ADD", accent="#185FA5", text="#0C447C"),
    "teal":   dict(bg="#E1F5EE", tint="#F2FBF7", mid="#5DCAA5", accent="#0F6E56", text="#04342C"),
    "amber":  dict(bg="#FAEEDA", tint="#FDF8EF", mid="#EF9F27", accent="#854F0B", text="#412402"),
    "purple": dict(bg="#EEEDFE", tint="#F7F6FE", mid="#7F77DD", accent="#534AB7", text="#26215C"),
}

RED = dict(bg="#FCEBEB", accent="#A32D2D", text="#501313")

# --- banners: (filename, palette key, tag, title, subtitle) ---
# --- grading bar: (label, weight, fill, text colour) ---
GRADING = [
    ("Assignments 40%", 40, "#0C447C", "#FFFFFF"),
    ("Midterm 20%",     20, "#185FA5", "#FFFFFF"),
    ("Final 20%",       20, "#378ADD", "#FFFFFF"),
    ("Att. 10%",        10, "#85B7EB", "#042C53"),
    ("Part. 10%",       10, "#B5D4F4", "#042C53"),
]

# --- weekly roadmap ---
ROADMAP_HEADER = ("Week 1 - Course Overview", "you are here")
ROADMAP_PHASES = [
    ("WEEKS 2-4", "Foundations", "#378ADD", [
        ("2", "Data Types and Variables"),
        ("3", "Lists and Tuples"),
        ("4", "Dictionaries and Sets"),
    ]),
    ("WEEKS 5-7", "Control and Functions", "#185FA5", [
        ("5", "Conditional Statements"),
        ("6", "Loops"),
        ("7", "Functions"),
    ]),
    ("WEEKS 9-14", "Applications", "#0C447C", [
        ("9",  "Strings and Regular Expr."),
        ("10", "Modules and Packages"),
        ("11", "File I/O and Exceptions"),
        ("12", "Classes"),
        ("13", "Advanced Topics"),
        ("14", "Data Analysis Libraries"),
    ]),
]
ROADMAP_EXAMS = [("Week 8 - Midterm Exam"), ("Week 15 - Final Exam")]

WIDTH = 900          # canvas width; matches <img width="900">
CHAR_W = 0.55        # rough glyph width factor, used for the overflow warning


# ============================================================
# BUILDERS - you rarely need to touch below this line
# ============================================================

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def warn_if_long(text, font_size, box_w, where):
    est = len(text) * font_size * CHAR_W
    if est > box_w:
        print(f"  ! too long for its box: {where!r} "
              f"(~{int(est)}px of {box_w}px) - shorten it or reduce font-size")


def txt(x, y, s, size, fill, weight="400", spacing=None, anchor=None):
    a = f' font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}"'
    if spacing:
        a += f' letter-spacing="{spacing}"'
    if anchor:
        a += f' text-anchor="{anchor}"'
    return f'<text x="{x}" y="{y}"{a}>{esc(s)}</text>'


def build_banner(pal, tag, title, subtitle, w=WIDTH, h=110):
    c = PALETTE[pal]
    warn_if_long(title, 30, w - 60, title)
    warn_if_long(subtitle, 15, w - 60, subtitle)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="{c["bg"]}"/>\n'
        f'<rect x="0" y="0" width="8" height="{h}" fill="{c["accent"]}"/>\n'
        + txt(30, 34, tag, 13, c["accent"], "700", spacing=2) + "\n"
        + txt(30, 68, title, 30, c["text"], "700") + "\n"
        + txt(30, 92, subtitle, 15, c["accent"]) + "\n"
        '</svg>'
    )


def build_grading(rows, w=WIDTH, h=46):
    total = sum(r[1] for r in rows)
    parts, x = [], 0.0
    for label, weight, fill, fg in rows:
        seg = w * weight / total
        warn_if_long(label, 14, seg - 8, label)
        parts.append(f'<rect x="{x:.1f}" y="0" width="{seg:.1f}" height="{h}" fill="{fill}"/>')
        parts.append(txt(x + seg / 2, h / 2 + 5, label, 14, fg, "700", anchor="middle"))
        x += seg
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            + "\n".join(parts) + "\n</svg>")


def build_roadmap(header, phases, exams, w=WIDTH):
    head_h, gap, top = 40, 15, 62
    col_w = (w - gap * (len(phases) - 1)) / len(phases)
    rows_max = max(len(p[3]) for p in phases)
    body_h = 70 + rows_max * 23
    parts = [f'<rect x="0" y="0" width="{w}" height="{head_h}" fill="#0C447C"/>',
             txt(16, 26, header[0], 15, "#FFFFFF", "700")]
    parts.append(txt(16 + len(header[0]) * 8.6, 26, header[1], 15, "#85B7EB"))

    for i, (wk, title, edge, items) in enumerate(phases):
        x = i * (col_w + gap)
        warn_if_long(title, 16, col_w - 32, title)
        parts.append(f'<rect x="{x:.1f}" y="{top}" width="{col_w:.1f}" height="{body_h}" fill="#F4F9FE"/>')
        parts.append(f'<rect x="{x:.1f}" y="{top}" width="{col_w:.1f}" height="4" fill="{edge}"/>')
        parts.append(txt(x + 16, top + 26, wk, 11, edge, "700", spacing=1.5))
        parts.append(txt(x + 16, top + 50, title, 16, "#0C447C", "700"))
        for j, (num, label) in enumerate(items):
            warn_if_long(f"{num}  {label}", 13, col_w - 32, label)
            parts.append(
                f'<text x="{x + 16:.1f}" y="{top + 70 + j * 23}" font-family="{FONT}" '
                f'font-size="13" fill="#0C447C"><tspan font-weight="700">{num}</tspan>  {esc(label)}</text>')

    y = top + body_h + 15
    for label in exams:
        parts.append(f'<rect x="0" y="{y}" width="{w}" height="30" fill="{RED["bg"]}"/>')
        parts.append(f'<rect x="0" y="{y}" width="6" height="30" fill="{RED["accent"]}"/>')
        parts.append(txt(18, y + 20, label, 14, RED["text"], "700"))
        y += 36

    h = y - 6
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            + "\n".join(parts) + "\n</svg>")


def write(name, svg):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {path}  ({len(svg)} bytes)")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    print("[w01_grading_bar.svg]")
    write("w01_grading_bar.svg", build_grading(GRADING))
    print("[w01_weekly_roadmap.svg]")
    write("w01_weekly_roadmap.svg", build_roadmap(ROADMAP_HEADER, ROADMAP_PHASES, ROADMAP_EXAMS))
    print("\ndone. In Colab, download with:")
    print("  from google.colab import files; files.download('w01_grading_bar.svg')")
