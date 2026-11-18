#!/usr/bin/env python3
"""Check the website: every internal link and asset exists, pages have lang/title/viewport,
and (with --final) no {{PLACEHOLDER}} or [pendiente] is left. Usage: check_web.py <dir> [--final]"""
import pathlib, re, sys
root = pathlib.Path(sys.argv[1]); final = '--final' in sys.argv
errors = []; pages = list(root.rglob('*.html'))
for page in pages:
    text = page.read_text(encoding='utf-8')
    for need in ['<html lang=', '<title>', 'name="viewport"']:
        if need not in text: errors.append(f'{page}: falta {need}')
    for ref in re.findall(r'(?:href|src)="([^"#]+)"', text):
        if re.match(r'(https?:|mailto:)', ref): continue
        if not (page.parent / ref).resolve().exists(): errors.append(f'{page.relative_to(root)}: enlace roto {ref}')
    if re.search(r'<script[^>]+src="https?:|<link[^>]+href="https?:', text):
        errors.append(f'{page.relative_to(root)}: carga recursos de terceros (rompería «sin terceros» de la política)')
    if final and (re.search(r'\{\{[A-Z_]+\}\}', text) or '[pendiente' in text or 'example.invalid' in text):
        errors.append(f'{page.relative_to(root)}: quedan datos pendientes')
for need in ['privacidad.html', 'soporte.html', 'condiciones.html', 'aviso-legal.html', 'en/privacy.html', 'en/support.html']:
    if not (root / need).exists(): errors.append(f'falta {need}')
if errors: print('\n'.join('ERROR: ' + e for e in errors)); sys.exit(1)
print(f'Web correcta: {len(pages)} páginas, enlaces y recursos internos verificados.')
