import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from data_collection.fetch_nba_data import fetch_nba_team_data
from data_collection.process_data import process_data, split_data


def train_model(X_train, y_train):
    # Initialize RandomForestClassifier with 100 trees
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    # Predict and evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy:.2%}")


if __name__ == "__main__":
    # Fetch and process data
    all_games, team_abbr_to_id = fetch_nba_team_data()
    processed_games = process_data(all_games, team_abbr_to_id)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(processed_games)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

    # Save the trained model
    with open("data/nba_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("Model saved to 'data/nba_model.pkl'.")