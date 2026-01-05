from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data_processed"

df = pd.read_csv(DATA / "comisiones_2025_final.csv")

df_fin = df[
    (df["es_activo"] == True) &
    (df["venta_usd"].notna()) &
    (df["venta_usd"] > 0)
].copy()

# Asegurar numéricos
for c in ["venta_usd", "num_noches"]:
    df_fin[c] = pd.to_numeric(df_fin[c], errors="coerce")

print("="*80)
print("AUDIT VENTAS")
print("="*80)

print("Registros:", len(df_fin))
print("\nventa_usd (Aprox in USD) stats:")
print(df_fin["venta_usd"].describe())

if "num_noches" in df_fin.columns:
    print("\nnum_noches stats:")
    print(df_fin["num_noches"].describe())

# Venta recalculada por noches (si aplica)
if "num_noches" in df_fin.columns:
    df_fin["venta_recalc"] = df_fin["venta_usd"] * df_fin["num_noches"]
    print("\nventa_recalc = Aprox in USD * Num Ntes")
    print(df_fin["venta_recalc"].describe())

    print("\nSUMAS:")
    print("Suma Aprox in USD:", df_fin["venta_usd"].sum())
    print("Suma recalculada:", df_fin["venta_recalc"].sum())
