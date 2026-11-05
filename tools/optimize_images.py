#!/usr/bin/env python3
"""Resize page images into images/opt/ (WebP + JPEG fallbacks) and rewrite <img> tags with
<picture>, srcset, sizes, intrinsic dimensions and lazy loading below the fold.
Display widths come from a headless measurement (tools/imgsizes.json) at 1440, 820 and 390px."""
import re, os, json, sys
from PIL import Image, ImageOps
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
M = json.load(open('tools/imgsizes.json'))
WIDTHS = [480, 800, 1200]
made = {}
def variants(src):
    if src in made: return made[src]
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    W, H = im.size; stem = os.path.splitext(os.path.basename(src))[0].lower()
    ws = sorted({w for w in WIDTHS if w < W} | {min(W, WIDTHS[-1])})
    out = []
    for w in ws:
        h = round(H * w / W); r = im.resize((w, h), Image.LANCZOS)
        base = f'images/opt/{stem}-{w}'
        r.save(base + '.webp', 'WEBP', quality=78, method=6)
        r.save(base + '.jpg', 'JPEG', quality=80, optimize=True, progressive=True)
        out.append((w, h, base))
    made[src] = out; return out
os.makedirs('images/opt', exist_ok=True)
FOLD = {'d': 900, 'm': 844}
total = 0
for page, vps in M.items():
    s = open(page, encoding='utf-8').read()
    a = s.index('<main'); b = s.index('</main>')
    main = s[a:b]; queue = list(range(len(vps['d'])))
    def repl(m):
        tag = m.group(0); src = re.search(r'src="([^"]+)"', tag).group(1)
        if not src.startswith('images/') or 'logo' in src or not queue: return tag
        k = queue.pop(0); d, t, mo = vps['d'][k], vps['t'][k], vps['m'][k]
        assert d['src'] == src, (page, k, d['src'], src)
        vs = variants(src); w, h, _ = vs[-1]
        sizes = f'(max-width: 699px) {max(1, round(mo["w"] / 390 * 100))}vw, (max-width: 1099px) {max(1, round(t["w"] / 820 * 100))}vw, {d["w"]}px'
        webp = ', '.join(f'{b_}.webp {w_}w' for w_, _, b_ in vs); jpg = ', '.join(f'{b_}.jpg {w_}w' for w_, _, b_ in vs)
        above = d['top'] < FOLD['d'] or mo['top'] < FOLD['m']
        t2 = re.sub(r'\s(src|srcset|sizes|loading|width|height|decoding|fetchpriority)="[^"]*"', '', tag)
        extra = f' src="{vs[-1][2]}.jpg" srcset="{jpg}" sizes="{sizes}" width="{w}" height="{h}" decoding="async"'
        extra += ' fetchpriority="high"' if 'hero-poster' in src else ('' if above else ' loading="lazy"')
        t2 = t2.replace('<img', '<img' + extra, 1)
        return f'<picture><source type="image/webp" srcset="{webp}" sizes="{sizes}">{t2}</picture>'
    if '<picture>' in main: print('skip (already done)', page); continue
    main2 = re.sub(r'<img\b[^>]*>', repl, main)
    s = s[:a] + main2 + s[b:]
    if ':where(img[width][height])' not in s:
        s = s.replace('</style>', '\n/* keep aspect ratio when only width is set by CSS (Nov 2026) */\n:where(img[width][height]){height:auto}\npicture{display:contents}\n</style>', 1)
    open(page, 'w', encoding='utf-8').write(s); print('rewrote', page, 'left', queue)
size = sum(os.path.getsize('images/opt/' + f) for f in os.listdir('images/opt'))
print(f'{len(made)} source images -> {len(os.listdir("images/opt"))} files, {size/1e6:.1f} MB in images/opt')
