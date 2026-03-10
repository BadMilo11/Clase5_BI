import streamlit as st
from Modules.UI.header import show_header
from Modules.Data.ecobici_service import cargar_estaciones_ecobici
from Modules.Viz.ecobici_viz import renderizar_mapa_total, renderizar_detalle_estacion

# Configuración de página (debe ser lo primero)
st.set_page_config(page_title="Ecobici Dashboard", layout="wide")

show_header("Mi primera GUI en Streamlit")

# 1. Cargar Datos una sola vez
df_estaciones = cargar_estaciones_ecobici()

if not df_estaciones.empty:
    # 2. Configurar Sidebar primero
    st.sidebar.title("Navegación")
    opcion = st.sidebar.radio(
        "Selecciona una visualización:",
        ["Mapa General", "Detalle de Estación"]
    )

    # 3. Lógica de despliegue según la opción
    if opcion == "Mapa General":
        st.title("🚲 Red Completa Ecobici")
        st.write(f"Mostrando {len(df_estaciones)} estaciones activas")
        renderizar_mapa_total(df_estaciones)
        
        # Opcional: ver tabla solo en el mapa general
        with st.expander("Ver tabla de datos"):
            st.dataframe(df_estaciones)
        
    elif opcion == "Detalle de Estación":
        st.title("🔍 Análisis de Disponibilidad")
        renderizar_detalle_estacion(df_estaciones)
else:
    st.error("No se pudieron cargar los datos de la API.")
