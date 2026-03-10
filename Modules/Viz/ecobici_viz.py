import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
from pywaffle import Waffle

def renderizar_mapa_total(df, zoom_level):
    """Muestra un mapa con todas las estaciones centrado en el centroide."""
    st.subheader("Mapa General de Estaciones")
    
    # FORZAMOS A FLOAT: Esto evita el TypeError en la serialización JSON de pydeck
    centro_lat = float(df['lat'].mean())
    centro_lon = float(df['lon'].mean())
    
    # Aseguramos que el zoom también sea un float/int simple
    zoom_val = float(zoom_level)
    
    view_state = pdk.ViewState(
        latitude=centro_lat,
        longitude=centro_lon,
        zoom=zoom_val,
        pitch=0
    )
    
    layer = pdk.Layer(
        'ScatterplotLayer',
        df,
        get_position='[lon, lat]',
        get_color='[0, 150, 255, 160]',
        get_radius=100,
        pickable=True
    )
    
    # Creamos el objeto deck y lo pasamos a streamlit
    mapa = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=None
    )
    
    st.pydeck_chart(mapa)

def renderizar_detalle_estacion(df, zoom_level):
    """Muestra detalle de una estación con métricas y gráfico de Waffle."""
    st.subheader("Detalle por Estación")
    
    lista_estaciones = sorted(df['name'].unique())
    estacion_seleccionada = st.selectbox("Selecciona una estación:", lista_estaciones)
    
    datos_estacion = df[df['name'] == estacion_seleccionada].iloc[0]
    
    # Métricas
    bicis_ok = int(datos_estacion.get('num_bikes_available', 0))
    bicis_bad = int(datos_estacion.get('num_bikes_disabled', 0))
    docks_ok = int(datos_estacion.get('num_docks_available', 0))
    docks_bad = int(datos_estacion.get('num_docks_disabled', 0))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Bicis OK", bicis_ok)
    c2.metric("Bicis Mal", bicis_bad)
    c3.metric("Docks OK", docks_ok)
    c4.metric("Docks Mal", docks_bad)

    # Gráfico de Waffle (Tu lógica original)
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
            icon_size=18,
            icon_legend=True
        )
        st.pyplot(fig)
        plt.close(fig)

    # Mapa de Detalle (también con conversión a float)
    st.write("---")
    view_state_det = pdk.ViewState(
        latitude=float(datos_estacion['lat']),
        longitude=float(datos_estacion['lon']),
        zoom=float(zoom_level),
        pitch=50
    )
    
    layer_det = pdk.Layer(
        'ScatterplotLayer',
        df[df['name'] == estacion_seleccionada],
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 200]',
        get_radius=30,
    )
    
    st.pydeck_chart(pdk.Deck(layers=[layer_det], initial_view_state=view_state_det, map_style=None))
