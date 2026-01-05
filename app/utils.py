from pathlib import Path
import pandas as pd
import streamlit as st
from app.cleaning import apply_alias_map, normalize_text

BASE = Path(__file__).resolve().parents[1]
DATA_FILE = BASE / "data_processed" / "comisiones_2025_final.csv"
MAPPINGS = BASE / "mappings"

def load_mapping(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["raw", "canonical"])
    df = pd.read_csv(path)
    # tolerancia si el user guarda columnas con mayúsculas raras
    df.columns = [c.strip().lower() for c in df.columns]
    if "raw" not in df.columns or "canonical" not in df.columns:
        return pd.DataFrame(columns=["raw", "canonical"])
    return df[["raw", "canonical"]].dropna(how="all")

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"No encontré el CSV en: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    # Tipos
    if "estancia" in df.columns:
        df["estancia"] = pd.to_datetime(df["estancia"], errors="coerce")

    # numéricos principales
    for c in ["venta_usd", "recibido_usd", "com_esp_low", "com_esp_mid", "com_esp_high"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Solo 2025 financiero (lo que ya definimos como “verdad”)
    df = df[
        (df["es_activo"] == True) &
        (df["estancia_valida"] == True) &
        (df["anio_estancia"] == 2025)
    ].copy()

    # Limpieza de hotel y ciudad (Nivel 1 + alias Nivel 2)
    hotel_alias = load_mapping(MAPPINGS / "hotel_aliases.csv")
    city_alias = load_mapping(MAPPINGS / "city_aliases.csv")

    if "Hotel" in df.columns:
        df["hotel_raw"] = df["Hotel"]
    elif "Hotel  " in df.columns:
        df["hotel_raw"] = df["Hotel  "]
    else:
        df["hotel_raw"] = ""

    if "Ciudad" in df.columns:
        df["ciudad_raw"] = df["Ciudad"]
    else:
        df["ciudad_raw"] = ""

    # normalización base (para agrupar mejor aunque no haya alias)
    df["hotel_norm_base"] = df["hotel_raw"].apply(normalize_text)
    df["ciudad_norm_base"] = df["ciudad_raw"].apply(normalize_text)

    # aplica alias (si existe)
    df["hotel_canon"] = apply_alias_map(df["hotel_raw"], hotel_alias)
    df["ciudad_canon"] = apply_alias_map(df["ciudad_raw"], city_alias)

    # fallback: si canon quedó vacío, usa raw
    df["hotel_canon"] = df["hotel_canon"].fillna(df["hotel_raw"])
    df["ciudad_canon"] = df["ciudad_canon"].fillna(df["ciudad_raw"])

    # Mes
    df["mes"] = df["estancia"].dt.month

    # Para sumas: recibido NaN = 0
    df["recibido_usd"] = df["recibido_usd"].fillna(0)

    return df

def apply_filters(df: pd.DataFrame, oficina, agentes, meses, estatus):
    out = df.copy()
    if oficina != "Todas":
        out = out[out["oficina_norm"] == oficina]
    if agentes:
        out = out[out["Agente"].isin(agentes)]
    if meses:
        out = out[out["mes"].isin(meses)]
    if estatus:
        out = out[out["estatus_cobro"].isin(estatus)]
    return out

def kpi_cards(df: pd.DataFrame):
    total_rec = df["recibido_usd"].sum()
    total_venta = df["venta_usd"].sum()
    n_reservas = len(df)
    ticket_prom = (total_venta / n_reservas) if n_reservas else 0

    # Cobrado% por estatus
    n_cobrado = (df["estatus_cobro"].isin(["COBRADO", "COBRADO_OUTLIER"])).sum()
    pct_cobrado = (n_cobrado / n_reservas) * 100 if n_reservas else 0

    return {
        "total_rec": total_rec,
        "total_venta": total_venta,
        "n_reservas": n_reservas,
        "ticket_prom": ticket_prom,
        "pct_cobrado": pct_cobrado,
    }
