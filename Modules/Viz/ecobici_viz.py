import streamlit as st
import pandas as pd
import pydeck as pdk

def renderizar_mapa_total(df, zoom_level):
    """Muestra un mapa con todas las estaciones centrado en el centroide."""
    st.subheader("Mapa General de Estaciones")
    
    # Calcular el centroide (promedio) de todas las estaciones
    centro_lat = df['lat'].mean()
    centro_lon = df['lon'].mean()
    
    # Crear los datos para el mapa
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
    """Muestra detalle de una estación con zoom controlado."""
    st.subheader("Detalle por Estación")
    
    lista_estaciones = sorted(df['name'].unique())
    estacion_seleccionada = st.selectbox("Selecciona una estación:", lista_estaciones)
    
    datos_estacion = df[df['name'] == estacion_seleccionada].iloc[0]
    
    # Métricas (tu código actual)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Bicis Disponibles", datos_estacion['num_bikes_available'])
    with col2: st.metric("Bicis Dañadas", datos_estacion.get('num_bikes_disabled', 0))
    with col3: st.metric("Puertos Libres", datos_estacion['num_docks_available'])
    with col4: st.metric("Puertos Dañados", datos_estacion.get('num_docks_disabled', 0))

    # Mapa centrado en la estación seleccionada
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
    
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=None
    )))
