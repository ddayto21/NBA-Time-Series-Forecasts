# tests/test_scraping.py
import unittest
from unittest.mock import patch
import os
import logging

from src.data_collection.scraping import scrape_mvp, scrape_player, scrape_team
from src.data_collection.constants import DIRECTORIES, YEARS

# Configure logging for the test module
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)


class TestScraping(unittest.TestCase):
    @patch("src.data_collection.scraping.requests.get")
    def test_scrape_mvp(self, mock_get):
        """Test scraping MVP data with mocked HTTP requests."""
        logging.info("[TEST] Starting test for scrape_mvp...")
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html><body>Mock Data</body></html>"

        logging.info("[TEST] Calling scrape_mvp()...")
        scrape_mvp()

        # Verify that files were created for all years
        for year in range(1991, 2024):
            file_path = os.path.join(DIRECTORIES["mvp"], "html", f"{year}.html")
            logging.info(f"[TEST] Checking file: {file_path}")
            self.assertTrue(os.path.exists(file_path))
            logging.info(f"[TEST] File found for year {year}. Removing file...")
            os.remove(file_path)  # Cleanup after test

        logging.info("[TEST] scrape_mvp test completed successfully.\n")

    @patch("src.data_collection.scraping.requests.get")
    def test_scrape_player(self, mock_get):
        """Test scraping Player data with mocked HTTP requests."""
        logging.info("[TEST] Starting test for scrape_player...")
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html><body>Mock Player Data</body></html>"

        logging.info("[TEST] Calling scrape_player()...")
        scrape_player()

        # Verify that files were created for all years
        for year in YEARS:
            file_path = os.path.join(DIRECTORIES["player"], "html", f"{year}.html")
            logging.info(f"[TEST] Checking file: {file_path}")
            self.assertTrue(os.path.exists(file_path))
            logging.info(f"[TEST] File found for year {year}. Removing file...")
            os.remove(file_path)  # Cleanup after test

        logging.info("[TEST] scrape_player test completed successfully.\n")

    @patch("src.data_collection.scraping.requests.get")
    def test_scrape_team(self, mock_get):
        """Test scraping team data with mocked HTTP requests."""
        logging.info("[TEST] Starting test for scrape_team...")
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html><body>Mock Team Data</body></html>"

        logging.info("[TEST] Calling scrape_team()...")
        scrape_team()

        # Verify that files were created for all years
        for year in YEARS:
            file_path = os.path.join(DIRECTORIES["team"], "html", f"{year}.html")
            logging.info(f"[TEST] Checking file: {file_path}")
            self.assertTrue(os.path.exists(file_path))
            logging.info(f"[TEST] File found for year {year}. Removing file...")
            os.remove(file_path)  # Cleanup after test

        logging.info("[TEST] scrape_team test completed successfully.\n")


if __name__ == "__main__":
    logging.info("[TEST] Running unit tests for scraping module...\n")
    unittest.main()
    logging.info("[TEST] All tests completed.")
