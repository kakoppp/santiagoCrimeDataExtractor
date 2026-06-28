import argparse
import sys

import pandas as pd

from config.constants import (
    DEFAULT_OUTPUT_FILE,
    DEFAULT_LOOKBACK_DAYS,
    DEFAULT_MAX_ITEMS_PER_QUERY,
    DEFAULT_DATE_WINDOW_DAYS,
)
from scraper.pipeline import run_pipeline


def print_results(articles_df: pd.DataFrame) -> None:
    separator = "=" * 70

    print(f"\n{separator}")
    print(f"  ARTICLES FOUND: {len(articles_df)} records")
    print(f"{separator}\n")

    for _, article in articles_df.iterrows():
        print(
            f"[{article['publication_date']}] "
            f"{article['crime_type'].upper()} — {article['district']}"
        )
        print(f"  Title   : {article['title']}")
        print(f"  Summary : {article['summary'][:120]}...")
        print(f"  Source  : {article['source']}")
        print(f"  URL     : {article['url']}")
        print()

    print("── By Crime Type ──")
    print(articles_df["crime_type"].value_counts().to_string())

    print("\n── By District (Top 15) ──")
    print(articles_df["district"].value_counts().head(15).to_string())

def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Police News Scraper - Metropolitan Region, Chile",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--view",
        action="store_true",
        help="Print results to the console without saving a CSV file",
    )

    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_FILE,
        help="Output CSV file path",
    )

    parser.add_argument(
        "--max",
        type=int,
        default=DEFAULT_MAX_ITEMS_PER_QUERY,
        help="Maximum number of articles per query",
    )

    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_LOOKBACK_DAYS,
        help="Number of days to look back",
    )

    parser.add_argument(
        "--window",
        type=int,
        default=DEFAULT_DATE_WINDOW_DAYS,
        help="Time window size in days",
    )

    parser.add_argument(
        "--no-time-windows",
        action="store_true",
        help="Disable time window search",
    )

    return parser.parse_args()

def RUN() -> None:
    args = arguments()

    articles_df = run_pipeline(
        lookback_days=args.days,
        window_size_days=args.window,
        max_articles=args.max,
        use_time_windows=not args.no_time_windows,
    )

    if articles_df.empty:
        print("\nNo articles were found. Please check your internet connection.")
        sys.exit(1)

    print_results(articles_df)

    if args.view:
        print("\n(--view mode: CSV file was not saved)")
        return

    articles_df.to_csv(args.output, index=False, encoding="utf-8-sig")

    print(f"\nCSV saved: {args.output} ({len(articles_df)} rows)")
    print(f"Columns: {list(articles_df.columns)}")