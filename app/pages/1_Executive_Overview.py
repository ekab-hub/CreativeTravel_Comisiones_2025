import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../CreativeTravel_Comisiones_2025
sys.path.append(str(ROOT))

from app.utils import load_data, apply_filters, kpi_cards

import streamlit as st
import plotly.express as px
import pandas as pd

from app.utils import load_data, apply_filters, kpi_cards

st.set_page_config(page_title="Executive Overview", layout="wide", initial_sidebar_state="expanded")

# CSS personalizado y paleta de colores
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    h1 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        color: #1a1a2e !important;
        letter-spacing: -0.5px;
    }
    
    h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        color: #16213e !important;
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        color: #1a1a2e !important;
        font-size: 1.8rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: #5a6c7d !important;
        font-size: 0.95rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    [data-testid="stSidebar"] [class*="header"] {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        color: #1a1a2e !important;
    }
    </style>
""", unsafe_allow_html=True)

# Paleta de colores para gráficos
COLOR_PALETTE = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'gradient': ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
}

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
st.markdown(
    """
    <div style='background: #f0f4ff; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea; margin-bottom: 1.5rem;'>
        <p style='margin: 0; color: #4a5568; font-size: 0.95rem;'>
            📈 Foco: <strong>comisión cobrada</strong> + volumen de reservas + tendencias. (Finanzas avanzadas está en su propia sección.)
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# KPIs
# ----------------------------
k = kpi_cards(df_f)
col1, col2, col3, col4, col5 = st.columns(5)

col1.markdown(
    f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <p style='color: white; margin: 0; font-size: 0.85rem; font-weight: 500; opacity: 0.9;'>Comisión cobrada (USD)</p>
        <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: 700; font-family: Poppins, sans-serif;'>${k['total_rec']:,.2f}</p>
    </div>
    """,
    unsafe_allow_html=True
)
col2.markdown(
    f"""
    <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1.2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <p style='color: white; margin: 0; font-size: 0.85rem; font-weight: 500; opacity: 0.9;'>Reservas activas</p>
        <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: 700; font-family: Poppins, sans-serif;'>{k['n_reservas']:,}</p>
    </div>
    """,
    unsafe_allow_html=True
)
col3.markdown(
    f"""
    <div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 1.2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <p style='color: white; margin: 0; font-size: 0.85rem; font-weight: 500; opacity: 0.9;'>% reservas cobradas</p>
        <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: 700; font-family: Poppins, sans-serif;'>{k['pct_cobrado']:.1f}%</p>
    </div>
    """,
    unsafe_allow_html=True
)
col4.markdown(
    f"""
    <div style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 1.2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <p style='color: white; margin: 0; font-size: 0.85rem; font-weight: 500; opacity: 0.9;'>Venta total (USD)</p>
        <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: 700; font-family: Poppins, sans-serif;'>${k['total_venta']:,.2f}</p>
    </div>
    """,
    unsafe_allow_html=True
)
col5.markdown(
    f"""
    <div style='background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); padding: 1.2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <p style='color: white; margin: 0; font-size: 0.85rem; font-weight: 500; opacity: 0.9;'>Ticket prom (USD)</p>
        <p style='color: white; margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: 700; font-family: Poppins, sans-serif;'>${k['ticket_prom']:,.2f}</p>
    </div>
    """,
    unsafe_allow_html=True
)

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
    fig = px.bar(by_m, x="mes", y="recibido_usd", hover_data=["reservas"],
                 color_discrete_sequence=[COLOR_PALETTE['primary']])
    fig.update_layout(
        yaxis_title="USD",
        xaxis_title="Mes",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12),
        hovermode='x unified'
    )
    fig.update_traces(marker_line_color='white', marker_line_width=1.5)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Estatus de cobro (conteo)")
    counts = df_f["estatus_cobro"].value_counts().reindex(
        ["COBRADO", "COBRADO_OUTLIER", "PARCIAL", "PENDIENTE"], fill_value=0
    ).reset_index()
    counts.columns = ["estatus", "conteo"]
    color_map = {
        "COBRADO": COLOR_PALETTE['success'],
        "COBRADO_OUTLIER": COLOR_PALETTE['warning'],
        "PARCIAL": COLOR_PALETTE['info'],
        "PENDIENTE": COLOR_PALETTE['danger']
    }
    fig2 = px.pie(counts, names="estatus", values="conteo", hole=0.45,
                  color="estatus", color_discrete_map=color_map)
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12),
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5)
    )
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
                  hover_data=["reservas", "venta_usd"],
                  color="recibido_usd",
                  color_continuous_scale=COLOR_PALETTE['gradient'])
    fig3.update_layout(
        xaxis_title="USD",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=11),
        showlegend=False
    )
    fig3.update_traces(marker_line_color='white', marker_line_width=1)
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
    fig4 = px.bar(off, x="oficina_norm", y="recibido_usd", hover_data=["reservas", "venta_usd"],
                  color="recibido_usd",
                  color_continuous_scale=COLOR_PALETTE['gradient'])
    fig4.update_layout(
        yaxis_title="USD",
        xaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=11),
        showlegend=False
    )
    fig4.update_traces(marker_line_color='white', marker_line_width=1)
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
