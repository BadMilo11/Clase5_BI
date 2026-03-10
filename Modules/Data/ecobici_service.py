import pandas as pd
import requests
import streamlit as st

@st.cache_data
def cargar_estaciones_ecobici():
    """
    Carga y cruza la información de estaciones y su estado en tiempo real.
    """
    url_info = "https://gbfs.mex.lyftbikes.com/gbfs/es/station_information.json"
    url_status = "https://gbfs.mex.lyftbikes.com/gbfs/es/station_status.json"

    try:
        # 1. Obtener datos de información (Estático: Nombre, Lat, Lon)
        resp_info = requests.get(url_info).json()
        df_info = pd.DataFrame(resp_info['data']['stations'])
        
        # 2. Obtener datos de estado (Dinámico: Bicis disponibles)
        resp_status = requests.get(url_status).json()
        df_status = pd.DataFrame(resp_status['data']['stations'])

        # 3. Unir ambos DataFrames usando 'station_id'
        df_completo = pd.merge(df_info, df_status, on="station_id")

        # 4. Selección segura de columnas
        # Verificamos cuáles de estas existen realmente para evitar el error "not in index"
        columnas_deseadas = [
            'station_id', 'name', 'lat', 'lon', 'capacity', 
            'num_bikes_available', 'num_docks_available', 'is_renting', 'is_returning'
        ]
        
        # Solo nos quedamos con las columnas que sí están presentes en el resultado
        columnas_finales = [c for c in columnas_deseadas if c in df_completo.columns]
        df_completo = df_completo[columnas_finales]

        return df_completo

    except Exception as e:
        st.error(f"Error al procesar datos de la API: {e}")
        return pd.DataFrame()
