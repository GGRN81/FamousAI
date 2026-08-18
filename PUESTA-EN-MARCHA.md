# Puesta en marcha — de los archivos a la primera factura

Todo está construido. Nada está en línea. Esta guía es la lista de lo que hay que abrir,
configurar y pegar, en orden, para poder cobrar.

**Tiempo total: 6 a 8 horas.** Se puede hacer en dos sábados.
**Costo del arranque: menos de $1,500 MXN**, más lo que ya pagas de IA.

---

## Antes de empezar: la única decisión técnica

Los tres productos se venden desde **tres dominios distintos**, no desde subcarpetas de uno.
Razón: el comprador de Puerto Peñasco no debe aterrizar en una página en español, y el
empresario de Hermosillo no debe ver una página en inglés. Son dos mercados que no se
mezclan.

| Producto | Dominio sugerido | Idioma |
|---|---|---|
| 01 Dictamen IFS | `indicedefragilidad.mx` o `ifs.mx` | español |
| 02 Sonora Closing File | `sonoraclosingfile.com` | inglés |
| 03 Expediente Vivo | subcarpeta del 01, o `expedientevivo.mx` | español |

⚠ Verifica disponibilidad antes de casarte con un nombre. Un `.mx` cuesta alrededor de
$500 al año; un `.com`, unos $250.

---

## Bloque 1 — Cobrar (2 horas) · **hazlo primero**

Sin esto, todo lo demás es decorativo.

### 1.1 Stripe

1. Abre cuenta en `stripe.com` como **persona física con actividad empresarial**. Ten a la mano
   RFC, constancia de situación fiscal, INE y CLABE.
2. La verificación tarda de 1 a 3 días hábiles. **Empieza por aquí y sigue con lo demás
   mientras tanto.**
3. Crea tres **Payment Links** (Productos → Payment Links):

| Nombre del enlace | Precio | Moneda | Notas |
|---|---|---|---|
| Dictamen de Fragilidad Societaria | 6,900 | MXN | activa "cobrar IVA" si tu configuración fiscal lo requiere |
| Sonora Closing File — Pre-Purchase Check | 449 | USD | descripción en inglés |
| Cross-Border Vehicle Blueprint | 1,290 | USD | descripción en inglés |

4. En cada enlace, activa **"Recolectar dirección"** y en el mensaje de confirmación pon:
   *"Recibirás un correo en menos de 2 horas con la lista de documentos."*
5. Para el MVP 03 crea tres **suscripciones** mensuales: $2,900, $4,900 y $7,900, con la
   opción anual como precio alterno.

### 1.2 Mercado Pago como alternativa nacional

Muchos clientes mexicanos prefieren transferencia SPEI. Ten lista una liga de Mercado Pago
para el Dictamen, y la CLABE a la mano. **No pierdas una venta por insistir en tarjeta.**

---

## Bloque 2 — Publicar las páginas (1.5 horas)

### 2.1 Genera las versiones autocontenidas

```bash
./build.sh
```

Produce `dist/` con diez archivos que no dependen de nada externo salvo las tipografías.

### 2.2 Súbelas

La ruta más simple, sin cuenta de desarrollador y sin línea de comandos:

1. Ve a `app.netlify.com/drop`
2. Arrastra la carpeta `dist/`
3. Te da una URL en segundos. Conecta tu dominio en **Site settings → Domain management**.

Sube estos cuatro:

| Archivo de `dist/` | Va en |
|---|---|
| `01-dictamen-ifs__index.html` | la raíz del dominio del IFS |
| `02-sonora-closing-file__index.html` | la raíz de sonoraclosingfile.com |
| `02-sonora-closing-file__checklist-12-puntos.html` | `/checklist` del mismo dominio |
| `03-expediente-vivo__index.html` | acceso privado, solo para clientes |

Renómbralos a `index.html` en cada sitio. **El panel del MVP 03 no se publica abierto:** ponlo
en una URL que no esté enlazada desde ningún lado, o protégela con contraseña (Netlify lo
permite en el plan pagado).

---

## Bloque 3 — Conectar los formularios (1 hora)

Cada página de venta trae un bloque `CONFIG` al inicio de su `<script>`. Es lo único que se
edita.

### 3.1 Endpoint de formulario

Abre cuenta gratuita en **Formspree** (`formspree.io`), crea un formulario, y copia la URL
que te da. Se ve así: `https://formspree.io/f/xxxxxxxx`.

### 3.2 Pega los valores

**En `01-dictamen-ifs/index.html`:**

