import pandas as pd
from time import sleep  # To handle rate-limiting
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


def process_data(all_games, team_abbr_to_id):
    all_games["GAME_DATE"] = pd.to_datetime(all_games["GAME_DATE"])
    all_games["WIN"] = all_games["WL"].apply(lambda x: 1 if x == "W" else 0)
    all_games["PTS"] = all_games["PTS"].astype(float)
    all_games["Points_Per_Game"] = all_games.groupby("TEAM_ID")["PTS"].transform("mean")

    def get_opponent_team_id(matchup, team_abbr_to_id, team_id):
        if "@" in matchup:
            opponent_abbr = matchup.split(" @ ")[-1]
        else:
            opponent_abbr = matchup.split(" vs. ")[-1]
        return team_abbr_to_id.get(opponent_abbr, team_id)

    all_games["OPPONENT_TEAM_ID"] = all_games.apply(
        lambda row: get_opponent_team_id(
            row["MATCHUP"], team_abbr_to_id, row["TEAM_ID"]
        ),
        axis=1,
    )
    all_games["HOME_GAME"] = all_games["MATCHUP"].apply(
        lambda x: 1 if "vs." in x else 0
    )
    all_games["LAST_GAME_RESULT"] = (
        all_games.groupby("TEAM_ID")["WIN"].shift(1).fillna(0)
    )

    # Encode categorical data
    le = LabelEncoder()
    all_games["TEAM_ID"] = le.fit_transform(all_games["TEAM_ID"])
    all_games["OPPONENT_TEAM_ID"] = le.fit_transform(all_games["OPPONENT_TEAM_ID"])

    return all_games


# Function to split the dataset into train and test sets
def split_data(all_games):
    features = [
        "TEAM_ID",
        "OPPONENT_TEAM_ID",
        "Points_Per_Game",
        "HOME_GAME",
        "LAST_GAME_RESULT",
    ]
    target = "WIN"

    X = all_games[features]
    y = all_games[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test
