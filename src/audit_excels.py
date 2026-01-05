from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data_work"

FILES = {
    "historico": DATA / "historico.xlsx",
    "mexico": DATA / "mexico.xlsx",
    "monterrey": DATA / "monterrey.xlsx",
}

KEYWORDS = {
    "fecha": ["fecha", "date", "emision", "pago", "travel", "viaje", "salida", "regreso"],
    "monto": ["monto", "importe", "total", "comision", "commission", "mxn", "usd"],
    "pago": ["pagado", "pago", "paid", "estatus", "status", "cobrado", "pendiente"],
    "agente": ["agente", "vendedor", "sales", "asesor", "ejecutivo"],
    "oficina": ["oficina", "sucursal", "city", "location"],
}

def score_columns(cols):
    cols_l = [c.lower().strip() for c in cols]
    hits = {k: [] for k in KEYWORDS}
    for c in cols_l:
        for k, words in KEYWORDS.items():
            if any(w in c for w in words):
                hits[k].append(c)
    return hits

def audit_file(label, path: Path):
    print("\n" + "="*80)
    print(f"{label.upper()} -> {path}")
    if not path.exists():
        print("!! NO EXISTE")
        return

    xls = pd.ExcelFile(path)
    print("Hojas:", xls.sheet_names)

    for sheet in xls.sheet_names:
        # Leemos pocas filas para detectar encabezados reales
        df_head = pd.read_excel(path, sheet_name=sheet, nrows=25)
        print("\n---")
        print(f"Sheet: {sheet}")
        print(f"Shape(head): {df_head.shape}")
        print("Columnas detectadas:")
        print(list(df_head.columns))

        hits = score_columns(df_head.columns.astype(str))
        print("Posibles columnas clave (por palabra):")
        for k, v in hits.items():
            if v:
                print(f"  - {k}: {v}")

if __name__ == "__main__":
    for label, path in FILES.items():
        audit_file(label, path)
