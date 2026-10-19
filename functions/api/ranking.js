export async function onRequest(context) {
  const sheetId = "1cqMfWRdFWjMnVcI_17VMFRblWYHcvbW2VjNS8XdKjwg";
  const gid = "539674599";
  const source = `https://docs.google.com/spreadsheets/d/${sheetId}/export?format=csv&gid=${gid}`;
  try {
    const upstream = await fetch(source, {
      headers: { "Accept": "text/csv,text/plain;q=0.9,*/*;q=0.8" },
      cf: { cacheTtl: 0, cacheEverything: false }
    });
    if (!upstream.ok) return new Response("No se pudo acceder a Google Sheets.", {
      status: 502, headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" }
    });
    const body = await upstream.text();
    if (body.trimStart().startsWith("<!DOCTYPE html") || body.trimStart().startsWith("<html")) {
      return new Response("Google Sheets no devolvió un CSV. Comprobá que la hoja permita lectura mediante enlace.", {
        status: 502, headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" }
      });
    }
    return new Response(body, { status: 200, headers: {
      "Content-Type": "text/csv; charset=utf-8", "Cache-Control": "no-store, max-age=0", "X-Content-Type-Options": "nosniff"
    }});
  } catch {
    return new Response("Error de conexión al consultar Google Sheets.", {
      status: 502, headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" }
    });
  }
}
