#!/usr/bin/env python3
"""Verifie les fichiers editables avant le deploiement. Echec = le site en ligne reste inchange."""
import json, os, re, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public')
errors = []

def err(msg):
    errors.append(msg)

# ---- products.json ----
try:
    data = json.load(open(os.path.join(ROOT, 'products.json'), encoding='utf-8'))
except Exception as e:
    print('ERREUR products.json invalide (JSON):', e)
    sys.exit(1)

products = data.get('products')
if not isinstance(products, list) or not products:
    err('products.json: la liste "products" est vide ou absente')
    products = []

ids = set()
for i, p in enumerate(products, 1):
    tag = 'produit #%d (%s)' % (i, p.get('id', '?') if isinstance(p, dict) else '?')
    if not isinstance(p, dict):
        err('%s: doit etre un objet' % tag); continue
    pid = p.get('id')
    if not isinstance(pid, str) or not re.fullmatch(r'[a-z0-9-]+', pid):
        err('%s: "id" obligatoire, lettres minuscules/chiffres/tirets seulement' % tag)
    elif pid in ids:
        err('%s: "id" deja utilise' % tag)
    else:
        ids.add(pid)
    for k in ('name', 'title'):
        if not isinstance(p.get(k), str) or not p[k].strip():
            err('%s: "%s" obligatoire' % (tag, k))
    price = p.get('price')
    if price is not None and (isinstance(price, bool) or not isinstance(price, int) or price <= 0):
        err('%s: "price" doit etre un nombre entier positif (ex: 18000) ou null' % tag)
    if p.get('quality') not in (None, 'origine', 'adaptable'):
        err('%s: "quality" doit etre "origine", "adaptable" ou null' % tag)
    imgs = p.get('images')
    if not isinstance(imgs, list) or not imgs:
        err('%s: "images" doit contenir au moins une image' % tag)
    else:
        for im in imgs:
            if not isinstance(im, str) or not os.path.isfile(os.path.join(ROOT, im)):
                err('%s: image introuvable: %s' % (tag, im))
    for k in ('description', 'vehicle', 'years', 'badge', 'compat', 'ref', 'unit', 'vehiclePrefill', 'vehiclePlaceholder'):
        if k in p and p[k] is not None and not isinstance(p[k], str):
            err('%s: "%s" doit etre du texte' % (tag, k))
    for k in ('active', 'motorisation'):
        if k in p and not isinstance(p[k], bool):
            err('%s: "%s" doit etre true ou false' % (tag, k))

# ---- config.js ----
cfg_path = os.path.join(ROOT, 'config.js')
r = subprocess.run(['node', '--check', cfg_path], capture_output=True, text=True)
if r.returncode != 0:
    lines = [l for l in r.stderr.splitlines() if 'Error' in l]
    err('config.js: erreur de syntaxe: ' + (lines[0].strip() if lines else 'voir le fichier'))
else:
    js = ("const vm=require('vm'),fs=require('fs');const c={};"
          "vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8')+';this.CONFIG=CONFIG',c);"
          "console.log(JSON.stringify(c.CONFIG))")
    r = subprocess.run(['node', '-e', js, cfg_path], capture_output=True, text=True)
    if r.returncode != 0:
        err('config.js: impossible de lire CONFIG')
    else:
        cfg = json.loads(r.stdout)
        if not re.fullmatch(r'213[567]\d{8}', str(cfg.get('phone', ''))):
            err('config.js: "phone" doit etre au format 2136XXXXXXXX (sans + ni espaces)')
        for c in cfg.get('calls', []):
            if not (isinstance(c, list) and len(c) == 2 and re.fullmatch(r'\+213[567]\d{8}', str(c[1]))):
                err('config.js: chaque entree de "calls" doit etre ["0XXX XX XX XX", "+2136XXXXXXXX"]')
        su = cfg.get('sheetUrl', '')
        if su and not re.fullmatch(r'https://script\.google\.com/macros/s/[\w-]+/exec', su):
            err('config.js: "sheetUrl" doit etre l\'URL de l\'application web Google (se termine par /exec)')
        px = cfg.get('pixelId', '')
        if px and not re.fullmatch(r'\d{10,20}', px):
            err('config.js: "pixelId" doit contenir uniquement des chiffres')

# ---- geo.js ----
r = subprocess.run(['node', '--check', os.path.join(ROOT, 'geo.js')], capture_output=True, text=True)
if r.returncode != 0:
    err('geo.js: erreur de syntaxe')

if errors:
    print('VALIDATION ECHOUEE:')
    for e in errors:
        print(' -', e)
    sys.exit(1)
print('Validation OK: %d produit(s), config.js et geo.js valides' % len(products))
