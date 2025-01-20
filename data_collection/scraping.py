# data_collection/scraping.py
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
            save_html(response.text, DIRECTORIES["mvp"], f"{year}.html")
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Failed to scrape year {year}: {e}")


def scrape_player():
    """Scrapes player statistics data using Selenium."""
    driver = get_chrome_driver()

    url_template = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
    for year in YEARS:
        try:
            print(f"Scraping player data for year {year}...")
            url = url_template.format(year)
            driver.get(url)
            time.sleep(2)
            html = driver.page_source
            save_html(html, DIRECTORIES["player"], f"{year}.html")
        except Exception as e:
            print(f"Failed to scrape player data for year {year}: {e}")
    driver.quit()


def scrape_team():
    """Scrapes team standings data."""
    url_template = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html"
    for year in YEARS:
        try:
            print(f"Scraping team data for year {year}...")
            url = url_template.format(year)
            response = requests.get(url)
            response.raise_for_status()
            save_html(response.text, DIRECTORIES["team"], f"{year}.html")
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Failed to scrape team data for year {year}: {e}")
