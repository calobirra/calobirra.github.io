#!/usr/bin/env python3
"""Fill the website's {{PLACEHOLDERS}} and write a publishable copy to _site/.

  python3 tools/build_web.py --config web.config.json      # real data → _site/ (fails if anything is missing)
  python3 tools/build_web.py --preview                     # highlights what is missing, for review only

web.config.json (or datos.json in the public web repo):
  {"OWNER_NAME": "...", "SUPPORT_EMAIL": "...", "OWNER_TAX_ID": "...", "OWNER_ADDRESS": "...", "HOSTING_PROVIDER": "GitHub Pages"}
OWNER_TAX_ID and OWNER_ADDRESS are optional: when empty, their rows are left out of the legal notice.
Values can also come from environment variables with the same names.
"""
import argparse, datetime, html, json, os, pathlib, re, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
KEYS = ['OWNER_NAME', 'SUPPORT_EMAIL', 'OWNER_TAX_ID', 'OWNER_ADDRESS', 'HOSTING_PROVIDER']
OPTIONAL = ['OWNER_TAX_ID', 'OWNER_ADDRESS']   # personal data: published only if the owner provides it
LABELS = {'OWNER_NAME': 'nombre legal', 'SUPPORT_EMAIL': 'correo de soporte', 'OWNER_TAX_ID': 'NIF',
          'OWNER_ADDRESS': 'domicilio', 'HOSTING_PROVIDER': 'proveedor de alojamiento'}
ap = argparse.ArgumentParser()
ap.add_argument('--config'); ap.add_argument('--preview', action='store_true'); ap.add_argument('--out', default=str(ROOT / '_site'))
a = ap.parse_args()
values = {k: os.environ.get(k, '').strip() for k in KEYS}
if a.config:
    values.update({k: str(v).strip() for k, v in json.load(open(a.config, encoding='utf-8')).items() if k in KEYS})
if values['SUPPORT_EMAIL'] and not re.fullmatch(r'[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+', values['SUPPORT_EMAIL']):
    sys.exit('SUPPORT_EMAIL no parece un correo válido')
values['YEAR'] = str(datetime.date.today().year)
out = pathlib.Path(a.out)
shutil.rmtree(out, ignore_errors=True)
shutil.copytree(ROOT / 'web', out)
missing = set()
for page in out.rglob('*.html'):
    text = page.read_text(encoding='utf-8')
    for key in OPTIONAL:
        if not values.get(key):
            text = re.sub(r'<tr><th>[^<]*</th><td>\{\{%s\}\}</td></tr>\n?' % key, '', text)
    def fill(m):
        key = m.group(1)
        if values.get(key):
            return html.escape(values[key])
        missing.add(key)
        return f'<span class="pending">[pendiente: {LABELS.get(key, key)}]</span>' if a.preview else m.group(0)
    # mailto: hrefs can't contain markup: leave a harmless placeholder address in preview.
    text = re.sub(r'mailto:\{\{SUPPORT_EMAIL\}\}', lambda m: 'mailto:' + values['SUPPORT_EMAIL'] if values['SUPPORT_EMAIL'] else ('mailto:pendiente@example.invalid' if a.preview else m.group(0)), text)
    page.write_text(re.sub(r'\{\{([A-Z_]+)\}\}', fill, text), encoding='utf-8')
if missing and not a.preview:
    shutil.rmtree(out)
    sys.exit('Faltan datos: ' + ', '.join(LABELS.get(k, k) for k in sorted(missing)))
print(('Vista previa' if a.preview else 'Web lista') + f' en {out}' + (f' · pendientes: {", ".join(sorted(missing))}' if missing else ''))
