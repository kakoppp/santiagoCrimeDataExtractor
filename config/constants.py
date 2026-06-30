# Project General Constants

METROPOLITAN_REGION_MUNICIPALITIES: list[str] = [
    "Santiago", "Providencia", "Las Condes", "Maipú", "Puente Alto",
    "La Florida", "Ñuñoa", "San Bernardo", "Pudahuel", "Peñalolén",
    "La Pintana", "El Bosque", "Quilicura", "Recoleta", "Independencia",
    "Macul", "San Miguel", "Lo Espejo", "Cerrillos", "Estación Central",
    "Pedro Aguirre Cerda", "Lo Prado", "Quinta Normal", "Cerro Navia",
    "Conchalí", "Huechuraba", "Vitacura", "Lo Barnechea", "La Reina",
    "Renca", "Colina", "Lampa", "Buin", "Melipilla", "Talagante",
    "San Ramón", "La Cisterna", "La Granja", "San Joaquín", "Pirque",
    "Padre Hurtado", "Peñaflor", "Isla de Maipo", "El Monte", "Curacaví",
]

# Keywords
GEOGRAPHIC_KEYWORDS: list[str] = ["Chile", "Santiago", *METROPOLITAN_REGION_MUNICIPALITIES]

REQUEST_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-CL,es;q=0.9",
}

# Request throttling delay to prevent server overload (in seconds)
REQUEST_DELAY_SECONDS: float = 2.0

DEFAULT_MAX_ITEMS_PER_QUERY: int = 100
DEFAULT_LOOKBACK_DAYS: int = 90
DEFAULT_DATE_WINDOW_DAYS: int = 10
DEFAULT_OUTPUT_FILE: str = "news.csv"