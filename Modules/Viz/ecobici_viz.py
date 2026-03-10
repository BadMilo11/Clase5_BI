import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
from pywaffle import Waffle

def renderizar_mapa_total(df, zoom_level):
    """Mapa de toda la red centrado en el promedio de coordenadas."""
    st.subheader("Mapa General de Estaciones")
    centro_lat, centro_lon = df['lat'].mean(), df['lon'].mean()
    
    view_state = pdk.ViewState(latitude=centro_lat, longitude=centro_lon, zoom=zoom_level)
    layer = pdk.Layer('ScatterplotLayer', df, get_position='[lon, lat]', 
                      get_color='[0, 150, 255, 160]', get_radius=100)
    
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_style=None))

def renderizar_detalle_estacion(df, zoom_level):
    """Detalle, Métricas y Gráfico de Waffle por estación."""
    st.subheader("Detalle por Estación")
    
    # Selector de estación
    estacion_seleccionada = st.selectbox("Selecciona una estación:", sorted(df['name'].unique()))
    row = df[df['name'] == estacion_seleccionada].iloc[0]
    
    # Extraer valores para el Waffle
    bicis_ok = int(row.get('num_bikes_available', 0))
    bicis_bad = int(row.get('num_bikes_disabled', 0))
    docks_ok = int(row.get('num_docks_available', 0))
    docks_bad = int(row.get('num_docks_disabled', 0))

    # 1. Métricas superiores
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Bicis Disponibles", bicis_ok)
    c2.metric("Bicis Dañadas", bicis_bad)
    c3.metric("Puertos Libres", docks_ok)
    c4.metric("Puertos Dañados", docks_bad)

    # 2. Gráfico de Waffle (Lógica de tu código original)
    st.write("---")
    st.write("### 📊 Estado de la Estación (Vista de Inventario)")
    
    # Diccionario de datos para el Waffle
    data = {
        f'Bicis OK ({bicis_ok})': bicis_ok,
        f'Bicis Mal ({bicis_bad})': bicis_bad,
        f'Docks OK ({docks_ok})': docks_ok,
        f'Docks Mal ({docks_bad})': docks_bad
    }

    # Solo creamos la figura si hay algún dato disponible
    if sum(data.values()) > 0:
        fig = plt.figure(
            FigureClass=Waffle,
            rows=5, # Como en tu código
            values=data,
            colors=("#27ae60", "#e74c3c", "#2ecc71", "#c0392b"), # Colores semáforo
            legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1)},
            icons='bicycle', # Icono de bicicleta
            icon_size=18,
            icon_legend=True
        )
        st.pyplot(fig)
        plt.close(fig) # IMPORTANTE: Evita que la memoria se sature
    else:
        st.warning("No hay datos de inventario para graficar en esta estación.")

    # 3. Mapa de ubicación individual
    st.write("---")
    view_state = pdk.ViewState(latitude=row['lat'], longitude=row['lon'], zoom=zoom_level, pitch=50)
    layer = pdk.Layer('ScatterplotLayer', df[df['name'] == estacion_seleccionada], 
                      get_position='[lon, lat]', get_color='[200, 30, 0, 200]', get_radius=30)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_style=None))
