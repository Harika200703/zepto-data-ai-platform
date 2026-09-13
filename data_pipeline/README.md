# Data Pipeline

This module scrapes book information from Books to Scrape and stores the cleaned data in SQLite.

## Features

- Scrapes 60 books from the website
- Extracts book titles and prices
- Converts GBP prices to INR using a fixed rate of 105.50
- Stores books and categories in SQLite
- Prevents duplicate book records
- Includes SQL analysis queries

## Files

- `scraper.py` — Scrapes book data and creates `books.csv`
- `database.py` — Creates tables and inserts book data
- `queries.sql` — Contains SQL analysis queries
- `books.csv` — Generated dataset
- `books.db` — Generated SQLite database