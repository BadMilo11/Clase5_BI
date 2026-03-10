import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
from pywaffle import Waffle

def renderizar_mapa_total(df, zoom_level):
    """Muestra un mapa con todas las estaciones con limpieza de tipos de datos."""
    st.subheader("Mapa General de Estaciones")
    
    # 1. Limpieza de datos: Convertimos las columnas del DF a tipos estándar de Python
    # Esto evita que Pydeck encuentre objetos de numpy que no sabe serializar
    df_mapa = df[['lat', 'lon']].copy()
    df_mapa['lat'] = df_mapa['lat'].astype(float)
    df_mapa['lon'] = df_mapa['lon'].astype(float)
    
    # 2. Cálculo de centroide forzado a float nativo
    c_lat = float(df_mapa['lat'].mean())
    c_lon = float(df_mapa['lon'].mean())
    
    view_state = pdk.ViewState(
        latitude=c_lat,
        longitude=c_lon,
        zoom=int(zoom_level), # Forzamos a entero
        pitch=0
    )
    
    layer = pdk.Layer(
        'ScatterplotLayer',
        df_mapa, # Usamos el dataframe limpio
        get_position='[lon, lat]',
        get_color='[0, 150, 255, 160]',
        get_radius=100,
    )
    
    # Intentamos renderizar con un estilo predeterminado simple
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=None
    ))

def renderizar_detalle_estacion(df, zoom_level):
    """Detalle por estación con Waffle Chart y Mapa Seguro."""
    st.subheader("Detalle por Estación")
    
    lista_estaciones = sorted(df['name'].unique())
    estacion_seleccionada = st.selectbox("Selecciona una estación:", lista_estaciones)
    
    row = df[df['name'] == estacion_seleccionada].iloc[0]
    
    # Extraer valores para métricas
    bicis_ok = int(row.get('num_bikes_available', 0))
    bicis_bad = int(row.get('num_bikes_disabled', 0))
    docks_ok = int(row.get('num_docks_available', 0))
    docks_bad = int(row.get('num_docks_disabled', 0))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Bicis OK", bicis_ok)
    c2.metric("Bicis Mal", bicis_bad)
    c3.metric("Docks OK", docks_ok)
    c4.metric("Docks Mal", docks_bad)

    # Gráfico de Waffle
    st.write("---")
    data_waffle = {
        f'Bicis OK ({bicis_ok})': bicis_ok,
        f'Bicis Mal ({bicis_bad})': bicis_bad,
        f'Docks OK ({docks_ok})': docks_ok,
        f'Docks Mal ({docks_bad})': docks_bad
    }

    if sum(data_waffle.values()) > 0:
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5,
            values=data_waffle,
            colors=("#27ae60", "#e74c3c", "#2ecc71", "#c0392b"),
            legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1)},
            icons='bicycle',
            icon_size=18
        )
        st.pyplot(fig)
        plt.close(fig)

    # Mapa de Detalle Seguro
    st.write("---")
    # Convertimos coordenadas de la fila a float nativo
    det_lat = float(row['lat'])
    det_lon = float(row['lon'])
    
    view_state_det = pdk.ViewState(
        latitude=det_lat,
        longitude=det_lon,
        zoom=int(zoom_level),
        pitch=50
    )
    
    # Dataframe de un solo punto limpio
    df_punto = pd.DataFrame({'lat': [det_lat], 'lon': [det_lon]})
    
    layer_det = pdk.Layer(
        'ScatterplotLayer',
        df_punto,
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 200]',
        get_radius=30,
    )
    
    st.pydeck_chart(pdk.Deck(layers=[layer_det], initial_view_state=view_state_det, map_style=None))
