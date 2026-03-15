import streamlit as st
import pandas as pd
import plotly.express as px

def render_global_dashboard(df):
    """Muestra los Pie Charts globales y el Top 15 de incidencias."""
    df_plot = df.copy()
    # Limpieza de nombres para que las barras no se vean amontonadas
    df_plot['name_clean'] = df_plot['name'].str[7:] 

    st.header("📊 Estado General de la Red")

    # --- PIE CHARTS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Bicicletas")
        # Usamos sum() directamente sobre las columnas habilitadas en ecobici_service
        total_bicis = [df_plot['num_bikes_available'].sum(), df_plot['num_bikes_disabled'].sum()]
        fig_pie_bikes = px.pie(
            values=total_bicis, 
            names=['Disponibles', 'Dañadas'],
            color_discrete_sequence=["#4C8CB5", "#FF4B4B"],
            hole=0.4
        )
        st.plotly_chart(fig_pie_bikes, use_container_width=True)

    with col2:
        st.subheader("Docks (Puertos)")
        total_docks = [df_plot['num_docks_available'].sum(), df_plot['num_docks_disabled'].sum()]
        fig_pie_docks = px.pie(
            values=total_docks, 
            names=['Disponibles', 'Dañados'],
            color_discrete_sequence=["#B7CBD7", "#333333"],
            hole=0.4
        )
        st.plotly_chart(fig_pie_docks, use_container_width=True)

    # --- TOP 15 INCIDENCIAS ---
    st.markdown("---")
    st.subheader("🏆 Estaciones con más fallos reportados")
    
    # Ranking basado en la suma de ambos tipos de daño
    df_plot['total_danos'] = df_plot['num_bikes_disabled'] + df_plot['num_docks_disabled']
    top_incidencias = df_plot.nlargest(15, 'total_danos')

    fig_bar = px.bar(
        top_incidencias, 
        x='name_clean', 
        y=['num_bikes_disabled', 'num_docks_disabled'],
        barmode='group',
        labels={'value': 'Cantidad', 'variable': 'Tipo de Falla', 'name_clean': 'Estación'},
        color_discrete_map={'num_bikes_disabled': '#FF4B4B', 'num_docks_disabled': '#E67E22'},
        template="plotly_white"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

def render_station_comparison(df, id_estacion):
    """Gráfica de barras apiladas comparando contra la capacidad total."""
    
    # Buscamos la fila de la estación
    row = df[df['station_id'] == id_estacion].iloc[0]
    nombre_estacion = row['name'][7:]

    st.write(f"#### 📊 Análisis de Ocupación: {nombre_estacion}")

    # Estructura para la barra
    df_cap = pd.DataFrame({
        'Categoría': ['Bicis Libres', 'Bicis Mal', 'Docks Libres', 'Docks Mal'],
        'Cantidad': [
            row['num_bikes_available'],
            row['num_bikes_disabled'],
            row['num_docks_available'],
            row['num_docks_disabled']
        ],
        # Creamos una columna auxiliar para el eje Y que sea igual para todos
        'Eje': [f"Capacidad Total: {row['capacity']}"] * 4 
    })

    fig_cap = px.bar(
        df_cap,
        x='Cantidad',
        y='Eje', # Ahora usamos la columna que tiene 4 elementos iguales
        color='Categoría',
        orientation='h',
        color_discrete_map={
            'Bicis Libres': '#4C8CB5',
            'Bicis Mal': '#FF4B4B',
            'Docks Libres': '#B7CBD7',
            'Docks Mal': '#333333'
        },
        height=250,
        text='Cantidad' # Opcional: muestra el número dentro de la barra
    )
    
    fig_cap.update_layout(
        yaxis_title=None, 
        xaxis_title="Número de Unidades",
        legend=dict(orientation="h", yanchor="bottom", y=-0.8, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig_cap, use_container_width=True)
    
    fig_cap.update_layout(
        yaxis_title=None, 
        legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_cap, use_container_width=True)
