# Tres MVPs digitales — GGR

Tres productos digitales **construidos**, no descritos: página de venta funcionando, plantilla
del entregable lista para imprimir a PDF, prompt maestro que la produce, intake, secuencia de
correos y contenido que genera el tráfico.

Meta de diseño: **$10,000 MXN netos por semana** (≈ $12,800 brutos, factor neto 0.78–0.82).
Los tres venden diagnóstico, estructuración y vigilancia documental.

| # | Producto | Tipo | Precio | Primer cobro |
|---|----------|------|--------|--------------|
| 01 | Dictamen de Fragilidad Societaria | Transaccional, MXN | $6,900 | día 9 |
| 02 | Sonora Closing File | Transaccional, USD | $449 / $1,290 / $249 | día 20 |
| 03 | Expediente Corporativo Vivo | Suscripción | $2,900 – $7,900 / mes | mes 4 |

## Empezar

Abre **`index.html`** con doble clic. Es el catálogo: desde ahí se llega a los 31 archivos.
Nada requiere servidor, instalación ni conexión salvo Google Fonts.

Para ponerlo en línea y poder cobrar: **`PUESTA-EN-MARCHA.md`**. Seis a ocho horas, dos
sábados, menos de $1,500 MXN de arranque.

## Estructura

```
index.html                     catálogo de todo
mvps/index.html                el documento de estrategia: aritmética, embudos, plan de 14 días
comun/ggr.css                  colores, tipografía y estilos de impresión — el único lugar que editas
comun/*.md                     alcance y limitaciones · aviso de privacidad · expediente de identificación
contenido/lote-linkedin.md     9 posts, tres semanas, alimenta los embudos 01 y 02

PUESTA-EN-MARCHA.md            de los archivos a la primera factura
mvps/planes-de-negocio.html    economía unitaria, lógica de precio, capacidad, rampa a 12 meses
contenido/modelo-financiero.py el script que produjo cada cifra

01-dictamen-ifs/
  index.html                   página de venta + autodiagnóstico funcional (14 preguntas, 7 factores)
  dictamen-plantilla.html      el entregable, 16 páginas imprimibles
  carta-de-encargo.html        se firma antes de empezar, 1 página
  resultado-ifs.html           el PDF que se adjunta al primer correo, 1 página
  prompt-maestro.md            de cuatro documentos a borrador en 50 minutos
  intake.md                    qué se le pide al cliente al cobrar
  secuencia-correos.md         5 correos, los primeros tres no venden

02-sonora-closing-file/
  index.html                   página de venta en inglés + formulario de pedido
  checklist-12-puntos.html     el imán de captura, 2 páginas
  report-template.html         el entregable del SKU A, 11 páginas
  blueprint-template.html      el entregable del SKU B ($1,290 USD), 8 páginas, con diagramas
  engagement-letter.html       se firma antes de empezar, 1 página
  master-prompt.md             incluye la regla de registro y la prohibición de inflar hallazgos
  intake.md · email-sequence.md · community-replies.md

03-expediente-vivo/
  index.html                   panel funcional: edita, guarda solo, exporta, imprime
  caratula-personalidad.html   la función estrella, 4 páginas, ES/EN
  reporte-mensual.html         la prueba de valor mensual, 3 páginas
  propuesta-honorarios.html    propuesta de suscripción, 4 páginas
  contrato-suscripcion.md · guion-venta.md
```

## Editar

- **Marca:** tokens al inicio de `comun/ggr.css`. Cambian los ocho documentos a la vez.
- **Precios, ligas de pago, correo, WhatsApp:** bloque `CONFIG` al inicio del `<script>` de
  cada página de venta.
- **Datos por llenar:** todo `[____]`. En las plantillas van resaltados, con un contador arriba
  y un botón para ocultar el resaltado antes de imprimir.

## Publicar

```bash
./build.sh      # genera dist/ con páginas autocontenidas para subir a cualquier hosting
```

## Antes del primer cliente

Todo lo marcado **⚠** requiere cotejo contra texto vigente. En particular: montos y plazos del
art. 32-B Ter y 84-M del CFF; el plazo de asamblea anual de la LGSM; la mecánica de retención
en la enajenación por residente en el extranjero; y el alcance del art. 17 fr. XI de la
LFPIORPI para los servicios de estructuración.

Ningún caso de los materiales de contenido está lleno: los casos son compuestos, con cifras
desviadas y rezago mínimo de 18 meses. Nunca se publica un caso identificable.
