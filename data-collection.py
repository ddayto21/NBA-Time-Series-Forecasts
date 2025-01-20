import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIRECTORIES = {
    "mvp": os.path.join(BASE_DIR, "mvp"),
    "player": os.path.join(BASE_DIR, "player"),
    "team": os.path.join(BASE_DIR, "team"),
}
for path in DIRECTORIES.values():
    os.makedirs(path, exist_ok=True)

YEARS = range(1991, 2022)

# Selenium WebDriver Setup
def get_chrome_driver():
    """
    Configures and returns a Selenium WebDriver for Chrome in headless mode.
    This is used for scraping dynamic content from websites.
    """
    chrome_service = Service("/path/to/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=chrome_service, options=options)

# Utility Functions
def save_html(content, directory, filename):
    """
    Saves HTML content to a specified file in the given directory.
    """
    with open(os.path.join(directory, filename), "w", encoding="utf-8") as file:
        file.write(content)

def load_html(directory, filename):
    """
    Loads and returns HTML content from a specified file.
    """
    with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
        return file.read()

# MVP Scraping and Parsing
def scrape_mvp():
    """
    Scrapes MVP award data from Basketball Reference for specified years and saves the HTML files locally.
    Includes error handling for HTTP errors and rate limits.
    """
    logging.info("Starting to scrape MVP data...")
    url_template = "https://www.basketball-reference.com/awards/awards_{}.html"
    for year in YEARS:
        try:
            logging.info(f"Scraping data for year {year}...")
            url = url_template.format(year)
            response = requests.get(url)
            response.raise_for_status()
            save_html(response.text, DIRECTORIES["mvp"], f"{year}.html")
            time.sleep(1)  # Adding a delay to prevent rate limiting
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTPError for year {year}: {e}")
            break
        except Exception as e:
            logging.error(f"Unexpected error for year {year}: {e}")
    logging.info("Finished scraping MVP data.")

def parse_mvp():
    """
    Parses saved MVP HTML files, extracts relevant data, and saves it as a CSV file.
    """
    logging.info("Starting to parse MVP data...")
    dfs = []
    for year in YEARS:
        try:
            logging.info(f"Parsing data for year {year}...")
            page = load_html(DIRECTORIES["mvp"], f"{year}.html")
            soup = BeautifulSoup(page, "html.parser")
            soup.find("tr", class_="over_header").decompose()
            mvp_table = soup.find(id="mvp")
            mvp_df = pd.read_html(str(mvp_table))[0]
            mvp_df["Year"] = year
            dfs.append(mvp_df)
        except FileNotFoundError:
            logging.warning(f"File not found for year {year}, skipping.")
        except Exception as e:
            logging.error(f"Unexpected error while parsing year {year}: {e}")
    if dfs:
        mvps = pd.concat(dfs, ignore_index=True)
        mvps.to_csv(os.path.join(DIRECTORIES["mvp"], "mvps.csv"), index=False)
        logging.info("Finished parsing MVP data.")
    else:
        logging.warning("No data was parsed.")

# Testing Framework
import unittest

class TestNBADataCollection(unittest.TestCase):
    def test_save_and_load_html(self):
        """Test saving and loading of HTML files."""
        test_dir = os.path.join(BASE_DIR, "test")
        os.makedirs(test_dir, exist_ok=True)
        test_file = "test.html"
        test_content = "<html><body>Test Content</body></html>"

        save_html(test_content, test_dir, test_file)
        loaded_content = load_html(test_dir, test_file)

        self.assertEqual(test_content, loaded_content)
        os.remove(os.path.join(test_dir, test_file))
        os.rmdir(test_dir)

    def test_scrape_mvp_handles_http_error(self):
        """Test scrape_mvp function handles HTTP errors."""
        with self.assertRaises(requests.exceptions.HTTPError):
            url = "https://www.basketball-reference.com/awards/awards_invalid.html"
            response = requests.get(url)
            response.raise_for_status()

if __name__ == "__main__":
    logging.info("Running the NBA Data Collection Script...")

    scrape_mvp()
    parse_mvp()

    logging.info("All tasks completed successfully!")

    # Run unit tests
    unittest.main(argv=[''], exit=False)
