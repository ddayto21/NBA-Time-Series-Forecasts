import pandas as pd
from bs4 import BeautifulSoup
from .constants import DIRECTORIES, YEARS
from .utils import load_html
from io import StringIO


import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from .constants import DIRECTORIES, YEARS
from .utils import load_html


def parse_mvp():
    """Parses MVP HTML files and generates a CSV file containing all player statistics."""
    dfs = []
    log_messages = []

    for year in YEARS:
        try:
            log_messages.append(f"Parsing MVP data for year {year}...")
            page = load_html(DIRECTORIES["mvp"], f"{year}.html")
            soup = BeautifulSoup(page, "html.parser")

            # Remove optional elements if present
            over_header = soup.find("tr", class_="over_header")
            if over_header:
                over_header.decompose()

            # Find and parse the MVP table
            mvp_table = soup.find(id="mvp")
            if not mvp_table:
                log_messages.append(f"No MVP table found for year {year}, skipping.")
                continue

            # Parse the table dynamically using all columns available
            mvp_df = pd.read_html(StringIO(str(mvp_table)))[0]

            # Normalize column names for consistency
            mvp_df.columns = mvp_df.columns.str.strip()

            # Add the year column for context
            mvp_df["Year"] = year
            dfs.append(mvp_df)

        except Exception as e:
            log_messages.append(f"Failed to parse MVP data for year {year}: {e}")

    # Save the parsed data if available
    if dfs:
        try:
            mvps = pd.concat(dfs, ignore_index=True)
            mvps.to_csv(DIRECTORIES["mvp"] + "/mvps.csv", index=False)
            log_messages.append("MVP data successfully parsed and saved.")

            # Display a preview of the dataframe
            print("\nSample of the parsed MVP data:")
            print(mvps.head())  # Display the first few rows of the dataframe
        except Exception as e:
            log_messages.append(f"Failed to save MVP data: {e}")
    else:
        log_messages.append("No MVP data was parsed.")

    # Print all log messages for better debugging
    print("\n".join(log_messages))


def parse_player():
    """Parses player statistics HTML files and generates a CSV file."""
    dfs = []
    for year in YEARS:
        try:
            print(f"Parsing player data for year {year}...")
            page = load_html(DIRECTORIES["player"], f"{year}.html")
            soup = BeautifulSoup(page, "html.parser")

            # Remove optional elements
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
        players.to_csv(DIRECTORIES["player"] + "/players.csv", index=False)
        print("Player statistics successfully parsed and saved.")
    else:
        print("No player data was parsed.")


def parse_team():
    """Parses team standings HTML files and generates a CSV file."""
    dfs = []
    for year in YEARS:
        try:
            print(f"Parsing team data for year {year}...")
            page = load_html(DIRECTORIES["team"], f"{year}.html")
            soup = BeautifulSoup(page, "html.parser")

            # Remove optional elements
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
        teams.to_csv(DIRECTORIES["team"] + "/teams.csv", index=False)
        print("Team data successfully parsed and saved.")
    else:
        print("No team data was parsed.")
