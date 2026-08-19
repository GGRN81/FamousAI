# -*- coding: utf-8 -*-
"""
Genera los códigos QR de GGR como SVG en línea, sin depender de ningún servicio externo.

    pip install segno
    python3 comun/generar-qr.py

Produce dos QR con propósitos distintos, y la distinción importa:

  qr-contacto.svg  vCard. Va en TODO, incluido lo público. Sin datos bancarios.
  qr-pago.svg      Instrucciones de pago. Va SOLO en documentos nominativos —
                   carta de encargo, propuesta, dictamen, reporte— nunca en una
                   página abierta ni en un imán de captura.

NO se incluye el número de tarjeta. Una tarjeta es una credencial, no una
dirección de cobro: quien la lee puede intentar cargos sin presencia física.
Una CLABE, en cambio, solo puede recibir. Si aun así quieres incluirla,
cambia INCLUIR_TARJETA a True y vuelve a correr — pero entonces el QR de pago
no debe salir de un documento entregado en mano a un cliente identificado.
"""
import segno, io, os, re

INCLUIR_TARJETA = False

CONTACTO = dict(
    nombre="Gilberto", apellidos="Gutiérrez Rodríguez", prefijo="Lic.",
    titulo="Abogado corporativo y notarial",
    cedula="9396385",
    tel="+526624052022", tel_legible="+52 662 405 2022",
    email="ggr@notaria81.com",
    calle="Blvd. Kino 309, Torre Hermosillo, Piso 11, Col. Country Club",
    ciudad="Hermosillo", estado="Sonora", pais="México",
)

PAGO_PERSONAL = dict(titular="GILBERTO GUTIERREZ RODRIGUEZ", banco="BANREGIO",
                     cuenta="850896380013", clabe="058760000148957666",
                     tarjeta="4741743510443477")
PAGO_NOTARIA  = dict(titular="GTZ NOTARIOS, SC", banco="BBVA BANCOMER",
                     cuenta="0125565723", clabe="012760001255657234")

def vcard():
    c = CONTACTO
    return "\r\n".join([
        "BEGIN:VCARD","VERSION:3.0",
        f"N:{c['apellidos']};{c['nombre']};;{c['prefijo']};",
        f"FN:{c['prefijo']} {c['nombre']} {c['apellidos']}",
        f"TITLE:{c['titulo']}",
        f"NOTE:Cédula profesional {c['cedula']}",
        f"TEL;TYPE=CELL,VOICE:{c['tel']}",
        f"EMAIL;TYPE=WORK,INTERNET:{c['email']}",
        f"ADR;TYPE=WORK:;;{c['calle']};{c['ciudad']};{c['estado']};;{c['pais']}",
        "END:VCARD"])

def texto_pago():
    p, n = PAGO_PERSONAL, PAGO_NOTARIA
    l = [f"PAGO — {CONTACTO['prefijo']} {CONTACTO['nombre']} {CONTACTO['apellidos']}",
         f"Cédula profesional {CONTACTO['cedula']}",
         f"{CONTACTO['tel_legible']} · {CONTACTO['email']}", "",
         "HONORARIOS PROFESIONALES",
         f"Titular: {p['titular']}", f"Banco: {p['banco']}",
         f"Cuenta: {p['cuenta']}", f"CLABE: {p['clabe']}"]
    if INCLUIR_TARJETA:
        l.append(f"Tarjeta: {p['tarjeta']}")
    l += ["", "DERECHOS Y HONORARIOS NOTARIALES",
          f"Beneficiario: {n['titular']}", f"Banco: {n['banco']}",
          f"Cuenta: {n['cuenta']}", f"CLABE: {n['clabe']}", "",
          "Verifique el nombre del beneficiario antes de transferir."]
    return "\n".join(l)

def clabe_valida(c):
    if len(c) != 18 or not c.isdigit(): return False
    pesos = [3, 7, 1] * 6
    s = sum((int(c[i]) * pesos[i]) % 10 for i in range(17))
    return (10 - s % 10) % 10 == int(c[17])

def svg(datos, ruta, escala=1):
    # UTF-8 forzado: sin esto segno codifica los acentos en latin-1 y los
    # lectores que asumen UTF-8 —entre ellos la cámara de varios teléfonos—
    # no decodifican el símbolo. Verificado: sin este parámetro el vCard no lee.
    q = segno.make(datos, error="m", encoding="utf-8")
    buf = io.BytesIO()
    q.save(buf, kind="svg", scale=escala, border=2, svgclass=None, lineclass=None,
           xmldecl=False, svgns=True, omitsize=True, dark="#000000")
    s = buf.getvalue().decode("utf-8")
    # tamaño gobernado por CSS y color heredado del texto: legible en claro y en oscuro
    for hex_ in ('#000000', '#000'):
        s = s.replace(f'stroke="{hex_}"', 'stroke="currentColor"')
        s = s.replace(f'fill="{hex_}"', 'fill="currentColor"')
    s = s.replace("<svg ", '<svg role="img" ', 1)
    io.open(ruta, "w", encoding="utf-8").write(s)
    return q.symbol_size(scale=1, border=2)[0], len(datos)

if __name__ == "__main__":
    for etiqueta, c in [("personal", PAGO_PERSONAL["clabe"]), ("notaría", PAGO_NOTARIA["clabe"])]:
        assert clabe_valida(c), f"CLABE {etiqueta} inválida: {c}"
    print("CLABEs verificadas · dígito de control correcto en ambas")

    os.makedirs(os.path.join(os.path.dirname(__file__), "qr"), exist_ok=True)
    base = os.path.join(os.path.dirname(__file__), "qr")
    m1, n1 = svg(vcard(), os.path.join(base, "qr-contacto.svg"))
    m2, n2 = svg(texto_pago(), os.path.join(base, "qr-pago.svg"))
    print(f"qr-contacto.svg  {m1}x{m1} módulos · {n1} caracteres · vCard")
    print(f"qr-pago.svg      {m2}x{m2} módulos · {n2} caracteres · "
          f"{'CON' if INCLUIR_TARJETA else 'SIN'} número de tarjeta")
    if m2 > 57:
        print("  aviso: el QR de pago pasa de la versión 10; imprímelo a 30 mm o más")
