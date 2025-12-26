# Tesis Clustering - SGDPN

Este repositorio contiene el desarrollo del proyecto de análisis de datos cuyo objetivo es segmentar comunidades, pueblos y organizaciones en función de la similitud de los trámites administrativos solicitados ante la Secretaría de Gestión de Pueblos y Nacionalidades del Ecuador (SGDPN).

El modelo permite identificar patrones comunes de pedidos administrativos y agrupar comunidades con características similares, proporcionando información útil para la optimización de los procesos institucionales y la planificación intercultural.

## Objetivo General

Desarrollar un modelo de análisis basado en técnicas de clustering implementado en Python para segmentar y optimizar los procesos administrativos asociados a los registros de organizaciones, pueblos y nacionalidades administrados por la Secretaria de Gestión de Pueblos y Nacionalidades del Ecuador.

## Objetivos Específicos

- Diagnosticar el estado actual de los registros administrativos de la SGDPN, identificando inconsistencias, datos duplicados, vacíos de datos.
- Implementar un proceso de preprocesamiento de datos que incluyen depuración, normalización, tratamiento de valores faltantes y codificación de variables para garantizar la calidad de la base analítica.
- Aplicar algoritmos de clustering, identificando el modelo mas adecuado para segmentar organizaciones, pueblos y nacionalidades.
- Proponer mejoras para la optimización de los procesos administrativos de la SGDPN que se basen en los resultados de clustering, fortaleciendo la planificación intercultural y la gestión institucional.

## Estructura del Proyecto

