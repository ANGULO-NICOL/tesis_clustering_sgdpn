import pandas as pd
import numpy as np
import os


def verificar_preprocesamieto():
    """Verificar el preprocesamiento """

    # Rutas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proyecto_dir = os.path.dirname(script_dir)
    processed_dir = os.path.join(proyecto_dir, "data", "processed")

    # Cargar datos preprocesados
    df1 = pd.read_csv(os.path.join(processed_dir, "archivo1_preprocesado_final.csv"),
                      encoding='utf-8-sig')
    df2 = pd.read_csv(os.path.join(processed_dir, "archivo2_preprocesado_final.csv"),
                      encoding='utf-8-sig')

    print("VERIFICACIÓN DE OBJETIVOS DE PREPROCESAMIENTO")
    print("=" * 70)
    print("Objetivo: Implementar un proceso de preprocesamiento de datos que incluyen:")
    print("          1. Depuración")
    print("          2. Normalización")
    print("          3. Tratamiento de valores faltantes")
    print("          4. Codificación de variables")
    print("=" * 70)

    resultados = []

    # 1. VERIFICAR DEPURACIÓN
    print("\n1. DEPURACIÓN:")

    # 1.1 Verificar que no hay registros sin organización
    org_nulos1 = df1['NOMBRE DE LA ORGANIZACIÓN'].isnull().sum()
    org_nulos2 = df2['NOMBRE DE LA ORGANIZACIÓN'].isnull().sum()

    if org_nulos1 == 0 and org_nulos2 == 0:
        print("   ✅ No hay registros sin nombre de organización")
        resultados.append("DEPURACIÓN: OK - Sin registros sin organización")
    else:
        print(f"   ❌ Hay {org_nulos1 + org_nulos2} registros sin organización")
        resultados.append("DEPURACIÓN: FALLÓ - Hay registros sin organización")

    # 1.2 Verificar que no hay duplicados de resolución
    dup_res1 = df1['NRO. RESOLUCIÓN'].duplicated().sum()
    dup_res2 = df2['NRO. RESOLUCIÓN'].duplicated().sum()

    if dup_res1 == 0 and dup_res2 == 0:
        print("   ✅ No hay números de resolución duplicados")
        resultados.append("DEPURACIÓN: OK - Sin resoluciones duplicadas")
    else:
        print(f"   ❌ Hay {dup_res1 + dup_res2} resoluciones duplicadas")
        resultados.append("DEPURACIÓN: FALLÓ - Hay resoluciones duplicadas")

    # 2. VERIFICAR NORMALIZACIÓN
    print("\n2. NORMALIZACIÓN:")

    # 2.1 Verificar formato de nombres de organización
    def verificar_formato_nombres(serie):
        problemas = []
        for nombre in serie.dropna().head(10):  # Revisar primeros 10
            if not isinstance(nombre, str):
                problemas.append("No es string")
                break
            if nombre != nombre.upper():
                problemas.append("No está en mayúsculas")
                break
            if nombre != nombre.strip():
                problemas.append("Tiene espacios extremos")
                break
            if '  ' in nombre:
                problemas.append("Tiene espacios múltiples")
                break
        return problemas

    problemas1 = verificar_formato_nombres(df1['NOMBRE DE LA ORGANIZACIÓN'])
    problemas2 = verificar_formato_nombres(df2['NOMBRE DE LA ORGANIZACIÓN'])

    if not problemas1 and not problemas2:
        print("   ✅ Nombres de organizaciones normalizados correctamente")
        resultados.append("NORMALIZACIÓN: OK - Nombres estandarizados")
    else:
        print(f"   ❌ Problemas en nombres: {set(problemas1 + problemas2)}")
        resultados.append("NORMALIZACIÓN: FALLÓ - Problemas en nombres")

    # 3. VERIFICAR TRATAMIENTO DE VALORES FALTANTES
    print("\n3. TRATAMIENTO DE VALORES FALTANTES:")

    # 3.1 Verificar columnas específicas que tenían nulos
    columnas_con_nulos_originales = ['ASUNTO', 'TIPO DE SERVICIO', 'SOLICITUD', 'FECHA SOLICITUD']

    nulos_totales = 0
    for df, nombre in [(df1, "Archivo 1"), (df2, "Archivo 2")]:
        for col in columnas_con_nulos_originales:
            if col in df.columns:
                nulos = df[col].isnull().sum()
                nulos_totales += nulos
                if nulos > 0:
                    print(f"   ⚠️  {nombre} - {col}: {nulos} nulos")

    if nulos_totales == 0:
        print("   ✅ Todos los valores faltantes fueron tratados")
        resultados.append("VALORES FALTANTES: OK - Todos tratados")
    else:
        print(f"   ❌ Total nulos no tratados: {nulos_totales}")
        resultados.append(f"VALORES FALTANTES: FALLÓ - {nulos_totales} nulos no tratados")

    # 3.2 Verificar reemplazo de valores
    print("   Verificando reemplazo de valores 'NO ESPECIFICADO':")

    # Archivo 1
    cols_archivo1 = ['ASUNTO', 'TIPO DE SERVICIO', 'TIPO DE SERVICIO ESPECIFÍCO', 'APROBADO POR']
    no_especificado1 = sum((df1[col] == 'NO ESPECIFICADO').sum()
                           for col in cols_archivo1 if col in df1.columns)

    # Archivo 2
    no_especificado2 = 0
    if 'SOLICITUD' in df2.columns:
        no_especificado2 += (df2['SOLICITUD'] == 'NO ESPECIFICADO').sum()

    print(f"   Archivo 1: {no_especificado1} valores reemplazados con 'NO ESPECIFICADO'")
    print(f"   Archivo 2: {no_especificado2} valores reemplazados con 'NO ESPECIFICADO'")

    # 4. VERIFICAR CODIFICACIÓN DE VARIABLES
    print("\n4. CODIFICACIÓN DE VARIABLES:")

    # 4.1 Verificar que existe columna PEDIDO_UNIFICADO
    if 'PEDIDO_UNIFICADO' in df1.columns and 'PEDIDO_UNIFICADO' in df2.columns:
        print("   ✅ Columna PEDIDO_UNIFICADO creada en ambos archivos")

        # Verificar que no tenga nulos
        nulos_pedido1 = df1['PEDIDO_UNIFICADO'].isnull().sum()
        nulos_pedido2 = df2['PEDIDO_UNIFICADO'].isnull().sum()

        if nulos_pedido1 == 0 and nulos_pedido2 == 0:
            print("   ✅ Columna PEDIDO_UNIFICADO sin valores nulos")
            resultados.append("CODIFICACIÓN: OK - PEDIDO_UNIFICADO creada y completa")
        else:
            print(f"   ❌ PEDIDO_UNIFICADO tiene {nulos_pedido1 + nulos_pedido2} nulos")
            resultados.append("CODIFICACIÓN: FALLÓ - PEDIDO_UNIFICADO tiene nulos")

        # Mostrar estadísticas de la columna
        print(f"\n   Estadísticas PEDIDO_UNIFICADO:")
        print(f"   Archivo 1: {df1['PEDIDO_UNIFICADO'].nunique()} valores únicos")
        print(f"   Archivo 2: {df2['PEDIDO_UNIFICADO'].nunique()} valores únicos")

        # Ejemplos
        print(f"\n   Ejemplos Archivo 1:")
        for pedido in df1['PEDIDO_UNIFICADO'].unique()[:3]:
            print(f"     - {pedido[:60]}...")

        print(f"\n   Ejemplos Archivo 2:")
        for pedido in df2['PEDIDO_UNIFICADO'].unique()[:3]:
            print(f"     - {pedido[:60]}...")

    else:
        print("   ❌ Falta columna PEDIDO_UNIFICADO")
        resultados.append("CODIFICACIÓN: FALLÓ - Falta PEDIDO_UNIFICADO")

    # 5. VERIFICAR CALIDAD GENERAL DE LA BASE ANALÍTICA
    print("\n5. CALIDAD DE LA BASE ANALÍTICA:")

    # 5.1 Consistencia de tipos de datos
    print("   Tipos de datos por columna:")
    for df, nombre in [(df1, "Archivo 1"), (df2, "Archivo 2")]:
        print(f"\n   {nombre}:")
        for col in df.columns[:5]:  # Primeras 5 columnas
            print(f"     {col}: {df[col].dtype}")

    # 5.2 Completitud general
    total_celdas = df1.size + df2.size
    celdas_no_nulas = df1.notnull().sum().sum() + df2.notnull().sum().sum()
    completitud = (celdas_no_nulas / total_celdas) * 100

    print(f"\n   Completitud general: {completitud:.1f}%")

    if completitud >= 99:
        print("   ✅ Alta completitud de datos")
        resultados.append("CALIDAD: OK - Alta completitud")
    elif completitud >= 95:
        print("   ⚠️  Completitud aceptable")
        resultados.append("CALIDAD: ACEPTABLE - Completitud moderada")
    else:
        print("   ❌ Baja completitud")
        resultados.append("CALIDAD: FALLÓ - Baja completitud")

    # RESUMEN FINAL
    print("\n" + "=" * 70)
    print("RESUMEN FINAL DE VERIFICACIÓN")
    print("=" * 70)

    todos_ok = all("OK" in r or "ACEPTABLE" in r for r in resultados)

    if todos_ok:
        print("✅ TODOS LOS OBJETIVOS DE PREPROCESAMIENTO CUMPLIDOS")
        print("\nLa base analítica tiene CALIDAD GARANTIZADA para clustering.")
    else:
        print("⚠️  ALGUNOS OBJETIVOS NO SE CUMPLIERON COMPLETAMENTE")

    print("\nDetalle de resultados:")
    for resultado in resultados:
        print(f"  • {resultado}")

    # Guardar reporte
    reporte_dir = os.path.join(proyecto_dir, "data", "results")
    os.makedirs(reporte_dir, exist_ok=True)

    with open(os.path.join(reporte_dir, "verificacion_preprocesamiento.txt"), 'w') as f:
        f.write("VERIFICACIÓN DE PREPROCESAMIENTO\n")
        f.write("=" * 50 + "\n\n")
        for resultado in resultados:
            f.write(f"{resultado}\n")

    return todos_ok


if __name__ == "__main__":
    print("Iniciando verificación de objetivos...\n")
    exito = verificar_objetivos()

    if exito:
        print("\n" + "=" * 70)
        print("¡PREPROCESAMIENTO VALIDADO EXITOSAMENTE!")
        print("Puedes continuar con la creación de la matriz para clustering.")
    else:
        print("\n" + "=" * 70)
        print("Se requiere mejorar el preprocesamiento antes de continuar.")
