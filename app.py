import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Mundial 2026", page_icon="🏆", layout="wide")

# 2. Estilo CSS mejorado
st.markdown("""
    <style>
    /* Fondo y tipografía */
    .main { background-color: #0e1117; }
    
    /* Centrar títulos y textos de tabla */
    h1, h4 { text-align: center; font-family: 'Arial Black', sans-serif; }
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        text-align: center !important;
        vertical-align: middle !important;
    }

    /* Hacer el cargador de archivos más compacto en la barra lateral */
    section[data-testid="stSidebar"] {
        width: 250px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL DE CARGA (Arriba a la derecha/Lateral) ---
# Usamos la sidebar para que sea más estético y no ocupe espacio central
with st.sidebar:
    st.header("⚙️ Administración")
    uploaded_file = st.file_uploader("Actualizar Tabla (Excel)", type=["xlsx"])
    st.info("Sube aquí el archivo para refrescar los puntos de la familia.")

# --- CUERPO PRINCIPAL ---
st.write("### 🏆")
st.title("Gran Juego Mundial Familiar")
st.markdown("<h4 style='color: #888;'>Ranking Oficial de la Fase de Grupos</h4>", unsafe_allow_html=True)
st.divider()

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        required_cols = ['Jugador', 'Puntos Totales', 'Aciertos Exactos', 'Partidos Acertados']
        
        if all(col in df.columns for col in required_cols):
            # Lógica de orden y posiciones
            df = df.sort_values(by=["Puntos Totales", "Aciertos Exactos"], ascending=False).reset_index(drop=True)
            df['Pos'] = df.index + 1
            df['Pos'] = df['Pos'].apply(lambda x: f"🥇 {x}" if x == 1 else (f"🥈 {x}" if x == 2 else (f"🥉 {x}" if x == 3 else f"{x}")))

            # Métricas destacadas
            m1, m2, m3 = st.columns(3)
            leader = df.iloc[0]
            m1.metric("Líder 👑", leader['Jugador'])
            m2.metric("Puntos", f"{int(leader['Puntos Totales'])}")
            m3.metric("Plenos 🎯", f"{int(df['Aciertos Exactos'].max())}")
            
            st.write("---")

            # Tabla principal
            df_display = df[['Pos', 'Jugador', 'Puntos Totales', 'Aciertos Exactos', 'Partidos Acertados']]
            st.table(df_display)
            
        else:
            st.error("Error: Las columnas del Excel no coinciden con la plantilla.")
            
    except Exception as e:
        st.error(f"Error al procesar: {e}")
else:
    # Mensaje inicial más limpio
    st.warning("⚠️ Esperando carga de datos desde el panel lateral.")
    ejemplo = pd.DataFrame({
        'Pos': ['-', '-', '-'],
        'Jugador': ['Esperando...', 'Esperando...', 'Esperando...'],
        'Puntos Totales': [0, 0, 0],
        'Aciertos Exactos': [0, 0, 0],
        'Partidos Acertados': [0, 0, 0]
    })
    st.table(ejemplo)

st.divider()
st.caption("⚽ Actualizado por el administrador.")
