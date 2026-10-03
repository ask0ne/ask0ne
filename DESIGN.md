# ask0ne design framework

Read this before changing any UI, spacing, colour, copy or content on this site.
It records the rules the 2026 redesign was built on. If a change doesn't fit
these rules, the change is wrong, not the rules. If a rule genuinely needs to
change, change it here first, in the same commit.

Source of truth in code: `assets/css/site.css` (tokens + components),
`templates/base.html` (shell), `templates/sections/*.html` and
`templates/detail.html` (pages).

---

## 1. The feel

Subtle, clean, a little dorky/geeky, stoically funny. Think: a rich gray-white
bedroom with one corner of colour. Calm first, quirks second.

- **Calm:** soft off-white / charcoal, lots of air, one accent, nothing shouting.
- **Dorky:** mono type for labels, dates and titles; `(■_■¬)` as the theme
  toggle; a to-scale career bar that admits to a gap.
- **Stoic funny:** dry, deadpan, understated. One small joke per page, never two.
  Never exclamation marks, never emoji, never "fun" copy that tries.
- **Intentional:** every element is one of the components below. If it isn't
  in the catalogue, don't invent it; reuse one.

Rejected on purpose (do not reintroduce): terminal/`$ git log` styling as a
layout, boxed cards everywhere, sticky or blurred nav, hamburger menu, solid
dividers, vertical lines of any kind, `#hashtag` pills, multiple accents,
gradients other than the corner glow, drop shadows on content.

---

## 2. Non-negotiables

1. **Everything visible is lowercase.** Headings, nav, buttons, tags, dates
   (`feb 08`), post titles, alt text shown to users, loading text. Lowercase the
   string itself, don't rely on `text-transform`. Exceptions: URLs, code,
   the markdown body of a post is lowercased by the service already.
2. **No vertical borders or dividers.** Only horizontal hairlines.
3. **One accent colour: clay.** Never add a second one.
4. **Light and dark both work, always.** Auto from the OS, toggle remembers.
5. **rem/em only.** No `px` in CSS or templates (only the `.0625rem` hairline).
6. **No raw colours or sizes in components.** Use the tokens (section 3).
7. **Never change text the owner wrote** unless asked. Layout/markup can move;
   words don't. Adding new copy needs the owner's voice (section 7).
8. **No new UI component** without adding it to section 5 first.
9. **Nothing private leaves the machine.** See section 10.

---

## 3. Tokens (all in `:root` of `assets/css/site.css`)

### Colour
| token | light | dark | use |
|---|---|---|---|
| `--bg` | `#e9e6df` | `#1d1c1b` | page background |
| `--paper` | `#f0ede7` | `#252422` | raised surface (stat cards, popover) |
| `--ink` | `#3a3835` | `#d9d5ce` | primary text, strong |
| `--dim` | `#6f6c66` | `#9d9890` | secondary text, blurbs, bullets |
| `--faint` | `#97938c` | `#6e6a64` | labels, dates, quirks, footer |
| `--line` | 12% ink | 10% ink | every hairline and border |
| `--accent` | `#b4573a` clay | `#e08a69` | the one accent |
| `--pop` | accent @ ~20% | accent @ ~18% | corner glow only |

The **corner pop** is a single soft radial glow, top-right, fixed
(`body.v2-body::before`). It is the only decorative element. Don't add others.

### Type: four roles, no more
| role | token | size | font | where |
|---|---|---|---|---|
| heading | `--t-heading` | 1.75rem | sans, 600 | page title (`h1`), stat numbers |
| subheading | `--t-sub` | 1rem | **mono**, 600 | row titles, group headings |
| text | `--t-text` | 1rem | sans | body, nav, intros, buttons |
| subtext | `--t-small` | .8125rem | **mono** (labels) / sans italic (quirks) | dates, tags, stat labels, footer, quirks |

Line height `--lh: 1.7`. Sans = Inter (Google Fonts), mono = system mono stack.
Never set a `font-size` outside these four. To retune the whole site, change
the four tokens only.

