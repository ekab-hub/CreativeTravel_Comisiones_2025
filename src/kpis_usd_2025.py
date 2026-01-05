from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data_processed"

df = pd.read_csv(DATA / "comisiones_2025_usd.csv")

# --- Base 2025 oficial: estancia 2025 con estancia válida ---
df_2025 = df[(df["es_2025"] == True) & (df["estancia_valida"] == True)].copy()

# --- Columnas clave ---
# monto_usd puede ser NaN (no pagado / incompleto); para SUMAS usaremos dropna
df_paid = df_2025[df_2025["status_pago"] == "PAGADO"].copy()
df_unpaid = df_2025[df_2025["status_pago"] == "NO_PAGADO"].copy()

def money_sum(series):
    return pd.to_numeric(series, errors="coerce").dropna().sum()

total_generado_usd = money_sum(df_2025["monto_usd"])
total_pagado_usd = money_sum(df_paid["monto_usd"])
total_no_pagado_usd = money_sum(df_unpaid["monto_usd"])

print("="*80)
print("KPIs GENERALES 2025 (USD)")
print("="*80)

print(f"Registros 2025 (con estancia válida): {len(df_2025)}")
print(f" - Pagados: {len(df_paid)}")
print(f" - No pagados: {len(df_unpaid)}")

print("\nMontos (USD) [solo suma donde monto_usd existe]:")
print(f"Total GENERADO (USD): {total_generado_usd:,.2f}")
print(f"Total PAGADO (USD):   {total_pagado_usd:,.2f}")
print(f"Total NO PAGADO (USD): {total_no_pagado_usd:,.2f}")

# --- Por oficina ---
print("\nComisiones PAGADAS por oficina (USD):")
print(
    df_paid.dropna(subset=["monto_usd"])
    .groupby("oficina_norm")["monto_usd"]
    .sum()
    .sort_values(ascending=False)
)

print("\nComisiones GENERADAS por oficina (USD):")
print(
    df_2025.dropna(subset=["monto_usd"])
    .groupby("oficina_norm")["monto_usd"]
    .sum()
    .sort_values(ascending=False)
)

# --- Ranking agentes (pagado es el principal) ---
print("\nTop 10 agentes por PAGADO (USD):")
print(
    df_paid.dropna(subset=["monto_usd"])
    .groupby("Agente")["monto_usd"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 agentes por GENERADO (USD):")
print(
    df_2025.dropna(subset=["monto_usd"])
    .groupby("Agente")["monto_usd"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# --- Pipeline: NO pagado (conteo + monto conocido) ---
pipeline_known = df_unpaid.dropna(subset=["monto_usd"])
print("\nPipeline NO PAGADO:")
print(f"Registros no pagados (conteo): {len(df_unpaid)}")
print(f"Registros no pagados con monto_usd conocido: {len(pipeline_known)}")
print(f"Monto NO PAGADO conocido (USD): {pipeline_known['monto_usd'].sum():,.2f}")

# --- Estacionalidad por mes (PAGADO vs GENERADO) ---
df_2025["mes"] = pd.to_datetime(df_2025["estancia"], errors="coerce").dt.month
df_paid["mes"] = pd.to_datetime(df_paid["estancia"], errors="coerce").dt.month

print("\nMonto GENERADO por mes (USD):")
print(
    df_2025.dropna(subset=["monto_usd"])
    .groupby("mes")["monto_usd"]
    .sum()
    .sort_index()
)

print("\nMonto PAGADO por mes (USD):")
print(
    df_paid.dropna(subset=["monto_usd"])
    .groupby("mes")["monto_usd"]
    .sum()
    .sort_index()
)
