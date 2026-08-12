"""
Lecture note FIGURE generator (SVG)
-----------------------------------
Body-content graphics: card grids, numbered steps, side-by-side comparisons.
Text wraps automatically, so you edit copy without touching coordinates.

    cd img && python ../tools/make_figures_svg.py
"""

import os

OUT_DIR = "."
FONT = "Roboto, Arial, Helvetica, sans-serif"
W = 900

NAVY   = "#0C447C"
BLUE   = "#185FA5"
MID    = "#378ADD"
PALE   = "#E6F1FB"
TINT   = "#F4F9FE"
BODY   = "#3D3D3A"
MUTED  = "#73726C"
RULE   = "#D6E4F3"
GREEN  = "#3B6D11"
RED    = "#A32D2D"

CHAR_W = 0.55        # latin; hangul handled separately


# ---------------- text helpers ----------------

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def width_of(s, size):
    return sum(size * (0.98 if ord(c) > 0x1100 else CHAR_W) for c in s)


def txt(x, y, s, size, fill, weight="400", anchor=None, spacing=None):
    a = f' font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}"'
    if anchor:
        a += f' text-anchor="{anchor}"'
    if spacing:
        a += f' letter-spacing="{spacing}"'
    return f'<text x="{x:.0f}" y="{y:.0f}"{a}>{esc(s)}</text>'


def wrap(s, size, max_w):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if width_of(trial, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(x, y, s, size, fill, max_w, leading=None, weight="400"):
    """Wrapped paragraph. Returns (svg, bottom_y)."""
    leading = leading or size * 1.5
    lines = wrap(s, size, max_w)
    out = [f'<text x="{x:.0f}" y="{y:.0f}" font-family="{FONT}" font-size="{size}" '
           f'font-weight="{weight}" fill="{fill}">']
    for i, ln in enumerate(lines):
        dy = "0" if i == 0 else f"{leading:.0f}"
        out.append(f'<tspan x="{x:.0f}" dy="{dy}">{esc(ln)}</tspan>')
    out.append('</text>')
    return "\n".join(out), y + leading * (len(lines) - 1)


def svg(w, h, parts):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h:.0f}" '
            f'viewBox="0 0 {w} {h:.0f}">\n' + "\n".join(parts) + "\n</svg>")


# ---------------- figure builders ----------------

def cards(items, cols=3, numbered=False, w=W):
    """items: list of (title, body). Returns svg string."""
    gap, pad = 14, 18
    cw = (w - gap * (cols - 1)) / cols
    rows = (len(items) + cols - 1) // cols
    inner = cw - pad * 2

    heights = []
    for t, b in items:
        n_t = len(wrap(t, 17, inner))
        n_b = len(wrap(b, 14, inner)) if b else 0
        heights.append(pad + (28 if numbered else 0) + n_t * 24 + (8 if b else 0) + n_b * 21 + pad)
    row_h = [max(heights[r * cols:(r + 1) * cols]) for r in range(rows)]

    parts, y = [], 0.0
    for r in range(rows):
        h = row_h[r]
        for c in range(cols):
            i = r * cols + c
            if i >= len(items):
                break
            t, b = items[i]
            x = c * (cw + gap)
            parts.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{h:.0f}" '
                         f'rx="6" fill="{TINT}" stroke="{RULE}" stroke-width="1"/>')
            ty = y + pad + 18
            if numbered:
                parts.append(f'<circle cx="{x + pad + 12:.0f}" cy="{y + pad + 10:.0f}" r="12" fill="{BLUE}"/>')
                parts.append(txt(x + pad + 12, y + pad + 15, str(i + 1), 14, "#FFFFFF", "700", anchor="middle"))
                ty = y + pad + 48
            s, ty = block(x + pad, ty, t, 17, NAVY, inner, 24, "700")
            parts.append(s)
            if b:
                s, _ = block(x + pad, ty + 25, b, 14, BODY, inner, 21)
                parts.append(s)
        y += h + gap
    return svg(w, y - gap, parts)


