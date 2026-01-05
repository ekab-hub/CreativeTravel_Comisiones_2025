from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data_processed"

df = pd.read_csv(DATA / "comisiones_2025_usd.csv")

# Base 2025 oficial
df_2025 = df[(df["es_2025"] == True) & (df["estancia_valida"] == True)].copy()

# Asegurar numérico
df_2025["monto_usd"] = pd.to_numeric(df_2025["monto_usd"], errors="coerce")
df_2025["monto_original"] = pd.to_numeric(df_2025["monto_original"], errors="coerce")

unpaid = df_2025[df_2025["status_pago"] == "NO_PAGADO"].copy()

print("="*80)
print("AUDIT PIPELINE NO_PAGADO (2025)")
print("="*80)

print("Registros NO_PAGADO:", len(unpaid))
print("monto_usd NaN:", unpaid["monto_usd"].isna().sum())
print("monto_usd == 0:", (unpaid["monto_usd"] == 0).sum())
print("monto_usd > 0:", (unpaid["monto_usd"] > 0).sum())
print("Suma monto_usd:", unpaid["monto_usd"].dropna().sum())

print("\nDescribe monto_usd (NO_PAGADO):")
print(unpaid["monto_usd"].describe())

print("\nTop 20 NO_PAGADO por monto_usd (si existen):")
top = unpaid.dropna(subset=["monto_usd"]).sort_values("monto_usd", ascending=False).head(20)
cols = ["Agente", "oficina_norm", "estancia", "monto_original", "monto_usd", "roe", "Recibida"]
# Recibida puede no existir como columna cruda (porque normalizamos a fecha_pago),
# así que mostramos fecha_pago si está.
if "Recibida" not in top.columns and "fecha_pago" in top.columns:
    cols[-1] = "fecha_pago"
print(top[[c for c in cols if c in top.columns]].to_string(index=False))
