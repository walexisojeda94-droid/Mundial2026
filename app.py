import streamlit as st
import pandas as pd
import re

# 1. Configuración de la página
st.set_page_config(page_title="Polla Mundial 2026", page_icon="🏆", layout="wide")

# --- PEGA TU LINK AQUÍ ---
LINK_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1cqMfWRdFWjMnVcI_17VMFRblWYHcvbW2VjNS8XdKjwg/edit?gid=539674599#gid=539674599"

def cargar_datos(url):
    try:
        # Buscamos el ID de la hoja usando una expresión regular (más seguro)
        match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
        if match:
            sheet_id = match.group(1)
            # Intentamos cargar la pestaña 'Resultados'
            url_directa = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&sheet=Resultados"
            return pd.read_excel(url_directa)
        else:
            st.error("No se encontró un ID válido en el enlace de Google Sheets.")
            return None
    except Exception as e:
        # Si falla por el nombre de la pestaña, intentamos cargar la primera por defecto
        try:
            sheet_id = re.search(r"/d/([a-zA-Z0-9-_]+)", url).group(1)
            url_simple = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
            return pd.read_excel(url_simple)
        except:
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
        # Limpieza básica
        df = df_raw.copy()
        
        # Validar que existan las columnas
        if 'Jugador' in df.columns and 'Puntos Totales' in df.columns:
            df = df.dropna(subset=['Jugador', 'Puntos Totales'])
            df['Puntos Totales'] = pd.to_numeric(df['Puntos Totales']).fillna(0).astype(int)
            
            # Ordenar
            df = df.sort_values(by="Puntos Totales", ascending=False).reset_index(drop=True)
            df['Pos'] = df.index + 1
            df['Pos'] = df['Pos'].apply(lambda x: f"🥇 {x}" if x == 1 else (f"🥈 {x}" if x == 2 else (f"🥉 {x}" if x == 3 else f"{x}")))

            # Métricas
            col_a, col_b = st.columns(2)
            leader = df.iloc[0]
            col_a.metric("Líder Actual 👑", leader['Jugador'])
            col_b.metric("Puntos", f"{leader['Puntos Totales']} pts")
            
            st.write("---")

            # Tabla
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.table(df[['Pos', 'Jugador', 'Puntos Totales']])
        else:
            st.error("Asegúrate de que las columnas en tu Excel se llamen exactamente 'Jugador' y 'Puntos Totales'")
            
    except Exception as e:
        st.error(f"Error al procesar los datos: {e}")
else:
    st.info("Configura el enlace de Google Sheets en el código para comenzar.")

st.divider()
st.caption("⚽ Datos sincronizados desde Google Sheets.")
