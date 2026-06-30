from datetime import datetime
import time as _time
import feedparser

from config.constants import (
    GEOGRAPHIC_KEYWORDS,
    REQUEST_HEADERS,
)
from utils.text import (
    strip_html,
    detectar_comuna
)

EXTRA_RSS_SOURCES = [
    "https://www.biobiochile.cl/lista/categorias/nacional.rss",
    "https://www.latercera.com/canal/nacional/feed/",
    "https://www.latercera.com/canal/policial/feed/",
    "https://www.adnradio.cl/feed/",
    "https://www.meganoticias.cl/rss.xml",
    "https://www.24horas.cl/rss.xml",
    "https://www.cooperativa.cl/noticias/pais/rss.xml",
    "https://www.elmostrador.cl/feed/",
    "https://www.theclinic.cl/feed/",
    "https://www.lanacion.cl/feed/",
    "https://www.radioagricultura.cl/feed/",
]


def build_rss_url(
    query: str,
    after: str | None = None,
    before: str | None = None,
) -> str:
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
    try:
        return datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
    except Exception:
        return datetime.today().strftime("%Y-%m-%d")


def fetch_feed(url: str) -> feedparser.FeedParserDict:
    for intento in range(3):
        feed = feedparser.parse(url, request_headers=REQUEST_HEADERS)
        if feed.get("status", 0) != 503:
            return feed
        print(f"\n  503 recibido, reintentando en 15s...")
        _time.sleep(15)
    return feed


def parse_entries(
    feed: feedparser.FeedParserDict,
    crime_type: str,
    max_items: int,
    after_dt: datetime | None,
    before_dt: datetime | None,
) -> list[dict]:
    noticias = []
    for entry in feed.entries[:max_items]:
        titulo = strip_html(entry.get("title", ""))
        descripcion = strip_html(entry.get("summary", ""))
        fuente = entry.get("source", {}).get("title", "") or entry.get("author", "Desconocida")
        url_noticia = entry.get("link", "")
        fecha_str = parse_publication_date(entry)
        fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")

        if after_dt and fecha_dt < after_dt:
            continue
        if before_dt and fecha_dt > before_dt:
            continue

        texto_completo = f"{titulo} {descripcion}"
        if not any(kw in texto_completo for kw in GEOGRAPHIC_KEYWORDS):
            continue

        noticias.append({
            "title": titulo,
            "summary": descripcion,
            "publication_date": fecha_str,
            "district": detectar_comuna(texto_completo),
            "crime_type": crime_type,
            "source": fuente,
            "url": url_noticia,
        })
    return noticias


def gets_news(
    query: str,
    crime_type: str,
    max_items: int = 100,
    after: str | None = None,
    before: str | None = None,
) -> list[dict]:

    after_dt = datetime.strptime(after, "%Y-%m-%d") if after else None
    before_dt = datetime.strptime(before, "%Y-%m-%d") if before else None

    url = build_rss_url(query, after=after, before=before)
    feed = fetch_feed(url)
    return parse_entries(feed, crime_type, max_items, after_dt, before_dt)


def gets_news_from_extra_sources(
    crime_type: str,
    max_items: int = 100,
    after: str | None = None,
    before: str | None = None,
) -> list[dict]:

    after_dt = datetime.strptime(after, "%Y-%m-%d") if after else None
    before_dt = datetime.strptime(before, "%Y-%m-%d") if before else None

    noticias = []
    for rss_url in EXTRA_RSS_SOURCES:
        try:
            feed = fetch_feed(rss_url)
            noticias += parse_entries(feed, crime_type, max_items, after_dt, before_dt)
        except Exception as e:
            print(f"\n  ERROR en {rss_url}: {e}")

    return noticias
