import streamlit as st
# Sección de importación de módulos
from Modules.UI.header import show_header
from Modules.Data.ecobici_service import cargar_estaciones_ecobici
from Modules.Viz.ecobici_viz import renderizar_mapa_total, renderizar_detalle_estacion

# Sección para crear la GUI
show_header("Mi primera GUI en Streamlit")

st.write(cargar_estaciones_ecobici())

df_estaciones = cargar_estaciones_ecobici()

if not df_estaciones.empty:
    st.write(f"Mostrando {len(df_estaciones)} estaciones activas")
    
    # Ejemplo: Mapa de disponibilidad
    st.map(df_estaciones, latitude='lat', longitude='lon')
    
    # Ejemplo: Ver tabla
    st.dataframe(df_estaciones.head())
    # 2. Sidebar para Navegación
    st.sidebar.title("Navegación")
    opcion = st.sidebar.radio(
        "Selecciona una visualización:",
        ["Mapa General", "Detalle de Estación"]
    )

    # 3. Lógica de despliegue
    if opcion == "Mapa General":
        st.title("🚲 Red Completa Ecobici")
        renderizar_mapa_total(df_estaciones)
        
    elif opcion == "Detalle de Estación":
        st.title("🔍 Análisis de Disponibilidad")
        renderizar_detalle_estacion(df_estaciones)
else:
    st.error("No se pudieron cargar los datos de la API.")
