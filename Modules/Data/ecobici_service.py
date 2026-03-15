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
        # 1. Obtener datos de información
        resp_info = requests.get(url_info).json()
        df_info = pd.DataFrame(resp_info['data']['stations'])
        
        # 2. Obtener datos de estado
        resp_status = requests.get(url_status).json()
        df_status = pd.DataFrame(resp_status['data']['stations'])

        # 3. Unir ambos DataFrames
        df_completo = pd.merge(df_info, df_status, on="station_id")

        # 4. Selección segura de columnas (Agregamos las de daños/mantenimiento)
        columnas_deseadas = [
            'station_id', 'name', 'lat', 'lon', 'capacity', 
            'num_bikes_available', 'num_bikes_disabled', # <-- Agregada
            'num_docks_available', 'num_docks_disabled', # <-- Agregada
            'is_renting', 'is_returning'
        ]
        
        columnas_finales = [c for c in columnas_deseadas if c in df_completo.columns]
        df_completo = df_completo[columnas_finales]

        return df_completo

    except Exception as e:
        st.error(f"Error al procesar datos de la API: {e}")
        return pd.DataFrame()
