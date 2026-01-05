import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../CreativeTravel_Comisiones_2025
sys.path.append(str(ROOT))

from app.utils import load_data, apply_filters, kpi_cards


import streamlit as st
import plotly.express as px
import pandas as pd

from app.utils import load_data, apply_filters

st.set_page_config(page_title="Hoteles & Ciudades", layout="wide")

df = load_data()

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.header("Filtros")

oficinas = ["Todas"] + sorted([x for x in df["oficina_norm"].dropna().unique().tolist() if x])
oficina = st.sidebar.selectbox("Oficina", oficinas, index=0)

meses = sorted(df["mes"].dropna().unique().astype(int).tolist())
mes_sel = st.sidebar.multiselect("Mes de estancia", meses, default=meses)

estatus_all = ["COBRADO", "COBRADO_OUTLIER", "PARCIAL", "PENDIENTE"]
estatus_sel = st.sidebar.multiselect("Estatus", estatus_all, default=estatus_all)

df_f = apply_filters(df, oficina, agentes=[], meses=mes_sel, estatus=estatus_sel)

st.title("Hoteles & Ciudades — Producción 2025")
st.caption("Rankings por **reservas**, **venta** y **comisión cobrada**. Incluye análisis de concentración (Top 5/10).")

# ----------------------------
# KPIs rápidos
# ----------------------------
total_res = len(df_f)
total_venta = df_f["venta_usd"].sum()
total_rec = df_f["recibido_usd"].sum()

c1, c2, c3 = st.columns(3)
c1.metric("Reservas (activas)", f"{total_res:,}")
c2.metric("Venta total (USD)", f"${total_venta:,.2f}")
c3.metric("Comisión cobrada (USD)", f"${total_rec:,.2f}")

st.divider()

# ----------------------------
# Top Hoteles
# ----------------------------
st.subheader("Top Hoteles")
tab1, tab2, tab3 = st.tabs(["Por # Reservas", "Por Venta (USD)", "Por Comisión Cobrada (USD)"])

hot_base = df_f.copy()
hot_base["hotel_show"] = hot_base["hotel_canon"].fillna("").astype(str).str.strip()
hot_base = hot_base[hot_base["hotel_show"] != ""]

def top_table(group_col, value_col, n=20):
    if value_col == "reservas":
        g = hot_base.groupby(group_col).size().reset_index(name="reservas")
        return g.sort_values("reservas", ascending=False).head(n)
    else:
        g = hot_base.groupby(group_col, as_index=False).agg(**{value_col: (value_col, "sum")})
        return g.sort_values(value_col, ascending=False).head(n)

with tab1:
    top = hot_base.groupby("hotel_show").size().reset_index(name="reservas").sort_values("reservas", ascending=False).head(20)
    fig = px.bar(top, x="reservas", y="hotel_show", orientation="h")
    fig.update_layout(yaxis_title="", xaxis_title="# reservas")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top, use_container_width=True, hide_index=True)

with tab2:
    top = hot_base.groupby("hotel_show", as_index=False).agg(venta_usd=("venta_usd", "sum")).sort_values("venta_usd", ascending=False).head(20)
    top["venta_usd"] = top["venta_usd"].round(2)
    fig = px.bar(top, x="venta_usd", y="hotel_show", orientation="h")
    fig.update_layout(yaxis_title="", xaxis_title="USD")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top, use_container_width=True, hide_index=True)

with tab3:
    top = hot_base.groupby("hotel_show", as_index=False).agg(recibido_usd=("recibido_usd", "sum")).sort_values("recibido_usd", ascending=False).head(20)
    top["recibido_usd"] = top["recibido_usd"].round(2)
    fig = px.bar(top, x="recibido_usd", y="hotel_show", orientation="h")
    fig.update_layout(yaxis_title="", xaxis_title="USD")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(top, use_container_width=True, hide_index=True)

st.divider()

# ----------------------------
# Ciudades
# ----------------------------
st.subheader("Ciudades")
left, right = st.columns(2)

city_base = df_f.copy()
city_base["city_show"] = city_base["ciudad_canon"].fillna("").astype(str).str.strip()
city_base = city_base[city_base["city_show"] != ""]

with left:
    top_city = city_base.groupby("city_show", as_index=False).agg(
        reservas=("city_show", "size"),
        venta_usd=("venta_usd", "sum"),
        recibido_usd=("recibido_usd", "sum"),
    ).sort_values("reservas", ascending=False).head(25)

    fig = px.scatter(
        top_city,
        x="venta_usd",
        y="recibido_usd",
        size="reservas",
        hover_name="city_show",
    )
    fig.update_layout(xaxis_title="Venta (USD)", yaxis_title="Comisión cobrada (USD)")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("**Top 25 ciudades** (reservas / venta / cobrado)")
    top_city_disp = top_city.copy()
    for c in ["venta_usd", "recibido_usd"]:
        top_city_disp[c] = top_city_disp[c].round(2)
    st.dataframe(top_city_disp, use_container_width=True, hide_index=True)

st.divider()

# ----------------------------
# Concentración (Top N)
# ----------------------------
st.subheader("Concentración (riesgo / dependencia)")
n = st.slider("Top N hoteles", min_value=3, max_value=25, value=10, step=1)

by_hotel = hot_base.groupby("hotel_show", as_index=False).agg(
    reservas=("hotel_show", "size"),
    venta_usd=("venta_usd", "sum"),
    recibido_usd=("recibido_usd", "sum"),
).sort_values("venta_usd", ascending=False)

topn = by_hotel.head(n)
share_venta = (topn["venta_usd"].sum() / by_hotel["venta_usd"].sum()) * 100 if by_hotel["venta_usd"].sum() else 0
share_res = (topn["reservas"].sum() / by_hotel["reservas"].sum()) * 100 if by_hotel["reservas"].sum() else 0
share_rec = (topn["recibido_usd"].sum() / by_hotel["recibido_usd"].sum()) * 100 if by_hotel["recibido_usd"].sum() else 0

c1, c2, c3 = st.columns(3)
c1.metric(f"% Venta en Top {n}", f"{share_venta:.1f}%")
c2.metric(f"% Reservas en Top {n}", f"{share_res:.1f}%")
c3.metric(f"% Comisión cobrada en Top {n}", f"{share_rec:.1f}%")

st.caption("Tip: si el Top N concentra demasiado, hay riesgo (dependencia) y oportunidad (negociación).")
