import unittest
from unittest.mock import patch
from data_collection.parsing import parse_mvp
from data_collection.constants import DIRECTORIES
import os
import pandas as pd


class TestParsingBase(unittest.TestCase):
    """Base test class for parsing tests, providing reusable setup and teardown."""

    def setUp(self):
        """Set up mock HTML files for testing."""
        self.mock_html = """
        <html>
            <table id="mvp">
                <tr class="over_header"></tr>
                <thead>
                    <tr><th>Player</th><th>Points</th></tr>
                </thead>
                <tbody>
                    <tr><td>John Doe</td><td>100</td></tr>
                </tbody>
            </table>
        </html>
        """
        self.test_dir = DIRECTORIES["mvp"]
        self.test_file = os.path.join(self.test_dir, "1991.html")
        os.makedirs(self.test_dir, exist_ok=True)
        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write(self.mock_html)

    def tearDown(self):
        """Clean up mock files after tests."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        csv_file = os.path.join(self.test_dir, "mvps.csv")
        if os.path.exists(csv_file):
            os.remove(csv_file)


class TestParsingMVP(TestParsingBase):
    """Test cases for parsing MVP data."""

    @patch("data_collection.parsing.YEARS", [1991])  # Mock YEARS to only include 1991
    @patch("data_collection.parsing.load_html")
    def test_parse_mvp(self, mock_load_html):
        """Test parsing MVP HTML files into a CSV."""
        mock_load_html.return_value = self.mock_html  # Mock HTML content
        parse_mvp()

        csv_file = os.path.join(self.test_dir, "mvps.csv")
        self.assertTrue(os.path.exists(csv_file))  # Ensure the file is created

        df = pd.read_csv(csv_file)
        self.assertEqual(len(df), 1)  # Ensure only one row is parsed
        self.assertEqual(df.iloc[0]["Player"], "John Doe")  # Verify Player name
        self.assertEqual(df.iloc[0]["Points"], 100)  # Verify Points value


if __name__ == "__main__":
    unittest.main()
