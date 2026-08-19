# -*- coding: utf-8 -*-
"""
Convierte el DENUE del INEGI en la lista de prospección del MVP 01 y del MVP 03.

    python3 datos/construir-lista.py <ruta-al-csv-del-denue>

El DENUE es información pública del INEGI. Los correos que publica son de
contacto del establecimiento. Aun así, en el primer contacto va el aviso de
privacidad y la vía para oponerse: un correo con nombre de persona física
—juan.perez@— sí es dato personal, aunque venga de una fuente pública.
"""
import csv, collections, io, re, sys, os

COLS=["id","clee","nom_estab","raz_social","codigo_act","nombre_act","per_ocu","tipo_vial","nom_vial",
"tipo_v_e_1","nom_v_e_1","tipo_v_e_2","nom_v_e_2","tipo_v_e_3","nom_v_e_3","numero_ext","letra_ext",
"edificio","edificio_e","numero_int","letra_int","tipo_asent","nomb_asent","tipoCenCom","nom_CenCom",
"num_local","cod_postal","cve_ent","entidad","cve_mun","municipio","cve_loc","localidad","ageb",
"manzana","telefono","correoelec","www","tipoUniEco","latitud","longitud","fecha_alta","extra"]
SZ={"0 a 5 personas":1,"6 a 10 personas":2,"11 a 30 personas":3,"31 a 50 personas":4,
    "51 a 100 personas":5,"101 a 250 personas":6,"251 y más personas":7}
ETQ={3:"11-30",4:"31-50",5:"51-100",6:"101-250",7:"251+"}
SEC={"11":"Agro","21":"Minería","22":"Energía y agua","23":"Construcción","31":"Manufactura",
 "32":"Manufactura","33":"Manufactura","43":"Comercio mayoreo","46":"Comercio menudeo",
 "48":"Transportes","49":"Transportes","51":"Información","52":"Financieros","53":"Inmobiliario",
 "54":"Serv. profesionales","55":"Corporativos","56":"Apoyo a negocios","61":"Educación","62":"Salud",
 "71":"Esparcimiento","72":"Hospedaje y alimentos","81":"Otros servicios","93":"Gobierno"}
GOB=re.compile(r'SECRETARIA|GOBIERNO|MUNICIPIO|INSTITUTO MEXICANO DEL SEGURO|ISSSTE|COMISION (FEDERAL|NACIONAL|ESTATAL)|SERVICIOS DE SALUD|AGUA DE HERMOSILLO|UNIVERSIDAD DE SONORA|COLEGIO DE BACHILLERES|CONALEP|DIF |PROCURADURIA|FISCALIA|PODER JUDICIAL|CONGRESO|AYUNTAMIENTO|SISTEMA PARA EL DESARROLLO|CENTRO DE CONCILIACION|TELECOMUNICACIONES DE MEXICO|CORREOS DE MEXICO|PETROLEOS MEXICANOS|BANCO DEL BIENESTAR|SERVICIOS EDUCATIVOS|SERVICIO POSTAL MEXICANO|COMISION ESTATAL|JUNTA (LOCAL|ESPECIAL)|TRIBUNAL|INSTITUTO (ESTATAL|SONORENSE|NACIONAL|TECNOLOGICO)|CENTRO DE READAPTACION|CRUZ ROJA')
CADENA=re.compile(r'COPPEL|OXXO|7-ELEVEN|SEVEN|FARMACIA(S)? (GUADALAJARA|BENAVIDES|DEL AHORRO|SIMILARES)|FARMACIA DE SIMILARES|CASA LEY|SORIANA|WAL[- ]?MART|CHEDRAUI|BANCO|BANCOMER|BANORTE|SANTANDER|HSBC|SCOTIABANK|CITIBANAMEX|BBVA|AZTECA|ELEKTRA|TELEFONIA POR CABLE|TELEFONOS DE MEXICO|RADIO ?MOVIL|AT&T|SEARS|LIVERPOOL|SUBURBIA|HOME DEPOT|OFFICE DEPOT|CINEPOLIS|CINEMEX|DOMINOS|BURGER|MCDONALD|STARBUCKS|ALSEA|BIMBO|LALA|COCA|PEPSI|FEMSA|MODELO|HEINEKEN|CEMEX|HOLCIM|GRUPO MEXICO|AUTOZONE|SAMS|BODEGA AURRERA|WALDOS|DEL SOL|VIPS|TOKS|COMERCIALIZADORA FARMACEUTICA')

