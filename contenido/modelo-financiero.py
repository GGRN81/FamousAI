# -*- coding: utf-8 -*-
FX = 18.50          # MXN/USD  ⚠ verificar
ISR = 0.10          # efectivo conservador (RESICO PF sería ~2.5%)
COM_MXN = 0.036     # Stripe/MP nacional
COM_USD = 0.051     # Stripe internacional + conversión
RESERVA = 0.03      # reproceso / reembolso (solo transaccionales)

def unidad(precio_mxn, com, ia, reserva=True, isr=ISR):
    c_com = precio_mxn*com + 3
    c_ia  = ia
    c_res = precio_mxn*RESERVA if reserva else 0
    contrib = precio_mxn - c_com - c_ia - c_res
    c_isr = precio_mxn*isr
    neto = contrib - c_isr
    return dict(precio=precio_mxn, com=c_com, ia=c_ia, res=c_res,
                contrib=contrib, isr=c_isr, neto=neto, factor=neto/precio_mxn)

print("═══ ECONOMÍA UNITARIA ═══")
u = {}
u['dictamen'] = unidad(6900, COM_MXN, 60)
u['scf_A']    = unidad(449*FX, COM_USD, 80)
u['scf_B']    = unidad(1290*FX, COM_USD, 140)
u['scf_C']    = unidad(249*FX, COM_USD, 40)
u['sus_vig']  = unidad(2900, COM_MXN, 25, reserva=False)
u['sus_gru']  = unidad(4900, COM_MXN, 45, reserva=False)
u['sus_cor']  = unidad(7900, COM_MXN, 70, reserva=False)
for k,v in u.items():
    print(f"{k:10} precio {v['precio']:9,.0f}  com {v['com']:7,.0f}  ia {v['ia']:5,.0f}  res {v['res']:7,.0f}  "
          f"contrib {v['contrib']:9,.0f}  isr {v['isr']:7,.0f}  NETO {v['neto']:9,.0f}  factor {v['factor']:.3f}")

