import pandas as pd
import os
import re


def preprocesamiento_completo():
    """Preprocesamiento completo de los datos"""

    # Rutas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proyecto_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(proyecto_dir, "data")
    processed_dir = os.path.join(proyecto_dir, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    # Archivos originales
    archivo1 = os.path.join(data_dir, "matriz_datos_abiertos_septiembre_final.xls")
    archivo2 = os.path.join(data_dir,
                            "2022-2025_RESOLUCIONES COMUNAS, COMUNIDADES, ORGANIZACIONES DE PUEBLOS Y NACIONALIDADES (1).xlsx")

    print("1. CARGANDO DATOS...")
    df1 = pd.read_excel(archivo1, header=4, engine='xlrd')
    df2 = pd.read_excel(archivo2)
    print(f"   Archivo 1: {df1.shape}")
    print(f"   Archivo 2: {df2.shape}")

    # Limpiar nombres de columnas
    print("\n2. NORMALIZANDO NOMBRES DE COLUMNAS...")
    df1.columns = [str(col).strip().upper() for col in df1.columns]
    df2.columns = [str(col).strip().upper() for col in df2.columns]

    # 1. DEPURACIÓN
    print("\n3. DEPURACIÓN...")

    # Eliminar registros sin organización
    inicial1 = len(df1)
    inicial2 = len(df2)

    df1 = df1.dropna(subset=['NOMBRE DE LA ORGANIZACIÓN'])
    df2 = df2.dropna(subset=['NOMBRE DE LA ORGANIZACIÓN'])

    print(f"   Registros eliminados (sin organización):")
    print(f"   Archivo 1: {inicial1 - len(df1)}")
    print(f"   Archivo 2: {inicial2 - len(df2)}")

    # Eliminar duplicados de resolución
    df1 = df1.drop_duplicates(subset=['NRO. RESOLUCIÓN'], keep='first')
    df2 = df2.drop_duplicates(subset=['NRO. RESOLUCIÓN'], keep='first')

    print(f"   Duplicados de resolución eliminados")

    # 2. NORMALIZACIÓN
    print("\n4. NORMALIZACIÓN...")

    # Normalizar nombres de organizaciones
    def normalizar_nombre(nombre):
        if pd.isna(nombre):
            return nombre
        nombre = str(nombre).upper().strip()
        nombre = re.sub(r'\s+', ' ', nombre)
        return nombre

    df1['NOMBRE DE LA ORGANIZACIÓN'] = df1['NOMBRE DE LA ORGANIZACIÓN'].apply(normalizar_nombre)
    df2['NOMBRE DE LA ORGANIZACIÓN'] = df2['NOMBRE DE LA ORGANIZACIÓN'].apply(normalizar_nombre)
    print("   Nombres de organizaciones normalizados")

    # 3. TRATAMIENTO DE VALORES FALTANTES
    print("\n5. TRATAMIENTO DE VALORES FALTANTES...")

    # Archivo 1
    columnas1 = ['ASUNTO', 'TIPO DE SERVICIO', 'TIPO DE SERVICIO ESPECIFÍCO', 'APROBADO POR']
    for col in columnas1:
        if col in df1.columns:
            df1[col] = df1[col].fillna('NO ESPECIFICADO')

    # Archivo 2
    if 'SOLICITUD' in df2.columns:
        df2['SOLICITUD'] = df2['SOLICITUD'].fillna('NO ESPECIFICADO')

    if 'FECHA SOLICITUD' in df2.columns:
        df2['FECHA SOLICITUD'] = df2['FECHA SOLICITUD'].fillna('FECHA NO ESPECIFICADA')

    print("   Valores faltantes tratados")

    # 4. CODIFICACIÓN DE VARIABLES
    print("\n6. CODIFICACIÓN DE VARIABLES...")

    # Crear columna PEDIDO_UNIFICADO
    # Para Archivo 1
    if all(col in df1.columns for col in ['ASUNTO', 'TIPO DE SERVICIO', 'TIPO DE SERVICIO ESPECIFÍCO']):
        df1['PEDIDO_UNIFICADO'] = df1['ASUNTO'].astype(str) + " | " + \
                                  df1['TIPO DE SERVICIO'].astype(str)
        print("   Archivo 1: PEDIDO_UNIFICADO creado (ASUNTO + TIPO DE SERVICIO)")

    # Para Archivo 2
    if 'SOLICITUD' in df2.columns:
        df2['PEDIDO_UNIFICADO'] = df2['SOLICITUD'].astype(str)
        print("   Archivo 2: PEDIDO_UNIFICADO creado (SOLICITUD)")

    # 7. VERIFICACIÓN FINAL
    print("\n7. VERIFICACIÓN FINAL...")

    # Contar nulos en columnas críticas
    columnas_criticas = ['NOMBRE DE LA ORGANIZACIÓN', 'NRO. RESOLUCIÓN', 'PEDIDO_UNIFICADO']

    print("\n   Nulos en columnas críticas:")
    for df, nombre in [(df1, "Archivo 1"), (df2, "Archivo 2")]:
        print(f"\n   {nombre}:")
        for col in columnas_criticas:
            if col in df.columns:
                nulos = df[col].isnull().sum()
                if nulos == 0:
                    print(f"     ✅ {col}: 0 nulos")
                else:
                    print(f"     ❌ {col}: {nulos} nulos")

    # 8. GUARDAR DATOS PREPROCESADOS
    print("\n8. GUARDANDO DATOS PREPROCESADOS...")

    archivo1_proc = os.path.join(processed_dir, "archivo1_preprocesado_final.csv")
    archivo2_proc = os.path.join(processed_dir, "archivo2_preprocesado_final.csv")

    df1.to_csv(archivo1_proc, index=False, encoding='utf-8-sig')
    df2.to_csv(archivo2_proc, index=False, encoding='utf-8-sig')

    print(f"   Archivo 1 guardado: {archivo1_proc}")
    print(f"   Archivo 2 guardado: {archivo2_proc}")

    # 9. RESUMEN
    print("\n" + "=" * 60)
    print("RESUMEN DEL PREPROCESAMIENTO")
    print("=" * 60)

    print(f"\nArchivo 1 final: {df1.shape}")
    print(f"Archivo 2 final: {df2.shape}")

    # Verificar que no haya nulos en columnas críticas
    nulos_criticos = 0
    for df in [df1, df2]:
        for col in columnas_criticas:
            if col in df.columns:
                nulos_criticos += df[col].isnull().sum()

    if nulos_criticos == 0:
        print("\n✅ PREPROCESAMIENTO COMPLETADO EXITOSAMENTE")
        print("   No hay nulos en columnas críticas")
        print("   Los datos están listos para clustering")
    else:
        print(f"\n⚠️  Aún hay {nulos_criticos} nulos en columnas críticas")

    return df1, df2


if __name__ == "__main__":
    print("INICIANDO PREPROCESAMIENTO COMPLETO")
    print("=" * 60)
    print("Objetivo: Depuración, Normalización, Tratamiento de")
    print("          valores faltantes y Codificación de variables")
    print("=" * 60)

    df1_final, df2_final = preprocesamiento_completo()