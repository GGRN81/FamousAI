# Modelo financiero — cómo se calcularon las cifras

Todo lo que aparece en `mvps/planes-de-negocio.html` sale de una sola hoja de cálculo mental
con cinco supuestos. Aquí quedan escritos para que puedas cambiarlos y rehacer los números.

## Supuestos

| Variable | Valor | Nota |
|---|---|---|
| Tipo de cambio | 18.50 MXN/USD | ⚠ verificar al fijar precio |
| ISR efectivo | 10 % | ⚠ conservador. RESICO PF sería ~2.5% |
| Comisión de cobro MXN | 3.6 % + $3 | Stripe / Mercado Pago |
| Comisión de cobro USD | 5.1 % + $3 | Stripe internacional, incluye conversión |
| Reserva de reproceso | 3 % | solo productos transaccionales |
| Horas disponibles | 12 / semana = 52 / mes | el recurso escaso |

El IVA no entra en ningún cálculo: se traslada y se entera. Todos los precios son sin IVA.

## Fórmula del neto por unidad

```
neto = precio − (precio × comisión + 3) − costo_IA − (precio × 3% si es transaccional) − (precio × ISR)
```

## Costo de IA por entregable

| Entregable | Costo |
|---|---|
| Dictamen (16 páginas) | $60 |
| Closing File A (11 páginas) | $80 |
| Vehículo B | $140 |
| Sucesorio C | $40 |
| Cuenta de suscripción / mes | $25 a $70 según plan |

## Costos fijos mensuales

| Fase | Monto | Qué incluye |
|---|---|---|
| Meses 1–6 | $2,800 | 3 dominios, formularios, correo transaccional, suscripción de IA |
| Meses 7+ | $6,800 | agrega pauta en inglés ($4,000) |
| Con asistente | $15,800 | agrega 20 h/semana ($9,000) |

**Regla:** ningún costo fijo se contrata antes de que el producto que va a pagarlo lo esté
pagando durante tres meses seguidos.

## Tiempo por unidad

| Entregable | Minutos |
|---|---|
| Dictamen | 70 producción + 15 admin |
| Closing File A | 80 + 20 de llamada |
| Vehículo B | 240 |
| Cuenta Vigilancia | 25 / mes |
| Cuenta Grupo | 45 / mes |
| Cuenta Corredor | 70 / mes |

## Los tres escenarios

| Escenario | Supuesto de tráfico | Cruza la meta | Neto/sem mes 12 |
|---|---|---|---|
| Optimista | 1,500 visitas/mes al mes 6, conversiones diseñadas | mes 3 | $30,947 |
| **Plan de trabajo** | **la mitad de ese tráfico** | **mes 5** | **$21,476** |
| Ácido | el contenido no despega; solo la red | — | $7,437 |

**El hallazgo del escenario ácido:** con costo fijo de $15,800 llega a 74% de la meta; con
costo fijo de $2,800 y exactamente las mismas ventas llega a 104%. La diferencia entre cumplir
y no cumplir en el peor caso está del lado del gasto, no del ingreso.

## Valor de vida

| Producto | LTV | Cómo se compone |
|---|---|---|
| 01 Dictamen | $57,360 | $6,900 + 30%×(suscripción 18 meses) + 30%×(estructuración $80,000) |
| 02 Closing File | $13,038 | A + 25%×C + 15%×B. No incluye el valor del agente referidor |
| 03 Suscripción | $122,500 | churn 4%/mes → 25 meses × $4,900. A 6% de churn: $81,667 |

## Para rehacer los números

El script que produjo todas las tablas está en `contenido/modelo-financiero.py`. Cambia las
constantes del inicio y vuelve a correrlo:

```bash
python3 contenido/modelo-financiero.py
```
