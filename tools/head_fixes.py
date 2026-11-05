#!/usr/bin/env python3
"""Titles, descriptions, H1s, social tags, JSON-LD, pixel placeholder, hero video, mobile call button."""
import re, glob, os, json, html
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = 'https://davisroofingandexteriors.com'
BRAND = 'Davis Roofing &amp; Exteriors'
log = []

META = {  # page: (title, description) — None keeps the current value
 'index.html': ('Staunton &amp; Richmond Roofing, Siding &amp; Gutters | ' + BRAND,
   'Roofing, siding, window and gutter contractor serving Staunton, the Shenandoah Valley, Richmond and Midlothian. Most roofs installed in one day. Free estimates.'),
 'about.html': ('About Us | Locally Owned Roofer in Staunton, VA | ' + BRAND, None),
 'contact.html': ('Free Estimate &amp; Contact | ' + BRAND, None),
 'service-areas.html': ('Service Areas: Shenandoah Valley &amp; Richmond Metro | ' + BRAND, None),
 'services.html': ('Roofing, Siding, Window &amp; Gutter Services | ' + BRAND, None),
 'service-roofing.html': ('Roof Replacement &amp; Repair in Staunton &amp; Richmond, VA | ' + BRAND, None),
 'service-siding.html': ('Siding Installation in Staunton &amp; Richmond, VA | ' + BRAND, None),
 'service-windows-and-doors.html': ('Window &amp; Door Replacement in Staunton &amp; Richmond, VA | ' + BRAND, None),
 'service-gutters.html': ('Seamless Gutters &amp; Guards in Staunton &amp; Richmond, VA | ' + BRAND,
   'Seamless aluminum gutters and gutter guards formed on site in Staunton, the Shenandoah Valley and Richmond, VA. Free estimates. Ask about free gutters with a roof replacement.'),
 'work.html': ('Our Work: Roofing, Siding, Windows &amp; Gutters | ' + BRAND,
   'Roofing, siding, window and gutter work by Davis Roofing &amp; Exteriors across the Shenandoah Valley and Richmond metro, including a before-and-after roof replacement.'),
}
H1 = {
 'services.html': ('Your whole exterior, handled by one crew.', 'Roofing, siding, windows and gutters, handled by one crew.'),
 'service-siding.html': ('Siding that protects and transforms.', 'Siding installation and replacement.'),
 'service-roofing.html': ("Staunton's roof replacement specialists.", 'Roof replacement and storm repair specialists.'),
 'service-areas.html': ('Two crews. Two regions. One standard.', 'Service areas: the Shenandoah Valley and Richmond metro.'),
}
SERVICE = {
 'service-roofing.html': 'Roof replacement and repair', 'service-siding.html': 'Siding installation and replacement',
 'service-windows-and-doors.html': 'Window and door replacement', 'service-gutters.html': 'Seamless gutter installation',
}
AREAS = ['Staunton','Waynesboro','Fishersville','Stuarts Draft','Verona','Greenville','Mount Sidney','Churchville','Augusta County',
         'Richmond','Midlothian','Chesterfield','Glen Allen','Henrico','Mechanicsville','Short Pump','Powhatan','Charlottesville','Palmyra']
BUSINESS = {
 '@type': 'RoofingContractor', '@id': SITE + '/#business',
 'name': 'Davis Roofing & Exteriors', 'legalName': 'Davis Roofing & Exteriors LLC',
 'url': SITE + '/', 'telephone': '+1-540-534-5380', 'email': 'info@davisroofingandexteriors.com',
 'logo': SITE + '/images/logo-transparent.png', 'image': SITE + '/images/og-image.jpg',
 'description': 'Roofing, siding, window and gutter contractor based in Staunton, Virginia, serving the Shenandoah Valley and the Richmond–Midlothian metro.',
 'address': {'@type': 'PostalAddress', 'addressLocality': 'Staunton', 'addressRegion': 'VA', 'addressCountry': 'US'},
 'areaServed': [{'@type': 'AdministrativeArea' if 'County' in a else 'City', 'name': a + ', VA'} for a in AREAS],
 'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification',
   'dayOfWeek': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], 'opens': '10:00', 'closes': '18:00'}],
 'founder': {'@type': 'Person', 'name': 'Jordan Davis'},
 'knowsAbout': ['Roof replacement', 'Storm damage repair', 'Siding', 'Replacement windows and doors', 'Seamless gutters'],
}
def url_of(f): return SITE + '/' if f == 'index.html' else f'{SITE}/{f}'
def textof(x): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip()