print()
print("═══ RAMPA BASE · 12 MESES (mes 1 = lanzamiento) ═══")
# 01 — traccionado por tráfico de LinkedIn
visitas = [250,450,700,900,1100,1300,1400,1500,1500,1600,1600,1600]
dicts   = [1,2,4,6,8,10,11,12,12,12,12,12]
# 02 — estacional: temporada de compra en la costa oct–abr (mes 3 = octubre)
scfA    = [0,1,2,3,3,4,5,5,4,2,2,2]
scfB    = [0,0,0,1,0,1,0,1,1,0,1,0]
scfC    = [0,0,1,1,1,2,2,2,2,1,1,1]
# 03 — traccionado por red propia, no por tráfico
cuentas = [0,1,3,5,7,9,11,13,14,15,16,17]
# mezcla de planes conforme madura la cartera
def mix(n, mes):
    if n==0: return 0,0,0
    cor = min(n//6, 3)                    # plan corredor
    gru = min((n-cor)//2 + (1 if mes>6 else 0), n-cor)
    vig = n-cor-gru
    return vig,gru,cor

fijos = [2800]*3 + [6800]*3 + [15800]*6   # + pauta desde mes 4, + asistente desde mes 7
META_BRUTO = 55500

filas=[]
acum_neto = 0
for i in range(12):
    m=i+1
    b01 = dicts[i]*6900
    b02 = scfA[i]*449*FX + scfB[i]*1290*FX + scfC[i]*249*FX
    v,g,c = mix(cuentas[i], m)
    b03 = v*2900 + g*4900 + c*7900
    bruto = b01+b02+b03
    n01 = dicts[i]*u['dictamen']['neto']
    n02 = scfA[i]*u['scf_A']['neto'] + scfB[i]*u['scf_B']['neto'] + scfC[i]*u['scf_C']['neto']
    n03 = v*u['sus_vig']['neto'] + g*u['sus_gru']['neto'] + c*u['sus_cor']['neto']
    neto = n01+n02+n03-fijos[i]
    acum_neto += neto
    horas = dicts[i]*1.4 + (scfA[i]+scfC[i])*2.0 + scfB[i]*4.0 + v*0.42 + g*0.75 + c*1.17
    filas.append((m,dicts[i],scfA[i]+scfB[i]+scfC[i],cuentas[i],b01,b02,b03,bruto,neto,neto/4.33,horas,acum_neto))

print(f"{'M':>2} {'dic':>4} {'scf':>4} {'cta':>4} {'01':>9} {'02':>9} {'03':>9} {'BRUTO':>10} {'NETO':>9} {'/sem':>8} {'hrs':>6} {'acum':>10}")
for f in filas:
    marca = " ←META" if f[9]>=10000 else ""
    print(f"{f[0]:>2} {f[1]:>4} {f[2]:>4} {f[3]:>4} {f[4]:>9,.0f} {f[5]:>9,.0f} {f[6]:>9,.0f} {f[7]:>10,.0f} {f[8]:>9,.0f} {f[9]:>8,.0f} {f[10]:>6.1f} {f[11]:>10,.0f}{marca}")

print()
print("═══ ESCENARIO CONSERVADOR (mitad de tráfico en 01 y 02; red rinde igual) ═══")
dicts_c   = [1,1,2,3,4,5,5,6,6,6,6,6]
scfA_c    = [0,0,1,1,2,2,2,3,2,1,1,1]
cuentas_c = [0,1,2,4,6,7,9,10,11,12,13,14]
acum=0
print(f"{'M':>2} {'BRUTO':>10} {'NETO':>9} {'/sem':>8} {'acum':>10}")
for i in range(12):
    b01=dicts_c[i]*6900; b02=scfA_c[i]*449*FX
    v,g,c=mix(cuentas_c[i], i+1); b03=v*2900+g*4900+c*7900
    n = dicts_c[i]*u['dictamen']['neto'] + scfA_c[i]*u['scf_A']['neto'] \
        + v*u['sus_vig']['neto']+g*u['sus_gru']['neto']+c*u['sus_cor']['neto'] - fijos[i]
    acum+=n
    print(f"{i+1:>2} {b01+b02+b03:>10,.0f} {n:>9,.0f} {n/4.33:>8,.0f} {acum:>10,.0f}")

print()
print("═══ PUNTO DE EQUILIBRIO Y TECHO ═══")
for nombre,fijo in [("mes 1-3",2800),("mes 4-6",6800),("mes 7+",15800)]:
    print(f"{nombre}: fijo {fijo:,} → equilibrio = {fijo/u['dictamen']['neto']:.2f} dictámenes/mes"
          f" · o {fijo/u['sus_gru']['neto']:.2f} cuentas Grupo")
HORAS = 52  # 12 h/semana
print(f"\nCon {HORAS} h/mes disponibles:")
print(f"  solo dictámenes: {HORAS/1.4:.0f}/mes = ${HORAS/1.4*6900:,.0f} bruto")
print(f"  solo closing files: {HORAS/2.0:.0f}/mes = ${HORAS/2.0*449*FX:,.0f} bruto")
print(f"  solo suscripciones Grupo: {HORAS/0.75:.0f} cuentas = ${HORAS/0.75*4900:,.0f}/mes")
print(f"  mezcla del mes 12 (base): {filas[11][10]:.1f} h de {HORAS} → {filas[11][10]/HORAS*100:.0f}% de capacidad")

print()
print("═══ LTV ═══")
ltv01 = 6900 + 0.30*(4900*18) + 0.30*80000
print(f"01 Dictamen: 6,900 + 30%×(susc 18m ${4900*18:,}) + 30%×(estructuración $80,000) = ${ltv01:,.0f}")
ltv02 = 449*FX + 0.25*249*FX + 0.15*1290*FX
print(f"02 Closing File: A + 25%×C + 15%×B = ${ltv02:,.0f}  (más el agente referidor: 2/año × N años)")
for churn,label in [(0.04,'4%'),(0.06,'6%')]:
    print(f"03 Suscripción, churn {label}/mes → vida {1/churn:.0f} meses × $4,900 = ${4900/churn:,.0f}")

print()
print("═══ ESCENARIO ÁCIDO · el contenido no despega; solo funciona la red ═══")
# 01: la conversión se queda en un tercio de lo diseñado
dicts_a   = [0,1,1,2,2,2,2,3,3,3,3,3]
# 02: uno al mes solo en temporada (meses 3-9), cero fuera
scfA_a    = [0,0,1,1,1,1,1,1,1,0,0,0]
# 03: solo su red conocida; 8 cuentas en el año, ninguna llega por contenido
cuentas_a = [0,1,2,3,4,5,6,6,7,7,8,8]
acum=0; peor=None
print(f"{'M':>2} {'dic':>4} {'scf':>4} {'cta':>4} {'BRUTO':>10} {'NETO':>9} {'/sem':>8} {'acum':>10}")
for i in range(12):
    b01=dicts_a[i]*6900; b02=scfA_a[i]*449*FX
    v,g,c=mix(cuentas_a[i], i+1); b03=v*2900+g*4900+c*7900
    n = dicts_a[i]*u['dictamen']['neto'] + scfA_a[i]*u['scf_A']['neto'] \
        + v*u['sus_vig']['neto']+g*u['sus_gru']['neto']+c*u['sus_cor']['neto'] - fijos[i]
    acum+=n
    print(f"{i+1:>2} {dicts_a[i]:>4} {scfA_a[i]:>4} {cuentas_a[i]:>4} {b01+b02+b03:>10,.0f} {n:>9,.0f} {n/4.33:>8,.0f} {acum:>10,.0f}")
    peor=(n/4.33)
print(f"→ mes 12 ácido: ${peor:,.0f}/semana neto = {peor/10000*100:.0f}% de la meta")
print("→ nota: el fijo del mes 7+ ($15,800 con asistente y pauta) NO se justifica en este escenario;")
print(f"   sin asistente ni pauta el neto del mes 12 sería ${peor + (15800-2800)/4.33:,.0f}/semana = {(peor+(15800-2800)/4.33)/10000*100:.0f}% de la meta")

print()
print("═══ CUÁNTAS UNIDADES PARA LA META, POR PRODUCTO EN SOLITARIO ═══")
META_NETO_MES = 43333
for k,label,fijo in [('dictamen','Dictamen $6,900',2800),('scf_A','Closing File $449 USD',2800),
                     ('sus_gru','Suscripción Grupo $4,900',2800)]:
    n = (META_NETO_MES+fijo)/u[k]['neto']
    print(f"{label:28} → {n:5.1f} al mes  ({n/4.33:.1f} por semana)" if k!='sus_gru'
          else f"{label:28} → {n:5.1f} cuentas activas")

print()
print("═══ ESCALERA DE PRECIO · 01 ═══")
for p in [4900, 6900, 8900, 12900]:
    uu = unidad(p, COM_MXN, 60)
    print(f"${p:>6,}  neto/unidad ${uu['neto']:>8,.0f}  → unidades para meta: {(META_NETO_MES+2800)/uu['neto']:>5.1f}/mes"
          f"  = {(META_NETO_MES+2800)/uu['neto']*1.4:>5.1f} h/mes")
print()
print("═══ ESCALERA DE PRECIO · 02 (USD) ═══")
for p in [299, 449, 649, 899]:
    uu = unidad(p*FX, COM_USD, 80)
    print(f"${p:>4} USD (${p*FX:>7,.0f} MXN)  neto ${uu['neto']:>8,.0f}  → unidades para meta: {(META_NETO_MES+2800)/uu['neto']:>5.1f}/mes"
          f"  = {(META_NETO_MES+2800)/uu['neto']*2.0:>5.1f} h/mes")