### Spacing scale
`--sp-1 .25rem` · `--sp-2 .5rem` · `--sp-3 .75rem` · `--sp-4 1rem` ·
`--sp-5 1.5rem` · `--sp-6 2.5rem` · `--sp-7 4rem`.
Row padding is `--row` (1.25rem) everywhere. Use only these. No arbitrary
margins like `.35rem` or `1.2rem`.

### Shape
`--r-sm .5rem` · `--r-md .75rem` · hairline `--hair .0625rem` ·
tap target `--tap 2.75rem` (min height of anything clickable).

### Layout
One content width: `--w 44rem`, centred, `1.5rem` side padding. Label column
`--label 7rem`. Everything (nav, header, rows, footer) shares that width so
edges align. Below `44rem` rows stack (label above content). Only the hidden
`whelmed`/`cases` pages use the `wide` variant.

---

## 4. Page skeleton

Every section template is wrapped in `<div class="v2">` (all content rules are
scoped under `.v2`). Pattern:

```html
<div class="v2">
    <header class="h">
        <h1>page title</h1>
        <p class="sub">one line, text role, dim</p>      <!-- optional -->
    </header>

    <!-- optional group heading, then rows -->
    <h2 class="grp">2026</h2>
    <article class="row">
        <div class="lab">feb 08</div>                    <!-- or class="row solo" with no .lab -->
        <div>
            <h2><a href="...">title</a></h2>            <!-- subheading, link = accent -->
            <p>blurb</p>                                 <!-- dim, justified -->
            <ul class="tags"><li>tag</li></ul>
        </div>
    </article>

    <p class="quirk">one dry line.</p>
</div>
```

`base.html` supplies nav, `<main class="v2-main">`, footer, loader and theme. `<body data-section="...">` carries the current section (kept current on htmx swaps); CSS keys off it. Shared markup lives in `templates/macros.html` (back link); private image urls come from `{{ private_url('name') }}`.
htmx swaps only `#main-content`; page meta travels via `SECTION_META` in
`app/routes/sections.py`.

---

## 5. Component catalogue (the complete list)

| component | class | notes |
|---|---|---|
| nav | `.v2-nav` / `.nav-link` | text links, dim; current page = clay + 2px underline bar. Five links, always visible, no hamburger. Theme toggle `(■_■¬)` right. |
| page header | `header.h` | `h1` clay heading + optional `.sub`. `.has-act` adds one action on the right (cv download). |
| row | `.row` | label column + content, hairline on top. `.row.solo` = full width, no label. `.row.tight` = skills rows only. |
| label | `.lab` | subtext mono faint: year, date, field name. |
| group heading | `.grp` | **one** component for thoughts years, work years and cv section titles: subheading role, mono bold, clay, letter-spaced. |
| row title | `h2`/`h3` in `.row` | subheading role; link = clay + underline (`↗` suffix if external); non-link = ink. |
| tag | `.tags li` | the only pill. Subtext mono, hairline outline, no `#`. Used identically on work, thoughts list and post header. |
| stat card | `.stat` | the only card. `--paper` fill, hairline, `--r-md`. Cv summary only. |
| toggle | `.tg` | clay text button + chevron. Smooth accordion (`.more`, grid-template-rows). |
| action | `.act` | clay text + small icon, same look as `.tg` (cv "download"). |
| back link | `.back` | same look as `.tg`, arrow nudges left on hover. |
| bullets | `ul.jobs`, `.post-body ul` | disc, clay marker, dim text. |
| progress bar | `.bar` | 3px, line track, clay fill; work "why" panel only. |
| career line | `.line` + `.ax` | to-scale bar, hatched gap segment, mono axis. Cv only. |
| popover | `.bike-pop` | `--paper`, hairline, `--r-md`. Appears on hover/click of the trigger. |
| quirk | `.quirk` | subtext italic faint, one per page, at the end. |
| footer | `.v2-foot` | subtext faint, "built using fastapi, htmx and tailwindcss". |
| loader | `.v2-loading` | small mono lowercase verb (cogitating, cooking, pondering...) with a clay spinner, tokens only. One random verb per request. Appears after a .15s grace so fast swaps never flash it. Add verbs to the `loadingVerbs` list in `base.html`: lowercase gerunds, dry, no emoji. |
| not found | `templates/404.html` | normal page skeleton: `h1` "not found", one-line sub, `.back` link, one quirk. Served for any unknown page request (browser navigation or htmx, decided by `Accept`/`HX-Request`; images, assets and APIs keep a plain 404) via `render_section(..., "notfound", status_code=404)`. `base.html` lets htmx swap a 404 into `#main-content`. |

