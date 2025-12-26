import pandas as pd
import os
import numpy as np


def analizar_archivo1(ruta_archivo):
    """Analizar el primer archivo Excel en detalle"""
    print("\n" + "=" * 60)
    print("ANÁLISIS DETALLADO - ARCHIVO 1")
    print("=" * 60)

    # Cargar archivo con encabezados correctos
    df = pd.read_excel(ruta_archivo, header=4, engine='xlrd')

    print(f"✓ Filas totales: {df.shape[0]}")
    print(f"✓ Columnas totales: {df.shape[1]}")

    # Mostrar nombres de columnas
    print("\nCOLUMNAS IDENTIFICADAS:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")

    # Análisis de valores nulos por columna
    print("\nVALORES NULOS POR COLUMNA:")
    for col in df.columns:
        nulos = df[col].isnull().sum()
        porcentaje = (nulos / len(df)) * 100
        print(f"  {col}: {nulos} nulos ({porcentaje:.1f}%)")

    # Identificar datos duplicados
    duplicados = df.duplicated().sum()
    print(f"\n✓ Registros duplicados completos: {duplicados}")

    # Verificar duplicados en columnas clave
    print("\nVERIFICACIÓN DE DUPLICADOS EN COLUMNAS CLAVE:")
    columnas_clave = ['Nro. RESOLUCIÓN', 'NOMBRE DE LA ORGANIZACIÓN']
    for col in columnas_clave:
        if col in df.columns:
            dups = df[col].duplicated().sum()
            print(f"  {col}: {dups} valores duplicados")

    return df


def analizar_archivo2(ruta_archivo):
    """Analizar el segundo archivo Excel en detalle"""
    print("\n" + "=" * 60)
    print("ANÁLISIS DETALLADO - ARCHIVO 2")
    print("=" * 60)

    # Cargar archivo
    df = pd.read_excel(ruta_archivo)

    print(f"✓ Filas totales: {df.shape[0]}")
    print(f"✓ Columnas totales: {df.shape[1]}")

    # Mostrar nombres de columnas
    print("\nCOLUMNAS IDENTIFICADAS:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")

    # Análisis de valores nulos por columna
    print("\nVALORES NULOS POR COLUMNA:")
    for col in df.columns:
        nulos = df[col].isnull().sum()
        porcentaje = (nulos / len(df)) * 100
        print(f"  {col}: {nulos} nulos ({porcentaje:.1f}%)")

    # Identificar datos duplicados
    duplicados = df.duplicated().sum()
    print(f"\n✓ Registros duplicados completos: {duplicados}")

    # Verificar duplicados en columnas clave
    print("\nVERIFICACIÓN DE DUPLICADOS EN COLUMNAS CLAVE:")
    columnas_clave = ['Nro. RESOLUCIÓN', 'NOMBRE DE LA ORGANIZACIÓN']
    for col in columnas_clave:
        if col in df.columns:
            dups = df[col].duplicated().sum()
            print(f"  {col}: {dups} valores duplicados")

    return df


def comparar_archivos(df1, df2):
    """Comparar características entre los dos archivos"""
    print("\n" + "=" * 60)
    print("COMPARACIÓN ENTRE ARCHIVOS")
    print("=" * 60)

    # Verificar columnas comunes
    columnas_comunes = set(df1.columns) & set(df2.columns)
    print(f"✓ Columnas comunes: {len(columnas_comunes)}")
    if columnas_comunes:
        print("  Columnas:", ", ".join(columnas_comunes))

    # Verificar organizaciones en común
    if 'NOMBRE DE LA ORGANIZACIÓN' in df1.columns and 'NOMBRE DE LA ORGANIZACIÓN' in df2.columns:
        org1 = set(df1['NOMBRE DE LA ORGANIZACIÓN'].dropna().unique())
        org2 = set(df2['NOMBRE DE LA ORGANIZACIÓN'].dropna().unique())
        comunes = org1 & org2
        print(f"\n✓ Organizaciones en común: {len(comunes)}")
        print(f"  Solo en Archivo 1: {len(org1 - org2)}")
        print(f"  Solo en Archivo 2: {len(org2 - org1)}")