def norm(s):
    s=s.upper().strip(); s=re.sub(r'[^A-ZÑÁÉÍÓÚ0-9 ]',' ',s)
    s=re.sub(r'\b(SA DE CV|S A DE C V|SAPI DE CV|S DE RL DE CV|S DE R L DE C V|SC|S C|AC|A C|SAS|SA|SAPI|SRL)\b','',s)
    return re.sub(r'\s+',' ',s).strip()

def main(ruta):
    rows=[]
    with io.open(ruta, encoding="latin-1", newline="") as f:
        for row in csv.reader(f):
            rows.append(dict(zip(COLS,(row+[""]*len(COLS))[:len(COLS)])))
    emp=collections.defaultdict(list)
    for r in rows:
        if r["raz_social"].strip() and SZ.get(r["per_ocu"].strip(),0)>=3:
            emp[norm(r["raz_social"])].append(r)
    salida=[]
    for k,v in emp.items():
        if GOB.search(k) or CADENA.search(k) or v[0]["codigo_act"][:2]=="93": continue
        tam=max(SZ.get(r["per_ocu"].strip(),0) for r in v)
        correo=next((r["correoelec"].strip() for r in v if r["correoelec"].strip()),"")
        tel   =next((r["telefono"].strip()    for r in v if r["telefono"].strip()),"")
        web   =next((r["www"].strip()         for r in v if r["www"].strip()),"")
        sector=SEC.get(v[0]["codigo_act"][:2],"Otro")
        # prioridad: tamaño, ser grupo, y contactabilidad
        p = (tam-2)*10 + (min(len(v),5))*6 + (8 if correo else 0) + (3 if tel else 0)
        salida.append(dict(
            prioridad=p, razon_social=v[0]["raz_social"].strip(), establecimientos=len(v),
            tamano=ETQ.get(tam,""), sector=sector, actividad=v[0]["nombre_act"][:70],
            correo=correo, telefono=tel, web=web,
            colonia=v[0]["nomb_asent"].strip(), cp=v[0]["cod_postal"].strip(),
            producto="03 Expediente Vivo" if len(v)>=2 else "01 Dictamen IFS",
            multiunidad="sí" if (len(v)>=2 and SEC.get(v[0]["codigo_act"][:2],"") in
                        ("Hospedaje y alimentos","Comercio menudeo","Salud","Transportes",
                         "Otros servicios","Esparcimiento")) else "no",
            correo_nominal="sí" if re.match(r'^[a-z]+[._][a-z]+@', correo.lower()) else "no"))
    salida.sort(key=lambda x:-x["prioridad"])
    os.makedirs("datos", exist_ok=True)
    campos=["prioridad","producto","multiunidad","razon_social","establecimientos","tamano","sector",
            "actividad","correo","correo_nominal","telefono","web","colonia","cp"]
    with io.open("datos/lista-prospeccion-hermosillo.csv","w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f, fieldnames=campos); w.writeheader()
        for r in salida: w.writerow({k:r[k] for k in campos})
    con=[r for r in salida if r["correo"]]
    print(f"empresas objetivo            {len(salida):>6,}")
    print(f"  con correo                 {len(con):>6,}")
    print(f"  candidatas al MVP 03       {sum(1 for r in salida if r['establecimientos']>=2):>6,}")
    print(f"    operador multiunidad     {sum(1 for r in salida if r['multiunidad']=='sí'):>6,}  ← el perfil objetivo")
    print(f"  correo con nombre de persona {sum(1 for r in con if r['correo_nominal']=='sí'):>4,}  ← aviso de privacidad obligatorio")
    print(f"\nprimeras 50 por prioridad: {sum(1 for r in salida[:50] if r['correo']):,} traen correo")
    print("archivo: datos/lista-prospeccion-hermosillo.csv")

if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else
         "/root/.claude/uploads/0e5548da-1a65-5053-bc8e-c1ca794d45dc/b4b8126e-denue_inegi_26___rev_ggr__HMO_1.csv")
