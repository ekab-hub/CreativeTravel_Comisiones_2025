# Creative Travel — Dashboard de Comisiones 2025

Dashboard interno de análisis de comisiones 2025 para Creative Travel.
El enfoque principal está en la **comisión efectivamente cobrada**, con análisis complementario por **oficina, agente, hotel y ciudad**.

> Este repositorio es público, pero **no incluye datos reales**.
> Los archivos de datos viven localmente y no se exponen por motivos de privacidad.

## Objetivo

Convertir los registros operativos de comisiones en **insights claros y accionables** para la toma de decisiones, respondiendo preguntas como:

- ¿Cuánto se ha cobrado realmente en comisiones en 2025?
- ¿Cómo evoluciona el cobro a lo largo del año?
- ¿Qué oficinas, agentes, hoteles y ciudades generan mayor valor?
- ¿Existe concentración o dependencia en ciertos hoteles o destinos?

El dashboard prioriza **lo cobrado**.
Las métricas de esperado vs recibido existen, pero se tratan como análisis secundarios.

## Contenido del dashboard

### Executive Overview
- Comisión cobrada
- Reservas activas
- % de reservas con comisión cobrada
- Venta total y ticket promedio
- Tendencia mensual
- Rankings por oficina y agente

### Hoteles & Ciudades
- Top hoteles por:
  - Número de reservas
  - Venta generada
  - Comisión cobrada
- Top ciudades
- Análisis de concentración (Top N hoteles)

### Agentes / Oficinas
- Performance y comparativos por volumen y comisión
- Drill-down por hoteles y ciudades (en expansión)

### Finanzas avanzadas
- Comisión esperada (rango 10–15%)
- Pipeline estimado
  (sección secundaria, no foco principal)

### Calidad de datos
- Detección de inconsistencias
- Apoyo para corrección de registros operativos

## Estructura del repositorio

- `app/` — Aplicación Streamlit multi-page
- `src/` — ETL y cálculo de KPIs
- `mappings/` — Alias para normalización de hoteles y ciudades

## Tecnologías

- Python
- Pandas
- Streamlit
- Plotly

## Ejecución local

Para ejecutar el dashboard se requiere contar con los datos de forma local (no incluidos en este repositorio).

1) Instalar dependencias:
- `pip install -r requirements.txt`

2) Ejecutar:
- `streamlit run app/Home.py`

Nota: el archivo `data_processed/comisiones_2025_final.csv` debe existir localmente.

## Privacidad

Este repositorio muestra **arquitectura, lógica analítica y visualización**,
pero **no expone información sensible ni archivos operativos reales**.