def generar_reporte_inconsistencias(df1, df2):
    """Generar reporte de inconsistencias identificadas"""
    print("\n" + "=" * 60)
    print("REPORTE DE INCONSISTENCIAS IDENTIFICADAS")
    print("=" * 60)

    inconsistencias = []

    # 1. Valores nulos críticos
    print("\n1. VALORES NULOS CRÍTICOS:")
    for df, nombre in [(df1, "Archivo 1"), (df2, "Archivo 2")]:
        if 'NOMBRE DE LA ORGANIZACIÓN' in df.columns:
            nulos = df['NOMBRE DE LA ORGANIZACIÓN'].isnull().sum()
            if nulos > 0:
                print(f"  ❌ {nombre}: {nulos} registros sin nombre de organización")
                inconsistencias.append(f"{nombre}: {nulos} registros sin nombre de organización")

    # 2. Datos duplicados problemáticos
    print("\n2. DATOS DUPLICADOS PROBLEMÁTICOS:")
    for df, nombre in [(df1, "Archivo 1"), (df2, "Archivo 2")]:
        if 'Nro. RESOLUCIÓN' in df.columns:
            dups = df['Nro. RESOLUCIÓN'].duplicated().sum()
            if dups > 0:
                print(f"  ⚠️  {nombre}: {dups} números de resolución duplicados")
                inconsistencias.append(f"{nombre}: {dups} números de resolución duplicados")

    # 3. Campos con alta tasa de nulos
    print("\n3. CAMPOS CON ALTA TASA DE VALORES NULOS (>20%):")
    for df, nombre in [(df1, "Archivo 1"), (df2, "Archivo 2")]:
        for col in df.columns:
            tasa_nulos = (df[col].isnull().sum() / len(df)) * 100
            if tasa_nulos > 20:
                print(f"  ⚠️  {nombre} - {col}: {tasa_nulos:.1f}% nulos")
                inconsistencias.append(f"{nombre} - {col}: {tasa_nulos:.1f}% nulos")

    return inconsistencias


def main():
    print("DIAGNÓSTICO DETALLADO DE REGISTROS ADMINISTRATIVOS - SGDPN")
    print("Objetivo: Identificar inconsistencias, datos duplicados y vacíos de datos")
    print("-" * 80)

    # Configurar rutas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proyecto_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(proyecto_dir, "data")

    # Verificar existencia de archivos
    archivo1 = os.path.join(data_dir, "matriz_datos_abiertos_septiembre_final.xls")
    archivo2 = os.path.join(data_dir,
                            "2022-2025_RESOLUCIONES COMUNAS, COMUNIDADES, ORGANIZACIONES DE PUEBLOS Y NACIONALIDADES (1).xlsx")

    if not os.path.exists(archivo1) or not os.path.exists(archivo2):
        print("Error: No se encuentran los archivos necesarios en la carpeta 'data'")
        return

    # Analizar archivo 1
    df1 = analizar_archivo1(archivo1)

    # Analizar archivo 2
    df2 = analizar_archivo2(archivo2)

    # Comparar archivos
    comparar_archivos(df1, df2)

    # Generar reporte de inconsistencias
    inconsistencias = generar_reporte_inconsistencias(df1, df2)

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    print(f"✓ Total de registros analizados: {len(df1) + len(df2)}")
    print(f"✓ Total de organizaciones únicas identificadas: Por calcular en siguiente paso")
    print(f"✓ Inconsistencias críticas identificadas: {len(inconsistencias)}")


    # Guardar diagnóstico en archivo
    output_path = os.path.join(data_dir, "diagnostico_resultados.txt")
    with open(output_path, 'w') as f:
        f.write("DIAGNÓSTICO COMPLETADO\n")
        f.write(f"Inconsistencias identificadas: {len(inconsistencias)}\n")
        for inc in inconsistencias:
            f.write(f"- {inc}\n")

    print(f"\n✓ Reporte guardado en: {output_path}")
    print("\n✅ DIAGNÓSTICO COMPLETADO")


if __name__ == "__main__":
    main()