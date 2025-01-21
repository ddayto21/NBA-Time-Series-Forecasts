from training.train import train_model, evaluate_model
from data_collection.fetch_nba_data import fetch_nba_team_data
from data_collection.process_data import process_data, split_data


if __name__ == "__main__":
    # Step 1: Fetch and process data
    all_games, team_abbr_to_id = fetch_nba_team_data()
    processed_games = process_data(all_games, team_abbr_to_id)

    # Step 2: Split data
    X_train, X_test, y_train, y_test = split_data(processed_games)

    # Step 3: Train and evaluate the model
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)