import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../CreativeTravel_Comisiones_2025
sys.path.append(str(ROOT))

from app.utils import load_data, apply_filters, kpi_cards

import streamlit as st
import plotly.express as px
import pandas as pd

from app.utils import load_data, apply_filters, kpi_cards

st.set_page_config(page_title="Executive Overview", layout="wide")

df = load_data()

# ----------------------------
# Sidebar filtros globales
# ----------------------------
st.sidebar.header("Filtros")

oficinas = ["Todas"] + sorted([x for x in df["oficina_norm"].dropna().unique().tolist() if x])
oficina = st.sidebar.selectbox("Oficina", oficinas, index=0)

meses = sorted(df["mes"].dropna().unique().astype(int).tolist())
mes_sel = st.sidebar.multiselect("Mes de estancia", meses, default=meses)

agentes_all = sorted(df["Agente"].dropna().unique().tolist())
agentes_sel = st.sidebar.multiselect("Agente", agentes_all, default=[])

estatus_all = ["COBRADO", "COBRADO_OUTLIER", "PARCIAL", "PENDIENTE"]
estatus_sel = st.sidebar.multiselect("Estatus", estatus_all, default=estatus_all)

df_f = apply_filters(df, oficina, agentes_sel, mes_sel, estatus_sel)

# ----------------------------
# Título
# ----------------------------
st.title("Executive Overview — Comisiones 2025")
st.caption("Foco: **comisión cobrada** + volumen de reservas + tendencias. (Finanzas avanzadas está en su propia sección.)")

# ----------------------------
# KPIs
# ----------------------------
k = kpi_cards(df_f)
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Comisión cobrada (USD)", f"${k['total_rec']:,.2f}")
col2.metric("Reservas activas", f"{k['n_reservas']:,}")
col3.metric("% reservas cobradas", f"{k['pct_cobrado']:.1f}%")
col4.metric("Venta total (USD)", f"${k['total_venta']:,.2f}")
col5.metric("Ticket prom (USD)", f"${k['ticket_prom']:,.2f}")

st.divider()

# ----------------------------
# Tendencia mensual: comisión cobrada
# ----------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("Comisión cobrada por mes")
    by_m = (
        df_f.groupby("mes", as_index=False)
        .agg(recibido_usd=("recibido_usd", "sum"),
             reservas=("recibido_usd", "size"))
        .sort_values("mes")
    )
    fig = px.bar(by_m, x="mes", y="recibido_usd", hover_data=["reservas"])
    fig.update_layout(yaxis_title="USD", xaxis_title="Mes")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Estatus de cobro (conteo)")
    counts = df_f["estatus_cobro"].value_counts().reindex(
        ["COBRADO", "COBRADO_OUTLIER", "PARCIAL", "PENDIENTE"], fill_value=0
    ).reset_index()
    counts.columns = ["estatus", "conteo"]
    fig2 = px.pie(counts, names="estatus", values="conteo", hole=0.45)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ----------------------------
# Top listas (agentes + oficinas)
# ----------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Top agentes por comisión cobrada")
    top_a = (
        df_f.groupby("Agente", as_index=False)
        .agg(recibido_usd=("recibido_usd", "sum"),
             reservas=("recibido_usd", "size"),
             venta_usd=("venta_usd", "sum"))
        .sort_values("recibido_usd", ascending=False)
        .head(15)
    )
    fig3 = px.bar(top_a, x="recibido_usd", y="Agente", orientation="h",
                  hover_data=["reservas", "venta_usd"])
    fig3.update_layout(xaxis_title="USD", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)

with c2:
    st.subheader("Oficinas: cobrado + reservas")
    off = (
        df_f.groupby("oficina_norm", as_index=False)
        .agg(recibido_usd=("recibido_usd", "sum"),
             reservas=("recibido_usd", "size"),
             venta_usd=("venta_usd", "sum"))
        .sort_values("recibido_usd", ascending=False)
    )
    fig4 = px.bar(off, x="oficina_norm", y="recibido_usd", hover_data=["reservas", "venta_usd"])
    fig4.update_layout(yaxis_title="USD", xaxis_title="")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ----------------------------
# Tabla ejecutiva (descargable)
# ----------------------------
st.subheader("Tabla ejecutiva (filtrada)")
exec_tbl = df_f[[
    "oficina_norm", "Agente", "estatus_cobro", "estancia", "mes",
    "hotel_canon", "ciudad_canon",
    "venta_usd", "recibido_usd"
]].copy()

# Redondeo presentación
for c in ["venta_usd", "recibido_usd"]:
    exec_tbl[c] = pd.to_numeric(exec_tbl[c], errors="coerce").round(2)

st.dataframe(exec_tbl, use_container_width=True, hide_index=True)

csv = exec_tbl.to_csv(index=False).encode("utf-8")
st.download_button("Descargar CSV (tabla filtrada)", csv, file_name="executive_overview_filtrado.csv", mime="text/csv")
