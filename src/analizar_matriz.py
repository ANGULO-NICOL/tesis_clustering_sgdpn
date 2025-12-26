import pandas as pd
import numpy as np
import os


def analizar_matriz_detalladamente():
    """Analizar la matriz en detalle para ver si sirve para clustering"""

    print("ANÁLISIS DETALLADO DE LA MATRIZ DE CLUSTERING")
    print("=" * 70)

    # Cargar matriz
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proyecto_dir = os.path.dirname(script_dir)
    matriz_path = os.path.join(proyecto_dir, "data", "results", "matriz_clustering_final.csv")

    if not os.path.exists(matriz_path):
        print("❌ No se encuentra la matriz")
        return

    matriz = pd.read_csv(matriz_path, index_col=0, encoding='utf-8-sig')

    print(f"\n1. DIMENSIONES DE LA MATRIZ:")
    print(f"   Comunidades: {matriz.shape[0]}")
    print(f"   Pedidos únicos: {matriz.shape[1]}")

    # 2. ANÁLISIS DE DISTRIBUCIÓN
    print("\n2. DISTRIBUCIÓN DE PEDIDOS POR COMUNIDAD:")
    pedidos_por_comunidad = matriz.sum(axis=1)

    print(f"   Promedio: {pedidos_por_comunidad.mean():.2f}")
    print(f"   Mediana: {pedidos_por_comunidad.median():.2f}")
    print(f"   Máximo: {pedidos_por_comunidad.max()}")
    print(f"   Mínimo: {pedidos_por_comunidad.min()}")

    # Contar cuántas comunidades tienen X pedidos
    print(f"\n   Comunidades por cantidad de pedidos:")
    for i in range(1, 11):
        count = (pedidos_por_comunidad == i).sum()
        if count > 0:
            print(f"   {i} pedido(s): {count} comunidades ({count / matriz.shape[0] * 100:.1f}%)")

    mas_de_1 = (pedidos_por_comunidad > 1).sum()
    print(f"\n   IMPORTANTE: {mas_de_1} comunidades tienen MÁS DE 1 pedido")
    print(f"   Solo {mas_de_1 / matriz.shape[0] * 100:.1f}% pueden clusterizarse bien")

    # 3. ANÁLISIS DE PEDIDOS
    print("\n3. DISTRIBUCIÓN DE COMUNIDADES POR PEDIDO:")
    comunidades_por_pedido = matriz.sum(axis=0)

    print(f"   Pedidos con solo 1 comunidad: {(comunidades_por_pedido == 1).sum()}")
    print(f"   Pedidos con 2-5 comunidades: {(comunidades_por_pedido.between(2, 5)).sum()}")
    print(f"   Pedidos con más de 5 comunidades: {(comunidades_por_pedido > 5).sum()}")

    # Top 10 pedidos más comunes
    print(f"\n   TOP 10 PEDIDOS MÁS COMUNES:")
    top_pedidos = comunidades_por_pedido.sort_values(ascending=False).head(10)
    for i, (pedido, count) in enumerate(top_pedidos.items(), 1):
        print(f"   {i:2d}. {count:3d} comunidades → {pedido[:50]}...")

    # 4. IDENTIFICAR COMUNIDADES CON MÚLTIPLES PEDIDOS
    print("\n4. IDENTIFICANDO COMUNIDADES CON MÚLTIPLES PEDIDOS:")

    # Filtrar comunidades con al menos 2 pedidos
    comunidades_multipes = pedidos_por_comunidad[pedidos_por_comunidad >= 2]

    if len(comunidades_multipes) > 0:
        print(f"   Se encontraron {len(comunidades_multipes)} comunidades con 2+ pedidos")

        # Mostrar algunas
        print(f"\n   Ejemplos de comunidades con múltiples pedidos:")
        for comunidad in comunidades_multipes.index[:5]:
            pedidos_de_comunidad = matriz.loc[comunidad]
            pedidos_activos = pedidos_de_comunidad[pedidos_de_comunidad == 1].index.tolist()
            print(f"   - {comunidad[:30]}...: {len(pedidos_activos)} pedidos")
            if pedidos_activos:
                print(f"     Pedidos: {', '.join([p[:20] for p in pedidos_activos[:2]])}...")
    else:
        print("   ❌ NO HAY COMUNIDADES CON MÚLTIPLES PEDIDOS")

    # 5. VERIFICAR SI HAY PEDIDOS COMPARTIDOS
    print("\n5. VERIFICANDO PEDIDOS COMPARTIDOS:")

    # Buscar pares de comunidades que compartan pedidos
    print("   Buscando comunidades que compartan al menos 1 pedido...")

    # Tomar muestra de 100 comunidades para no demorar
    muestra = matriz.iloc[:100] if matriz.shape[0] > 100 else matriz

    compartidos = 0
    for i in range(len(muestra)):
        for j in range(i + 1, len(muestra)):
            comunidad1 = muestra.iloc[i]
            comunidad2 = muestra.iloc[j]
            # Si comparten al menos 1 pedido
            if ((comunidad1 == 1) & (comunidad2 == 1)).any():
                compartidos += 1

    total_pares = len(muestra) * (len(muestra) - 1) / 2
    porcentaje_compartido = (compartidos / total_pares * 100) if total_pares > 0 else 0

    print(f"   En muestra de {len(muestra)} comunidades:")
    print(f"   {compartidos} pares de comunidades comparten al menos 1 pedido")
    print(f"   {porcentaje_compartido:.1f}% de los pares comparten pedidos")

    # 6. RECOMENDACIONES
    print("\n" + "=" * 70)
    print("RECOMENDACIONES PARA EL CLUSTERING")
    print("=" * 70)

    if mas_de_1 < 10:
        print("❌ PROBLEMA GRAVE: Menos de 10 comunidades tienen múltiples pedidos")
        print("   El clustering NO será efectivo")
        print("\n   SOLUCIÓN 1: Agrupar pedidos similares (ej: todos los de 'REGISTRO')")
        print("   SOLUCIÓN 2: Usar solo comunidades con 2+ pedidos")
        print("   SOLUCIÓN 3: Revisar preprocesamiento de PEDIDO_UNIFICADO")

    elif porcentaje_compartido < 5:
        print("⚠️  PROBLEMA: Pocas comunidades comparten pedidos")
        print(f"   Solo {porcentaje_compartido:.1f}% de pares comparten")
        print("\n   SOLUCIÓN: Agrupar pedidos por categorías más generales")

    else:
        print("✅ La matriz puede usarse para clustering")
        print("   Considerar filtrar comunidades con solo 1 pedido")

    # 7. GUARDAR ANÁLISIS
    print("\n" + "=" * 70)
    print("GUARDANDO ANÁLISIS DETALLADO")

    results_dir = os.path.join(proyecto_dir, "data", "results")
    analisis_path = os.path.join(results_dir, "analisis_matriz_detallado.txt")

    with open(analisis_path, 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS DETALLADO DE LA MATRIZ\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Comunidades totales: {matriz.shape[0]}\n")
        f.write(f"Pedidos únicos: {matriz.shape[1]}\n")
        f.write(f"Densidad: {(matriz.sum().sum() / (matriz.shape[0] * matriz.shape[1]) * 100):.4f}%\n\n")

        f.write("DISTRIBUCIÓN DE PEDIDOS POR COMUNIDAD:\n")
        for i in range(1, 11):
            count = (pedidos_por_comunidad == i).sum()
            if count > 0:
                f.write(f"  {i} pedido(s): {count} comunidades ({count / matriz.shape[0] * 100:.1f}%)\n")

        f.write(f"\nComunidades con 2+ pedidos: {mas_de_1}\n")
        f.write(f"Porcentaje de pares que comparten: {porcentaje_compartido:.1f}%\n")

    print(f"   Análisis guardado en: {analisis_path}")


if __name__ == "__main__":
    analizar_matriz_detalladamente()