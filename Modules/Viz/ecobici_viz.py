import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.graph_objects as go

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
    
    vals = {
        'Bicis OK': int(row.get('num_bikes_available', 0)),
        'Bicis Mal': int(row.get('num_bikes_disabled', 0)),
        'Docks OK': int(row.get('num_docks_available', 0)),
        'Docks Mal': int(row.get('num_docks_disabled', 0))
    }

    # Métricas
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Bicis OK", vals['Bicis OK'])
    c2.metric("Bicis Mal", vals['Bicis Mal'], delta_color="inverse")
    c3.metric("Docks OK", vals['Docks OK'])
    c4.metric("Docks Mal", vals['Docks Mal'], delta_color="inverse")

    st.write("---")
    st.subheader("Distribución de Inventario")

    # Crear un gráfico de barras apiladas horizontal (Alternativa profesional a Waffle)
    fig = go.Figure()
    colores = ['#2ecc71', '#e74c3c', '#3498db', '#95a5a6']
    
    for i, (label, valor) in enumerate(vals.items()):
        fig.add_trace(go.Bar(
            name=label,
            y=["Estado"],
            x=[valor],
            orientation='h',
            marker=dict(color=colores[i])
        ))

    fig.update_layout(
        barmode='stack', 
        height=200, 
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("---")
    # Mapa
    view_state = pdk.ViewState(latitude=row['lat'], longitude=row['lon'], zoom=zoom_level, pitch=50)
    layer = pdk.Layer('ScatterplotLayer', df[df['name'] == estacion_seleccionada], 
                      get_position='[lon, lat]', get_color='[200, 30, 0, 200]', get_radius=30)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, map_style=None))
