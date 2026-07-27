# Young Ah Shin — Academic Homepage

A static academic homepage in the layout convention used by faculty and postdoc pages
(Home / Research / Publications / Projects / Teaching / Service / CV). No build step, no
dependencies — plain HTML and one stylesheet.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | Home: profile, bio, news, research directions, education, skills |
| `research.html` | Research statement, doctoral research, areas of interest, work in progress |
| `publications.html` | Journal articles, manuscripts under review, theses |
| `projects.html` | Funded projects, patents, registered software |
| `teaching.html` | Courses, teaching interests, student training |
| `service.html` | Conference organisation, international collaboration, outreach |
| `about.html` | Redirect to `index.html` (kept so old links do not break) |
| `styles.css` | Shared stylesheet |
| `cvShin_updated.pdf` | CV |

## Deploy to GitHub Pages

Upload every file to the **root** of `youngahshin/youngahshin.github.io` — not inside a
folder. Then go to *Settings → Pages* and set the source to the `main` branch, root
directory. The site appears at `https://youngahshin.github.io`.

```text
index.html
research.html
publications.html
projects.html
teaching.html
service.html
about.html
styles.css
cvShin_updated.pdf
README.md
```

## Add a photo

1. Put a portrait image named `profile.jpg` in the same folder (4:5 ratio works best,
   at least 600 × 750 px).
2. Open `index.html`, find `<div class="portrait">`, and replace the `YS` initials with:

```html
<img src="profile.jpg" alt="Portrait of Young Ah Shin">
```

## Routine updates

- **New paper** — copy an existing `<li class="pub">` block in `publications.html`,
  change the year in `pub-key`, and drop the `tag` element once it is published.
- **Status change** — the badge classes are `tag review` (crimson outline),
  `tag progress` (dashed outline), and plain `tag`.
- **New project or course** — copy a `<article class="rail-item">` block; the left column
  is the date, the right column is the content.
- **News** — add an `<li>` to the `.news` list on `index.html`. Keep it to about six
  items; delete the oldest as you add.
- Update the "Last updated" date in each footer when you make a substantive change.

## Design notes

- **Type**: Source Serif 4 for prose, Inter for navigation and labels, IBM Plex Mono for
  dates and identifiers. Loaded from Google Fonts.
- **Colour**: ink `#17191d`, crimson accent `#8a1f2b`, warm wash `#f6f5f2`.
- The left-hand mono date rail is the recurring structural device — it runs through
  education, publications, projects, teaching, and service, so the whole site reads as one
  timeline. On screens under 720px it collapses above each entry.
- Accessibility: skip link, visible focus rings, semantic headings, `prefers-reduced-motion`
  respected.
