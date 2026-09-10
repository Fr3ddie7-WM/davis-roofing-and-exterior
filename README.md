# Davis Roofing & Exteriors — new website

Six static pages, no build step, no dependencies. Open `index.html` in a browser
and it runs. Drop the folder on any host (Netlify, Vercel, Cloudflare Pages,
cPanel) and it's live.

```
index.html          Home
services.html       Roofing / Siding / Windows / Gutters (+ anchors #roofing etc.)
work.html           Portfolio with category filter + before/after slider
about.html          Story, rules, stats, pull quote
service-areas.html  Two regions, town chips, coverage FAQ
contact.html        Estimate form + booking calendar slot
images/             Drop photos here (see below)
```

Each page is fully self-contained (CSS and JS inlined), so nothing breaks when
you move a file. Favicon is inline SVG — no separate file needed.

## 1. Drone footage — the hero

In `index.html`, find `DRONE FOOTAGE GOES HERE` near the top of the `<body>`.
Drop the clip at `images/hero-drone.mp4`, uncomment the `<video>` block, delete
the `<img>` below it. The poster is already set so there's no flash of black.

Keep it under ~8 MB and 15–20 seconds, muted, looping. A slow push-in over a
finished roof works better than fast movement — the headline sits on top of it.

## 2. Photos

Every image slot shows a designed placeholder until the real file exists, so
nothing ever renders as a broken image:

| File | Where |
|---|---|
| `images/project-01.jpg` … `project-09.jpg` | Portfolio grid (work.html) + home strip |
| `images/before-01.jpg`, `images/after-01.jpg` | Before/after slider (home + work) |
| `images/windows.jpg`, `images/gutters.jpg` | Services page |
| `images/og-image.jpg` | Link preview when the site is shared |

**The before/after pair matters most.** It needs to be the *same house from the
same angle* — one shot before the tear-off, one after. A mismatched pair makes
the slider look broken. One good set from a single job is enough.

The two photos currently showing (hero and siding) are Unsplash stock, carried
over from the current site. Swap them for Jordan's real drone stills as soon as
you have them.

## 3. The estimate form

`contact.html` validates properly — required fields highlight in red with inline
messages, it won't submit empty, and errors clear as you type. It does not send
anywhere yet. Wire it to the GoHighLevel endpoint (or drop a GHL embed in) and
the design is unchanged. The booking-calendar slot lower on the page is sized for
the existing GHL widget.

## 4. Design notes

- **Palette:** graphite/navy gradient panels with copper (`#D97B36`) and ember
  (`#F5B04C`) accents, alternating with warm bone light sections. Two distinct
  dark treatments (`.dark` and `.dark-alt`) so the gradient panels don't read as
  wallpaper when they repeat.
- **Type:** Bricolage Grotesque (display, 300/700/800 — the light weight carries
  the two-tone headlines), DM Sans (body), DM Mono (labels).
- **Tokens** live in the `:root` block at the top of each page's `<style>`.
- **Contrast:** copper is darkened to `#9C4E16` on light backgrounds and the
  offers band uses a deep copper gradient — everything clears WCAG AA.
- **Interactions:** sticky nav, full-screen mobile drawer, staggered scroll
  reveals, draggable *and keyboard-operable* before/after slider, portfolio
  filter, accordion FAQs. All respect `prefers-reduced-motion`.
- **Robustness:** page content is visible even if JavaScript fails (`no-js`
  fallback), and there's a print stylesheet so a homeowner printing the estimate
  page gets clean black-on-white.
- **Responsive:** phone number stays visible in the header from 700px up, so it
  doesn't vanish on tablets. Hero grows with its content instead of clipping.

Built by WAT Media.
