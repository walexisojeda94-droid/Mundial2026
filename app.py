import streamlit as st
import pandas as pd
import re

# 1. Configuración de la página
st.set_page_config(page_title="Mundial 2026", page_icon="🏆", layout="wide")

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
        df = df_raw.copy()
        
        # --- MEJORA: Limpiar nombres de columnas ---
        # Esto quita espacios vacíos y pone todo en un formato estándar
        df.columns = df.columns.astype(str).str.strip()
        
        # Buscamos las columnas sin importar si escribiste 'jugador' o 'Jugador'
        col_jugador = next((c for c in df.columns if c.lower() == 'jugador'), None)
        col_puntos = next((c for c in df.columns if 'puntos' in c.lower()), None)

        if col_jugador and col_puntos:
            # Renombramos internamente para que el código funcione siempre
            df = df.rename(columns={col_jugador: 'Jugador', col_puntos: 'Puntos Totales'})
            
            # Quitar filas vacías
            df = df.dropna(subset=['Jugador'])
            
            # Convertir puntos a números (si hay un texto, pone 0)
            df['Puntos Totales'] = pd.to_numeric(df['Puntos Totales'], errors='coerce').fillna(0).astype(int)
            
            # Ordenar
            df = df.sort_values(by="Puntos Totales", ascending=False).reset_index(drop=True)
            df['Pos'] = df.index + 1
            df['Pos'] = df['Pos'].apply(lambda x: f"🥇 {x}" if x == 1 else (f"🥈 {x}" if x == 2 else (f"🥉 {x}" if x == 3 else f"{x}")))

            # Mostrar métricas
            col_a, col_b = st.columns(2)
            if not df.empty:
                leader = df.iloc[0]
                col_a.metric("Líder Actual 👑", leader['Jugador'])
                col_b.metric("Puntos", f"{leader['Puntos Totales']} pts")
            
            st.write("---")

            # Tabla centrada
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.table(df[['Pos', 'Jugador', 'Puntos Totales']])
        else:
            st.error(f"No encontré las columnas. En tu Sheets leí: {list(df.columns)}")
            st.info("Asegúrate de que la primera fila de la pestaña 'Resultados' tenga los títulos.")
            
    except Exception as e:
        st.error(f"Error al procesar los datos: {e}")
else:
    st.info("Configura el enlace de Google Sheets en el código para comenzar.")

st.divider()
st.caption(⚽ ¡Suerte a todos! "No vale enojarse" ⚽)
