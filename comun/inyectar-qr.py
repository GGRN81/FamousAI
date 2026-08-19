# -*- coding: utf-8 -*-
"""
Inserta el bloque de identidad con QR en cada documento. Es idempotente:
correrlo dos veces no duplica nada.

    python3 comun/generar-qr.py && python3 comun/inyectar-qr.py

Clasificación, y la distinción no es cosmética:

  NOMINATIVO  lleva QR de contacto y QR de pago. Son documentos que se
              entregan a un cliente identificado y bajo encargo firmado.
  PÚBLICO     lleva solo QR de contacto. Cualquiera puede verlo o descargarlo,
              así que no lleva datos bancarios.
"""
import io, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCA = "<!-- bloque-qr -->"

NOMINATIVOS = {
 "01-dictamen-ifs/dictamen-plantilla.html",
 "01-dictamen-ifs/carta-de-encargo.html",
 "02-sonora-closing-file/report-template.html",
 "02-sonora-closing-file/blueprint-template.html",
 "02-sonora-closing-file/engagement-letter.html",
 "03-expediente-vivo/caratula-personalidad.html",
 "03-expediente-vivo/propuesta-honorarios.html",
 "03-expediente-vivo/reporte-mensual.html",
}
PUBLICOS = {
 "index.html",
 "mvps/index.html",
 "mvps/planes-de-negocio.html",
 "mvps/memo-socio.html",
 "01-dictamen-ifs/index.html",
 "01-dictamen-ifs/resultado-ifs.html",
 "02-sonora-closing-file/index.html",
 "02-sonora-closing-file/checklist-12-puntos.html",
 "03-expediente-vivo/index.html",
}
INGLES = {"02-sonora-closing-file/index.html","02-sonora-closing-file/checklist-12-puntos.html",
          "02-sonora-closing-file/report-template.html","02-sonora-closing-file/blueprint-template.html",
          "02-sonora-closing-file/engagement-letter.html"}

T = {
 "es": dict(nombre="Lic. Gilberto Gutiérrez Rodríguez",
            cargo="Abogado corporativo y notarial · Cédula profesional 9396385",
            dir="Torre Hermosillo, Piso 11 · Blvd. Kino 309 · Hermosillo, Sonora",
            hint="Escanea para guardar el contacto",
            pago_t="Datos de pago", hint_pago="Escanea para transferir",
            pago_1="Honorarios profesionales · BANREGIO · CLABE 058760000148957666",
            pago_2="Notaría 81 · GTZ NOTARIOS, SC · BBVA · CLABE 012760001255657234",
            aviso="Verifique el nombre del beneficiario antes de transferir."),
 "en": dict(nombre="Gilberto Gutiérrez Rodríguez", 
            cargo="Corporate &amp; notarial attorney · Mexican license 9396385",
            dir="Torre Hermosillo, 11th floor · Blvd. Kino 309 · Hermosillo, Sonora, Mexico",
            hint="Scan to save the contact",
            pago_t="Payment details", hint_pago="Scan to transfer",
            pago_1="Professional fees · BANREGIO · CLABE 058760000148957666",
            pago_2="Notaría 81 · GTZ NOTARIOS, SC · BBVA · CLABE 012760001255657234",
            aviso="Confirm the beneficiary name before transferring."),
}

def leer(n):
    return io.open(os.path.join(RAIZ,"comun","qr",n), encoding="utf-8").read().strip()

def bloque(rel, con_pago):
    t = T["en" if rel in INGLES else "es"]
    qc = leer("qr-contacto.svg")
    html = [MARCA, '<div class="qrblock">',
        '  <div class="qrone">',
        f'    <div class="qrsvg" aria-label="Código QR con los datos de contacto">{qc}</div>',
        '    <div class="qrtxt">',
        f'      <b>{t["nombre"]}</b>',
        f'      <span>{t["cargo"]}</span>',
        '      <span>+52 662 405 2022 · ggr@notaria81.com</span>',
        f'      <span>{t["dir"]}</span>',
        f'      <span class="qrhint">{t["hint"]}</span>',
        '    </div>', '  </div>']
    if con_pago:
        qp = leer("qr-pago.svg")
        html += ['  <div class="qrone">',
            f'    <div class="qrsvg grande" aria-label="Código QR con los datos de pago">{qp}</div>',
            '    <div class="qrtxt">',
            f'      <b>{t["pago_t"]}</b>',
            f'      <span>{t["pago_1"]}</span>',
            f'      <span>{t["pago_2"]}</span>',
            f'      <span>{t["aviso"]}</span>',
            f'      <span class="qrhint">{t["hint_pago"]}</span>',
            '    </div>', '  </div>']
    html += ['</div>']
    return "\n".join(html)

def limpiar(s):
    return re.sub(re.escape(MARCA) + r'.*?</div>\s*(?=</footer>|<div class="foot">|</div>\s*</body>)',
                  '', s, flags=re.S)

def insertar(rel):
    ruta = os.path.join(RAIZ, rel)
    s = io.open(ruta, encoding="utf-8").read()
    if MARCA in s:                      # idempotencia: quita el bloque previo
        i = s.index(MARCA)
        j = s.index('</div>', s.rindex('</div>', i, s.index('\n', s.index('qrblock'))) ) if False else None
        s = re.sub(re.escape(MARCA) + r'\n<div class="qrblock">.*?\n</div>\n', '', s, flags=re.S)
    b = bloque(rel, rel in NOMINATIVOS)
    if 'class="doc"' in s:
        # documento impreso: va en la última página, antes de su pie
        idx = s.rfind('<div class="foot">')
        if idx == -1: return False
        s = s[:idx] + b + "\n  " + s[idx:]
    else:
        idx = s.rfind('</footer>')
        if idx == -1: return False
        cierre = s.rfind('</div>', 0, idx)
        s = s[:cierre] + "\n    " + b + "\n  " + s[cierre:]
    io.open(ruta, "w", encoding="utf-8").write(s)
    return True

if __name__ == "__main__":
    n = 0
    for rel in sorted(NOMINATIVOS | PUBLICOS):
        tipo = "nominativo" if rel in NOMINATIVOS else "público   "
        ok = insertar(rel)
        print(f"  {'OK ' if ok else '** '} {tipo}  {rel}")
        n += ok
    print(f"\n{n} de {len(NOMINATIVOS|PUBLICOS)} documentos con bloque de identidad")
