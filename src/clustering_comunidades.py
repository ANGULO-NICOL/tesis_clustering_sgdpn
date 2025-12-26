import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def clustering_comunidades():
    """Realizar clustering solo con comunidades que tienen múltiples pedidos"""

    print("CLUSTERING DE COMUNIDADES CON MÚLTIPLES PEDIDOS")
    print("=" * 70)

    # Cargar matriz
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proyecto_dir = os.path.dirname(script_dir)
    matriz_path = os.path.join(proyecto_dir, "data", "results", "matriz_clustering_final.csv")

    matriz = pd.read_csv(matriz_path, index_col=0, encoding='utf-8-sig')

    # 1. FILTRAR: Solo comunidades con 2+ pedidos
    print("\n1. FILTRANDO COMUNIDADES...")
    pedidos_por_comunidad = matriz.sum(axis=1)
    comunidades_multiples = pedidos_por_comunidad[pedidos_por_comunidad >= 2]

    matriz_filtrada = matriz.loc[comunidades_multiples.index]

    print(f"   Total comunidades: {matriz.shape[0]}")
    print(f"   Comunidades con 2+ pedidos: {matriz_filtrada.shape[0]}")
    print(f"   Pedidos únicos: {matriz_filtrada.shape[1]}")

    # 2. PREPARAR DATOS PARA CLUSTERING
    print("\n2. PREPARANDO DATOS...")
    X = matriz_filtrada.values

    # 3. PROBAR DIFERENTES NÚMEROS DE CLUSTERS
    print("\n3. BUSCANDO MEJOR NÚMERO DE CLUSTERS...")

    inertias = []
    silhouette_scores = []
    ks = range(2, 11)

    for k in ks:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)

        inertias.append(kmeans.inertia_)

        if k > 1:
            labels = kmeans.labels_
            if len(np.unique(labels)) > 1:
                score = silhouette_score(X, labels)
                silhouette_scores.append(score)
            else:
                silhouette_scores.append(0)

    # Mostrar resultados
    print(f"\n   Resultados por número de clusters:")
    for i, k in enumerate(ks):
        print(f"   K={k}: Inercia={inertias[i]:.0f}, Silhouette={silhouette_scores[i]:.3f}")

    # Encontrar mejor K
    mejor_k_idx = np.argmax(silhouette_scores)
    mejor_k = ks[mejor_k_idx]

    print(f"\n   MEJOR K encontrado: {mejor_k} clusters")
    print(f"   Score Silhouette: {silhouette_scores[mejor_k_idx]:.3f}")

    # 4. APLICAR K-MEANS CON EL MEJOR K
    print(f"\n4. APLICANDO K-MEANS CON {mejor_k} CLUSTERS...")
    kmeans_final = KMeans(n_clusters=mejor_k, random_state=42, n_init=10)
    cluster_labels = kmeans_final.fit_predict(X)

    # Agregar labels a la matriz
    matriz_resultados = matriz_filtrada.copy()
    matriz_resultados['CLUSTER'] = cluster_labels

    # 5. ANALIZAR LOS CLUSTERS
    print(f"\n5. ANÁLISIS DE LOS {mejor_k} CLUSTERS:")

    clusters_info = []

    for cluster_id in range(mejor_k):
        comunidades_cluster = matriz_resultados[matriz_resultados['CLUSTER'] == cluster_id]

        pedidos_cluster = comunidades_cluster.drop('CLUSTER', axis=1)
        pedidos_frecuentes = pedidos_cluster.sum().sort_values(ascending=False)

        top_pedidos = pedidos_frecuentes.head(3)

        clusters_info.append({
            'cluster': cluster_id,
            'comunidades': len(comunidades_cluster),
            'pedidos_comunes': top_pedidos.to_dict()
        })

        print(f"\n   CLUSTER {cluster_id}:")
        print(f"   - Comunidades: {len(comunidades_cluster)}")
        print(f"   - Pedidos más comunes:")
        for pedido, count in top_pedidos.items():
            print(f"     • {pedido[:40]}...: {count}/{len(comunidades_cluster)} comunidades")

    # 6. MOSTRAR EJEMPLOS DE COMUNIDADES EN CADA CLUSTER
    print(f"\n6. EJEMPLOS DE COMUNIDADES POR CLUSTER:")

    for cluster_id in range(mejor_k):
        comunidades_cluster = matriz_resultados[matriz_resultados['CLUSTER'] == cluster_id]

        print(f"\n   Cluster {cluster_id} (muestra de 3 comunidades):")
        for comunidad in comunidades_cluster.index[:3]:
            pedidos = matriz_filtrada.loc[comunidad]
            pedidos_activos = pedidos[pedidos == 1].index.tolist()
            print(f"   - {comunidad[:30]}...")
            print(f"     Pedidos: {', '.join([p[:20] for p in pedidos_activos[:2]])}...")

    # 7. GUARDAR RESULTADOS
    print("\n7. GUARDANDO RESULTADOS...")

    results_dir = os.path.join(proyecto_dir, "data", "results")

    resultados_path = os.path.join(results_dir, "comunidades_clusters.csv")
    matriz_resultados.to_csv(resultados_path, encoding='utf-8-sig')

    resumen_path = os.path.join(results_dir, "resumen_clusters.txt")
    with open(resumen_path, 'w', encoding='utf-8') as f:
        f.write("RESUMEN DE CLUSTERING DE COMUNIDADES\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total comunidades analizadas: {matriz_filtrada.shape[0]}\n")
        f.write(f"Número óptimo de clusters: {mejor_k}\n")
        f.write(f"Score Silhouette: {silhouette_scores[mejor_k_idx]:.3f}\n\n")

        f.write("DETALLE DE CLUSTERS:\n")
        for info in clusters_info:
            f.write(f"\nCLUSTER {info['cluster']} ({info['comunidades']} comunidades):\n")
            for pedido, count in info['pedidos_comunes'].items():
                f.write(f"  - {pedido[:50]}...: {count} comunidades\n")

    print(f"   Resultados guardados en: {resultados_path}")
    print(f"   Resumen guardado en: {resumen_path}")

    # 8. RECOMENDACIONES FINALES
    print("\n" + "=" * 70)
    print("RESULTADO DEL CLUSTERING")
    print("=" * 70)

    print(f"✅ Se agruparon {matriz_filtrada.shape[0]} comunidades en {mejor_k} clusters")
    print(f"📊 Cada cluster agrupa comunidades con pedidos similares")

    cluster_sizes = matriz_resultados['CLUSTER'].value_counts()
    print(f"\n📈 Tamaño de clusters:")
    for cluster_id, size in cluster_sizes.items():
        print(f"   Cluster {cluster_id}: {size} comunidades")

    return matriz_resultados


if __name__ == "__main__":
    resultados = clustering_comunidades()