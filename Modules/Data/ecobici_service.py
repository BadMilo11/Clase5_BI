import pandas as pd

def cargar_datos_ecobici():
    """
    Carga y limpia los datos de Ecobici siguiendo la lógica del cuaderno original.
    Retorna un DataFrame procesado.
    """
    # URLs de los archivos originales en el repositorio
    urls = [
        "https://raw.githubusercontent.com/PameCardoso/Hito_1_Equipo_10/main/2023-01.csv",
        "https://raw.githubusercontent.com/PameCardoso/Hito_1_Equipo_10/main/2023-02.csv",
        "https://raw.githubusercontent.com/PameCardoso/Hito_1_Equipo_10/main/2023-03.csv"
    ]
    
    # 1. Carga de datos
    li = []
    for url in urls:
        # Se asume que el separador es coma y se manejan posibles errores de tipos
        df_temp = pd.read_csv(url, index_col=None, header=0, low_memory=False)
        li.append(df_temp)

    # 2. Concatenación
    df = pd.concat(li, axis=0, ignore_index=True)

    # 3. Limpieza de columnas (Eliminar las que no se usan según tu lógica)
    columnas_a_eliminar = ['Genero_Usuario', 'Edad_Usuario', 'Bici']
    df.drop(columns=columnas_a_eliminar, inplace=True, errors='ignore')

    # 4. Transformación de fechas y tiempos
    # Convertir a datetime
    df['Fecha_Retiro'] = pd.to_datetime(df['Fecha_Retiro'], dayfirst=True)
    df['Fecha_Arribo'] = pd.to_datetime(df['Fecha_Arribo'], dayfirst=True)
    
    # Extraer componentes temporales
    df['Hora_Retiro_H'] = pd.to_datetime(df['Hora_Retiro'], format='%H:%M:%S').dt.hour
    df['Mes_Retiro'] = df['Fecha_Retiro'].dt.month
    df['Dia_Semana'] = df['Fecha_Retiro'].dt.day_name()

    # 5. Manejo de valores nulos
    # Siguiendo tu cuaderno, eliminamos filas donde falten datos críticos
    df.dropna(subset=['Ciclo_Estacion_Retiro', 'Ciclo_Estacion_Arribo'], inplace=True)
    
    # Convertir IDs de estación a enteros para consistencia
    df['Ciclo_Estacion_Retiro'] = df['Ciclo_Estacion_Retiro'].astype(int)
    df['Ciclo_Estacion_Arribo'] = df['Ciclo_Estacion_Arribo'].astype(int)

    return df

if __name__ == "__main__":
    # Prueba rápida de funcionamiento
    datos = cargar_datos_ecobici()
    print(f"Datos cargados exitosamente. Total de registros: {len(datos)}")
    print(datos.head())
