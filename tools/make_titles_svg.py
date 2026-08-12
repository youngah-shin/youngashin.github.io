"""
Lecture note TITLE generator (SVG)
----------------------------------
Builds cover and unit-header graphics. Edit CONFIG, run, get .svg files.
Runs in Colab as-is. No external packages.
"""

import os

# ============================================================
# CONFIG
# ============================================================

OUT_DIR = "."
FONT = "Roboto, Arial, Helvetica, sans-serif"
WIDTH = 900

C_COURSE = "#0C447C"
C_WEEK   = "#0F6E56"
C_WEEK_BG= "#E1F5EE"
C_UNIT   = "#0C447C"
C_UNIT_BG= "#E6F1FB"
C_UNIT_TX= "#185FA5"
C_META   = "#8A8880"
C_RULE   = "#E3E3E0"

COVER = dict(
    course="AI Programming Fundamentals",
    week_no="W01",
    week_title="Course Overview",
    meta="youngah2026@iscu.ac.kr",
    filename="w01_cover.svg",
)

UNITS = [
    (1, "Course Plan",                       "w01_unit1.svg"),
    (2, "Introduction to Python and Colab",  "w01_unit2.svg"),
    (3, "Getting Started with Colab",        "w01_unit3.svg"),
    (4, "Key Takeaways",                     "w01_unit4.svg"),
]

# Latin ~0.55, Hangul ~0.98. Raise this if your titles are in Korean.
CHAR_W = 0.55


# ============================================================
# BUILDERS
# ============================================================

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def width_of(s, size):
    w = 0.0
    for ch in s:
        w += size * (0.98 if ord(ch) > 0x1100 else CHAR_W)
    return w


def warn(s, size, box, where):
    est = width_of(s, size)
    if est > box:
        print(f"  ! overflows: {where!r} (~{int(est)}px of {int(box)}px)")


def txt(x, y, s, size, fill, weight="400", spacing=None, anchor=None):
    a = f' font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}"'
    if spacing:
        a += f' letter-spacing="{spacing}"'
    if anchor:
        a += f' text-anchor="{anchor}"'
    return f'<text x="{x}" y="{y}"{a}>{esc(s)}</text>'


def build_cover(cfg, w=WIDTH, h=222, dark=False):
    course, wk, wt, meta = cfg["course"], cfg["week_no"], cfg["week_title"], cfg["meta"]


    if dark:
        bg, c_course, c_week_bg, c_week_tx, c_wt, c_meta = (
            C_COURSE, "#FFFFFF", "#5DCAA5", "#04342C", "#B5D4F4", "#85B7EB")
    else:
        bg, c_course, c_week_bg, c_week_tx, c_wt, c_meta = (
            "#E6F1FB", C_COURSE, C_WEEK, "#FFFFFF", C_WEEK, C_META)

    badge_w = width_of(wk, 17) + 30
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    p.append(f'<rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{bg}"/>')
    if not dark:
        p.append(f'<rect x="0" y="0" width="{w}" height="7" rx="3" fill="{C_COURSE}"/>')
    p.append(txt(34, 104, course, fit(course, 56, w - 68), c_course, "700"))
    p.append(f'<rect x="34" y="134" width="{badge_w:.0f}" height="32" rx="4" fill="{c_week_bg}"/>')
    p.append(txt(34 + badge_w / 2, 156, wk, 17, c_week_tx, "700", anchor="middle"))
    p.append(txt(34 + badge_w + 14, 160, wt, 32, c_wt, "700"))
    p.append(txt(w - 34, 200, meta, 14, c_meta, anchor="end"))
    p.append('</svg>')
    return "\n".join(p)


BOLD = 1.14   # bold glyphs run wider than the plain-text estimate


def fit(text, target, box):
    """Largest size <= target that still fits box, measured as bold."""
    size = target
    while size > 12 and width_of(text, size) * BOLD > box:
        size -= 1
    if size < target:
        print(f"  ~ shrunk to {size}px to fit: {text!r}")
    return size


def build_unit(n, title, w=WIDTH, h=96):
    """Boxed unit header. Title targets 48px (font size 7) and shrinks only if it would overflow."""
    badge, r = 68, 6
    size = fit(title, 48, w - badge - 40)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    p.append(f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{r}" fill="{C_UNIT_BG}"/>')
    p.append(f'<rect x="1" y="1" width="{badge}" height="{h - 2}" rx="{r}" fill="{C_UNIT}"/>')
    p.append(f'<rect x="{badge - r + 1}" y="1" width="{r}" height="{h - 2}" fill="{C_UNIT}"/>')
    p.append(txt(badge / 2 + 1, h / 2 + 17, str(n), 46, "#FFFFFF", "700", anchor="middle"))
    p.append(txt(badge + 26, h / 2 + 17, title, size, C_UNIT_TX, "700"))
    p.append(f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{r}" fill="none" '
             f'stroke="{C_UNIT}" stroke-width="1.5"/>')
    p.append('</svg>')
    return "\n".join(p)


def write(name, svg):
    path = os.path.join(OUT_DIR, name)
    open(path, "w", encoding="utf-8").write(svg)
    print(f"wrote {path}  ({len(svg)} bytes)")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"[{COVER['filename']}]")
    write(COVER["filename"], build_cover(COVER))
    print("[w01_cover_dark.svg]")
    write("w01_cover_dark.svg", build_cover(COVER, dark=True))
    for n, title, fname in UNITS:
        print(f"[{fname}]")
        write(fname, build_unit(n, title))
    print("\ndone. In Colab:  from google.colab import files; files.download('w01_cover.svg')")
