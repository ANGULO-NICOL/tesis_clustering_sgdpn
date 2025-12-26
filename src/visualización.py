import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns


def visualizacion_profesional():
    """Visualización profesional de resultados del clustering"""

    print("VISUALIZACIÓN PROFESIONAL DE RESULTADOS")
    print("=" * 70)

    # Cargar resultados
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proyecto_dir = os.path.dirname(script_dir)
    clusters_path = os.path.join(proyecto_dir, "data", "results", "comunidades_clusters.csv")

    clusters_df = pd.read_csv(clusters_path, index_col=0, encoding='utf-8-sig')

    # Preparar datos
    X = clusters_df.drop('CLUSTER', axis=1).values
    labels = clusters_df['CLUSTER'].values

    # 1. CONFIGURACIÓN DE ESTILO PROFESIONAL
    print("\n1. Configurando estilo profesional...")

    # Estilo personalizado
    plt.style.use('seaborn-v0_8-whitegrid')

    # Paleta de colores pastel profesional
    pastel_colors = [
        '#FFB6C1', '#87CEEB', '#98FB98', '#DDA0DD', '#FFD700',
        '#FFA07A', '#20B2AA', '#F0E68C', '#CD853F', '#B0E0E6'
    ]

    # Configuración de fuentes
    plt.rcParams.update({
        'font.size': 11,
        'font.family': 'DejaVu Sans',
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16
    })

    # 2. GRÁFICO 1: DISTRIBUCIÓN DE CLUSTERS
    print("2. Creando gráfico de distribución...")

    fig1 = plt.figure(figsize=(12, 8))

    # Reducción PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    # Scatter plot con colores pastel
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1],
                          c=labels,
                          cmap=plt.cm.Pastel1,
                          s=120,
                          alpha=0.85,
                          edgecolors='gray',
                          linewidth=0.8)

    # Título y etiquetas
    plt.title('Distribución de Comunidades por Cluster',
              fontweight='bold',
              pad=20)

    plt.xlabel(f'Componente Principal 1 ({pca.explained_variance_ratio_[0] * 100:.1f}% varianza)',
               fontweight='bold')
    plt.ylabel(f'Componente Principal 2 ({pca.explained_variance_ratio_[1] * 100:.1f}% varianza)',
               fontweight='bold')

    # Leyenda
    legend_elements = []
    for cluster_id in sorted(np.unique(labels)):
        count = (labels == cluster_id).sum()
        legend_elements.append(plt.Line2D([0], [0],
                                          marker='o',
                                          color='w',
                                          markerfacecolor=plt.cm.Pastel1(cluster_id / 9),
                                          markersize=10,
                                          label=f'Cluster {cluster_id} ({count} comunidades)'))

    plt.legend(handles=legend_elements,
               title="Clusters",
               loc='upper right',
               frameon=True,
               framealpha=0.9)

    # Grid y ajustes
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()

    # Guardar gráfico 1
    results_dir = os.path.join(proyecto_dir, "data", "results", "visualizaciones")
    os.makedirs(results_dir, exist_ok=True)

    fig1_path = os.path.join(results_dir, "distribucion_clusters.png")
    plt.savefig(fig1_path, dpi=300, bbox_inches='tight')
    print(f"   Gráfico 1 guardado: {fig1_path}")
    plt.show()

    # 3. GRÁFICO 2: TAMAÑO DE CLUSTERS
    print("\n3. Creando gráfico de tamaño de clusters...")

    fig2, ax2 = plt.subplots(figsize=(10, 6))

    # Contar comunidades por cluster
    cluster_sizes = clusters_df['CLUSTER'].value_counts().sort_index()

    # Crear barras horizontales
    y_pos = np.arange(len(cluster_sizes))
    bars = ax2.barh(y_pos, cluster_sizes.values,
                    color=pastel_colors[:len(cluster_sizes)],
                    edgecolor='gray',
                    height=0.7)

    # Añadir números
    for i, (bar, size) in enumerate(zip(bars, cluster_sizes.values)):
        ax2.text(size + 0.5, bar.get_y() + bar.get_height() / 2,
                 f'{size}',
                 va='center',
                 fontweight='bold',
                 fontsize=11)

    # Configurar eje Y
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([f'Cluster {cluster_id}' for cluster_id in cluster_sizes.index])

    # Títulos
    ax2.set_title('Distribución de Comunidades por Cluster',
                  fontweight='bold',
                  pad=20)
    ax2.set_xlabel('Número de Comunidades', fontweight='bold')
    ax2.set_ylabel('Cluster ID', fontweight='bold')

    # Grid
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)

    plt.tight_layout()

    # Guardar gráfico 2
    fig2_path = os.path.join(results_dir, "tamano_clusters.png")
    plt.savefig(fig2_path, dpi=300, bbox_inches='tight')
    print(f"   Gráfico 2 guardado: {fig2_path}")
    plt.show()

    # 4. GRÁFICO 3: PEDIDOS PRINCIPALES POR CLUSTER
    print("\n4. Creando gráfico de pedidos principales...")

    fig3 = plt.figure(figsize=(14, 8))

    # Preparar datos
    pedidos_por_cluster = []
    nombres_clusters = []

    for cluster_id in sorted(clusters_df['CLUSTER'].unique()):
        cluster_data = clusters_df[clusters_df['CLUSTER'] == cluster_id].drop('CLUSTER', axis=1)
        pedido_mas_comun = cluster_data.sum().idxmax()
        frecuencia = cluster_data.sum().max()

        # Acortar nombre del pedido
        pedido_corto = pedido_mas_comun[:35] + "..." if len(pedido_mas_comun) > 35 else pedido_mas_comun

        pedidos_por_cluster.append({
            'cluster': cluster_id,
            'pedido': pedido_corto,
            'frecuencia': frecuencia,
            'total_comunidades': len(cluster_data)
        })
        nombres_clusters.append(f'Cluster {cluster_id}')

    # Crear DataFrame
    pedidos_df = pd.DataFrame(pedidos_por_cluster)

    # Gráfico de barras agrupadas
    x = np.arange(len(pedidos_df))
    width = 0.35

    fig3, (ax3a, ax3b) = plt.subplots(2, 1, figsize=(14, 10))

    # Subgráfico A: Frecuencia del pedido principal
    bars1 = ax3a.bar(x - width / 2, pedidos_df['frecuencia'],
                     width,
                     label='Comunidades con este pedido',
                     color='#87CEEB',
                     edgecolor='gray')

    bars2 = ax3a.bar(x + width / 2, pedidos_df['total_comunidades'],
                     width,
                     label='Total comunidades en cluster',
                     color='#FFB6C1',
                     edgecolor='gray')

    ax3a.set_ylabel('Número de Comunidades', fontweight='bold')
    ax3a.set_title('Pedido Principal vs Total de Comunidades por Cluster',
                   fontweight='bold',
                   pad=20)
    ax3a.set_xticks(x)
    ax3a.set_xticklabels(nombres_clusters, rotation=45, ha='right')
    ax3a.legend()
    ax3a.grid(axis='y', alpha=0.3, linestyle='--')

    # Añadir porcentajes
    for i, (freq, total) in enumerate(zip(pedidos_df['frecuencia'], pedidos_df['total_comunidades'])):
        porcentaje = (freq / total) * 100
        ax3a.text(i, max(freq, total) + 1,
                  f'{porcentaje:.0f}%',
                  ha='center',
                  fontsize=9,
                  fontweight='bold')

    # Subgráfico B: Descripción de pedidos
    ax3b.axis('off')
    ax3b.set_title('Descripción de Pedidos Principales',
                   fontweight='bold',
                   pad=20)

    # Crear tabla con pedidos
    cell_text = []
    for idx, row in pedidos_df.iterrows():
        cell_text.append([f'Cluster {row["cluster"]}',
                          row['pedido'],
                          f'{row["frecuencia"]}/{row["total_comunidades"]}',
                          f'{(row["frecuencia"] / row["total_comunidades"] * 100):.0f}%'])

    tabla = ax3b.table(cellText=cell_text,
                       colLabels=['Cluster', 'Pedido Principal', 'Frecuencia', '%'],
                       colColours=['#F0F8FF', '#F0F8FF', '#F0F8FF', '#F0F8FF'],
                       cellLoc='left',
                       loc='center')

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.5)

    # Color alternado para filas
    for i in range(len(pedidos_df) + 1):
        if i % 2 == 0:
            for j in range(4):
                tabla[(i, j)].set_facecolor('#F9F9F9')

    plt.tight_layout()

    # Guardar gráfico 3
    fig3_path = os.path.join(results_dir, "pedidos_principales.png")
    plt.savefig(fig3_path, dpi=300, bbox_inches='tight')
    print(f"   Gráfico 3 guardado: {fig3_path}")
    plt.show()

    # 5. GRÁFICO 4: RESUMEN EJECUTIVO
    print("\n5. Creando resumen ejecutivo...")

    # Cargar análisis previo
    analisis_path = os.path.join(proyecto_dir, "data", "results", "resumen_analisis_clusters.txt")

    if os.path.exists(analisis_path):
        with open(analisis_path, 'r') as f:
            lineas = f.readlines()

        # Extraer distribución por tipo
        distribucion = {}
        for linea in lineas:
            if '- Legalización:' in linea:
                distribucion['Legalización'] = int(linea.split(':')[1].split()[0])
            elif '- Membresía:' in linea:
                distribucion['Membresía'] = int(linea.split(':')[1].split()[0])
            elif '- Gestión interna:' in linea:
                distribucion['Gestión interna'] = int(linea.split(':')[1].split()[0])
            elif '- Actualización:' in linea:
                distribucion['Actualización'] = int(linea.split(':')[1].split()[0])
            elif '- Otros:' in linea:
                distribucion['Otros'] = int(linea.split(':')[1].split()[0])

        # Crear gráfico de torta
        fig4 = plt.figure(figsize=(10, 8))

        tipos = list(distribucion.keys())
        valores = list(distribucion.values())
        colores_torta = ['#FFD700', '#98FB98', '#87CEEB', '#FFA07A', '#DDA0DD']

        # Gráfico de torta
        wedges, texts, autotexts = plt.pie(valores,
                                           labels=tipos,
                                           colors=colores_torta,
                                           autopct='%1.1f%%',
                                           startangle=90,
                                           shadow=False,
                                           explode=[0.05] * len(tipos),
                                           textprops={'fontsize': 11})

        plt.title('Distribución de Comunidades por Tipo de Trámite',
                  fontweight='bold',
                  pad=30)

        # Mejorar aspecto de porcentajes
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)

        plt.axis('equal')
        plt.tight_layout()

        # Guardar gráfico 4
        fig4_path = os.path.join(results_dir, "resumen_tipos_tramite.png")
        plt.savefig(fig4_path, dpi=300, bbox_inches='tight')
        print(f"   Gráfico 4 guardado: {fig4_path}")
        plt.show()

    print("\n" + "=" * 70)
    print("✅ VISUALIZACIONES PROFESIONALES COMPLETADAS")
    print("=" * 70)
    print(f"\n📊 Gráficos generados en: {results_dir}")
    print("\n1. distribucion_clusters.png - Visualización 2D de clusters")
    print("2. tamano_clusters.png - Tamaño de cada cluster")
    print("3. pedidos_principales.png - Pedidos principales por cluster")
    print("4. resumen_tipos_tramite.png - Resumen por tipo de trámite")


if __name__ == "__main__":
    visualizacion_profesional()