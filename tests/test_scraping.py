# tests/test_scraping.py
import unittest
from unittest.mock import patch
from data_collection.scraping import scrape_mvp
from data_collection.constants import DIRECTORIES
import os

class TestScraping(unittest.TestCase):
    @patch("data_collection.scraping.requests.get")
    def test_scrape_mvp(self, mock_get):
        """Test scraping MVP data with mocked HTTP requests."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html><body>Mock Data</body></html>"

        scrape_mvp()

        # Verify that files were created for all years
        for year in range(1991, 2022):
            file_path = os.path.join(DIRECTORIES["mvp"], f"{year}.html")
            self.assertTrue(os.path.exists(file_path))
            os.remove(file_path)  # Cleanup after test

if __name__ == "__main__":
    unittest.main()
