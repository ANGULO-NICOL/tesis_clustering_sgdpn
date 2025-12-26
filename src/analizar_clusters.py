import pandas as pd
import os


def analizar_caracteristicas_clusters():
    """Analizar características demográficas/geográficas de cada cluster"""

    print("ANÁLISIS DE CARACTERÍSTICAS POR CLUSTER")
    print("=" * 70)

    # Cargar resultados del clustering
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proyecto_dir = os.path.dirname(script_dir)
    clusters_path = os.path.join(proyecto_dir, "data", "results", "comunidades_clusters.csv")

    if not os.path.exists(clusters_path):
        print("❌ Primero ejecuta clustering_comunidades.py")
        return

    clusters_df = pd.read_csv(clusters_path, index_col=0, encoding='utf-8-sig')

    # Cargar datos originales para obtener provincia/información adicional
    processed_dir = os.path.join(proyecto_dir, "data", "processed")
    archivo1 = os.path.join(processed_dir, "archivo1_preprocesado_final.csv")
    archivo2 = os.path.join(processed_dir, "archivo2_preprocesado_final.csv")

    df1 = pd.read_csv(archivo1, encoding='utf-8-sig')
    df2 = pd.read_csv(archivo2, encoding='utf-8-sig')

    # Crear diccionario de comunidad -> información
    print("\n1. EXTRACCIÓN DE INFORMACIÓN ADICIONAL...")

    info_comunidades = {}

    # Del archivo 1 (no tiene provincia)
    for _, row in df1.iterrows():
        comunidad = row['NOMBRE DE LA ORGANIZACIÓN']
        if comunidad not in info_comunidades:
            info_comunidades[comunidad] = {'archivo': 'Archivo 1'}

    # Del archivo 2 (tiene provincia)
    if 'PROVINCIA' in df2.columns:
        for _, row in df2.iterrows():
            comunidad = row['NOMBRE DE LA ORGANIZACIÓN']
            provincia = row['PROVINCIA']
            if comunidad not in info_comunidades:
                info_comunidades[comunidad] = {'archivo': 'Archivo 2', 'provincia': provincia}
            elif 'provincia' not in info_comunidades[comunidad]:
                info_comunidades[comunidad]['provincia'] = provincia

    print(f"   Información extraída para {len(info_comunidades)} comunidades")

    # 2. ANALIZAR CLUSTERS
    print("\n2. ANÁLISIS POR CLUSTER:")

    n_clusters = clusters_df['CLUSTER'].nunique()

    analisis_completo = []

    for cluster_id in range(n_clusters):
        comunidades_cluster = clusters_df[clusters_df['CLUSTER'] == cluster_id].index

        print(f"\n   CLUSTER {cluster_id} ({len(comunidades_cluster)} comunidades):")

        # Información de archivos
        archivos = []
        provincias = []

        for comunidad in comunidades_cluster:
            if comunidad in info_comunidades:
                info = info_comunidades[comunidad]
                archivos.append(info.get('archivo', 'Desconocido'))
                if 'provincia' in info:
                    provincias.append(info['provincia'])

        # Estadísticas
        if archivos:
            archivo1_count = archivos.count('Archivo 1')
            archivo2_count = archivos.count('Archivo 2')
            print(f"   - Del Archivo 1: {archivo1_count} ({archivo1_count / len(archivos) * 100:.0f}%)")
            print(f"   - Del Archivo 2: {archivo2_count} ({archivo2_count / len(archivos) * 100:.0f}%)")

        if provincias:
            provincia_counts = pd.Series(provincias).value_counts()
            if len(provincia_counts) > 0:
                print(f"   - Provincia más común: {provincia_counts.index[0]} ({provincia_counts.iloc[0]})")

        # Pedidos del cluster
        pedidos_cluster = clusters_df.loc[comunidades_cluster].drop('CLUSTER', axis=1)
        pedidos_frecuentes = pedidos_cluster.sum().sort_values(ascending=False)

        print(f"   - Pedidos principales:")
        for i, (pedido, count) in enumerate(pedidos_frecuentes.head(2).items(), 1):
            porcentaje = count / len(comunidades_cluster) * 100
            print(f"     {i}. {pedido[:30]}... ({porcentaje:.0f}% del cluster)")

        # Guardar análisis
        cluster_info = {
            'cluster': cluster_id,
            'n_comunidades': len(comunidades_cluster),
            'pedido_principal': pedidos_frecuentes.index[0] if len(pedidos_frecuentes) > 0 else 'N/A',
            'frecuencia_principal': pedidos_frecuentes.iloc[0] if len(pedidos_frecuentes) > 0 else 0
        }

        if provincias:
            cluster_info['provincia_comun'] = pd.Series(provincias).mode()[0]
            cluster_info['n_provincias'] = len(set(provincias))

        analisis_completo.append(cluster_info)

    # 3. IDENTIFICAR PATRONES
    print("\n3. PATRONES IDENTIFICADOS:")

    # Crear DataFrame de análisis
    analisis_df = pd.DataFrame(analisis_completo)

    # Agrupar por tipo de pedido principal
    print("\n   Agrupación por tipo de trámite:")

    tipos_pedidos = {
        'PERSONERIA': 'Legalización',
        'REGISTRO DE DIRECTIVA': 'Gestión interna',
        'INCLUSIÓN': 'Membresía',
        'INCLUSION': 'Membresía',
        'REFORMA': 'Actualización',
        'EXCLUSIÓN': 'Membresía',
        'EXCLUSION': 'Membresía'
    }

    for _, row in analisis_df.iterrows():
        pedido = str(row['pedido_principal']).upper()
        tipo = 'Otros'

        for key, value in tipos_pedidos.items():
            if key in pedido:
                tipo = value
                break

        print(f"   Cluster {row['cluster']}: {tipo} ({row['n_comunidades']} comunidades)")

    # 4. RESUMEN EJECUTIVO
    print("\n4. RESUMEN EJECUTIVO:")

    total_comunidades = analisis_df['n_comunidades'].sum()
    print(f"   Total comunidades analizadas: {total_comunidades}")
    print(f"   Total clusters identificados: {len(analisis_df)}")

    # Distribución por tipo de trámite
    tipo_counts = {}
    for _, row in analisis_df.iterrows():
        pedido = str(row['pedido_principal']).upper()
        tipo = 'Otros'

        for key, value in tipos_pedidos.items():
            if key in pedido:
                tipo = value
                break

        tipo_counts[tipo] = tipo_counts.get(tipo, 0) + row['n_comunidades']

    print(f"\n   Distribución por tipo de trámite:")
    for tipo, count in tipo_counts.items():
        print(f"   - {tipo}: {count} comunidades ({count / total_comunidades * 100:.0f}%)")

    # 5. GUARDAR ANÁLISIS
    print("\n5. GUARDANDO ANÁLISIS...")

    results_dir = os.path.join(proyecto_dir, "data", "results")

    # Guardar análisis detallado
    analisis_path = os.path.join(results_dir, "analisis_caracteristicas_clusters.csv")
    analisis_df.to_csv(analisis_path, encoding='utf-8-sig')

    # Guardar resumen ejecutivo
    resumen_path = os.path.join(results_dir, "resumen_analisis_clusters.txt")
    with open(resumen_path, 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS DE CARACTERÍSTICAS DE CLUSTERS\n")
        f.write("=" * 50 + "\n\n")

        f.write("RESUMEN EJECUTIVO:\n")
        f.write(f"- Total clusters: {len(analisis_df)}\n")
        f.write(f"- Total comunidades: {total_comunidades}\n")
        f.write(
            f"- Comunidades con información de provincia: {sum('provincia_comun' in row for row in analisis_completo)}\n\n")

        f.write("DISTRIBUCIÓN POR TIPO DE TRÁMITE:\n")
        for tipo, count in tipo_counts.items():
            f.write(f"- {tipo}: {count} comunidades ({count / total_comunidades * 100:.0f}%)\n")

        f.write("\nDETALLE POR CLUSTER:\n")
        for info in analisis_completo:
            f.write(f"\nCluster {info['cluster']}:\n")
            f.write(f"  Comunidades: {info['n_comunidades']}\n")
            f.write(f"  Pedido principal: {info['pedido_principal'][:50]}...\n")
            f.write(f"  Frecuencia: {info['frecuencia_principal']}/{info['n_comunidades']}\n")
            if 'provincia_comun' in info:
                f.write(f"  Provincia común: {info['provincia_comun']}\n")

    print(f"   Análisis guardado en: {analisis_path}")
    print(f"   Resumen guardado en: {resumen_path}")

    print("\n" + "=" * 70)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    analizar_caracteristicas_clusters()