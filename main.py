import streamlit as st
# BLOQUE DE DIAGNÓSTICO
try:
    from Modules.UI.header import show_header
    from Modules.Data.ecobici_service import cargar_estaciones_ecobici
    from Modules.Viz.ecobici_viz import renderizar_mapa_total, renderizar_detalle_estacion
    import Modules.Viz.PieBarChart as pbc
except Exception as e:
    st.error(f"Error crítico de importación: {e}")
    st.stop() # Detiene la app aquí para que leas el error

# Configuración de página (debe ser lo primero)
st.set_page_config(page_title="Ecobici Dashboard", layout="wide")

show_header("Mi primera GUI en Streamlit")

df_estaciones = cargar_estaciones_ecobici()

if not df_estaciones.empty:
    # Sidebar para Navegación y Controles
    st.sidebar.title("Configuración")
    opcion = st.sidebar.radio(
        "Selecciona una visualización:",
        ["Mapa General", "Detalle de Estación"]
    )
    
    # Slider de Zoom (valor min, valor max, valor default)
    zoom_seleccionado = st.sidebar.slider("Nivel de Zoom", 10, 20, 13)

    # Lógica de despliegue
    if opcion == "Mapa General":
        st.title("🚲 Red Completa Ecobici")
        renderizar_mapa_total(df_estaciones)
        pbc.renderizar_mapa_total(df_estaciones, zoom_seleccionado)
        
    elif opcion == "Detalle de Estación":
        st.title("🔍 Análisis de Disponibilidad")
        id_sel = st.selectbox("Selecciona Estación", df['station_id'].values)
        # Para detalle, quizás queremos un zoom inicial más cercano
        renderizar_detalle_estacion(df_estaciones, zoom_seleccionado)
        pbc.render_station_comparison(df, id_sel)
else:
    st.error("No se pudieron cargar los datos.")
