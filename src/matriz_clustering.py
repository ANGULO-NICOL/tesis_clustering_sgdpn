import pandas as pd
import numpy as np
import os


def crear_matriz_clustering():
    """Crear matriz binaria comunidades vs pedidos para clustering"""

    print("CREACIÓN DE MATRIZ PARA CLUSTERING")
    print("=" * 60)

    # Rutas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proyecto_dir = os.path.dirname(script_dir)
    processed_dir = os.path.join(proyecto_dir, "data", "processed")

    # Cargar datos preprocesados
    print("\n1. Cargando datos preprocesados...")
    df1 = pd.read_csv(os.path.join(processed_dir, "archivo1_preprocesado_final.csv"),
                      encoding='utf-8-sig')
    df2 = pd.read_csv(os.path.join(processed_dir, "archivo2_preprocesado_final.csv"),
                      encoding='utf-8-sig')

    print(f"   Archivo 1: {df1.shape}")
    print(f"   Archivo 2: {df2.shape}")

    # 1. Extraer todas las comunidades únicas
    print("\n2. Extrayendo comunidades únicas...")
    comunidades1 = set(df1['NOMBRE DE LA ORGANIZACIÓN'].unique())
    comunidades2 = set(df2['NOMBRE DE LA ORGANIZACIÓN'].unique())
    todas_comunidades = sorted(list(comunidades1.union(comunidades2)))

    print(f"   Total comunidades únicas: {len(todas_comunidades)}")
    print(f"   - Solo en Archivo 1: {len(comunidades1 - comunidades2)}")
    print(f"   - Solo en Archivo 2: {len(comunidades2 - comunidades1)}")
    print(f"   - En ambos archivos: {len(comunidades1.intersection(comunidades2))}")

    # 2. Extraer todos los pedidos únicos
    print("\n3. Extrayendo pedidos únicos...")
    pedidos1 = set(df1['PEDIDO_UNIFICADO'].unique())
    pedidos2 = set(df2['PEDIDO_UNIFICADO'].unique())
    todos_pedidos = sorted(list(pedidos1.union(pedidos2)))

    print(f"   Total pedidos únicos: {len(todos_pedidos)}")
    print(f"   - Solo en Archivo 1: {len(pedidos1 - pedidos2)}")
    print(f"   - Solo en Archivo 2: {len(pedidos2 - pedidos1)}")
    print(f"   - En ambos archivos: {len(pedidos1.intersection(pedidos2))}")

    # 3. Crear matriz binaria
    print("\n4. Creando matriz binaria...")
    matriz = pd.DataFrame(0, index=todas_comunidades, columns=todos_pedidos)

    # Rellenar con Archivo 1
    print("   Rellenando con Archivo 1...")
    for _, row in df1.iterrows():
        comunidad = row['NOMBRE DE LA ORGANIZACIÓN']
        pedido = row['PEDIDO_UNIFICADO']
        if comunidad in matriz.index and pedido in matriz.columns:
            matriz.loc[comunidad, pedido] = 1

    # Rellenar con Archivo 2
    print("   Rellenando con Archivo 2...")
    for _, row in df2.iterrows():
        comunidad = row['NOMBRE DE LA ORGANIZACIÓN']
        pedido = row['PEDIDO_UNIFICADO']
        if comunidad in matriz.index and pedido in matriz.columns:
            matriz.loc[comunidad, pedido] = 1

    print(f"   Matriz inicial: {matriz.shape[0]} comunidades x {matriz.shape[1]} pedidos")

    # 4. Filtrar matriz
    print("\n5. Filtrando matriz...")

    # Eliminar comunidades sin pedidos
    comunidades_con_pedidos = matriz.sum(axis=1) > 0
    matriz = matriz[comunidades_con_pedidos]
    print(f"   Comunidades con al menos 1 pedido: {matriz.shape[0]}")

    # Eliminar pedidos sin comunidades
    pedidos_con_comunidades = matriz.sum(axis=0) > 0
    matriz = matriz.loc[:, pedidos_con_comunidades]
    print(f"   Pedidos con al menos 1 comunidad: {matriz.shape[1]}")

    # 5. Calcular estadísticas
    print("\n6. Calculando estadísticas...")

    total_celdas = matriz.shape[0] * matriz.shape[1]
    celdas_con_uno = matriz.sum().sum()
    densidad = (celdas_con_uno / total_celdas) * 100

    pedidos_por_comunidad = matriz.sum(axis=1)
    comunidades_por_pedido = matriz.sum(axis=0)

    print(f"   Densidad de la matriz: {densidad:.4f}%")
    print(f"   Pedidos por comunidad (promedio): {pedidos_por_comunidad.mean():.2f}")
    print(f"   Comunidades por pedido (promedio): {comunidades_por_pedido.mean():.2f}")

    # 6. Guardar matriz
    print("\n7. Guardando matriz...")
    results_dir = os.path.join(proyecto_dir, "data", "results")
    os.makedirs(results_dir, exist_ok=True)

    # Guardar matriz completa
    matriz_path = os.path.join(results_dir, "matriz_clustering_final.csv")
    matriz.to_csv(matriz_path, encoding='utf-8-sig')

    # Guardar estadísticas
    stats_path = os.path.join(results_dir, "estadisticas_matriz.txt")
    with open(stats_path, 'w') as f:
        f.write("ESTADÍSTICAS DE LA MATRIZ DE CLUSTERING\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Comunidades: {matriz.shape[0]}\n")
        f.write(f"Pedidos únicos: {matriz.shape[1]}\n")
        f.write(f"Densidad: {densidad:.4f}%\n")
        f.write(f"Pedidos por comunidad (promedio): {pedidos_por_comunidad.mean():.2f}\n")
        f.write(f"Comunidades por pedido (promedio): {comunidades_por_pedido.mean():.2f}\n\n")

        f.write("TOP 5 PEDIDOS MÁS COMUNES:\n")
        for pedido, count in comunidades_por_pedido.sort_values(ascending=False).head(5).items():
            f.write(f"  {pedido[:50]}...: {count} comunidades\n")

    print(f"   Matriz guardada en: {matriz_path}")
    print(f"   Estadísticas guardadas en: {stats_path}")

    # 7. Mostrar resumen
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    print(f"✅ Matriz creada exitosamente")
    print(f"📊 Dimensiones: {matriz.shape[0]} comunidades x {matriz.shape[1]} pedidos")
    print(f"📈 Densidad: {densidad:.4f}%")
    print(f"🎯 Lista para aplicar algoritmos de clustering")

    # Mostrar pedidos más comunes
    print("\n📋 Pedidos más frecuentes:")
    top_pedidos = comunidades_por_pedido.sort_values(ascending=False).head(3)
    for i, (pedido, count) in enumerate(top_pedidos.items(), 1):
        print(f"  {i}. '{pedido[:40]}...' → {count} comunidades")

    return matriz


if __name__ == "__main__":
    matriz = crear_matriz_clustering()