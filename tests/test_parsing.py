import unittest
from unittest.mock import patch
import os
import pandas as pd

from src.data_collection.parsing import parse_mvp, parse_player, parse_team
from src.data_collection.constants import DIRECTORIES


class TestParsingBase(unittest.TestCase):
    """Base test class for parsing tests, providing reusable setup and teardown."""

    def setUp(self):
        """
        Prepare directories and mock HTML files for MVP, player, and team scraping.
        Each test can override or add to these if needed.
        """
        # Mock HTML snippets for each parser
        self.mock_mvp_html = """
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

        self.mock_player_html = """
        <html>
            <table id="per_game_stats">
                <tr class="thead"></tr>
                <thead>
                    <tr><th>Player</th><th>PPG</th></tr>
                </thead>
                <tbody>
                    <tr><td>Jane Smith</td><td>25.4</td></tr>
                </tbody>
            </table>
        </html>
        """

        self.mock_team_html = """
        <html>
            <table id="divs_standings_E">
                <thead>
                    <tr class="thead"></tr>
                    <tr><th>Team</th><th>Wins</th></tr>
                </thead>
                <tbody>
                    <tr><td>Boston Celtics</td><td>50</td></tr>
                </tbody>
            </table>
            <table id="divs_standings_W">
                <thead>
                    <tr class="thead"></tr>
                    <tr><th>Team</th><th>Wins</th></tr>
                </thead>
                <tbody>
                    <tr><td>Los Angeles Lakers</td><td>48</td></tr>
                </tbody>
            </table>
        </html>
        """

        # Set up directories for each category
        self.mvp_html_dir = os.path.join(DIRECTORIES["mvp"], "html")
        self.mvp_data_dir = os.path.join(DIRECTORIES["mvp"], "data")

        self.player_html_dir = os.path.join(DIRECTORIES["player"], "html")
        self.player_data_dir = os.path.join(DIRECTORIES["player"], "data")

        self.team_html_dir = os.path.join(DIRECTORIES["team"], "html")
        self.team_data_dir = os.path.join(DIRECTORIES["team"], "data")

        # Create needed directories
        os.makedirs(self.mvp_html_dir, exist_ok=True)
        os.makedirs(self.mvp_data_dir, exist_ok=True)
        os.makedirs(self.player_html_dir, exist_ok=True)
        os.makedirs(self.player_data_dir, exist_ok=True)
        os.makedirs(self.team_html_dir, exist_ok=True)
        os.makedirs(self.team_data_dir, exist_ok=True)

        # Create a test HTML file for each category (Year 1991, for example)
        self.mvp_test_file = os.path.join(self.mvp_html_dir, "1991.html")
        with open(self.mvp_test_file, "w", encoding="utf-8") as f:
            f.write(self.mock_mvp_html)

        self.player_test_file = os.path.join(self.player_html_dir, "1991.html")
        with open(self.player_test_file, "w", encoding="utf-8") as f:
            f.write(self.mock_player_html)

        self.team_test_file = os.path.join(self.team_html_dir, "1991.html")
        with open(self.team_test_file, "w", encoding="utf-8") as f:
            f.write(self.mock_team_html)

    def tearDown(self):
        """Clean up mock files after tests."""
        # Remove the test HTML files
        for file_path in [
            self.mvp_test_file,
            self.player_test_file,
            self.team_test_file,
        ]:
            if os.path.exists(file_path):
                os.remove(file_path)

        # Remove the CSV files created during parsing
        mvp_csv = os.path.join(self.mvp_data_dir, "mvps.csv")
        if os.path.exists(mvp_csv):
            os.remove(mvp_csv)

        player_csv = os.path.join(self.player_data_dir, "players.csv")
        if os.path.exists(player_csv):
            os.remove(player_csv)

        team_csv = os.path.join(self.team_data_dir, "teams.csv")
        if os.path.exists(team_csv):
            os.remove(team_csv)


class TestParsingMVP(TestParsingBase):
    """Test cases for parsing MVP data."""

    @patch("src.data_collection.parsing.YEARS", [1991])  # Only test for year 1991
    @patch("src.data_collection.parsing.load_html")
    def test_parse_mvp(self, mock_load_html):
        """Test parsing MVP HTML files into a CSV."""
        mock_load_html.return_value = self.mock_mvp_html  # Use the mock MVP HTML

        parse_mvp()

        csv_file = os.path.join(self.mvp_data_dir, "mvps.csv")
        self.assertTrue(
            os.path.exists(csv_file),
            "mvps.csv should be created after parsing MVP data",
        )

        df = pd.read_csv(csv_file)
        self.assertEqual(
            len(df), 1, "There should be exactly one row in the parsed MVP data"
        )
        self.assertEqual(
            df.iloc[0]["Player"], "John Doe", "Player name should match mock data"
        )
        self.assertEqual(
            df.iloc[0]["Points"], 100, "Points value should match mock data"
        )


class TestParsingPlayer(TestParsingBase):
    """Test cases for parsing player data."""

    @patch("src.data_collection.parsing.YEARS", [1991])  # Only test for year 1991
    @patch("src.data_collection.parsing.load_html")
    def test_parse_player(self, mock_load_html):
        """Test parsing Player HTML files into a CSV."""
        mock_load_html.return_value = self.mock_player_html

        from src.data_collection.parsing import parse_player

        parse_player()

        csv_file = os.path.join(self.player_data_dir, "players.csv")
        self.assertTrue(
            os.path.exists(csv_file),
            "players.csv should be created after parsing player data",
        )

        df = pd.read_csv(csv_file)
        self.assertEqual(
            len(df), 1, "There should be exactly one row in the parsed player data"
        )
        self.assertEqual(
            df.iloc[0]["Player"], "Jane Smith", "Player name should match mock data"
        )
        self.assertEqual(df.iloc[0]["PPG"], 25.4, "PPG value should match mock data")


class TestParsingTeam(TestParsingBase):
    """Test cases for parsing team data."""

    @patch("src.data_collection.parsing.YEARS", [1991])  # Only test for year 1991
    @patch("src.data_collection.parsing.load_html")
    def test_parse_team(self, mock_load_html):
        """Test parsing Team HTML files into a CSV."""
        mock_load_html.return_value = self.mock_team_html

        from src.data_collection.parsing import parse_team

        parse_team()

        csv_file = os.path.join(self.team_data_dir, "teams.csv")
        self.assertTrue(
            os.path.exists(csv_file),
            "teams.csv should be created after parsing team data",
        )

        df = pd.read_csv(csv_file)
        self.assertEqual(
            len(df),
            2,
            "There should be two rows (Eastern + Western) in the parsed team data",
        )

        # Check first row (Eastern conference)
        self.assertEqual(
            df.iloc[0]["Team"],
            "Boston Celtics",
            "Team name should match Eastern mock data",
        )
        self.assertEqual(df.iloc[0]["Wins"], 50, "Wins should match Eastern mock data")
        self.assertEqual(
            df.iloc[0]["Conference"], "Eastern", "Conference should be Eastern"
        )

        # Check second row (Western conference)
        self.assertEqual(
            df.iloc[1]["Team"],
            "Los Angeles Lakers",
            "Team name should match Western mock data",
        )
        self.assertEqual(df.iloc[1]["Wins"], 48, "Wins should match Western mock data")
        self.assertEqual(
            df.iloc[1]["Conference"], "Western", "Conference should be Western"
        )


if __name__ == "__main__":
    unittest.main()
