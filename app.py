import streamlit as st
import pandas as pd
import re

# ─────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────
st.set_page_config(page_title="Mundial 2026", page_icon="⚽", layout="wide")

LINK_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1cqMfWRdFWjMnVcI_17VMFRblWYHcvbW2VjNS8XdKjwg/edit?gid=539674599#gid=539674599"

PREDICCIONES = {
    "🟦 Jugador 1": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ9slIKhMrDbrowDn4WbtYQ3UXQVpXe3Sj_ESe-13nvJ7yTG1CVwOh7MhaS7MQq7ZAjdD4yQTeQcNw0/pubhtml?gid=828118121&single=true",
    "🟩 Jugador 2": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ9slIKhMrDbrowDn4WbtYQ3UXQVpXe3Sj_ESe-13nvJ7yTG1CVwOh7MhaS7MQq7ZAjdD4yQTeQcNw0/pubhtml?gid=1804906006&single=true",
    "🟨 Jugador 3": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ9slIKhMrDbrowDn4WbtYQ3UXQVpXe3Sj_ESe-13nvJ7yTG1CVwOh7MhaS7MQq7ZAjdD4yQTeQcNw0/pubhtml?gid=2028438095&single=true",
    "🟥 Jugador 4": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ9slIKhMrDbrowDn4WbtYQ3UXQVpXe3Sj_ESe-13nvJ7yTG1CVwOh7MhaS7MQq7ZAjdD4yQTeQcNw0/pubhtml?gid=2007132205&single=true",
}

# ─────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1, h4 { text-align: center; font-family: 'Arial Black', sans-serif; }
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        text-align: center !important;
        vertical-align: middle !important;
    }
    div[data-testid="stHorizontalBlock"] button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# NAVEGACIÓN
# ─────────────────────────────────────────
PAGINAS = ["🏆 Ranking", "🟦 Jugador 1", "🟩 Jugador 2", "🟨 Jugador 3", "🟥 Jugador 4"]

if "pagina" not in st.session_state:
    st.session_state.pagina = "🏆 Ranking"

cols = st.columns(len(PAGINAS))
for i, pag in enumerate(PAGINAS):
    if cols[i].button(pag, use_container_width=True):
        st.session_state.pagina = pag

st.divider()

# ─────────────────────────────────────────
# PÁGINA: RANKING
# ─────────────────────────────────────────
def cargar_datos(url):
    try:
        match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
        if match:
            sheet_id = match.group(1)
            url_directa = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&sheet=Resultados"
            return pd.read_excel(url_directa)
        else:
            st.error("No se encontró un ID válido en el enlace.")
            return None
    except Exception as e:
        try:
            sheet_id = re.search(r"/d/([a-zA-Z0-9-_]+)", url).group(1)
            url_simple = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
            return pd.read_excel(url_simple)
        except:
            st.error(f"Error técnico: {e}")
            return None

if st.session_state.pagina == "🏆 Ranking":
    st.write("### 🏆")
    st.title("Gran Juego Mundial Familiar")
    st.markdown("<h4 style='color: #888;'>Ranking en Vivo</h4>", unsafe_allow_html=True)

    if st.button("🔄 Actualizar Puntos Ahora"):
        st.cache_data.clear()

    st.divider()

    df_raw = cargar_datos(LINK_GOOGLE_SHEETS)

    if df_raw is not None:
        try:
            df = df_raw.copy()
            df.columns = df.columns.astype(str).str.strip()

            col_jugador = next((c for c in df.columns if c.lower() == "jugador"), None)
            col_puntos  = next((c for c in df.columns if "puntos" in c.lower()), None)

            if col_jugador and col_puntos:
                df = df.rename(columns={col_jugador: "Jugador", col_puntos: "Puntos Totales"})
                df = df.dropna(subset=["Jugador"])
                df["Puntos Totales"] = pd.to_numeric(df["Puntos Totales"], errors="coerce").fillna(0).astype(int)
                df = df.sort_values(by="Puntos Totales", ascending=False).reset_index(drop=True)
                df["Pos"] = df.index + 1
                df["Pos"] = df["Pos"].apply(
                    lambda x: f"🥇 {x}" if x == 1 else (f"🥈 {x}" if x == 2 else (f"🥉 {x}" if x == 3 else str(x)))
                )

                if not df.empty:
                    col_a, col_b = st.columns(2)
                    col_a.metric("Líder Actual 👑", df.iloc[0]["Jugador"])
                    col_b.metric("Puntos", f"{df.iloc[0]['Puntos Totales']} pts")

                st.write("---")
                c1, c2, c3 = st.columns([1, 2, 1])
                with c2:
                    st.table(df[["Pos", "Jugador", "Puntos Totales"]])
            else:
                st.error(f"No encontré las columnas. Leí: {list(df.columns)}")
                st.info("Asegurate de que la primera fila tenga los títulos correctos.")

        except Exception as e:
            st.error(f"Error al procesar los datos: {e}")
    else:
        st.info("Configurá el enlace de Google Sheets en el código para comenzar.")

# ─────────────────────────────────────────
# PÁGINAS: PREDICCIONES
# ─────────────────────────────────────────
elif st.session_state.pagina in PREDICCIONES:
    nombre = st.session_state.pagina
    url    = PREDICCIONES[nombre]

    st.title(f"Predicciones — {nombre}")
    st.markdown(
        f"""
        <iframe
            src="{url}"
            width="100%"
            height="900"
            frameborder="0"
            scrolling="yes"
            style="border-radius:10px; border:1px solid #333;">
        </iframe>
        """,
        unsafe_allow_html=True,
    )

st.divider()
st.caption("⚽ ¡Suerte a todos! No vale enojarse 😤 | 🍳 El último en la tabla debe cocinar una comida | 🍮 El anteúltimo el postre o algo dulce 🍰")