def steps(items, w=W):
    """items: list of (title, body) rendered as a numbered vertical flow."""
    pad, gap, badge = 18, 12, 44
    inner = w - badge - pad * 3
    parts, y = [], 0.0
    for i, (t, b) in enumerate(items, 1):
        n_t = len(wrap(t, 18, inner))
        n_b = len(wrap(b, 14, inner)) if b else 0
        h = pad + n_t * 25 + (6 if b else 0) + n_b * 21 + pad
        parts.append(f'<rect x="0" y="{y:.0f}" width="{w}" height="{h:.0f}" rx="6" fill="{TINT}" '
                     f'stroke="{RULE}" stroke-width="1"/>')
        parts.append(f'<rect x="0" y="{y:.0f}" width="{badge}" height="{h:.0f}" rx="6" fill="{BLUE}"/>')
        parts.append(f'<rect x="{badge - 8}" y="{y:.0f}" width="8" height="{h:.0f}" fill="{BLUE}"/>')
        parts.append(txt(badge / 2, y + h / 2 + 8, str(i), 24, "#FFFFFF", "700", anchor="middle"))
        ty = y + pad + 18
        s, ty = block(badge + pad, ty, t, 18, NAVY, inner, 25, "700")
        parts.append(s)
        if b:
            s, _ = block(badge + pad, ty + 25, b, 14, BODY, inner, 21)
            parts.append(s)
        y += h + gap
    return svg(w, y - gap, parts)


def compare(left, right, rows, w=W):
    """left/right: (title, badge_text or None). rows: (label, left_ok, left_txt, right_ok, right_txt)."""
    gap = 14
    cw = (w - gap) / 2
    head_h, row_h, pad = 54, 46, 18
    h = head_h + row_h * len(rows) + 10

    parts = []
    for idx, (col, (title, badge)) in enumerate([(0, left), (1, right)]):
        x = idx * (cw + gap)
        fill = PALE if idx == 1 else TINT
        parts.append(f'<rect x="{x:.0f}" y="0" width="{cw:.0f}" height="{h:.0f}" rx="6" '
                     f'fill="{fill}" stroke="{RULE}" stroke-width="1"/>')
        parts.append(f'<rect x="{x:.0f}" y="0" width="{cw:.0f}" height="4" '
                     f'fill="{BLUE if idx == 1 else MUTED}"/>')
        parts.append(txt(x + pad, 36, title, 20, NAVY if idx == 1 else BODY, "700"))
        if badge:
            bw = width_of(badge, 12) + 22
            parts.append(f'<rect x="{x + cw - pad - bw:.0f}" y="18" width="{bw:.0f}" height="22" rx="11" fill="{BLUE}"/>')
            parts.append(txt(x + cw - pad - bw / 2, 34, badge, 12, "#FFFFFF", "700", anchor="middle"))

    for r, (label, lok, ltxt, rok, rtxt) in enumerate(rows):
        y = head_h + r * row_h
        for idx, (ok, val) in enumerate([(lok, ltxt), (rok, rtxt)]):
            x = idx * (cw + gap)
            parts.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw:.0f}" height="1" fill="{RULE}"/>')
            mark, colour = ("\u2713", GREEN) if ok else ("\u2715", RED)
            parts.append(txt(x + pad, y + 30, mark, 15, colour, "700"))
            parts.append(txt(x + pad + 22, y + 22, label, 12, MUTED, "700"))
            parts.append(txt(x + pad + 22, y + 38, val, 14, BODY))
    return svg(w, h, parts)


# ---------------- figures ----------------

FIGURES = {}

FIGURES["w01_python_stack.svg"] = cards([
    ("NumPy", "High-performance numerical computing. Arrays and vectorised maths underneath almost every "
              "data library."),
    ("Pandas", "Data processing and analysis. Tables, filtering, grouping, joining, and reading files."),
    ("Matplotlib / Seaborn", "Data visualization. Charts for exploring data and for presenting results."),
], cols=3)

FIGURES["w01_why_python.svg"] = cards([
    ("Readable syntax", "Concise and intuitive. A variable is named total_price rather than x."),
    ("Versatility", "Web development, data analysis, artificial intelligence, game development, and more."),
    ("Strong community", "A vast set of open-source libraries and active support."),
    ("High productivity", "Students accomplish a great deal with little code."),
    ("Industry demand", "Employers ask for Python across many roles, including data scientist and "
                        "software developer."),
], cols=3)

