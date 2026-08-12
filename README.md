# AI Programming Fundamentals

Lecture notebooks for an introductory Python course, delivered through Google Colab.
Notebooks are executable: concepts and hands-on practice live in the same file.

## Weekly notebooks

| Week | Topic | Open |
|---|---|---|
| 1 | Course Overview | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/youngkorea/ai-programming-fundamentals/blob/main/notebooks/Week01.ipynb) |
| 2 | Data Types and Variables | _not yet published_ |
| 3 | Lists and Tuples | _not yet published_ |
| 4 | Dictionaries and Sets | _not yet published_ |
| 5 | Conditional Statements | _not yet published_ |
| 6 | Loops | _not yet published_ |
| 7 | Functions | _not yet published_ |
| **8** | **Midterm Exam** | |
| 9 | Strings and Regular Expressions | _not yet published_ |
| 10 | Modules and Packages | _not yet published_ |
| 11 | File I/O and Exception Handling | _not yet published_ |
| 12 | Classes | _not yet published_ |
| 13 | Advanced Topics | _not yet published_ |
| 14 | Introduction to Data Analysis Libraries | _not yet published_ |
| **15** | **Final Exam** | |

## Repository layout

```
notebooks/   lecture notebooks, one per week   Week01.ipynb ...
img/         SVG graphics referenced by the notebooks
tools/       generators that produce everything in img/
```

## How graphics work

Notebooks do not embed images. They reference this repository over HTTPS:

```html
<img src="https://raw.githubusercontent.com/youngkorea/ai-programming-fundamentals/main/img/w01_cover.svg" width="900" alt="AI Programming Fundamentals - W01">
```

Colab strips inline CSS from text cells, so anything that needs real layout is either an
SVG in `img/` or a `#@title` code cell whose HTML output is stored in the notebook.

## File naming

`w{week:02d}_{element}.svg`

| Element | Example |
|---|---|
| Cover | `w01_cover.svg` |
| Unit header | `w01_unit1.svg` ... `w01_unit4.svg` |
| Chart or figure | `w01_grading_bar.svg`, `w01_weekly_roadmap.svg` |

## Regenerating graphics

```bash
cd img
python ../tools/make_titles_svg.py    # cover and unit headers
python ../tools/make_svg.py           # grading bar, weekly roadmap
```

Edit the `CONFIG` block at the top of each script; the layout maths adjusts on its own.
Both scripts print a warning when a title is too long for its box, and both account for
the wider glyphs of Korean text.

## Notes for future edits

- `raw.githubusercontent.com` caches for a few minutes. A graphic changed minutes before
  class may still serve the old version. Finalise the day before.
- The repository must stay **public**. Raw URLs from a private repository require a token
  that expires, which breaks every image for every student.
- SVG text renders with a font from the reader's machine. These files request Roboto,
  then Arial, then Helvetica. Export to PNG if a missing font would be unacceptable.
- Always set `alt` on `<img>`. If the image fails to load, the title still reads.

## Colour system

Colour encodes heading depth, not section identity, so the rule holds across all fifteen weeks.

| Level | Markdown | Light theme | Dark theme |
|---|---|---|---|
| Course | `#` | `#0C447C` | `#85B7EB` |
| Week | `##` | `#0F6E56` | `#5DCAA5` |
| Unit | `###` | `#185FA5` on `#E6F1FB`, badge `#0C447C` | `#B5D4F4` |

Course and Unit share the blue ramp. They stay apart through size and through the
badge-and-band device on the unit header, not through hue. Below the unit level,
headings are plain markdown text — there is no per-topic graphic.
