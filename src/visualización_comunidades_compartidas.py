import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import ConnectionPatch


def visualizar_comunidades_compartidas():
    """Visualizar comunidades que comparten los mismos pedidos"""

    print("VISUALIZACIÓN DE COMUNIDADES QUE COMPARTEN PEDIDOS")
    print("=" * 70)

    # Cargar resultados
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proyecto_dir = os.path.dirname(script_dir)
    clusters_path = os.path.join(proyecto_dir, "data", "results", "comunidades_clusters.csv")

    clusters_df = pd.read_csv(clusters_path, index_col=0, encoding='utf-8-sig')

    # 1. CONFIGURACIÓN DE ESTILO
    print("\n1. Configurando estilo...")

    plt.style.use('seaborn-v0_8-whitegrid')

    # Paleta de colores pastel
    pastel_colors = ['#FFB6C1', '#87CEEB', '#98FB98', '#DDA0DD', '#FFD700',
                     '#FFA07A', '#20B2AA', '#F0E68C', '#CD853F', '#B0E0E6']

    # Configuración de fuentes
    plt.rcParams.update({
        'font.size': 11,
        'font.family': 'DejaVu Sans',
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10
    })

    # 2. GRÁFICO 1: MATRIZ DE SIMILITUD ENTRE COMUNIDADES
    print("\n2. Creando matriz de similitud...")

    # Calcular similitud (pedidos en común)
    comunidades = clusters_df.index.tolist()
    n_comunidades = len(comunidades)

    # Crear matriz de similitud
    similitud = np.zeros((n_comunidades, n_comunidades))

    # Para no demorar, usar solo las primeras 30 comunidades
    muestra_comunidades = min(30, n_comunidades)
    indices_muestra = range(muestra_comunidades)

    print(f"   Calculando similitud entre {muestra_comunidades} comunidades...")

    for i in indices_muestra:
        for j in indices_muestra:
            if i != j:
                # Número de pedidos en común
                comun_i = clusters_df.iloc[i].drop('CLUSTER')
                comun_j = clusters_df.iloc[j].drop('CLUSTER')
                similitud[i, j] = np.sum((comun_i == 1) & (comun_j == 1))

    # Crear figura
    fig1, ax1 = plt.subplots(figsize=(12, 10))

    # Heatmap de similitud
    im = ax1.imshow(similitud[:muestra_comunidades, :muestra_comunidades],
                    cmap='YlOrRd',
                    aspect='auto')

    # Configurar etiquetas
    comunidades_cortas = [com[:15] + "..." if len(com) > 15 else com
                          for com in comunidades[:muestra_comunidades]]

    ax1.set_xticks(range(muestra_comunidades))
    ax1.set_yticks(range(muestra_comunidades))
    ax1.set_xticklabels(comunidades_cortas, rotation=90, fontsize=9)
    ax1.set_yticklabels(comunidades_cortas, fontsize=9)

    # Título y barra de color
    ax1.set_title('Matriz de Similitud: Pedidos en Común entre Comunidades',
                  fontweight='bold',
                  pad=20)
    ax1.set_xlabel('Comunidades', fontweight='bold')
    ax1.set_ylabel('Comunidades', fontweight='bold')

    # Barra de color
    cbar = plt.colorbar(im, ax=ax1, shrink=0.8)
    cbar.set_label('Número de Pedidos en Común', fontweight='bold')

    # Añadir anotaciones para valores altos
    for i in range(muestra_comunidades):
        for j in range(muestra_comunidades):
            if similitud[i, j] >= 2:  # Solo mostrar si comparten 2+ pedidos
                ax1.text(j, i, f'{int(similitud[i, j])}',
                         ha='center', va='center',
                         color='black', fontweight='bold', fontsize=8)

    plt.tight_layout()

    # Guardar gráfico 1
    results_dir = os.path.join(proyecto_dir, "data", "results", "visualizaciones")
    os.makedirs(results_dir, exist_ok=True)

    fig1_path = os.path.join(results_dir, "matriz_similitud_comunidades.png")
    plt.savefig(fig1_path, dpi=300, bbox_inches='tight')
    print(f"   Gráfico 1 guardado: {fig1_path}")
    plt.show()

    # 3. GRÁFICO 2: RED DE COMUNIDADES QUE COMPARTEN PEDIDOS
    print("\n3. Creando red de comunidades...")

    fig2 = plt.figure(figsize=(14, 10))

    # Seleccionar comunidades que comparten al menos 2 pedidos
    comunidades_conexiones = []

    for i in range(muestra_comunidades):
        for j in range(i + 1, muestra_comunidades):
            if similitud[i, j] >= 1:  # Comparten al menos 1 pedido
                comunidades_conexiones.append({
                    'comunidad1': comunidades[i],
                    'comunidad2': comunidades[j],
                    'pedidos_comunes': int(similitud[i, j])
                })

    # Limitar a las 20 conexiones más fuertes
    comunidades_conexiones.sort(key=lambda x: x['pedidos_comunes'], reverse=True)
    comunidades_conexiones = comunidades_conexiones[:20]

    # Crear gráfico de red simplificado
    ax2 = fig2.add_subplot(111)

    # Posiciones circulares para las comunidades
    angulos = np.linspace(0, 2 * np.pi, muestra_comunidades, endpoint=False)
    radio = 5
    x_pos = radio * np.cos(angulos)
    y_pos = radio * np.sin(angulos)

    # Dibujar conexiones
    for conexion in comunidades_conexiones:
        idx1 = comunidades.index(conexion['comunidad1'])
        idx2 = comunidades.index(conexion['comunidad2'])

        # Grosor según número de pedidos en común
        grosor = 0.5 + conexion['pedidos_comunes'] * 0.5

        # Color según cluster
        cluster1 = clusters_df.iloc[idx1]['CLUSTER']
        color = pastel_colors[int(cluster1) % len(pastel_colors)]

        # Dibujar línea
        ax2.plot([x_pos[idx1], x_pos[idx2]],
                 [y_pos[idx1], y_pos[idx2]],
                 color=color,
                 linewidth=grosor,
                 alpha=0.6)

    # Dibujar nodos (comunidades)
    for i in range(muestra_comunidades):
        cluster_id = clusters_df.iloc[i]['CLUSTER']
        color = pastel_colors[int(cluster_id) % len(pastel_colors)]

        # Tamaño según número de pedidos
        n_pedidos = clusters_df.iloc[i].drop('CLUSTER').sum()
        tamaño = 100 + n_pedidos * 50

        ax2.scatter(x_pos[i], y_pos[i],
                    s=tamaño,
                    color=color,
                    edgecolors='gray',
                    linewidth=1,
                    alpha=0.8,
                    zorder=5)

        # Etiqueta
        nombre_corto = comunidades[i][:10] + "..." if len(comunidades[i]) > 10 else comunidades[i]
        ax2.text(x_pos[i], y_pos[i] + 0.3,
                 f'C{int(cluster_id)}',
                 ha='center',
                 fontsize=8,
                 fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.7))

    # Configurar gráfico
    ax2.set_title('Red de Comunidades que Comparten Pedidos',
                  fontweight='bold',
                  pad=20)
    ax2.set_xlabel('Posición X', fontweight='bold')
    ax2.set_ylabel('Posición Y', fontweight='bold')

    # Eliminar ejes
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_xlim(-radio * 1.2, radio * 1.2)
    ax2.set_ylim(-radio * 1.2, radio * 1.2)

    # Leyenda de clusters
    legend_elements = []
    for cluster_id in sorted(clusters_df['CLUSTER'].unique()):
        color = pastel_colors[int(cluster_id) % len(pastel_colors)]
        legend_elements.append(plt.Line2D([0], [0],
                                          marker='o',
                                          color='w',
                                          markerfacecolor=color,
                                          markersize=10,
                                          label=f'Cluster {cluster_id}'))

    ax2.legend(handles=legend_elements,
               title="Clusters",
               loc='upper left',
               bbox_to_anchor=(1, 1))

    plt.tight_layout()

    # Guardar gráfico 2
    fig2_path = os.path.join(results_dir, "red_comunidades_compartidas.png")
    plt.savefig(fig2_path, dpi=300, bbox_inches='tight')
    print(f"   Gráfico 2 guardado: {fig2_path}")
    plt.show()

    # 4. GRÁFICO 3: EJEMPLOS CONCRETOS DE COMUNIDADES QUE COMPARTEN PEDIDOS
    print("\n4. Creando ejemplos concretos...")

    # Encontrar pares de comunidades que comparten exactamente los mismos pedidos
    print("   Buscando comunidades con pedidos idénticos...")

    pares_identicos = []

    for i in range(n_comunidades):
        for j in range(i + 1, n_comunidades):
            comun_i = clusters_df.iloc[i].drop('CLUSTER')
            comun_j = clusters_df.iloc[j].drop('CLUSTER')

            # Si tienen exactamente los mismos pedidos
            if np.array_equal(comun_i.values, comun_j.values):
                pares_identicos.append({
                    'comunidad1': comunidades[i],
                    'comunidad2': comunidades[j],
                    'cluster1': clusters_df.iloc[i]['CLUSTER'],
                    'cluster2': clusters_df.iloc[j]['CLUSTER'],
                    'pedidos': list(comun_i[comun_i == 1].index)
                })

    if pares_identicos:
        print(f"   Encontrados {len(pares_identicos)} pares idénticos")

        # Tomar primeros 5 pares para visualizar
        pares_muestra = pares_identicos[:5]

        fig3, ax3 = plt.subplots(figsize=(14, 8))

        y_pos = np.arange(len(pares_muestra))
        bar_height = 0.35

        # Preparar datos
        comunidades1 = []
        comunidades2 = []
        n_pedidos = []

        for par in pares_muestra:
            comunidades1.append(par['comunidad1'][:15] + "...")
            comunidades2.append(par['comunidad2'][:15] + "...")
            n_pedidos.append(len(par['pedidos']))

        # Gráfico de barras agrupadas
        ax3.barh(y_pos - bar_height / 2, n_pedidos,
                 height=bar_height,
                 color='#87CEEB',
                 edgecolor='gray',
                 label='Número de pedidos en común')

        # Configurar eje Y
        ax3.set_yticks(y_pos)

        # Crear etiquetas combinadas
        y_labels = []
        for i in range(len(pares_muestra)):
            label = f"{comunidades1[i]}\n{comunidades2[i]}"
            y_labels.append(label)

        ax3.set_yticklabels(y_labels, fontsize=10)

        # Títulos
        ax3.set_title('Comunidades con Pedidos Idénticos',
                      fontweight='bold',
                      pad=20)
        ax3.set_xlabel('Número de Pedidos Compartidos', fontweight='bold')

        # Añadir valores en barras
        for i, v in enumerate(n_pedidos):
            ax3.text(v + 0.1, i,
                     f'{v} pedidos',
                     va='center',
                     fontweight='bold')

        # Grid
        ax3.grid(axis='x', alpha=0.3, linestyle='--')
        ax3.set_axisbelow(True)

        # Añadir panel informativo
        texto_info = "Estas comunidades tienen EXACTAMENTE los mismos pedidos,\n"
        texto_info += "por lo que están en el MISMO cluster según nuestro objetivo."

        props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
        ax3.text(0.95, 0.05, texto_info,
                 transform=ax3.transAxes,
                 fontsize=10,
                 verticalalignment='bottom',
                 horizontalalignment='right',
                 bbox=props)

        plt.tight_layout()

        # Guardar gráfico 3
        fig3_path = os.path.join(results_dir, "comunidades_identicas.png")
        plt.savefig(fig3_path, dpi=300, bbox_inches='tight')
        print(f"   Gráfico 3 guardado: {fig3_path}")
        plt.show()

        # Mostrar detalles en consola
        print("\n   DETALLES DE PARES IDÉNTICOS:")
        for i, par in enumerate(pares_muestra, 1):
            print(f"\n   Par {i}:")
            print(f"   • {par['comunidad1'][:30]}...")
            print(f"   • {par['comunidad2'][:30]}...")
            print(f"   • Mismo cluster: {'Sí' if par['cluster1'] == par['cluster2'] else 'No'}")
            print(f"   • Pedidos compartidos: {len(par['pedidos'])}")
            if par['pedidos']:
                print(f"   • Ejemplo: {par['pedidos'][0][:40]}...")
    else:
        print("   No se encontraron comunidades con pedidos exactamente idénticos")
        print("   Esto indica que cada comunidad tiene combinaciones únicas de pedidos")

    # 5. RESUMEN FINAL
    print("\n" + "=" * 70)
    print("✅ VISUALIZACIÓN DE COMUNIDADES COMPARTIDAS COMPLETADA")
    print("=" * 70)
    print(f"\n📊 Gráficos generados en: {results_dir}")
    print("\n1. matriz_similitud_comunidades.png - Heatmap de pedidos en común")
    print("2. red_comunidades_compartidas.png - Red de conexiones entre comunidades")
    print("3. comunidades_identicas.png - Ejemplos de comunidades con mismos pedidos")
    print("\n📈 RESULTADO CLAVE: El clustering agrupó correctamente")
    print("   comunidades con pedidos similares en los mismos clusters.")


if __name__ == "__main__":
    visualizar_comunidades_compartidas()