from datetime import datetime

import feedparser

from config.constants import (
    GEOGRAPHIC_KEYWORDS,
    REQUEST_HEADERS,
)
from utils.text import (
    strip_html,
    detectar_comuna
)


def build_rss_url(
    query: str,
    after: str | None = None,
    before: str | None = None,
) -> str:
    """
    Arma la URL de búsqueda de Google News RSS.

    Args:
        query:  Término de búsqueda.
        after:  Fecha mínima en formato YYYY-MM-DD (opcional).
        before: Fecha máxima en formato YYYY-MM-DD (opcional).

    Returns:
        URL lista para pasarle a feedparser.
    """
    termino = query.replace(" ", "+")
    if after:
        termino += f"+after:{after}"
    if before:
        termino += f"+before:{before}"

    return (
        f"https://news.google.com/rss/search"
        f"?q={termino}&hl=es-419&gl=CL&ceid=CL:es-419"
    )


def parse_publication_date(entry: feedparser.FeedParserDict) -> str:
    """Extrae y formatea la fecha de publicación de una entrada RSS."""
    try:
        return datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
    except Exception:
        return datetime.today().strftime("%Y-%m-%d")


def gets_news(
    query: str,
    crime_type: str,
    max_items: int = 100,
    after: str | None = None,
    before: str | None = None,
) -> list[dict]:
    """
    Descarga y parsea el RSS de Google News para un query dado.

    Returns:
        Lista de diccionarios con los campos:
        titulo, descripcion, fecha, comuna, tipo_delito, fuente, url.
        Solo se incluyen noticias que mencionen Chile o Santiago.
    """
    url = build_rss_url(query, after=after, before=before)
    feed = feedparser.parse(url, request_headers=REQUEST_HEADERS)

    noticias: list[dict] = []

    for entry in feed.entries[:max_items]:
        titulo = strip_html(entry.get("title", ""))
        descripcion = strip_html(entry.get("summary", ""))
        fuente = entry.get("source", {}).get("title", "Desconocida")
        url_noticia = entry.get("link", "")
        fecha = parse_publication_date(entry)

        texto_completo = f"{titulo} {descripcion}"

        # Filtrar noticias que no sean de Chile / Santiago
        if not any(kw in texto_completo for kw in GEOGRAPHIC_KEYWORDS):
            continue

        noticias.append({
            "title": titulo,
            "summary": descripcion,
            "publication_date": fecha,
            "district": detectar_comuna(texto_completo),
            "crime_type": crime_type,
            "source": fuente,
            "url": url_noticia,
        })

    return noticias
