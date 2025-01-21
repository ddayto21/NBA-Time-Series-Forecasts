import pandas as pd
import os
import matplotlib.pyplot as plt

# Define file paths
DATA_DIR = "src/data_collection/player/data"
INPUT_FILE = os.path.join(DATA_DIR, "players.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "players_2024-2025.csv")
PLOT_FILE = os.path.join(DATA_DIR, "mvp_ranking_plot.png")

def compute_mvp_score(df):
    """
    Compute MVP scores for players based on available statistical metrics.
    The scoring formula combines weighted contributions from key stats.
    """
    # Add calculated metrics if not present
    if "TRB" not in df.columns:
        df["TRB"] = df["ORB"] + df["DRB"]  # Total rebounds

    # Normalize stats for fair comparison
    normalized_columns = ["PTS", "MP", "AST", "TRB", "STL", "BLK"]
    for col in normalized_columns:
        if col in df.columns:
            df[col] = df[col] / df[col].max()

    # MVP scoring formula (weights can be adjusted based on importance)
    df["MVP_Score"] = (
        0.35 * df["PTS"]
        + 0.2 * df["MP"]
        + 0.15 * df["AST"]
        + 0.15 * df["TRB"]
        + 0.1 * df["STL"]
        + 0.05 * df["BLK"]
    )
    return df

def plot_top_players(df, top_n=10):
    """
    Generate and save a bar chart for the top N ranked players based on MVP scores.
    """
    top_players = df.head(top_n)
    plt.figure(figsize=(10, 6))
    plt.barh(top_players["Player"], top_players["MVP_Score"], color="skyblue")
    plt.xlabel("MVP Score")
    plt.ylabel("Player")
    plt.title(f"Top {top_n} Players Likely to Win MVP (2024-2025)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(PLOT_FILE)
    print(f"MVP ranking plot saved to {PLOT_FILE}")
    plt.show()

def rank_players():
    """
    Rank players based on their likelihood of winning the MVP award.
    Filters players for the years 2024 and 2025, computes MVP scores,
    and saves the ranked data to a new CSV file.
    """
    # Load the dataset
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file {INPUT_FILE} not found.")
        return

    print("Loading player data...")
    players_df = pd.read_csv(INPUT_FILE)

    # Filter data for the years 2024 and 2025
    filtered_df = players_df[players_df["Year"].isin([2024, 2025])]

    if filtered_df.empty:
        print("No data found for the years 2024-2025.")
        return

    # Compute MVP scores
    print("Computing MVP scores...")
    ranked_df = compute_mvp_score(filtered_df)

    # Sort players by MVP score in descending order
    ranked_df = ranked_df.sort_values(by="MVP_Score", ascending=False)

    # Save the results to a new CSV file
    print(f"Saving ranked players to {OUTPUT_FILE}...")
    ranked_df.to_csv(OUTPUT_FILE, index=False)

    print("Ranking completed successfully!")
    print(ranked_df[["Player", "Year", "MVP_Score"]].head())  # Display top players

    # Generate and save a plot for the top-ranked players
    plot_top_players(ranked_df)

if __name__ == "__main__":
    rank_players()