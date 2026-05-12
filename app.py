import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Mundial 2026", page_icon="🏆", layout="wide")

# 2. Estilo CSS para centrar y embellecer
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1, h4 { text-align: center; font-family: 'Arial Black', sans-serif; }
    
    /* Forzar el centrado total de la tabla y aumentar tamaño de fuente */
    [data-testid="stTable"] {
        margin-left: auto;
        margin-right: auto;
        font-size: 20px;
    }
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        text-align: center !important;
        vertical-align: middle !important;
        padding: 15px !important;
    }

    section[data-testid="stSidebar"] { width: 250px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL DE CARGA (Lateral) ---
with st.sidebar:
    st.header("⚙️ Administración")
    uploaded_file = st.file_uploader("Actualizar Tabla (Excel)", type=["xlsx"])
    st.info("Sube el Excel con las columnas 'Jugador' y 'Puntos Totales'.")

# --- CUERPO PRINCIPAL ---
st.write("### 🏆")
st.title("Gran Juego Mundial Familiar")
st.markdown("<h4 style='color: #888;'>Ranking de Posiciones</h4>", unsafe_allow_html=True)
st.divider()

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        # Ahora solo requerimos estas dos columnas
        required_cols = ['Jugador', 'Puntos Totales']
        
        if all(col in df.columns for col in required_cols):
            # Limpieza de datos vacíos
            df['Puntos Totales'] = df['Puntos Totales'].fillna(0).astype(int)
            
            # Ordenar por puntaje
            df = df.sort_values(by="Puntos Totales", ascending=False).reset_index(drop=True)
            
            # Crear columna de Posición con medallas
            df['Pos'] = df.index + 1
            df['Pos'] = df['Pos'].apply(lambda x: f"🥇 {x}" if x == 1 else (f"🥈 {x}" if x == 2 else (f"🥉 {x}" if x == 3 else f"{x}")))

            # Métricas destacadas (Líder y puntaje)
            col_a, col_b = st.columns(2)
            leader = df.iloc[0]
            col_a.metric("Líder Actual 👑", leader['Jugador'])
            col_b.metric("Puntos", f"{leader['Puntos Totales']} pts")
            
            st.write("---")

            # Tabla simplificada y centrada
            # Usamos columnas de Streamlit para "centrar" la tabla en el medio de la pantalla
            col_central_1, col_central_2, col_central_3 = st.columns([1, 2, 1])
            with col_central_2:
                df_display = df[['Pos', 'Jugador', 'Puntos Totales']]
                st.table(df_display)
            
        else:
            st.error("Error: El Excel debe tener las columnas: 'Jugador' y 'Puntos Totales'.")
            
    except Exception as e:
        st.error(f"Error al procesar: {e}")
else:
    st.warning("⚠️ Esperando carga de datos.")
    ejemplo = pd.DataFrame({'Pos': ['-'], 'Jugador': ['Esperando...'], 'Puntos Totales': [0]})
    col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
    with col_e2:
        st.table(ejemplo)

st.divider()
st.caption("⚽ ¡Suerte a todos!")
