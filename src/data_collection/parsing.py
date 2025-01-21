import os
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

from .constants import DIRECTORIES, YEARS
from .utils import load_html

def parse_mvp():
    """
    Parses MVP HTML files and generates a CSV file containing all player statistics.
    The resulting CSV file is saved under /data within the 'mvp' directory.
    """
    dfs = []
    log_messages = []

    for year in YEARS:
        try:
            log_messages.append(f"Parsing MVP data for year {year}...")
            # Combine directory path for the HTML file
            page_content = load_html(
                os.path.join(DIRECTORIES["mvp"], "html"), 
                f"{year}.html"
            )

            soup = BeautifulSoup(page_content, "html.parser")

            # Remove optional 'over_header' if present
            over_header = soup.find("tr", class_="over_header")
            if over_header:
                over_header.decompose()

            # Find and parse the MVP table
            mvp_table = soup.find(id="mvp")
            if not mvp_table:
                log_messages.append(f"No MVP table found for year {year}, skipping.")
                continue

            mvp_df = pd.read_html(StringIO(str(mvp_table)))[0]

            # Normalize column names
            mvp_df.columns = mvp_df.columns.str.strip()

            # Add the year column
            mvp_df["Year"] = year
            dfs.append(mvp_df)

        except Exception as e:
            log_messages.append(f"Failed to parse MVP data for year {year}: {e}")

    if dfs:
        try:
            mvps = pd.concat(dfs, ignore_index=True)

            # Ensure the /data directory exists
            data_dir = os.path.join(DIRECTORIES["mvp"], "data")
            os.makedirs(data_dir, exist_ok=True)

            csv_path = os.path.join(data_dir, "mvps.csv")
            mvps.to_csv(csv_path, index=False)
            log_messages.append("MVP data successfully parsed and saved.")

            print("\nSample of the parsed MVP data:")
            print(mvps.head())
        except Exception as e:
            log_messages.append(f"Failed to save MVP data: {e}")
    else:
        log_messages.append("No MVP data was parsed.")

    print("\n".join(log_messages))


def parse_player():
    """
    Parses player statistics HTML files and generates a CSV file.
    The resulting CSV file is saved under /data within the 'player' directory.
    """
    dfs = []
    for year in YEARS:
        try:
            print(f"Parsing player data for year {year}...")
            page_content = load_html(
                os.path.join(DIRECTORIES["player"], "html"), 
                f"{year}.html"
            )
            soup = BeautifulSoup(page_content, "html.parser")

            # Remove optional row
            thead_row = soup.find("tr", class_="thead")
            if thead_row:
                thead_row.decompose()

            player_table = soup.find(id="per_game_stats")
            if not player_table:
                print(f"No player stats table found for year {year}, skipping.")
                continue

            player_df = pd.read_html(StringIO(str(player_table)))[0]
            player_df["Year"] = year
            dfs.append(player_df)

        except Exception as e:
            print(f"Failed to parse player data for year {year}: {e}")

    if dfs:
        players = pd.concat(dfs, ignore_index=True)

        # Ensure the /data directory exists
        data_dir = os.path.join(DIRECTORIES["player"], "data")
        os.makedirs(data_dir, exist_ok=True)

        csv_path = os.path.join(data_dir, "players.csv")
        players.to_csv(csv_path, index=False)
        print("Player statistics successfully parsed and saved.")
    else:
        print("No player data was parsed.")


def parse_team():
    """
    Parses team standings HTML files and generates a CSV file.
    The resulting CSV file is saved under /data within the 'team' directory.
    """
    dfs = []
    for year in YEARS:
        try:
            print(f"Parsing team data for year {year}...")
            page_content = load_html(
                os.path.join(DIRECTORIES["team"], "html"), 
                f"{year}.html"
            )
            soup = BeautifulSoup(page_content, "html.parser")

            # Remove optional row
            thead_row = soup.find("tr", class_="thead")
            if thead_row:
                thead_row.decompose()

            # Parse Eastern Conference standings
            east_table = soup.find(id="divs_standings_E")
            if east_table:
                east_teams = pd.read_html(StringIO(str(east_table)))[0]
                east_teams["Year"] = year
                east_teams["Conference"] = "Eastern"
                dfs.append(east_teams)

            # Parse Western Conference standings
            west_table = soup.find(id="divs_standings_W")
            if west_table:
                west_teams = pd.read_html(StringIO(str(west_table)))[0]
                west_teams["Year"] = year
                west_teams["Conference"] = "Western"
                dfs.append(west_teams)

        except Exception as e:
            print(f"Failed to parse team data for year {year}: {e}")

    if dfs:
        teams = pd.concat(dfs, ignore_index=True)

        # Ensure the /data directory exists
        data_dir = os.path.join(DIRECTORIES["team"], "data")
        os.makedirs(data_dir, exist_ok=True)

        csv_path = os.path.join(data_dir, "teams.csv")
        teams.to_csv(csv_path, index=False)
        print("Team data successfully parsed and saved.")
    else:
        print("No team data was parsed.")