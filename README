# Santiago Crime Data Extractor

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20development-yellow?style=flat)


A scraper for police-related news from the Santiago Metropolitan Region, Chile, collected via Google News RSS.

---

## What does it do?

The program searches for public safety news (robberies, homicides, drug trafficking, car-door robberies, etc.) using more than 40 different search terms grouped by crime type. For each search:

1. Builds a Google News RSS search URL with the term and, optionally, a date range.
2. Downloads and parses the RSS feed.
3. Strips HTML from the title and description.
4. Filters to keep only news that mention Chile, Santiago, or a municipality in the Metropolitan Region.
5. Automatically detects which municipality is mentioned in the text.
6. Removes duplicates (first by URL, then by normalized title).
7. Combines everything into a table and exports it to a CSV file.

To cover more news over time, the total date range is split into "windows" (for example, 9 windows of 10 days each to cover 90 days), and a search is run for every combination of (crime type, time window).

---

## Before running

- Have **Python 3.11+** installed.
- Have an internet connection (the scraper queries Google News live).
- Install the dependencies:

```bash
pip install -r requirements.txt
```

This installs `feedparser` (RSS reading), `beautifulsoup4` (HTML cleanup), and `pandas` (data handling and CSV export).

- Make sure you're running `pip install` and `python main.py` with the **same Python interpreter** (check in VS Code with `Ctrl+Shift+P` → *Python: Select Interpreter*).

---

## How to run

```bash
# Default run (90 days, 10-day windows, ~1700 articles, saves news.csv)
python main.py

# To get ~3000 articles
python main.py --days 90 --window 5 --max 150

# Just view results in the console, without saving a CSV
python main.py --view

# Customize the output file
python main.py --days 90 --window 5 --max 150 --output output/news.csv

# Without time partitioning (a single search per query, faster but fewer articles)
python main.py --no-time-windows --max 50
```

### Available parameters

| Parameter              | Default     | Description                                            |
|------------------------|-------------|----------------------------------------------------------|
| `--view`                | `False`     | Prints to console, does not save a CSV                  |
| `--output`              | `news.csv`  | Output CSV file path                                     |
| `--max`                 | `100`       | Maximum number of articles per query+window              |
| `--days`                | `90`        | Number of days to look back                              |
| `--window`              | `10`        | Size in days of each time window                          |
| `--no-time-windows`     | `False`     | Disables date-based partitioning                          |

---

## While it's running

You'll see the progress of each search printed line by line in the console:

```
[12/810] Homicide | 2026-05-10 → 2026-05-15... 8 new (total: 412)
```

This tells you how many new (non-duplicate) articles were found for that query + window combination, and the running total so far. The full process can take several minutes depending on how many windows/queries there are (there's a ~1.2 second delay between each request so as not to overload Google's server).

---

## After running

When it finishes, you'll see a summary in the console:

```
======================================================================
  ARTICLES FOUND: 2934 records
======================================================================
...
── By Crime Type ──
Homicide            412
Violent Robbery     380
...

── By District (Top 15) ──
Santiago            210
Puente Alto         150
...

CSV saved: news.csv (2934 rows)
Columns: ['id', 'title', 'summary', 'publication_date', 'district', 'crime_type', 'source', 'url']
```

And you'll have a `news.csv` file (or whatever name you set with `--output`) ready to open in Excel, Google Sheets, or load into pandas/Python for analysis.

---

## Project structure

```
.
├── main.py                  # Entry point
├── requirements.txt
├── config/
│   ├── constants.py          # RM municipalities, HTTP headers, default values
│   └── extract.py            # Search queries by crime type (crimeRadar)
├── scraper/
│   ├── feed.py                 # Builds RSS URL and fetches news
│   └── pipeline.py             # Orchestrates queries × windows + deduplication
├── utils/
│   ├── dates.py                  # Time window generation
│   └── text.py                    # HTML cleanup and district detection
└── serviceMain.py                # CLI: arguments, results printing, RUN()
```

---

## Generated CSV columns

| Column                | Description                          |
|------------------------|----------------------------------------|
| `id`                    | Sequential identifier                  |
| `title`                 | Article title (HTML-free)              |
| `summary`               | Description/summary                     |
| `publication_date`      | Publication date (YYYY-MM-DD)          |
| `district`              | Municipality detected in the text      |
| `crime_type`            | Crime category according to the query   |
| `source`                | News outlet                             |
| `url`                    | Link to the original article           |

---

## Notes

- The scraper respects a 1.2-second delay between requests to avoid overloading Google News' server.
- Deduplication happens in two steps: by URL on the fly, and by normalized title at the end.
- Only news that mentions Chile, Santiago, or an RM municipality is included; everything else is automatically discarded.
--- 
## PD
This project is still a work in progress, so apologies for my Spanglish. Also, the news/results shown are currently 100% Chilean.
