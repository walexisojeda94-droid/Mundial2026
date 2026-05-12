import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Mundial 2026", page_icon="🏆", layout="wide")

# --- REEMPLAZA CON TU LINK ---
LINK_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1cqMfWRdFWjMnVcI_17VMFRblWYHcvbW2VjNS8XdKjwg/edit?gid=539674599#gid=539674599"

def cargar_datos(url):
    try:
        sheet_id = url.split("/d/")[1].split("/")[0]
        # Agregamos '&sheet=Resultados' para que busque esa pestaña específica
        url_directa = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&sheet=Resultados"
        return pd.read_excel(url_directa)
    except Exception as e:
        st.error(f"Error técnico: {e}")
        return None

# 2. Estilo CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1, h4 { text-align: center; font-family: 'Arial Black', sans-serif; }
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        text-align: center !important;
        vertical-align: middle !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Cuerpo Principal
st.write("### 🏆")
st.title("Gran Juego Mundial Familiar")
st.markdown("<h4 style='color: #888;'>Ranking en Vivo</h4>", unsafe_allow_html=True)

if st.button('🔄 Actualizar Puntos Ahora'):
    st.cache_data.clear()

st.divider()

# Carga de datos
df_raw = cargar_datos(LINK_GOOGLE_SHEETS)

if df_raw is not None:
    try:
        # Limpieza: quitamos filas vacías que pueda tener el Sheets
        df = df_raw.dropna(subset=['Jugador', 'Puntos Totales']).copy()
        
        df['Puntos Totales'] = pd.to_numeric(df['Puntos Totales']).fillna(0).astype(int)
        
        # Ordenar y Posiciones
        df = df.sort_values(by="Puntos Totales", ascending=False).reset_index(drop=True)
        df['Pos'] = df.index + 1
        df['Pos'] = df['Pos'].apply(lambda x: f"🥇 {x}" if x == 1 else (f"🥈 {x}" if x == 2 else (f"🥉 {x}" if x == 3 else f"{x}")))

        # Métricas
        col_a, col_b = st.columns(2)
        leader = df.iloc[0]
        col_a.metric("Líder Actual 👑", leader['Jugador'])
        col_b.metric("Puntos", f"{leader['Puntos Totales']} pts")
        
        st.write("---")

        # Tabla centrada
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.table(df[['Pos', 'Jugador', 'Puntos Totales']])
            
    except Exception as e:
        st.error("No encontré los datos. Asegúrate de que en la pestaña 'Resultados' las columnas sean exactamente: Jugador y Puntos Totales")
else:
    st.error("No se pudo conectar. Verifica que el Google Sheets sea 'Público - Cualquier persona con el enlace'.")
