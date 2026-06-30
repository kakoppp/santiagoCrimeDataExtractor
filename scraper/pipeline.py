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

    time_windows = (
        generate_time_windows(lookback_days, window_size_days)
        if use_time_windows
        else [(None, None)]
    )

   
    oldest_after = time_windows[-1][0] if use_time_windows and time_windows else None
    newest_before = time_windows[0][1] if use_time_windows and time_windows else None

    print(f"Time windows: {len(time_windows)}")
    print(f"Defined queries: {len(crimeRadar)}")
    print(f"Total requests: {len(crimeRadar)}  (1 por query, filtrado local)\n")

    all_articles: list[dict] = []
    processed_urls: set[str] = set()

    total_requests = len(crimeRadar)

    for request_count, (crime_type, search_query) in enumerate(crimeRadar, start=1):

        print(
            f"[{request_count}/{total_requests}] "
            f"{crime_type} | {oldest_after or 'start'} → {newest_before or 'today'}...",
            end=" ",
            flush=True,
        )

        try:
            articles = gets_news(
                query=search_query,
                crime_type=crime_type,
                max_items=max_articles,
                after=oldest_after,
                before=newest_before,
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
