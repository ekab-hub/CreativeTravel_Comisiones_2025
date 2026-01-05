from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data_work"
OUT = BASE / "data_processed"

FILES = {
    "historico": DATA / "historico.xlsx",
    "mexico": DATA / "mexico.xlsx",
    "monterrey": DATA / "monterrey.xlsx",
}

# ==============================
# Parámetros de negocio
# ==============================
COM_LOW = 0.10
COM_HIGH = 0.15
COM_MID = 0.125

TOL = 0.15          # tolerancia sobre el mínimo esperado
OUTLIER_UP = 1.20   # 20% arriba del máximo esperado


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    return df


def load_excel(path: Path, force_office: str | None = None) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="Hoja1")
    df = clean_columns(df)
    if force_office:
        df["Oficina"] = force_office
    df["source_file"] = path.name
    return df


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ==============================
    # STS / CANCELACIÓN
    # ==============================
    df["sts"] = df.get("Sts").astype(str).str.strip()
    df["es_cancelado"] = df["sts"].str.upper().eq("XLD")
    df["es_activo"] = ~df["es_cancelado"]

    # ==============================
    # FECHA DE NEGOCIO
    # ==============================
    df["estancia"] = pd.to_datetime(df.get("Estancia"), errors="coerce")
    df["anio_estancia"] = df["estancia"].dt.year
    df["estancia_valida"] = df["estancia"].notna()
    df["es_2025"] = df["anio_estancia"] == 2025

    # ==============================
    # OFICINA
    # ==============================
    df["oficina_norm"] = df.get("Oficina").replace({
        "Mty": "Monterrey",
        "BK Mex": "Mexico",
        "Ext": "Mexico",
    })

    # ==============================
    # NOCHES
    # ==============================
    df["num_noches"] = pd.to_numeric(df.get("Num Ntes"), errors="coerce")

    # ==============================
    # VENTA (USD)
    # ==============================
    df["venta_usd"] = pd.to_numeric(df.get("Aprox in USD"), errors="coerce")
    df["venta_usd_missing"] = df["venta_usd"].isna()

    # ==============================
    # RECIBIDO (USD)
    # ==============================
    df["recibido_usd"] = pd.to_numeric(df.get("Monto USD"), errors="coerce")
    df["recibido_usd_missing"] = df["recibido_usd"].isna()

    # Fecha recibida (auxiliar, puede estar mal capturada)
    df["fecha_pago"] = pd.to_datetime(df.get("Recibida"), errors="coerce")

    # ==============================
    # FUENTE DE VERDAD: RECIBIDO
    # ==============================
    df["es_recibido"] = (
        df["sts"].str.upper().eq("OK")
        | df["fecha_pago"].notna()
    )

    # ==============================
    # COMISIÓN ESPERADA
    # ==============================
    df["com_esp_low"] = df["venta_usd"] * COM_LOW
    df["com_esp_mid"] = df["venta_usd"] * COM_MID
    df["com_esp_high"] = df["venta_usd"] * COM_HIGH

    # Gap contra esperado medio
    df["gap_mid_usd"] = df["com_esp_mid"] - df["recibido_usd"]

    # ==============================
    # CLASIFICACIÓN FINANCIERA
    # ==============================
    def classify(row):
        if row["es_cancelado"]:
            return "CANCELADO"

        venta = row["venta_usd"]
        rec = row["recibido_usd"]
        low = row["com_esp_low"]
        high = row["com_esp_high"]

        if pd.isna(venta) or venta <= 0:
            return "VENTA_USD_FALTANTE"

        if not row["es_recibido"]:
            return "PENDIENTE"

        # Ya se considera recibido (por STS OK o fecha)
        if pd.isna(rec) or rec <= 0:
            return "PARCIAL"

        if rec >= (1 - TOL) * low:
            if rec > OUTLIER_UP * high:
                return "COBRADO_OUTLIER"
            return "COBRADO"

        return "PARCIAL"

    df["estatus_cobro"] = df.apply(classify, axis=1)

    return df


def main():
    OUT.mkdir(exist_ok=True)

    dfs = []
    dfs.append(normalize(load_excel(FILES["historico"])))
    dfs.append(normalize(load_excel(FILES["mexico"])))
    dfs.append(normalize(load_excel(FILES["monterrey"], force_office="Mty")))

    df_all = pd.concat(dfs, ignore_index=True)

    # Dataset 2025:
    # - Incluye estancias 2025
    # - + NO descarta registros sin estancia válida
    df_2025 = df_all[df_all["es_2025"] | ~df_all["estancia_valida"]].copy()

    df_2025.to_csv(OUT / "comisiones_2025_final.csv", index=False)

    print("Archivo generado: comisiones_2025_final.csv")
    print("Total filas:", len(df_2025))
    print("\nConteo estatus_cobro:")
    print(df_2025["estatus_cobro"].value_counts(dropna=False))
    print("\nCancelados (XLD):", int(df_2025["es_cancelado"].sum()))
    print("Activos:", int(df_2025["es_activo"].sum()))

# === REDONDEO FINAL (solo presentación) ===
cols_to_round = [
    "venta_usd",
    "recibido_usd",
    "com_esp_low",
    "com_esp_mid",
    "com_esp_high",
    "gap_mid_usd",
]

for c in cols_to_round:
    if c in df_2025.columns:
        df_2025[c] = df_2025[c].round(2)


if __name__ == "__main__":
    main()
