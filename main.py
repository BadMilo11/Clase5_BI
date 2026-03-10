import streamlit as st
# Sección de importación de módulos
from Modules.UI.header import show_header
from Modules.Data.ecobici_service import cargar_estaciones_ecobici

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
