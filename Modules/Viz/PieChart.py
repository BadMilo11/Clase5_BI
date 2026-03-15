import plotly.express as px
import streamlit as st

def Pie_chart(df):
  # Cálculos globales
  total_bicis_libres = df['num_bikes_available'].sum()
  total_bicis_danadas = df['num_bikes_disabled'].sum()
  total_docks_libres = df['num_docks_available'].sum()
  total_docks_danadas = df['num_docks_disabled'].sum()
  
  col1, col2 = st.columns(2)
  
  with col1:
      st.subheader("Estado Global de Bicicletas")
      fig_bicis = px.pie(
          names=['Disponibles', 'Dañadas'],
          values=[total_bicis_libres, total_bicis_danadas],
          color_discrete_sequence=['#4C8CB5', '#FF4B4B'],
          hole=0.4
      )
      st.plotly_chart(fig_bicis, use_container_width=True)
  
  with col2:
      st.subheader("Estado Global de Docks")
      fig_docks = px.pie(
          names=['Disponibles', 'Dañados'],
          values=[total_docks_libres, total_docks_danadas],
          color_discrete_sequence=['#B7CBD7', '#333333'],
          hole=0.4
      )
      st.plotly_chart(fig_docks, use_container_width=True)
