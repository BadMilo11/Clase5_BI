import streamlit as st

# La siguiente línea de código es equivalente a print()
st.write("# Hola Mundo")
# Sección de importación de módulos
from Modules.UI.header import show_header

# Sección para crear la GUI
show_header("Mi primera GUI en Streamlit")
