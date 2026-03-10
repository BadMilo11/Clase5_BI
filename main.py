# Sección de importación de módulos
from Modules.UI.header import show_header
from Modules.Data.ecobici_service import cargar_datos_ecobici

# Sección para crear la GUI
show_header("Mi primera GUI en Streamlit")

# Obtienes el DataFrame ya limpio y listo
df_ecobici = cargar_datos_ecobici()

# Ahora puedes aplicar tu lógica de visualización o análisis
print(df_ecobici['Dia_Semana'].value_counts())
 st.write(cargar_datos_ecobici())
