import streamlit as st
import pandas as pd

def renderizar_mapa_total(df):
    """Muestra un mapa con todas las estaciones."""
    st.subheader("Mapa General de Estaciones")
    # Streamlit detecta automáticamente 'lat' y 'lon'
    st.map(df)

def renderizar_detalle_estacion(df):
    """Muestra un selector y métricas detalladas de una estación."""
    st.subheader("Detalle por Estación")
    
    # Selector de estación (Equivalente a tu Dropdown de Colab)
    lista_estaciones = sorted(df['name'].unique())
    estacion_seleccionada = st.selectbox("Selecciona una estación:", lista_estaciones)
    
    # Filtrar datos
    datos_estacion = df[df['name'] == estacion_seleccionada].iloc[0]
    
    # Crear columnas para las métricas (Bicis y Puertos)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Bicis Disponibles", datos_estacion['num_bikes_available'])
    
    with col2:
        # En la API actual, las 'dañadas' se calculan o vienen en campos específicos
        # Si no existe 'num_bikes_disabled', usamos 0 por seguridad
        dañadas = datos_estacion.get('num_bikes_disabled', 0)
        st.metric("Bicis Dañadas", dañadas, delta_color="inverse")
        
    with col3:
        st.metric("Puertos Libres", datos_estacion['num_docks_available'])
        
    with col4:
        puertos_dañados = datos_estacion.get('num_docks_disabled', 0)
        st.metric("Puertos Dañados", puertos_dañados, delta_color="inverse")

    # Mostrar mapa centrado en esa estación específica
    map_data = pd.DataFrame({'lat': [datos_estacion['lat']], 'lon': [datos_estacion['lon']]})
    st.pydeck_chart(create_deck_map(map_data))

def create_deck_map(data):
    """Función auxiliar para un mapa más profesional con zoom cercano."""
    import pydeck as pdk
    return pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=data['lat'][0],
            longitude=data['lon'][0],
            zoom=15,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=50,
            ),
        ],
    )
