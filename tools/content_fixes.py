#!/usr/bin/env python3
"""One-off content fixes for the Nov 2026 SEO/maintenance update. Safe to re-run."""
import re, glob, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
log = []
def sub(f, old, new, regex=False, need=True):
    s = open(f, encoding='utf-8').read()
    n = len(re.findall(old, s)) if regex else s.count(old)
    if n == 0:
        if need and new not in s: log.append(f'MISS {f}: {old[:70]}')
        return
    s = re.sub(old, new, s) if regex else s.replace(old, new)
    open(f, 'w', encoding='utf-8').write(s); log.append(f'ok {n}x {f}: {old[:60]}')
ALL = sorted(glob.glob('*.html'))

for f in ALL:
    # 1. header displayed the wrong number (links already dialed 534-5380)
    sub(f, '(540)&nbsp;985-7868', '(540)&nbsp;534-5380', need=False)
    # 2. promo wording: the offer is one OR the other
    sub(f, 'Lock in $1,000 off plus free gutters this season.', 'Choose $1,000 off a roof replacement or free gutters this season.', need=False)
    # 3. home link without the /index.html duplicate URL
    sub(f, 'href="index.html"', 'href="/"', need=False)

# 4. closing CTA on non-roof service pages
CTA = r'<h2 class="rv">A roof done right (?:—|&mdash;) <span class="accent">and done fast\.</span></h2>\s*<p class="lead rv d1" style="margin-top:18px">[^<]*</p>'
def cta(h2a, h2b, p): return f'<h2 class="rv">{h2a} <span class="accent">{h2b}</span></h2>\n    <p class="lead rv d1" style="margin-top:18px">{p}</p>'
sub('service-siding.html', CTA, cta('New siding,', 'done right.', 'Free estimates, financing available, and most homes finished in two to four days.'), regex=True)
sub('service-windows-and-doors.html', CTA, cta('Replacement windows,', 'installed right.', 'Free estimates, financing available, and every opening measured and flashed by our own crew.'), regex=True)
sub('service-gutters.html', CTA, cta('Seamless gutters,', 'sized to your home.', 'Free estimates, financing available, and gutters formed on site to the exact length of every run. Ask about free gutters with a roof replacement.'), regex=True)

# 5. unsupported absolute promises and numbers
sub('index.html', 'brighten rooms and kill drafts. Precise measurement, proper flashing, no callbacks.', 'brighten rooms and cut drafts. Precise measurement and proper flashing on every opening.')
sub('index.html', 'locks out moisture, cuts energy bills and completely resets', 'keeps out moisture, can help lower energy bills and resets')
sub('services.html', 'Flashed, foamed and caulked — no drafts, no callbacks', 'Flashed, foamed and caulked to keep drafts out')
sub('services.html', 'Insulated options that measurably cut energy bills', 'Insulated options that can help lower energy bills')
sub('service-windows-and-doors.html', 'installed properly &mdash; no drafts, no callbacks.', 'installed properly and sealed against drafts.')
sub('service-gutters.html', '<h1>Seamless gutters. Zero seams. Zero leaks.</h1>', '<h1>Seamless gutter installation and gutter guards.</h1>')
sub('service-gutters.html', 'with a lifetime finish warranty.', 'with a manufacturer finish warranty (terms vary by product).')
sub('service-siding.html', r'by 20(?:–|&ndash;|-)30% compared to', 'compared to', regex=True)
sub('service-windows-and-doors.html', r'can reduce heat loss by 25(?:–|&ndash;|-)50% through the glass alone', 'can noticeably reduce heat loss through the glass', regex=True)
WAR = 'Materials carry the manufacturer’s warranty, and our installation carries our own workmanship warranty. We walk you through both before work starts.'
sub('index.html', '<h3>Quality install, guaranteed</h3><p>Premium materials and a meticulous process — backed by both manufacturer and workmanship warranties.</p>', f'<h3>Quality install, two warranties</h3><p>{WAR}</p>')
sub('about.html', '<h3>Quality Install, Guaranteed</h3>', '<h3>Quality Install, Two Warranties</h3>')
sub('about.html', '<p>Premium materials and a meticulous install process — backed by manufacturer and workmanship warranties.</p>', f'<p>{WAR}</p>')

# 6. stock photos are not Davis jobs: drop local-job captions, label as illustrative
sub('work.html', '<span class="eyebrow">Recent projects</span>\n    <h1>Proof, not promises.</h1>', '<span class="eyebrow">Our work</span>\n    <h1>Roofing, siding, window and gutter work.</h1>')
sub('work.html', "Every one of these is a real Virginia home. Drone shots, ground shots, and a few before-and-afters we're particularly proud of.", 'The kinds of jobs our crews handle every week across the Shenandoah Valley and Richmond metro. Gallery photos are illustrative; the before-and-after is a Davis job.')
for f in ['work.html', 'index.html']:
    s = open(f, encoding='utf-8').read()
    # <span class="ph"><b>Roofing</b><span>Staunton, VA · Drone</span></span> ... alt="… — Town, VA" ... <span class="cap">X · Town</span>
    s2 = re.sub(r'(<span class="ph"><b>[^<]+</b><span>)[^<]*(</span></span>)', r'\1Illustrative photo\2', s)
    s2 = re.sub(r'(alt="[^"]*?) — [A-Z][a-z]+(?: [A-Z][a-z]+)?, VA"', r'\1"', s2)
    s2 = re.sub(r'<span class="cap">([^<·]+?) · [A-Z][A-Za-z ]+</span>', r'<span class="cap">\1</span>', s2)
    if s2 != s: open(f, 'w', encoding='utf-8').write(s2); log.append(f'ok captions {f}')

# 7. leftover map placeholder visible on the live service-areas page
sub('service-areas.html', r'\s*<div class="slot flat rv"[^>]*>\s*<b>Map embed slot</b>\s*<span>[^<]*</span>\s*</div>', '', regex=True)

print('\n'.join(log))
