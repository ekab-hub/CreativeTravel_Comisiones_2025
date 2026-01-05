import streamlit as st

st.set_page_config(
    page_title="Creative Travel | Comisiones 2025",
    layout="wide",
)

st.title("Creative Travel — Dashboard Comisiones 2025")
st.write(
    """
    Este dashboard está pensado para uso interno.
    **Nota:** el repo es público pero **los datos NO se incluyen**.
    """
)

st.markdown("### ¿Qué puedes ver aquí?")
st.markdown(
    """
    - **Executive Overview:** comisión cobrada, reservas, tendencia mensual, estatus.
    - **Hoteles & Ciudades:** top hoteles, top ciudades, concentración, patrones.
    - **Agentes:** performance por comisión cobrada y volumen.
    - **Oficinas:** comparativo México vs Monterrey.
    - **Finanzas avanzadas:** (opcional) esperado vs recibido.
    - **Calidad de datos:** casos para corregir en Excel.
    """
)
