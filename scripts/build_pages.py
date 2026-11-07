#!/usr/bin/env python3
"""Genere, pour chaque produit actif: public/p/<id>/index.html (apercu Facebook propre au produit)
et public/img/og/<id>.jpg (image 1200x630). Les fichiers generes ne sont pas versionnes."""
import html, json, os, re, shutil, sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public'))
SITE = 'https://almoutamad-commande.web.app'
FONTS = ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf']

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    Image = None


def font(size):
    for f in FONTS:
        if os.path.isfile(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=fnt) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def make_og(p, out):
    W, H, SPLIT = 1200, 630, 560
    im = Image.new('RGB', (W, H), '#0f2438')
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 14, H], fill='#ff7a1a')
    src = os.path.join(ROOT, p['images'][0])
    ph = Image.open(src).convert('RGB')
    r = max((W - SPLIT) / ph.width, H / ph.height)
    ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1))
    x0, y0 = (ph.width - (W - SPLIT)) // 2, (ph.height - H) // 2
    im.paste(ph.crop((x0, y0, x0 + W - SPLIT, y0 + H)), (SPLIT, 0))
    d.text((60, 72), 'AL MOUTAMAD', font=font(38), fill='#ff7a1a')
    d.text((60, 124), 'Pièces détachées auto', font=font(26), fill='#9fb3c8')
    size = 56
    while True:
        f = font(size)
        lines = wrap(d, p['title'].replace(' — ', ' '), f, SPLIT - 100)
        if len(lines) <= 4 or size <= 36:
            break
        size -= 4
    y = 220
    for l in lines[:4]:
        d.text((60, y), l, font=f, fill='#ffffff'); y += int(size * 1.22)
    label = 'Commander en ligne'
    bf = font(28); tw = d.textlength(label, font=bf)
    d.rounded_rectangle([60, 545, 60 + tw + 60, 598], radius=27, fill='#ff7a1a')
    d.text((90, 556), label, font=bf, fill='#ffffff')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, 'JPEG', quality=85, optimize=True)


def meta(s, prop, val, attr='property'):
    pat = r'(<meta %s="%s" content=")[^"]*(")' % (attr, re.escape(prop))
    new, n = re.subn(pat, lambda m: m.group(1) + html.escape(val, quote=True) + m.group(2), s, count=1)
    if n != 1:
        raise SystemExit('balise manquante dans index.html: ' + prop)
    return new


def main():
    data = json.load(open(os.path.join(ROOT, 'products.json'), encoding='utf-8'))
    tpl = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    for sub in ('p', os.path.join('img', 'og')):
        shutil.rmtree(os.path.join(ROOT, sub), ignore_errors=True)
    count = 0
    for p in data.get('products', []):
        if p.get('active') is False:
            continue
        pid = p['id']
        og_rel = 'img/og/%s.jpg' % pid
        og_ok = False
        if Image is not None:
            try:
                make_og(p, os.path.join(ROOT, og_rel)); og_ok = True
            except Exception as e:
                print('Avertissement: image og non generee pour %s: %s' % (pid, e))
        img = og_rel if og_ok else p['images'][0]
        desc = ((p.get('description') or p.get('compat') or '').strip().replace('\n', ' ')[:160]
                or 'Commandez en ligne en une minute, paiement à la livraison.')
        s = tpl
        s = re.sub(r'<title>.*?</title>', lambda m: '<title>%s — Al Moutamad</title>' % html.escape(p['title']), s, count=1)
        s = meta(s, 'description', desc, 'name')
        s = meta(s, 'og:url', '%s/p/%s/' % (SITE, pid))
        s = meta(s, 'og:title', p['title'])
        s = meta(s, 'og:description', desc)
        s = meta(s, 'og:image', '%s/%s' % (SITE, img))
        if not og_ok:
            s = re.sub(r'<meta property="og:image:(width|height)"[^>]*>\n?', '', s)
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="/">', 1)
        out = os.path.join(ROOT, 'p', pid, 'index.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(s)
        count += 1
    print('Pages produit generees: %d' % count)


main()