```js
const CONFIG = {
  precio:      6900,
  ligaPago:    "PEGA AQUÍ LA LIGA DE STRIPE DEL DICTAMEN",
  endpoint:    "PEGA AQUÍ LA URL DE FORMSPREE",
  correo:      "ggr@notaria81.com",
  whatsapp:    "5216624052022",
  guardarLocal:true
};
```

**En `02-sonora-closing-file/index.html`:**

```js
const CONFIG = {
  endpoint: "PEGA AQUÍ LA URL DE FORMSPREE (puede ser otra distinta)",
  email:    "ggr@notaria81.com",
  whatsapp: "5216624052022",
  prices:   { A:449, B:1290, C:249 }
};
```

Si dejas `endpoint` vacío, el formulario abre el correo del usuario en vez de enviarse solo.
**Funciona, pero pierdes leads:** mucha gente no completa el envío. Ponlo.

### 3.3 Vuelve a correr `./build.sh` y sube otra vez

Los archivos de `dist/` se regeneran desde los originales. Edita siempre el original, nunca
el de `dist/`.

---

## Bloque 4 — Correo (1 hora)

### 4.1 Correo transaccional

**MailerLite** o **Brevo** en plan gratuito bastan para los primeros meses.

1. Crea una lista para cada producto.
2. Carga las secuencias:
   - `01-dictamen-ifs/secuencia-correos.md` → 5 correos, día 0, 2, 4, 6, 8
   - `02-sonora-closing-file/email-sequence.md` → 4 correos, día 0, 2, 4, 6
3. Conecta Formspree con la lista vía **Zapier** o **Make** (ambos tienen plan gratuito
   suficiente para este volumen).

### 4.2 El adjunto del primer correo

Abre `01-dictamen-ifs/resultado-ifs.html`, llena los campos con el resultado del prospecto,
imprime a PDF y adjúntalo. **Los primeros veinte se hacen a mano.** Automatizarlo antes de
saber qué preguntan los clientes es tiempo perdido.

---

## Bloque 5 — Antes de cobrarle a nadie (30 minutos)

Esto no es opcional.

- [ ] **Aviso de privacidad publicado** en una URL fija. Llena los `[____]` de
      `comun/aviso-privacidad.md`, conviértelo a página y enlázalo al pie de las tres páginas
      de venta.
- [ ] **Carta de encargo lista para firma.** Llena la plantilla de
      `01-dictamen-ifs/carta-de-encargo.html`, guárdala como PDF y súbela a tu herramienta de
      firma electrónica.
- [ ] **Engagement letter en inglés,** igual, desde
      `02-sonora-closing-file/engagement-letter.html`.
- [ ] **Expediente de identificación.** Define dónde se guarda y quién tiene acceso, conforme
      a `comun/kyc-lfpiorpi.md`.
- [ ] **Cotejar los ⚠.** Los preceptos, montos y plazos marcados en las plantillas, contra
      texto vigente. Es la única tarea de esta lista que no puede delegarse.
- [ ] **Régimen fiscal confirmado con tu contador.** Determina si el factor neto real es 0.82
      o 0.90.

---

## Bloque 6 — Abrir la llave (30 minutos)

1. Programa los nueve posts de `contenido/lote-linkedin.md`. Lunes, miércoles y viernes, tres
   semanas. Llena los `[____]` con tus casos compuestos antes de programar. **Nunca publiques
   un caso con cifras inventadas.**
2. Publica el primero. Ese es el día 9 del plan.
3. Manda la carátula a los seis contactos de tu red. Ese mismo día.
4. Entra a tres grupos de expatriados y contesta una pregunta en cada uno, con las respuestas
   de `02-sonora-closing-file/community-replies.md`. **Sin vender.**

---

## Orden recomendado por sesión

| Sesión | Qué haces | Horas |
|---|---|---|
| Sábado 1 · mañana | Stripe, dominios, Mercado Pago | 2.5 |
| Sábado 1 · tarde | Netlify, formularios, `CONFIG`, subir todo | 2.5 |
| Entre semana | Cotejar los ⚠ · contador · aviso de privacidad | 1.5 |
| Sábado 2 · mañana | Correo, secuencias, cartas de encargo | 1.5 |
| Sábado 2 · tarde | Programar posts, mandar seis carátulas, abrir | 1 |

---

## Lo que NO hay que hacer en el arranque

- Contratar asistente. El modelo dice que en el peor caso previsible el costo fijo es lo que
  te hunde, no las ventas.
- Pagar publicidad. Antes del mes 7 no.
- Comprar herramientas de pago. Todo lo de esta guía tiene plan gratuito suficiente para los
  primeros meses.
- Automatizar la producción de los entregables. Los primeros diez se hacen a mano, porque los
  primeros diez son los que enseñan qué vale la pena automatizar.
- Rediseñar nada. El diseño es el que menos importa hoy.