FIGURES["w01_objectives.svg"] = cards([
    ("Explain", "Why Python is the dominant language in data analysis and artificial intelligence."),
    ("Identify", "The equipment required for coursework and exams."),
    ("Compare", "Jupyter Notebook and Colab, and select Colab as the practice environment."),
    ("Create", "A Colab notebook, then write, run, and comment a first Python program."),
], cols=4, numbered=True)

FIGURES["w01_getting_started.svg"] = steps([
    ("Create a Google account",
     "Go to accounts.google.com and click Create account. Skip this step if you already have one."),
    ("Open the Google Colab website",
     "colab.google"),
    ("Create or open a notebook",
     "Click + New notebook to start fresh. Or click Upload, then Browse, to select a notebook file such "
     "as AIProgrammingFundamentals_Week01.ipynb."),
])

FIGURES["w01_jupyter_vs_colab.svg"] = compare(
    ("Jupyter Notebook", None),
    ("Google Colab", "WE USE THIS"),
    [("Installation", False, "Required", True, "Not required"),
     ("Internet connection", True, "Works offline", False, "Required"),
     ("Computing resources", False, "Local machine only", True, "GPU and TPU, free or paid"),
     ("Environment setup", False, "Version management", True, "Not required by default")],
)






# ---------------- summary recap ----------------

def pill(x, y, label, size=14, fill=PALE, fg=NAVY, pad=14, h=32):
    w = width_of(label, size) * 1.05 + pad * 2
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h}" rx="{h//2}" fill="{fill}"/>'
         + txt(x + w / 2, y + h / 2 + 5, label, size, fg, "500", anchor="middle"))
    return s, w


def recap(concepts, flow_label, flow, w=W):
    """2x2 concept cards on top, one procedural strip underneath. Body text at 24px."""
    gap, pad = 14, 22
    cw = (w - gap) / 2
    inner = cw - pad * 2
    TS, BS, LEAD = 26, 24, 34          # title, body, line height

    heights = []
    for t, b in concepts:
        heights.append(pad + 30 + 12 + len(wrap(b, BS, inner)) * LEAD + pad)
    row1 = max(heights[:2]); row2 = max(heights[2:])

    parts, y = [], 0.0
    for r, rh in enumerate([row1, row2]):
        for c in range(2):
            t, b = concepts[r * 2 + c]
            x = c * (cw + gap)
            parts.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{rh:.0f}" rx="6" '
                         f'fill="{TINT}" stroke="{RULE}" stroke-width="1"/>')
            parts.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="5" height="{rh:.0f}" fill="{BLUE}"/>')
            s, ty = block(x + pad, y + pad + 26, t, TS, NAVY, inner, 34, "700")
            parts.append(s)
            s, _ = block(x + pad, ty + 40, b, BS, BODY, inner, LEAD)
            parts.append(s)
        y += rh + gap

    strip_h = 108
    parts.append(f'<rect x="0" y="{y:.0f}" width="{w}" height="{strip_h}" rx="6" fill="{PALE}"/>')
    parts.append(txt(pad, y + 38, flow_label, TS, NAVY, "700"))
    px, py = float(pad), y + 56
    for i, step in enumerate(flow):
        s, pw = pill(px, py, step, 20, "#FFFFFF", NAVY, 16, 40)
        parts.append(s)
        px += pw
        if i < len(flow) - 1:
            parts.append(txt(px + 11, py + 27, "\u2192", 19, MID, "700", anchor="middle"))
            px += 22
    if px > w:
        print(f"  ! step strip overflows by {px - w:.0f}px — shorten a step label")
    return svg(w, y + strip_h, parts)


def chips(label, items, w=W):
    gap, pad, h = 10, 0, 46
    parts = [txt(0, 22, label, 15, MUTED, "700", spacing=1.2)]
    x, y = 0.0, 40.0
    for it in items:
        cw = width_of(it, 24) * 1.05 + 40
        if x + cw > w:
            x, y = 0.0, y + h + gap
        s, cw = pill(x, y, it, 24, PALE, NAVY, 20, h)
        parts.append(s)
        x += cw + gap
    return svg(w, y + h, parts)


