import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
from pywaffle import Waffle

def renderizar_mapa_total(df, zoom_level):
    """Muestra un mapa con todas las estaciones centrado en el centroide."""
    st.subheader("Mapa General de Estaciones")
    
    # Cálculo del centroide
    centro_lat = df['lat'].mean()
    centro_lon = df['lon'].mean()
    
    view_state = pdk.ViewState(
        latitude=centro_lat,
        longitude=centro_lon,
        zoom=zoom_level,
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
    
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=None
    ))

def renderizar_detalle_estacion(df, zoom_level):
    """Muestra detalle de una estación con métricas y gráfico de Waffle."""
    st.subheader("Detalle por Estación")
    
    lista_estaciones = sorted(df['name'].unique())
    estacion_seleccionada = st.selectbox("Selecciona una estación:", lista_estaciones)
    
    datos_estacion = df[df['name'] == estacion_seleccionada].iloc[0]
    
    # 1. Métricas Numéricas
    col1, col2, col3, col4 = st.columns(4)
    bicis_ok = datos_estacion['num_bikes_available']
    bicis_bad = datos_estacion.get('num_bikes_disabled', 0)
    docks_ok = datos_estacion['num_docks_available']
    docks_bad = datos_estacion.get('num_docks_disabled', 0)

    with col1: st.metric("Bicis Disponibles", bicis_ok)
    with col2: st.metric("Bicis Dañadas", bicis_bad, delta_color="inverse")
    with col3: st.metric("Puertos Libres", docks_ok)
    with col4: st.metric("Puertos Dañados", docks_bad, delta_color="inverse")

    # 2. Gráfico de Waffle (Lógica de tu cuaderno)
    st.write("---")
    st.subheader("Distribución de Inventario (Waffle Chart)")
    
    # Preparamos los datos para el Waffle
    data_waffle = {
        f'Bicis OK ({bicis_ok})': bicis_ok,
        f'Bicis Dañadas ({bicis_bad})': bicis_bad,
        f'Puertos OK ({docks_ok})': docks_ok,
        f'Puertos Dañados ({docks_bad})': docks_bad
    }

    # Creamos la figura
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
    st.write("---")

    # 3. Mapa de ubicación
    view_state = pdk.ViewState(
        latitude=datos_estacion['lat'],
        longitude=datos_estacion['lon'],
        zoom=zoom_level,
        pitch=50
    )
    
    layer = pdk.Layer(
        'ScatterplotLayer',
        df[df['name'] == estacion_seleccionada],
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 200]',
        get_radius=30,
    )
    
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_style=None))
