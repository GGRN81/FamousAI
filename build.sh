#!/usr/bin/env bash
# Genera dist/ con versiones autocontenidas: la hoja común queda incrustada
# en cada página, así cada archivo funciona solo — subido a cualquier hosting,
# mandado por correo o abierto con doble clic.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p dist
python3 - <<'PY'
import io, os, re, glob
css = io.open('comun/ggr.css', encoding='utf-8').read()
paginas = []
for carpeta in ('01-dictamen-ifs','02-sonora-closing-file','03-expediente-vivo','mvps'):
    paginas += sorted(glob.glob(os.path.join(carpeta,'*.html')))
os.makedirs('dist', exist_ok=True)
for p in paginas:
    s = io.open(p, encoding='utf-8').read()
    s = s.replace('<link rel="stylesheet" href="../comun/ggr.css">',
                  '<style>\n/* comun/ggr.css incrustado por build.sh */\n' + css + '\n</style>')
    destino = os.path.join('dist', os.path.basename(os.path.dirname(p)) + '__' + os.path.basename(p))
    io.open(destino, 'w', encoding='utf-8').write(s)
    print('%-58s %6.1f KB' % (destino, len(s.encode('utf-8'))/1024))
PY
echo
echo "Listo. dist/ contiene páginas autocontenidas (solo Google Fonts es externo)."