PIXEL = re.compile(r'<!-- =+\s*META PIXEL.*?<!-- =+ -->\s*', re.S)
CALL_BTN = ('\n    <a class="m-call" href="tel:+15405345380" aria-label="Call (540) 534-5380">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
            '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg><span>Call</span></a>\n')
CALL_CSS = ('\n/* mobile header call button (Nov 2026) */\n'
            '.m-call{display:inline-flex;align-items:center;gap:8px;margin-left:auto;min-height:48px;padding:0 18px;border-radius:9999px;'
            'background:hsl(var(--sky));color:#fff;font-family:var(--mono);font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}\n'
            '.m-call:focus-visible{outline:2px solid #fff;outline-offset:3px}\n'
            '@media(min-width:700px){.m-call{display:none}}\n')

for f in sorted(glob.glob('*.html')):
    if f in ('privacy-policy.html', 'terms-of-service.html', '404.html'): continue
    s = open(f, encoding='utf-8').read(); o = s
    s = PIXEL.sub('', s)
    if f in META:
        t, d = META[f]
        s = re.sub(r'<title>.*?</title>', f'<title>{t}</title>', s, count=1, flags=re.S)
        s = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + t + '"', s)
        if d:
            s = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + d + '"', s)
            s = re.sub(r'(<meta property="og:description" content=")[^"]*"', lambda m: m.group(1) + d + '"', s)
    if f in H1:
        a, b = H1[f]; assert a in s, (f, a); s = s.replace(f'<h1>{a}</h1>', f'<h1>{b}</h1>')
    if f == 'service-areas.html':
        s = s.replace('<span class="eyebrow">Where we work</span>', '<span class="eyebrow">Two crews. Two regions. One standard.</span>')
    # social tags: absolute image, og:url, twitter image
    s = s.replace('content="images/og-image.jpg"', f'content="{SITE}/images/og-image.jpg"')
    if '<meta property="og:url"' not in s and '<meta property="og:type"' in s:
        s = s.replace('<meta property="og:type"', f'<meta property="og:url" content="{url_of(f)}">\n<meta property="og:type"', 1)
    if 'og:image:width' not in s and 'og:image" content' in s:
        s = re.sub(r'(<meta property="og:image" content="[^"]*">)', r'\1\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta name="twitter:image" content="' + SITE + '/images/og-image.jpg">', s, count=1)
    # structured data
    if 'noindex' not in s:
        graph = [dict(BUSINESS)]
        crumb = re.search(r'<p class="crumb">(.*?)</p>', s, re.S)
        if crumb:
            parts = re.split(r'&nbsp;/&nbsp;', crumb.group(1)); items = []
            for i, p in enumerate(parts):
                m = re.search(r'href="([^"]+)"', p)
                href = (SITE + '/' if m.group(1) == '/' else f'{SITE}/{m.group(1)}') if m else url_of(f)
                items.append({'@type': 'ListItem', 'position': i + 1, 'name': textof(p), 'item': href})
            graph.append({'@type': 'BreadcrumbList', '@id': url_of(f) + '#breadcrumb', 'itemListElement': items})
        if f in SERVICE:
            graph.append({'@type': 'Service', '@id': url_of(f) + '#service', 'name': SERVICE[f], 'serviceType': SERVICE[f],
                          'provider': {'@id': SITE + '/#business'}, 'areaServed': BUSINESS['areaServed'], 'url': url_of(f)})
        if f != 'index.html': graph[0] = {'@id': SITE + '/#business', **{k: v for k, v in BUSINESS.items() if k != '@id'}}
        ld = '<script type="application/ld+json">\n' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1) + '\n</script>\n'
        s = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', s, flags=re.S)
        s = s.replace('</head>', ld + '</head>', 1)
    # mobile call button in the header
    if 'class="m-call"' not in s and '<button class="burger"' in s:
        s = s.replace('\n    <button class="burger"', CALL_BTN + '    <button class="burger"', 1)
        s = s.replace('</style>', CALL_CSS + '</style>', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); log.append('ok ' + f)

# homepage hero: the stock clip was never deployed (404). Keep the existing poster as the hero image.
s = open('index.html', encoding='utf-8').read()
s2 = re.sub(r'<video autoplay muted loop playsinline preload="metadata"\s*poster="images/hero-poster.jpg">\s*<source src="images/17624839-uhd_3840_2160_30fps.mp4" type="video/mp4">\s*</video>',
            '<img src="images/hero-poster.jpg" alt="" width="1920" height="1080" fetchpriority="high" decoding="async">', s)
if s2 != s: open('index.html', 'w', encoding='utf-8').write(s2); log.append('ok hero video -> poster image')
print('\n'.join(log))