Hairlines are horizontal `border-top`/`border-bottom` in `--line`. There are no
other kinds of line. Separators inside inline lists use `<span class="dot">·</span>`.

If you think you need a new component, first try composing these. If you
truly can't, add it here with its tokens, then build it.

---

## 6. Emphasis and typography rules

- **Bold** (`<strong>`, ink): the one key phrase/term in a paragraph; titles;
  stat numbers; metrics in cv bullets. Not whole sentences.
- *Italic* (`<em>`): asides and notes (`(claudependant)`, `(because startups)`),
  the title of a published work, quirk lines. Never for emphasis of facts.
- Underline: **links only**, soft clay underline. The dotted underline on
  "motorcyclist" signals "hover/click me" and is the single exception.
- ~~Strikethrough~~: only the `prompt context harness` joke in skills.
- **Clay** is for: links, `h1`, group headings, stat numbers, bullet markers,
  current nav item, toggles/actions. Never for body text or decoration.
- Body paragraphs are **justified** (`text-align: justify`, no auto
  hyphenation). Labels, tags, stats, contact line and intros stay left-aligned.
- Standalone paragraphs are `--ink`; secondary copy inside rows and bullets is
  `--dim` with `<strong>` in ink for contrast.

---

## 7. Voice and copy

Owner's voice: lowercase, dry, first-person, plain. Short sentences. Brackets
for a deadpan aside. Self-deprecating, never boastful.

Do:
- `journaling stuff i build (or want to).`
- `i wanted to ... because i once bombed an interview (hard)`
- `last proofread: not recently.`
- `to scale. the gap is a gap.`
- `curated by one person with no quality control.`

Don't:
- title case, exclamation marks, emoji, "excited to", "passionate about",
  marketing language, "we".
