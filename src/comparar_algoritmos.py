import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score


def comparar_algoritmos_clustering():
    """Comparar diferentes algoritmos de clustering"""

    print("COMPARACIÓN DE ALGORITMOS DE CLUSTERING")
    print("=" * 70)

    # Cargar datos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proyecto_dir = os.path.dirname(script_dir)
    matriz_path = os.path.join(proyecto_dir, "data", "results", "matriz_clustering_final.csv")

    matriz = pd.read_csv(matriz_path, index_col=0, encoding='utf-8-sig')

    # Filtrar comunidades con 2+ pedidos
    pedidos_por_comunidad = matriz.sum(axis=1)
    matriz_filtrada = matriz.loc[pedidos_por_comunidad[pedidos_por_comunidad >= 2].index]
    X = matriz_filtrada.values

    print(f"\nDatos: {matriz_filtrada.shape[0]} comunidades, {matriz_filtrada.shape[1]} pedidos")

    resultados = []

    # 1. K-MEANS (ya lo hiciste, pero vamos a documentar mejor)
    print("\n1. K-MEANS:")
    mejor_kmeans_score = -1
    mejor_kmeans_k = 0

    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)

        if len(np.unique(labels)) > 1:
            silhouette = silhouette_score(X, labels)
            davies = davies_bouldin_score(X, labels)
            calinski = calinski_harabasz_score(X, labels)

            if silhouette > mejor_kmeans_score:
                mejor_kmeans_score = silhouette
                mejor_kmeans_k = k

            print(f"   K={k}: Silhouette={silhouette:.3f}, Davies={davies:.3f}, Calinski={calinski:.0f}")

    resultados.append({
        'algoritmo': 'K-Means',
        'mejor_k': mejor_kmeans_k,
        'silhouette': mejor_kmeans_score,
        'ventajas': 'Rápido, escalable, bueno para datos esféricos',
        'desventajas': 'Requiere especificar K, sensible a outliers'
    })

    # 2. DBSCAN (no requiere número de clusters)
    print("\n2. DBSCAN:")

    # Probar diferentes parámetros
    eps_values = [0.3, 0.5, 0.7, 1.0]
    min_samples_values = [2, 3, 5]

    mejor_dbscan_score = -1
    mejor_dbscan_params = {}

    for eps in eps_values:
        for min_samples in min_samples_values:
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            labels = dbscan.fit_predict(X)

            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

            if n_clusters > 1:
                silhouette = silhouette_score(X, labels)

                if silhouette > mejor_dbscan_score:
                    mejor_dbscan_score = silhouette
                    mejor_dbscan_params = {'eps': eps, 'min_samples': min_samples, 'n_clusters': n_clusters}

    if mejor_dbscan_score > -1:
        print(f"   Mejor: eps={mejor_dbscan_params['eps']}, min_samples={mejor_dbscan_params['min_samples']}")
        print(f"   Clusters: {mejor_dbscan_params['n_clusters']}, Silhouette={mejor_dbscan_score:.3f}")

        resultados.append({
            'algoritmo': 'DBSCAN',
            'clusters': mejor_dbscan_params['n_clusters'],
            'silhouette': mejor_dbscan_score,
            'ventajas': 'No requiere K, detecta outliers, encuentra clusters no esféricos',
            'desventajas': 'Sensible a parámetros, no funciona bien con densidad variable'
        })

    # 3. CLUSTERING JERÁRQUICO
    print("\n3. CLUSTERING JERÁRQUICO:")

    mejor_hier_score = -1
    mejor_hier_k = 0

    for k in range(2, 11):
        hierarchical = AgglomerativeClustering(n_clusters=k)
        labels = hierarchical.fit_predict(X)

        if len(np.unique(labels)) > 1:
            silhouette = silhouette_score(X, labels)

            if silhouette > mejor_hier_score:
                mejor_hier_score = silhouette
                mejor_hier_k = k

    print(f"   Mejor K={mejor_hier_k}, Silhouette={mejor_hier_score:.3f}")

    resultados.append({
        'algoritmo': 'Jerárquico',
        'mejor_k': mejor_hier_k,
        'silhouette': mejor_hier_score,
        'ventajas': 'Visualización dendrograma, no requiere K inicial',
        'desventajas': 'Computacionalmente costoso, sensible a outliers'
    })

    # 4. COMPARACIÓN FINAL
    print("\n" + "=" * 70)
    print("COMPARACIÓN FINAL DE ALGORITMOS")
    print("=" * 70)

    print("\n   ALGORITMO           | CLUSTERS | SILHOUETTE | RECOMENDACIÓN")
    print("   " + "-" * 60)

    mejor_algoritmo = None
    mejor_score = -1

    for resultado in resultados:
        clusters = resultado.get('mejor_k', resultado.get('clusters', 'N/A'))
        silhouette = resultado['silhouette']

        if silhouette > mejor_score:
            mejor_score = silhouette
            mejor_algoritmo = resultado['algoritmo']

        print(f"   {resultado['algoritmo']:20} | {clusters:^8} | {silhouette:^10.3f} | ", end="")

        if resultado['algoritmo'] == 'K-Means':
            print("Buen equilibrio velocidad-calidad")
        elif resultado['algoritmo'] == 'DBSCAN':
            print("Mejor para datos con outliers")
        else:
            print("Mejor para visualización jerárquica")

    print(f"\n✅ MEJOR ALGORITMO: {mejor_algoritmo} (Score: {mejor_score:.3f})")

    # Guardar comparación
    results_dir = os.path.join(proyecto_dir, "data", "results")
    comparacion_path = os.path.join(results_dir, "comparacion_algoritmos.txt")

    with open(comparacion_path, 'w', encoding='utf-8') as f:
        f.write("COMPARACIÓN DE ALGORITMOS DE CLUSTERING\n")
        f.write("=" * 50 + "\n\n")

        f.write("RESUMEN:\n")
        f.write(f"- Mejor algoritmo: {mejor_algoritmo}\n")
        f.write(f"- Score Silhouette: {mejor_score:.3f}\n")
        f.write(f"- Comunidades analizadas: {matriz_filtrada.shape[0]}\n\n")

        f.write("DETALLE POR ALGORITMO:\n")
        for resultado in resultados:
            f.write(f"\n{resultado['algoritmo']}:\n")
            f.write(f"  Score Silhouette: {resultado['silhouette']:.3f}\n")
            f.write(f"  Ventajas: {resultado['ventajas']}\n")
            f.write(f"  Desventajas: {resultado['desventajas']}\n")

    print(f"\n📄 Comparación guardada en: {comparacion_path}")

    return mejor_algoritmo, mejor_score


if __name__ == "__main__":
    mejor_algoritmo, mejor_score = comparar_algoritmos_clustering()