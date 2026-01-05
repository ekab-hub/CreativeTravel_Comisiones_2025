from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data_processed"

# ------------------------------
# Configuración de display
# ------------------------------
pd.options.display.float_format = "{:,.2f}".format

# ------------------------------
# Carga de datos
# ------------------------------
df = pd.read_csv(DATA / "comisiones_2025_final.csv")

# ------------------------------
# Base FINANCIERA correcta (KPIs)
# Regla:
# - Activos (no cancelados)
# - Estancia válida
# - Año de estancia = 2025
# - Venta USD válida y > 0
# ------------------------------
df_fin = df[
    (df["es_activo"] == True) &
    (df["estancia_valida"] == True) &
    (df["anio_estancia"] == 2025) &
    (df["venta_usd"].notna()) &
    (df["venta_usd"] > 0)
].copy()

# Asegurar numéricos
num_cols = [
    "venta_usd",
    "recibido_usd",
    "com_esp_low",
    "com_esp_mid",
    "com_esp_high",
]
for c in num_cols:
    if c in df_fin.columns:
        df_fin[c] = pd.to_numeric(df_fin[c], errors="coerce")

# Lo no recibido cuenta como 0 para sumas
df_fin["recibido_usd"] = df_fin["recibido_usd"].fillna(0)

# ------------------------------
# KPIs globales
# ------------------------------
total_venta = df_fin["venta_usd"].sum()

esp_low = df_fin["com_esp_low"].sum()
esp_mid = df_fin["com_esp_mid"].sum()
esp_high = df_fin["com_esp_high"].sum()

recibido = df_fin["recibido_usd"].sum()

pipeline_low = esp_low - recibido
pipeline_mid = esp_mid - recibido
pipeline_high = esp_high - recibido

print("=" * 80)
print("KPIs DEFINITIVOS 2025 (FILTRO CORRECTO)")
print("=" * 80)
print(f"Registros financieros (2025, activos): {len(df_fin)}")
print(f"Venta total 2025 (USD): {total_venta:,.2f}")

print("\nComisión esperada (USD):")
print(f" - Low  (10%):  {esp_low:,.2f}")
print(f" - Mid (12.5%): {esp_mid:,.2f}")
print(f" - High (15%):  {esp_high:,.2f}")

print(f"\nComisión recibida (USD): {recibido:,.2f}")

print("\nPipeline real (USD) = Esperado - Recibido:")
print(f" - Pipeline Low:  {pipeline_low:,.2f}")
print(f" - Pipeline Mid:  {pipeline_mid:,.2f}")
print(f" - Pipeline High: {pipeline_high:,.2f}")

# ------------------------------
# Por oficina
# ------------------------------
print("\n--- Por oficina (Recibido USD / Pipeline Mid USD) ---")
by_off = (
    df_fin.groupby("oficina_norm")
    .agg(
        recibido_usd=("recibido_usd", "sum"),
        esp_mid=("com_esp_mid", "sum"),
        venta_usd=("venta_usd", "sum"),
        registros=("recibido_usd", "size"),
    )
)
by_off["pipeline_mid"] = by_off["esp_mid"] - by_off["recibido_usd"]
print(by_off.sort_values("recibido_usd", ascending=False))

# ------------------------------
# Top agentes por Pipeline Mid
# ------------------------------
print("\n--- Top 10 agentes por Pipeline Mid (USD) ---")
by_agent = (
    df_fin.groupby("Agente")
    .agg(
        recibido_usd=("recibido_usd", "sum"),
        esp_mid=("com_esp_mid", "sum"),
        venta_usd=("venta_usd", "sum"),
        registros=("recibido_usd", "size"),
    )
)
by_agent["pipeline_mid"] = by_agent["esp_mid"] - by_agent["recibido_usd"]
print(by_agent.sort_values("pipeline_mid", ascending=False).head(10))

# ------------------------------
# Estacionalidad por mes (estancia)
# ------------------------------
df_fin["mes"] = pd.to_datetime(df_fin["estancia"], errors="coerce").dt.month
by_month = (
    df_fin.groupby("mes")
    .agg(
        recibido_usd=("recibido_usd", "sum"),
        esp_mid=("com_esp_mid", "sum"),
        venta_usd=("venta_usd", "sum"),
    )
)
by_month["pipeline_mid"] = by_month["esp_mid"] - by_month["recibido_usd"]

print("\n--- Por mes (Recibido USD / Pipeline Mid USD) ---")
print(by_month.sort_index())

