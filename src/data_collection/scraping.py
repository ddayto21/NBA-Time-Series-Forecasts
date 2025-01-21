# src/data_collection/scraping.py
import os
import requests
import time
from .constants import DIRECTORIES, YEARS
from .utils import save_html
from .driver import get_chrome_driver


def scrape_mvp():
    """Scrapes MVP award data and saves HTML files."""
    url_template = "https://www.basketball-reference.com/awards/awards_{}.html"
    for year in YEARS:
        try:
            print(f"Scraping MVP data for year {year}...")
            url = url_template.format(year)
            response = requests.get(url)
            response.raise_for_status()
            save_html(
                response.text, os.path.join(DIRECTORIES["mvp"], "html"), f"{year}.html"
            )
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Failed to scrape year {year}: {e}")


def scrape_player():
    """
    Scrapes player statistics data and saves HTML files using Requests.
    """
    url_template = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
    for year in YEARS:
        try:
            print(f"Scraping player data for year {year}...")
            url = url_template.format(year)
            response = requests.get(url)
            response.raise_for_status()
            save_html(
                response.text,
                os.path.join(DIRECTORIES["player"], "html"),
                f"{year}.html",
            )
            time.sleep(1)  # Pause to avoid rate limiting
        except requests.exceptions.RequestException as e:
            print(f"Failed to scrape player data for year {year}: {e}")


def scrape_team():
    """
    Scrapes team standings data and saves HTML files using Requests.
    """
    url_template = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html"
    for year in YEARS:
        try:
            print(f"Scraping team data for year {year}...")
            url = url_template.format(year)
            response = requests.get(url)
            response.raise_for_status()
            # Updated so all path components are joined in one call:
            save_html(
                response.text, os.path.join(DIRECTORIES["team"], "html"), f"{year}.html"
            )
            time.sleep(1)  # Pause to avoid rate limiting
        except requests.exceptions.RequestException as e:
            print(f"Failed to scrape team data for year {year}: {e}")

