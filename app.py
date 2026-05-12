import streamlit as st
import pandas as pd

# 1. Configuración de la página (Título en la pestaña del navegador)
st.set_page_config(page_title="Polla Mundial 2026", page_icon="🏆", layout="wide")

# 2. Estilo CSS personalizado para centrar datos y mejorar la visual
st.markdown("""
    <style>
    /* Fondo general */
    .main {
        background-color: #f4f7f6;
    }
    
    /* Títulos */
    h1 {
        color: #1e3d59;
        font-family: 'Arial Black', sans-serif;
        text-align: center;
        padding-bottom: 20px;
    }
    
    /* Centrar el contenido de las tablas */
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        text-align: center !important;
        vertical-align: middle !important;
    }

    /* Estilo para las tarjetas de métricas */
    [data-testid="stMetricValue"] {
        color: #ff6e40;
        justify-content: center;
    }
    
    /* Personalizar el botón de carga */
    .stFileUploader {
        border: 1px solid #1e3d59;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Encabezado principal
st.write("### 🏆")
st.title("Gran Juego Mundial Familiar")
st.markdown("<h4 style='text-align: center; color: #555;'>Ranking Oficial de la Fase de Grupos</h4>", unsafe_allow_html=True)
st.divider()

# 4. Barra lateral o Superior para Carga
with st.container():
    col_t1, col_t2, col_t3 = st.columns([1, 2, 1])
    with col_t2:
        uploaded_file = st.file_uploader("📂 Sube el Excel actualizado aquí", type=["xlsx"])

# 5. Lógica de Datos
if uploaded_file is not None:
    try:
        # Cargar datos
        df = pd.read_excel(uploaded_file)
        
        # Validar columnas necesarias
        required_cols = ['Jugador', 'Puntos Totales', 'Aciertos Exactos', 'Partidos Acertados']
        if all(col in df.columns for col in required_cols):
            
            # Ordenar: 1° por puntos, 2° por aciertos exactos (desempate)
            df = df.sort_values(by=["Puntos Totales", "Aciertos Exactos"], ascending=False).reset_index(drop=True)
            
            # Crear columna de posición con emoji para el podio
            df['Pos'] = df.index + 1
            df['Pos'] = df['Pos'].apply(lambda x: f"🥇 {x}" if x == 1 else (f"🥈 {x}" if x == 2 else (f"🥉 {x}" if x == 3 else f"{x}")))

            # Mostrar destacados arriba (Métricas)
            st.write("---")
            m1, m2, m3 = st.columns(3)
            leader = df.iloc[0]
            m1.metric("Líder Actual 👑", leader['Jugador'])
            m2.metric("Puntaje Máximo", f"{int(leader['Puntos Totales'])} pts")
            m3.metric("Más Aciertos", f"{int(df['Aciertos Exactos'].max())} 🎯")
            
            st.write("---")

            # Mostrar la tabla elegante
            # Reorganizamos columnas para que 'Pos' sea la primera
            df_display = df[['Pos', 'Jugador', 'Puntos Totales', 'Aciertos Exactos', 'Partidos Acertados']]
            
            # Convertir a HTML para tener control total de la visualización (centrado)
            st.table(df_display)
            
        else:
            st.error("El archivo no tiene las columnas correctas. Asegúrate de usar la plantilla.")
            
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
else:
    # Vista previa cuando no hay archivo
    st.info("👆 Por favor, carga el archivo Excel para ver el ranking actualizado.")
    
    # Mostrar una tabla de ejemplo "vacía" o ilustrativa
    ejemplo = pd.DataFrame({
        'Pos': ['-', '-', '-'],
        'Jugador': ['Esperando...', 'Esperando...', 'Esperando...'],
        'Puntos Totales': [0, 0, 0],
        'Aciertos Exactos': [0, 0, 0],
        'Partidos Acertados': [0, 0, 0]
    })
    st.table(ejemplo)

# 6. Pie de página
st.divider()
st.caption("⚽ Creado para la familia - Prohibido enojarse por los resultados.")
