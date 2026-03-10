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
        # 1. Obtener datos de información de estaciones (Nombre, Lat, Lon)
        resp_info = requests.get(url_info).json()
        df_info = pd.DataFrame(resp_info['data']['stations'])
        
        # 2. Obtener datos de estado (Bicis disponibles, anclajes libres)
        resp_status = requests.get(url_status).json()
        df_status = pd.DataFrame(resp_status['data']['stations'])

        # 3. Unir ambos DataFrames usando 'station_id'
        # Esto combina la ubicación física con el estado actual
        df_completo = pd.merge(df_info, df_status, on="station_id")

        # Limpieza básica siguiendo tu lógica de optimización
        columnas_utiles = [
            'station_id', 'name', 'lat', 'lon', 'capacity', 
            'num_bikes_available', 'num_docks_available', 'status'
        ]
        df_completo = df_completo[columnas_utiles]

        return df_completo

    except Exception as e:
        st.error(f"Error al conectar con la API de Ecobici: {e}")
        return pd.DataFrame()

def procesar_datos_historicos(df_historico):
    """
    Aplica la lógica de transformación que tenías en tu Jupyter 
    a los datos de viajes (CSV).
    """
    df = df_historico.copy()
    
    # Convertir fechas
    df['Fecha_Retiro'] = pd.to_datetime(df['Fecha_Retiro'], dayfirst=True)
    
    # Extraer componentes como en tu cuaderno
    df['Hora_Retiro_H'] = pd.to_datetime(df['Hora_Retiro'], format='%H:%M:%S').dt.hour
    df['Mes_Retiro'] = df['Fecha_Retiro'].dt.month
    df['Dia_Semana'] = df['Fecha_Retiro'].dt.day_name()
    
    return df
