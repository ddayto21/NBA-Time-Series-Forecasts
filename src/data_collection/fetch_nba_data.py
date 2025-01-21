import pandas as pd
from time import sleep
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder


# Function to fetch historical NBA game data for all teams
def fetch_nba_team_data():
    nba_teams = teams.get_teams()
    team_abbr_to_id = {team["abbreviation"]: team["id"] for team in nba_teams}
    all_games = pd.DataFrame()

    for team in nba_teams:
        team_id = team["id"]
        print(f"Fetching data for {team['full_name']} (ID: {team_id})...")
        try:
            gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
            games = gamefinder.get_data_frames()[0]
            all_games = pd.concat([all_games, games], ignore_index=True)
            print(f"Fetched {len(games)} games for {team['full_name']}.")
        except Exception as e:
            print(f"Error fetching data for {team['full_name']}: {e}")
        sleep(1)  # Rate limiting to avoid API issues

    all_games.to_csv("data/nba_game_data.csv", index=False)
    print("\nAll game data saved to 'data/nba_game_data.csv'.")
    return all_games, team_abbr_to_id


