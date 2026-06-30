import time
import pandas as pd
from config.constants import REQUEST_DELAY_SECONDS
from config.extract import crimeRadar
from scraper.feed import gets_news, gets_news_from_extra_sources, EXTRA_RSS_SOURCES
from utils.dates import generate_time_windows


def run_pipeline(
    lookback_days: int = 90,
    window_size_days: int = 10,
    max_articles: int = 100,
    use_time_windows: bool = True,
) -> pd.DataFrame:
    """
    Corre el pipeline completo: todas las queries de crimeRadar contra
    todas las ventanas de tiempo (Google News RSS), más un barrido extra
    de fuentes RSS de medios chilenos.
    """

    time_windows = (
        generate_time_windows(lookback_days, window_size_days)
        if use_time_windows
        else [(None, None)]
    )

    total_google_requests = len(crimeRadar) * len(time_windows)

    print(f"Time windows: {len(time_windows)}")
    print(f"Defined queries: {len(crimeRadar)}")
    print(f"Total requests (Google News): {total_google_requests}")
    print(f"Fuentes RSS extra: {len(EXTRA_RSS_SOURCES)}\n")

    all_articles: list[dict] = []
    processed_urls: set[str] = set()

    request_count = 0

    # ── 1. Google News RSS, query x ventana de tiempo
    for crime_type, search_query in crimeRadar:
        for after, before in time_windows:
            request_count += 1

            time_range = f"{after or 'start'} -> {before or 'today'}"

            print(
                f"[{request_count}/{total_google_requests}] "
                f"{crime_type} | {time_range}...",
                end=" ",
                flush=True,
            )

            try:
                articles = gets_news(
                    query=search_query,
                    crime_type=crime_type,
                    max_items=max_articles,
                    after=after,
                    before=before,
                )

                new_articles = [
                    article
                    for article in articles
                    if article["url"] not in processed_urls
                ]

                processed_urls.update(
                    article["url"] for article in new_articles
                )

                all_articles.extend(new_articles)

                print(
                    f"{len(new_articles)} new "
                    f"(total: {len(all_articles)})"
                )

            except Exception as exception:
                print(f"ERROR: {exception}")

            time.sleep(REQUEST_DELAY_SECONDS)

    # ── 2. Fuentes RSS extra (medios chilenos, una pasada por fuente)
    oldest_after = time_windows[-1][0] if use_time_windows and time_windows else None
    newest_before = time_windows[0][1] if use_time_windows and time_windows else None

    print(f"\n[EXTRA] Consultando fuentes RSS adicionales ({len(EXTRA_RSS_SOURCES)})...")

    try:
        extra_articles = gets_news_from_extra_sources(
            crime_type="General",
            max_items=max_articles,
            after=oldest_after,
            before=newest_before,
        )

        new_extra = [
            article
            for article in extra_articles
            if article["url"] not in processed_urls
        ]

        processed_urls.update(article["url"] for article in new_extra)
        all_articles.extend(new_extra)

        print(f"Noticias nuevas desde fuentes extra: {len(new_extra)}")
        print(f"Total: {len(all_articles)}")

    except Exception as exception:
        print(f"ERROR fuentes extra: {exception}")

    if not all_articles:
        return pd.DataFrame()

    df = pd.DataFrame(all_articles)

    # Second deduplication based on normalized title
    df["_title_key"] = (
        df["title"]
        .str.lower()
        .str.strip()
    )

    df = (
        df
        .drop_duplicates(subset=["_title_key"])
        .drop(columns=["_title_key"])
        .reset_index(drop=True)
    )

    df.insert(0, "id", range(1, len(df) + 1))

    return df
