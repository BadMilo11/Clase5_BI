import streamlit as st
import pandas as pd
import plotly.express as px

def render_global_dashboard(df):
    """Muestra los Pie Charts globales y el Top 15 de incidencias."""
    # Limpieza de nombres local para no afectar el DF original fuera de la función
    df_plot = df.copy()
    df_plot['name_clean'] = df_plot['name'].str[7:] 

    st.header("Estado General de la Red EcoBici")

    # --- PIE CHARTS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Disponibilidad de Bicicletas")
        total_bicis = [df_plot['num_bikes_available'].sum(), df_plot['num_bikes_disabled'].sum()]
        fig_pie_bikes = px.pie(
            values=total_bicis, 
            names=['Disponibles', 'Dañadas'],
            color_discrete_sequence=["#4C8CB5", "#FF4B4B"],
            hole=0.4
        )
        st.plotly_chart(fig_pie_bikes, use_container_width=True)

    with col2:
        st.subheader("Disponibilidad de Docks")
        total_docks = [df_plot['num_docks_available'].sum(), df_plot['num_docks_disabled'].sum()]
        fig_pie_docks = px.pie(
            values=total_docks, 
            names=['Disponibles', 'Dañados'],
            color_discrete_sequence=["#B7CBD7", "#333333"],
            hole=0.4
        )
        st.plotly_chart(fig_pie_docks, use_container_width=True)

    # --- TOP 15 INCIDENCIAS ---
    st.subheader("Top 15 Estaciones con más Daños")
    
    # Obtenemos las estaciones con más fallos (sumando ambos tipos de daño para el ranking)
    df_plot['total_danos'] = df_plot['num_bikes_disabled'] + df_plot['num_docks_disabled']
    top_incidencias = df_plot.nlargest(15, 'total_danos')

    fig_bar = px.bar(
        top_incidencias, 
        x='name_clean', 
        y=['num_bikes_disabled', 'num_docks_disabled'],
        title="Estaciones con mayor necesidad de mantenimiento",
        barmode='group',
        labels={'value': 'Cantidad', 'variable': 'Categoría', 'name_clean': 'Estación'},
        color_discrete_map={'num_bikes_disabled': '#FF4B4B', 'num_docks_disabled': '#E67E22'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

def render_station_comparison(df, id_estacion):
    """Muestra la comparación de una estación específica contra su capacidad total."""
    df_estacion = df[df['station_id'] == id_estacion].iloc[0]
    nombre_estacion = df_estacion['name'][7:]

    st.subheader(f"Distribución de Capacidad: {nombre_estacion}")

    # Estructura de datos para Plotly
    df_cap = pd.DataFrame({
        'Categoría': ['Bicis Disponibles', 'Bicis Dañadas', 'Docks Disponibles', 'Docks Dañados'],
        'Cantidad': [
            df_estacion['num_bikes_available'],
            df_estacion['num_bikes_disabled'],
            df_estacion['num_docks_available'],
            df_estacion['num_docks_disabled']
        ]
    })

    fig_cap = px.bar(
        df_cap,
        x='Cantidad',
        y=[f"Capacidad: {df_estacion['capacity']}"], 
        color='Categoría',
        orientation='h',
        color_discrete_map={
            'Bicis Disponibles': '#4C8CB5',
            'Bicis Dañadas': '#FF4B4B',
            'Docks Disponibles': '#B7CBD7',
            'Docks Dañados': '#333333'
        },
        height=300
    )
    
    # Ajustes estéticos para que parezca una barra de progreso
    fig_cap.update_layout(yaxis_title=None, showlegend=True)
    st.plotly_chart(fig_cap, use_container_width=True)
