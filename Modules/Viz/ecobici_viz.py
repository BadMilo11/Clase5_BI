import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt

# Intentamos importar pywaffle de forma segura
try:
    from pywaffle import Waffle
    PYWAFFLE_AVAILABLE = True
except ImportError:
    PYWAFFLE_AVAILABLE = False

def renderizar_mapa_total(df, zoom_level):
    st.subheader("Mapa General de Estaciones")
    centro_lat = df['lat'].mean()
    centro_lon = df['lon'].mean()
    
    view_state = pdk.ViewState(latitude=centro_lat, longitude=centro_lon, zoom=zoom_level)
    layer = pdk.Layer('ScatterplotLayer', df, get_position='[lon, lat]', 
                      get_color='[0, 150, 255, 160]', get_radius=100)
    
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_style=None))

def renderizar_detalle_estacion(df, zoom_level):
    st.subheader("Detalle por Estación")
    
    estacion_seleccionada = st.selectbox("Selecciona una estación:", sorted(df['name'].unique()))
    row = df[df['name'] == estacion_seleccionada].iloc[0]
    
    # Datos de la estación
    vals = {
        'Bicis OK': int(row.get('num_bikes_available', 0)),
        'Bicis Dañadas': int(row.get('num_bikes_disabled', 0)),
        'Puertos OK': int(row.get('num_docks_available', 0)),
        'Puertos Dañados': int(row.get('num_docks_disabled', 0))
    }

    # Métricas
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Bicis OK", vals['Bicis OK'])
    c2.metric("Bicis Mal", vals['Bicis Dañadas'])
    c3.metric("Docks OK", vals['Puertos OK'])
    c4.metric("Docks Mal", vals['Puertos Dañados'])

    st.write("---")
    
    # Lógica del Waffle
    if PYWAFFLE_AVAILABLE:
        try:
            if sum(vals.values()) > 0:
                fig = plt.figure(
                    FigureClass=Waffle,
                    rows=5,
                    values=vals,
                    colors=("#2ecc71", "#e74c3c", "#3498db", "#95a5a6"),
                    legend={'loc': 'upper left', 'bbox_to_anchor': (1, 1)},
                    icons='bicycle',
                    icon_size=15
                )
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.warning("Sin datos de inventario.")
        except Exception as e:
            st.error(f"Error visualizando Waffle: {e}")
            st.info("Mostrando gráfico de barras alternativo:")
            st.bar_chart(pd.Series(vals)) # Opción de respaldo
    else:
        st.error("La librería 'pywaffle' no está instalada correctamente.")
        st.bar_chart(pd.Series(vals))

    st.write("---")
    # Mapa
    view_state = pdk.ViewState(latitude=row['lat'], longitude=row['lon'], zoom=zoom_level, pitch=50)
    layer = pdk.Layer('ScatterplotLayer', df[df['name'] == estacion_seleccionada], 
                      get_position='[lon, lat]', get_color='[200, 30, 0, 200]', get_radius=30)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_style=None))