```text
tesis_clustering_sgdpn/
├── data/
│   ├── datos_originales/     # Archivos Excel originales
│   ├── processed/            # Datos preprocesados (CSV finales)
│   ├── results/              # Resultados del análisis
│   └── visualizaciones/      # Gráficos y figuras generadas
├── src/                      # Código fuente en Python
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo

¿Cómo Funciona el Modelo?

El proyecto implementa un flujo completo de análisis de datos, desde el diagnóstico inicial hasta la interpretación de clusters, siguiendo buenas prácticas de ciencia de datos.

El principio central del modelo es el siguiente:

Comunidades que realizan los mismos trámites administrativos deben agruparse en el mismo
cluster o en clusters muy similares.

Para lograr esto, se utiliza una representación binaria de los pedidos administrativos y se aplican algoritmos de clustering no supervisado.

Etapas del Proyecto
Diagnóstico de los Datos

Script: diagnostico.py

¿Qué hace?
Analiza los archivos Excel originales para identificar problemas estructurales antes de cualquier transformación.

Entrada:

Dos archivos Excel con registros administrativos desordenados.

Proceso:

Detecta automáticamente la fila correcta de encabezados (fila 4).

Cuenta valores nulos por columna.

Identifica duplicados críticos.

Compara inconsistencias entre ambos archivos.

Salida:

diagnostico_resultados.txt

Resultados clave:

54 valores nulos

10 duplicados críticos

4 inconsistencias relevantes

Preprocesamiento de Datos

Script: preprocesamiento.py

¿Qué hace?
Limpia y prepara los datos para que puedan ser utilizados en el análisis de clustering.

Proceso realizado:

Eliminación de 3 registros sin nombre de organización.

Eliminación de 10 registros duplicados por número de resolución.

Normalización de textos (mayúsculas y espacios).

Tratamiento de valores faltantes con el valor NO ESPECIFICADO.

Creación de la variable clave PEDIDO_UNIFICADO.

Salida:

Dos archivos CSV preprocesados sin valores nulos en columnas críticas.

verificacion_preprocesamiento.txt

Creación de la Matriz de Clustering

Script: matriz_clustering.py

¿Qué hace?
Convierte los datos limpios en una matriz binaria adecuada para algoritmos de clustering.

Proceso:

712 comunidades únicas identificadas.

153 tipos de pedidos administrativos.

Construcción de una matriz 712 × 153:

1 = la comunidad realizó el pedido

0 = no lo realizó

Estadísticas:

Densidad de la matriz: 0.75%

Promedio: 1.15 pedidos por comunidad

Salida:

matriz_clustering_final.csv

Aplicación del Clustering

Script: clustering_comunidades.py

¿Qué hace?
Aplica clustering sobre la matriz para agrupar comunidades similares.

Proceso:

Se filtran comunidades con dos o más pedidos (100 comunidades).

Se evalúan valores de K entre 2 y 10.

Se identifica K = 9 como el valor más adecuado.

Se aplica K-Means para generar los clusters finales.

Salida:

9 clusters con comunidades asignadas.

Comparación de Algoritmos

Script: comparar_algoritmos.py

Se comparan tres algoritmos utilizando la misma matriz y la métrica Silhouette:

Algoritmo	Silhouette
K-Means	0.472
DBSCAN	0.434
Jerárquico	0.516

Conclusión:
El clustering jerárquico presenta el mejor desempeño global; sin embargo, K-Means genera clusters coherentes y cumple el objetivo principal del proyecto.

Análisis de Clusters

Script: analizar_clusters.py

¿Qué hace?

Analiza las características internas de cada cluster.

Clasifica los clusters según el tipo de trámite predominante.

Resultados principales:

40% de comunidades buscan Personería Jurídica.

32% corresponden a trámites de membresía.

Clusters con alta homogeneidad interna.

Visualización de Resultados

Las visualizaciones permiten validar e interpretar el clustering:

Distribución de clusters en 2D (PCA).

Tamaño de clusters.

Pedido predominante por cluster.

Mapas de similitud y redes de comunidades.

Estas figuras demuestran visualmente que las comunidades con pedidos similares se agrupan correctamente.

Descripción de los Archivos de Resultados

A continuación, se describe la finalidad de los principales archivos generados por el modelo, con el objetivo de facilitar su interpretación y evaluación.

Archivos clave del análisis

matriz_clustering_final.csv
Matriz binaria de tamaño 712 × 153 que representa la relación entre comunidades y pedidos administrativos.

diagnostico_resultados.txt
Resultados del diagnóstico inicial de los datos originales.

verificacion_preprocesamiento.txt
Validación del proceso de limpieza y preprocesamiento.

estadisticas_matriz.txt
Métricas descriptivas de la matriz binaria.

comparacion_algoritmos.txt
Comparación entre K-Means, DBSCAN y clustering jerárquico.

resumen_analisis_clustering.txt
Síntesis de los principales hallazgos del análisis.

analisis_caracteristicas_clusters.csv
Características principales de cada cluster.

analisis_matriz_detallado.txt
Análisis detallado de la estructura de la matriz binaria.

Orden de Ejecución del Proyecto

diagnostico.py

preprocesamiento.py

matriz_clustering.py

comparar_algoritmos.py

clustering_comunidades.py

analizar_clusters.py

visualizacion.py y visualizacion_comunidades_compartidas.py

Nota: No es obligatorio ejecutar nuevamente los scripts, ya que los resultados finales se encuentran almacenados en la carpeta data/results/.

¿Cómo Usar este Proyecto?
Para evaluación o revisión:

Revisar los archivos en data/results/.

Analizar los gráficos en visualizaciones/.

Leer los archivos .txt con resultados y métricas.

Para generar el análisis:

Instalar Python 3.9 o superior.

Instalar dependencias:

pip install -r requirements.txt

Resultados Finales del Proyecto

El modelo de clustering permitió identificar patrones claros en los trámites administrativos realizados por comunidades, pueblos y organizaciones registradas en la SGDPN.

Los principales resultados obtenidos son:

Identificación de 9 clusters de comunidades con comportamientos administrativos similares.

Valor máximo de Silhouette = 0.516, indicando una estructura de agrupamiento adecuada.

Agrupación correcta de 218 pares de comunidades con pedidos idénticos.

Predominio de trámites relacionados con:

Personería jurídica (40%)

Membresía y actualización de registros (32%)

Estos resultados evidencian que los procesos administrativos presentan patrones repetitivos que pueden ser aprovechados para mejorar la planificación institucional y la atención a las comunidades.
