# Mundial 2026

Versión web estática preparada para Cloudflare Pages.

## Estructura
- `index.html`: interfaz adaptable, navegación, ranking y pestañas de predicciones.
- `functions/api/ranking.js`: endpoint de Cloudflare Pages Functions que obtiene el CSV de resultados de Google Sheets.

## Configuración de Cloudflare Pages
- Framework preset: None
- Production branch: `main`
- Build command: dejar vacío (o `exit 0`)
- Build output directory: `.` (raíz del repositorio)

La función `/api/ranking` necesita que la hoja de resultados permita lectura al servidor mediante enlace. Si no es accesible, la página mostrará un mensaje de error en el ranking.
