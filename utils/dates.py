# Helpers para manejo de fechas y ventanas temporales

from datetime import datetime, timedelta


def generate_time_windows(
    dias_atras: int = 90,
    ventana_dias: int = 10,
) -> list[tuple[str, str]]:
    """
    Divide los últimos `dias_atras` días en ventanas de `ventana_dias` días.

    Returns:
        Lista de tuplas (after, before) en formato YYYY-MM-DD,
        ordenadas de más reciente a más antigua.
    """
    hoy = datetime.today()
    ventanas: list[tuple[str, str]] = []
    cursor = hoy

    while (hoy - cursor).days < dias_atras:
        before = cursor.strftime("%Y-%m-%d")
        cursor -= timedelta(days=ventana_dias)
        after = cursor.strftime("%Y-%m-%d")
        ventanas.append((after, before))

    return ventanas