FIGURES["w01_summary.svg"] = recap(
    [("Course goals", "Learn the basic syntax and concepts of Python for data analysis and AI modeling, "
                      "and build hands-on programming skills."),
     ("Requirements", "A computer that runs Python. Mobile devices are not recommended, and a separate "
                      "coding computer is required for the exams."),
     ("Why Python", "A rich library ecosystem (NumPy, Pandas, Matplotlib and Seaborn), readable syntax, "
                    "a strong community, and compatibility with machine learning frameworks."),
     ("Why Colab", "No installation, free access to GPU and TPU resources, and the same environment for "
                   "every student.")],
    "First steps in Colab",
    ["New notebook", "Run a cell", "Add cells", "Variables", "Comments"],
)

FIGURES["w01_key_terms.svg"] = chips(
    "KEY TERMS",
    ["Python", "Google Colab", "Jupyter Notebook", "code cell", "text cell",
     "runtime", "variable", "comment", "automatic output"],
)


# ---------------- question / answer recap ----------------

A_BG, A_BAR, A_Q, A_A = "#FAEEDA", "#854F0B", "#412402", "#854F0B"
BOLD = 1.14


def qa(rows, w=W, size=24, rh=64, gap=10):
    """Amber question/answer rows. Font size 24 matches <font size="5"> body text."""
    pad, bar, split = 22, 6, 0.47
    qbox = w * split - pad - bar - 16
    abox = w * (1 - split) - pad
    parts, y = [], 0.0
    for q, a in rows:
        qs, as_ = size, size
        while qs > 12 and width_of(q, qs) * BOLD > qbox:
            qs -= 1
        while as_ > 12 and width_of(a, as_) > abox:
            as_ -= 1
        if qs < size:
            print(f"  ~ question shrunk to {qs}px: {q!r}")
        if as_ < size:
            print(f"  ~ answer shrunk to {as_}px: {a!r}")
        parts.append(f'<rect x="0" y="{y:.0f}" width="{w}" height="{rh}" rx="6" fill="{A_BG}"/>')
        parts.append(f'<rect x="0" y="{y:.0f}" width="{bar + 6}" height="{rh}" rx="6" fill="{A_BAR}"/>')
        parts.append(f'<rect x="{bar}" y="{y:.0f}" width="6" height="{rh}" fill="{A_BAR}"/>')
        parts.append(txt(bar + pad, y + rh / 2 + 9, q, qs, A_Q, "700"))
        parts.append(txt(w * split, y + rh / 2 + 9, a, as_, A_A))
        y += rh + gap
    return svg(w, y - gap, parts)


FIGURES["w01_summary_qa.svg"] = qa([
    ("What is this course for?", "Python for data analysis and AI"),
    ("What do I need?",          "A computer, plus one for exams"),
    ("Why Python?",              "Libraries, readability, demand"),
    ("Why Colab?",               "No install, free GPU, one setup"),
    ("What can I already do?",   "Write, run, and comment a cell"),
])


# ---------------- reusable callout badges ----------------
# Week-independent: three files cover the whole course.

BADGES = [
    ("badge_important.svg", "IMPORTANT",      "#FCEBEB", "#A32D2D", "#501313"),
    ("badge_pause.svg",     "PAUSE A MINUTE", "#EAF3DE", "#3B6D11", "#173404"),
    ("badge_note.svg",      "NOTE",           "#F1EFE8", "#5F5E5A", "#2C2C2A"),
]


def badge(label, bg, bar, fg, size=26, h=52):
    """Standalone label chip. Body text goes underneath as ordinary markdown."""
    pad, r = 22, 6
    w = int(width_of(label, size) * BOLD + pad * 2 + 14)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
         f'<rect x="0" y="0" width="{w}" height="{h}" rx="{r}" fill="{bg}"/>',
         f'<rect x="0" y="0" width="{8 + r}" height="{h}" rx="{r}" fill="{bar}"/>',
         f'<rect x="8" y="0" width="{r}" height="{h}" fill="{bar}"/>',
         txt(8 + pad, h / 2 + size / 3, label, size, fg, "700", spacing=1.2),
         '</svg>']
    return "\n".join(p)


for fname, label, bg, bar, fg in BADGES:
    FIGURES[fname] = badge(label, bg, bar, fg)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, s in FIGURES.items():
        path = os.path.join(OUT_DIR, name)
        open(path, "w", encoding="utf-8").write(s)
        print(f"wrote {path}  ({len(s)} bytes)")