- explain the joke. One quirk line per page, at the end, subtext italic.
- repeat the page subtitle in the quirk (tangents lesson: "filed under: things
  that don't fit" duplicated the subtitle and was cut).

Rules for editing content:
- The owner's existing wording is canonical. Do not reword, "improve" or
  reorder it unless asked. When in doubt, diff old vs new text (see checklist).
- Keep factual claims true to the source (cv, repos). Don't invent numbers,
  dates, employers or skills. Unknown? Ask.
- Dates: `feb 08` in lists, `feb 08, 2026` in a post header, `november 2025 – present` on the cv.
- Self-referential honesty is the brand: `(claudependant)`, `(prompting counts)`,
  `too many roles (because startups)`.

---

## 8. Motion

Subtle and short. Allowed: staggered fade-up of rows on load, smooth accordion,
chevron rotate, link opacity .8 on hover, progress-bar fill, nav underline.
Nothing bounces, spins (except the loader), parallaxes or autoplays.
Everything is disabled under `prefers-reduced-motion`.

---

## 9. Accessibility (do not regress)

- Tap targets >= `--tap` (2.75rem) for anything clickable.
- Visible `:focus-visible` outline in the accent.
- Current nav item uses `aria-current="page"` (driven by `markActiveSection`).
- Icon-only or shortened controls keep a full `aria-label`
  (`download` -> "download as pdf").
- Colour is never the only cue: links are underlined, current page has a bar.
- Both themes meet contrast for text roles; `--faint` is for non-essential labels only.
- Images need meaningful `alt`; the toggled content uses `aria-expanded`/`aria-controls`.

---

## 10. Privacy and media

The repo is **public**. Anything committed is public and scrapable.

- Personal photos live in `private/` (git-ignored), never in `assets/` or `static/`.
- They are served only through a signed, expiring route
  (`/_/p/{name}/{token}`, `app/services/private_media.py`): blocked for bots
  and non-browser clients, `no-store`, `noindex/noai` headers, loaded only on
  interaction (`data-src`, no `src` in HTML).
- Strip **all** metadata (EXIF, GPS, ICC, XMP) before use. Verify nothing
  remains.
- Set `MEDIA_SECRET` in the environment in production. The image itself is not in git:
  on Railway it lives in `PRIVATE_<NAME>_B64_0..n` variables (base64, 30,000-character
  chunks, Railway's per-variable limit is 32,768) and `private_media` rebuilds
  `private/<name>.jpg` from them on first use. Locally just keep the file in `private/`.
- Nothing is ever fully un-saveable (screenshots). Don't claim otherwise.

---

## 11. How to add or change things

**New page**
1. Add an entry to `SECTION_META` and a route in `app/routes/sections.py`.
2. Create `templates/sections/<name>.html` using the skeleton in section 4.
3. Add the nav link in `templates/base.html` (keep five-ish links, lowercase).
4. Use only catalogue components. Give it one quirk line.

**New content row** (project, post, tangent, job): copy an existing row of
that type; change text only.

**New style**: change a token or extend a component in `site.css`; scope under
`.v2`; use tokens; update section 5 if a component's behaviour changes.

**States** (loading, 404, empty, error) are part of the design: build them from the same components. `mockups/v2/states.html` is a local preview of the loader and swap animation.

**Mockups**: local HTML only (`mockups/`, git-ignored). Never publish
mockups or design work for this project to any cloud/hosting service.

**Do not touch** `whelmed`/`cases` styling as part of site changes; they are a
separate legacy design (known inconsistency, intentionally out of scope).

---

## 12. Pre-merge checklist

Run these against a local server (`uvicorn main:app --port 8000`).

1. **Lowercase:** no uppercase in visible text on any page or post.
   ```bash
   python3 - <<'EOF'
   import re,urllib.request,html
   for p in ['me','work','thoughts','tangents','cv']:
       h=urllib.request.urlopen('http://localhost:8000/'+p).read().decode()
       h=re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->|<head>.*?</head>','',h,flags=re.S)
       t=html.unescape(' '.join(re.findall(r'>([^<>]+)<',h)))
       print(p,sorted(set(re.findall(r'\b\w*[A-Z]\w*\b',t))))
   EOF
   ```
2. **No px / stray sizes:** `grep -nE "[0-9]px|font-size" assets/css/site.css templates/sections/*.html`
   should show only the allowed tokens and the hairline.
3. **No raw colours in templates:** no `#hex`, `rgb(` or Tailwind colour classes in `templates/sections/*`.
4. **Inline styles:** only data values (`--p`, `flex` on the career bar).
5. **Both themes** and **phone width** (<44rem: rows stack, nav fits one line, stats 2x2).
6. **Keyboard:** tab through the page; every control is reachable and visibly focused.
7. **Text fidelity:** diff visible text old vs new for any page you touched;
   every difference must be intentional.
8. **Consistency:** same row padding, same tag component, same group heading,
   same link treatment, one quirk line, footer present.
9. **Privacy:** `git status` shows nothing under `private/`; no new images in `assets/`/`static/` without a reason.

---

## 13. Decision log (why things are the way they are)

- One width + one row pattern across pages: variants with different widths
  looked inconsistent ("hot glob of mess").
- Four type roles at normal sizes: 12px text was tried and was unreadable; the
  scale is tokenised so it can be retuned in one place.
- Mono for subheadings/subtext: gives the dorky feel without turning body text
  into a terminal.
- Year grouping (`.grp`) is the shared timeline for work and thoughts, with the same
  label column; work's label is the self-assessed progress (`40%`) because projects only have years.
- Tags are one pill component everywhere (the post page used a different pill
  and `#` text; unified).
- Clay chosen over teal/ochre as the single accent.
- Skills row is deliberately personal: struck-through `prompt context harness`
  (the field keeps moving), `(claudependant)`. Keep the jokes, keep the list honest.
- Career bar is to scale with a visible gap; proportions are hard-coded
  (45/5/2/12 months) and need updating when the timeline changes.

### Open items
- `whelmed` / `cases` pages don't use this design.
- Phone-width and light-mode were spot-checked, not exhaustively tested.
