from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data_processed"

df = pd.read_csv(DATA / "comisiones_2025_base.csv")

print("="*80)
print("KPIs GENERALES 2025")
print("="*80)

# --- Filtros base ---
df_valid = df[df["estancia_valida"] == True]
df_2025 = df_valid[df_valid["es_2025"] == True]

# --- KPI 1: Totales ---
total_monto = df_2025["Monto"].sum()
total_pagado = df_2025[df_2025["status_pago"] == "PAGADO"]["Monto"].sum()
total_no_pagado = df_2025[df_2025["status_pago"] == "NO_PAGADO"]["Monto"].sum()

print(f"Total comisiones 2025 (Monto): {total_monto:,.2f}")
print(f"Total PAGADO: {total_pagado:,.2f}")
print(f"Total NO PAGADO: {total_no_pagado:,.2f}")

# --- KPI 2: Por oficina ---
print("\nComisiones por oficina:")
print(
    df_2025.groupby("oficina_norm")["Monto"]
    .sum()
    .sort_values(ascending=False)
)

# --- KPI 3: Ranking de agentes ---
print("\nTop 10 agentes por Monto:")
print(
    df_2025.groupby("Agente")["Monto"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# --- KPI 4: Pipeline pendiente ---
pipeline = df_2025[df_2025["status_pago"] == "NO_PAGADO"]
print("\nPipeline pendiente (NO PAGADO):")
print(f"Registros: {len(pipeline)}")
print(f"Monto pendiente: {pipeline['Monto'].sum():,.2f}")

# --- KPI 5: Meses (estacionalidad) ---
df_2025["mes"] = pd.to_datetime(df_2025["estancia"]).dt.month
print("\nMonto por mes:")
print(
    df_2025.groupby("mes")["Monto"]
    .sum()
    .sort_index()
)

