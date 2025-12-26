# Tesis Clustering - SGDPN

Este repositorio contiene el desarrollo del proyecto de análisis de datos cuyo objetivo es segmentar comunidades, pueblos y organizaciones en función de la similitud de los trámites administrativos solicitados ante la Secretaría de Gestión de Pueblos y Nacionalidades del Ecuador (SGDPN).

El modelo permite identificar patrones comunes de pedidos administrativos y agrupar comunidades con características similares, proporcionando información útil para la optimización de los procesos institucionales y la planificación intercultural.

## Objetivo General

Desarrollar y validar un modelo de análisis basado en técnicas de clustering Jerárquico implementado en Python que permita segmentar y optimizar los registros administrativos asociados a los registros de organizaciones, pueblos y nacionalidades administrados por la Secretaría de Gestión de Pueblos y Nacionalidades del Ecuador, con el fin de optimizar sus procesos administrativos y fortalecer la toma de decisiones institucionales.

## Objetivos Específicos

- Diagnosticar el estado actual de los registros administrativos de la secretaría de Gestión de Pueblos y Nacionalidades, identificando problemas de calidad de datos, como inconsistencias, duplicidades, valores faltantes y falta de estandarización.
- Implementar un proceso integral de limpieza y preprocesamiento de datos, que incluya depuración, tratamiento de valores faltantes y codificación de variables, con el propósito de construir una base de datos confiable.
- Aplicar y validar técnicas de clustering jerárquico sobre los registros depurados, evaluando la calidad y estabilidad de los clústeres mediante métricas estadísticas, para segmentar organizaciones, pueblos y nacionalidades según la similitud de sus trámites administrativos.
- Proponer recomendaciones orientadas a la optimización de los procesos administrativos de la SGDPN, que sean accionables para la toma de decisiones gerenciales.

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
└── README.md                 
```

## ¿Cómo Funciona el Modelo?

El proyecto implementa un **flujo completo de análisis de datos**, desde el diagnóstico inicial hasta la interpretación de clusters, siguiendo buenas prácticas de ciencia de datos.

El principio central del modelo es el siguiente:

> **Comunidades que realizan los mismos trámites administrativos deben agruparse en el mismo
cluster o en clusters muy similares.**

Para lograr esto, se utiliza una representación binaria de los pedidos administrativos y se aplican algoritmos de clustering no supervisado.

## Etapas del Proyecto 

### Diagnóstico de los Datos  
**Script:** `diagnostico.py`

**¿Qué hace?**  
Analiza los archivos Excel originales para identificar problemas estructurales antes de
cualquier transformación.

**Entrada:**  
- Dos archivos Excel con registros administrativos desordenados.

**Proceso:**
1. Detecta automáticamente la fila correcta de encabezados (fila 4).
2. Cuenta valores nulos por columna.
3. Identifica duplicados críticos.
4. Compara inconsistencias entre ambos archivos.

**Salida:**  
- `diagnostico_resultados.txt`

**Resultados clave:**
- 54 valores nulos
- 10 duplicados críticos
- 4 inconsistencias relevantes

### Preprocesamiento de Datos  
**Script:** `preprocesamiento.py`

**¿Qué hace?**  
Limpia y prepara los datos para que puedan ser utilizados en el análisis de clustering.

**Proceso realizado:**
1. Eliminación de 3 registros sin nombre de organización.
2. Eliminación de 10 registros duplicados por número de resolución.
3. Normalización de textos (mayúsculas y espacios).
4. Tratamiento de valores faltantes con el valor `NO ESPECIFICADO`.
5. Creación de la variable clave `PEDIDO_UNIFICADO`.

**Salida:**  
- Dos archivos CSV preprocesados sin valores nulos en columnas críticas.
- `verificacion_preprocesamiento.txt`

### Creación de la Matriz de Clustering  
**Script:** `matriz_clustering.py`

**¿Qué hace?**  
Convierte los datos limpios en una matriz binaria adecuada para algoritmos de clustering.

**Proceso:**
- 712 comunidades únicas identificadas.
- 153 tipos de pedidos administrativos.
- Construcción de una matriz 712 × 153:
  - 1 = la comunidad realizó el pedido
  - 0 = no lo realizó

**Estadísticas:**
- Densidad de la matriz: 0.75%
- Promedio: 1.15 pedidos por comunidad

**Salida:**  
- `matriz_clustering_final.csv`

### Aplicación del Clustering  
**Script:** `clustering_comunidades.py`

**¿Qué hace?**  
Aplica clustering sobre la matriz para agrupar comunidades similares.

**Proceso:**
1. Se filtran comunidades con dos o más pedidos (100 comunidades).
2. Se evalúan valores de K entre 2 y 10.
3. Se identifica K = 9 como el valor más adecuado.
4. Se aplica K-Means para generar los clusters finales.

**Salida:**  
- 9 clusters con comunidades asignadas.

## Comparación de Algoritmos
Script: comparar_algoritmos.py

Se comparan tres algoritmos utilizando la misma matriz y la métrica Silhouette:
```text
Algoritmo     | Silhouette
--------------|-----------
K-Means       | 0.472
DBSCAN        | 0.434
Jerárquico    | 0.516
```

**Conclusión:**  
El clustering jerárquico presenta el mejor desempeño global; sin embargo, K-Means genera clusters
coherentes y cumple el objetivo principal del proyecto.

### Análisis de Clusters  
**Script:** `analizar_clusters.py`

**¿Qué hace?**
- Analiza las características internas de cada cluster.
- Clasifica los clusters según el tipo de trámite predominante.

**Resultados principales:**
- 40% de comunidades buscan Personería Jurídica.
- 32% corresponden a trámites de membresía.
- Clusters con alta homogeneidad interna.

### Visualización de Resultados

Las visualizaciones permiten validar e interpretar el clustering:

- Distribución de clusters en 2D (PCA).
- Tamaño de clusters.
- Pedido predominante por cluster.
- Mapas de similitud y redes de comunidades.

Estas figuras demuestran visualmente que las comunidades con pedidos similares se agrupan correctamente.

## Descripción de los Archivos de Resultados

A continuación, se describe la finalidad de los principales archivos generados por el modelo, con el objetivo de facilitar su interpretación y evaluación.

### Archivos clave del análisis

- **matriz_clustering_final.csv**  
Matriz binaria de tamaño 712 × 153 que representa la relación entre comunidades y pedidos administrativos. Es la base principal para la aplicación de los algoritmos de clustering.

- **diagnostico_resultados.txt**  
Contiene los resultados del diagnóstico inicial de los datos originales, incluyendo conteo de valores nulos, duplicados e inconsistencias detectadas.

- **verificacion_preprocesamiento.txt**  
Archivo de validación que confirma que el proceso de limpieza y preprocesamiento eliminó correctamente los valores nulos y errores críticos.

- **estadisticas_matriz.txt**  
Presenta métricas descriptivas de la matriz binaria, como densidad, número promedio de pedidos por comunidad y distribución de valores.

- **comparacion_algoritmos.txt**  
Resume la comparación entre K-Means, DBSCAN y Clustering Jerárquico utilizando la métrica Silhouette.

- **resumen_analisis_clustering.txt**  
Documento de apoyo que sintetiza los principales hallazgos del análisis de clustering.

- **analisis_caracteristicas_clusters.csv**  
Archivo que describe las características principales de cada cluster, incluyendo el tipo de trámite predominante.

- **analisis_matriz_detallado.txt**  
Análisis profundo de la estructura de la matriz binaria y sus implicaciones para el clustering.

## Orden de Ejecución del Proyecto

Para ejecutar completamente el análisis desde los datos originales, los scripts deben ejecutarse en el siguiente orden:

1. **diagnostico.py**  
Analiza la calidad de los datos originales y genera el diagnóstico inicial.

2. **preprocesamiento.py**  
Limpia y normaliza los datos, generando archivos CSV listos para el análisis.

3. **matriz_clustering.py**  
Construye la matriz binaria comunidades × pedidos administrativos.

4. **comparar_algoritmos.py**  
Evalúa distintos algoritmos de clustering y determina el más adecuado.

5. **clustering_comunidades.py**
Aplica el modelo de clustering seleccionado y asigna comunidades a clusters.

6. **analizar_clusters.py**  
Analiza las características internas de cada cluster.

8. **visualizacion.py** y **visualizacion_comunidades_compartidas.py**  
Generan las visualizaciones utilizadas para interpretar los resultados.

> Nota: No es obligatorio ejecutar nuevamente los scripts, ya que los resultados finales se encuentran almacenados en la carpeta `data/results/`.

## ¿Cómo Usar este Proyecto?

### Para evaluación o revisión:
- Revisar los archivos en `data/results/`.
- Analizar los gráficos en `visualizaciones/`.
- Leer los archivos `.txt` con resultados y métricas.

### Para ejecutar el proyecto
1. Instalar Python 3.9 o superior.
2. Instalar dependencias:
bash pip install -r requirements.txt

## Resultados Finales del Proyecto 
El modelo de clustering permitió identificar patrones claros en los trámites administrativos realizados por comunidades, pueblos y organizaciones registradas en la SGDPN. Los principales resultados obtenidos son:
 - Identificación de **9 clusters** de comunidades con comportamientos administrativos similares.
 - Valor máximo de **Silhouette = 0.516**, indicando una estructura de agrupamiento adecuada.
 - Agrupación correcta de **218 pares de comunidades con pedidos idénticos**.
 - Predominio de trámites relacionados con:
 - Personería jurídica (40%)
 - Membresía y actualización de registros (32%)
Estos resultados evidencian que los procesos administrativos presentan patrones repetitivos que pueden ser aprovechados para mejorar la planificación institucional y la atención a las comunidades.
