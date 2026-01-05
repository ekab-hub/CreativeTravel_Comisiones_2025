import re
import unicodedata
import pandas as pd

def _strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(c)
    )

def normalize_text(x) -> str:
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return ""
    s = str(x).strip()
    s = re.sub(r"\s+", " ", s)         # colapsa espacios
    s = _strip_accents(s)              # quita acentos
    s = s.lower()
    # pequeñas normalizaciones comunes
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9 ]+", "", s)  # quita signos raros
    s = re.sub(r"\s+", " ", s).strip()
    return s

def apply_alias_map(series: pd.Series, alias_df: pd.DataFrame) -> pd.Series:
    """
    alias_df: columnas raw, canonical
    Se aplica después de normalize_text(raw) para matcheo robusto.
    """
    if alias_df is None or alias_df.empty:
        return series

    m = {}
    for _, r in alias_df.iterrows():
        raw = normalize_text(r["raw"])
        canon = str(r["canonical"]).strip()
        if raw:
            m[raw] = canon

    def _map_one(v):
        key = normalize_text(v)
        return m.get(key, v)

    return series.apply(_map_one)
