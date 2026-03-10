import streamlit as st

def show_header(text):
   # Layout: logo + title side by side
    col1, col2 = st.columns([1, 6])
    
    with col1:
        st.image("imagenes/UPlogo.jpg", width=200)
        
    with col2:
        st.title(text)
        st.caption("📘 Developed for: *Business Intelligence (Graduate Level)*")
        st.caption("Instructor: Luis Emilio Heimpel Covarrubias (2026), Universidad Panamericana")
