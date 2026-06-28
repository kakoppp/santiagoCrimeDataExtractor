# Funciones para limpiar texto y detectar comunas

import re
from bs4 import BeautifulSoup

from config.constants import METROPOLITAN_REGION_MUNICIPALITIES


def strip_html(raw_text: str) -> str:
    """Elimina etiquetas HTML y normaliza espacios en blanco."""
    soup = BeautifulSoup(raw_text or "", "html.parser")
    plain = soup.get_text(separator=" ")
    return re.sub(r"\s+", " ", plain).strip()


def detectar_comuna(texto: str) -> str:
    """
    Busca la primera comuna de la RM mencionada en el texto.
    Devuelve 'Sin identificar' si no hay coincidencia.
    """
    texto_lower = texto.lower()
    for comuna in METROPOLITAN_REGION_MUNICIPALITIES:
        if comuna.lower() in texto_lower:
            return comuna
    return "Sin identificar"
