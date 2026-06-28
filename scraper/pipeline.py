# Orquesta las queries, ventanas temporales, deduplicación y retorna el DataFrame

import time

import pandas as pd

from config.constants import REQUEST_DELAY_SECONDS
from config.extract import crimeRadar
from scraper.feed import gets_news
from utils.dates import generate_time_windows

def run_pipeline(
    lookback_days: int = 90,
    window_size_days: int = 10,
    max_articles: int = 100,
    use_time_windows: bool = True,
) -> pd.DataFrame:
    """
    Runs the complete scraping pipeline across all search queries and time windows.

    Args:
        lookback_days: Number of days to look back.
        window_size_days: Size of each time window in days.
        max_articles: Maximum number of articles per query and time window.
        use_time_windows: If False, performs a single search without date filters.

    Returns:
        A deduplicated DataFrame containing all collected articles.
    """

    time_windows = (
        generate_time_windows(lookback_days, window_size_days)
        if use_time_windows
        else [(None, None)]
    )

    print(f"Time windows: {len(time_windows)}")
    print(f"Defined queries: {len(crimeRadar)}")
    print(f"Total requests: {len(crimeRadar) * len(time_windows)}\n")

    all_articles: list[dict] = []
    processed_urls: set[str] = set()

    total_requests = len(crimeRadar) * len(time_windows)
    request_count = 0

    for crime_type, search_query in crimeRadar:
        for after, before in time_windows:
            request_count += 1

            time_range = f"{after or 'start'} → {before or 'today'}"

            print(
                f"[{request_count}/{total_requests}] "
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
