import streamlit as st

st.set_page_config(
    page_title="Creative Travel | Comisiones 2025",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personalizado para mejorar la visualización
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Fuentes principales */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Títulos principales */
    h1 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        color: #1a1a2e !important;
        letter-spacing: -0.5px;
        margin-bottom: 1rem;
    }
    
    /* Subtítulos */
    h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        color: #16213e !important;
        letter-spacing: -0.3px;
    }
    
    /* Texto general */
    p, li, div {
        font-family: 'Inter', sans-serif !important;
        color: #2c3e50 !important;
        line-height: 1.6;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    [data-testid="stSidebar"] [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        color: #1a1a2e !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: #5a6c7d !important;
    }
    
    /* Botones */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Tabs */
    [data-baseweb="tab-list"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Captions */
    .stCaption {
        font-family: 'Inter', sans-serif !important;
        color: #6c757d !important;
        font-style: italic;
    }
    
    /* Dividers */
    hr {
        border: none;
        border-top: 2px solid #e9ecef;
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Creative Travel — Dashboard Comisiones 2025")
st.markdown(
    """
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem;'>
        <p style='color: white; margin: 0; font-size: 1.1rem; font-weight: 500;'>
            📊 Este dashboard está pensado para uso interno.
        </p>
        <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.95rem;'>
            <strong>Nota:</strong> el repo es público pero <strong>los datos NO se incluyen</strong>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("### ¿Qué puedes ver aquí?")
st.markdown(
    """
    <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #667eea;'>
    <ul style='margin: 0; padding-left: 1.5rem;'>
        <li style='margin-bottom: 0.8rem;'><strong style='color: #667eea;'>Executive Overview:</strong> comisión cobrada, reservas, tendencia mensual, estatus.</li>
        <li style='margin-bottom: 0.8rem;'><strong style='color: #667eea;'>Hoteles & Ciudades:</strong> top hoteles, top ciudades, concentración, patrones.</li>
        <li style='margin-bottom: 0.8rem;'><strong style='color: #667eea;'>Agentes:</strong> performance por comisión cobrada y volumen.</li>
        <li style='margin-bottom: 0.8rem;'><strong style='color: #667eea;'>Oficinas:</strong> comparativo México vs Monterrey.</li>
        <li style='margin-bottom: 0.8rem;'><strong style='color: #667eea;'>Finanzas avanzadas:</strong> (opcional) esperado vs recibido.</li>
        <li><strong style='color: #667eea;'>Calidad de datos:</strong> casos para corregir en Excel.</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)
