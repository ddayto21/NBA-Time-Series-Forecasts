# main.py
from src.data_collection.scraping import scrape_mvp, scrape_player, scrape_team
from src.data_collection.parsing import parse_mvp, parse_player, parse_team
from src.data_collection.data_cleaning import DataCleaner


def display_menu():
    """Display the menu options for the data collection pipeline."""
    print("Welcome to the NBA Data Collection Pipeline!")
    print("\nSelect an option:")
    print("1: Run the entire pipeline")
    print("2: Scrape MVP data")
    print("3: Parse MVP data")
    print("4: Scrape player statistics")
    print("5: Parse player statistics")
    print("6: Scrape team statistics")
    print("7: Parse team statistics")
    print("8: Clean MVP data")
    print("9: Clean player statistics")
    print("10: Clean team data")
    print("11: Clean nicknames")
    print("0: Exit")


def main():
    """Main function to execute the data collection workflow."""
    data_cleaner = DataCleaner()  # Initialize the data cleaner

    while True:
        display_menu()
        choice = input("\nEnter your choice (0-11): ")

        # Define the file paths
        mvp_file_path = "src/data_collection/mvp/data/mvps.csv"
        players_file_path = "src/data_collection/player/data/players.csv"
        teams_file_path = "src/data_collection/team/data/teams.csv"
        nicknames_file_path = "src/data_collection/team/data/nicknames.csv"

        if choice == "1":
            print("\nRunning the entire pipeline...")
            print("\nStep 1: Scraping MVP Data...")
            scrape_mvp()

            print("\nStep 2: Parsing MVP Data...")
            parse_mvp()

            print("\nStep 3: Scraping Player Statistics...")
            scrape_player()

            print("\nStep 4: Parsing Player Statistics...")
            parse_player()

            print("\nStep 5: Scraping Team Statistics...")
            scrape_team()

            print("\nStep 6: Parsing Team Statistics...")
            parse_team()

            print("\nCleaning MVP Data...")
            data_cleaner.clean_mvp(mvp_file_path)

            print("\nCleaning Player Data...")
            cleaned_players = data_cleaner.clean_players(players_file_path)
            print("\nPreview of Cleaned Player Data:")
            print(cleaned_players.head())

            print("\nCleaning Team Data...")
            cleaned_teams = data_cleaner.clean_teams(teams_file_path)
            print("\nPreview of Cleaned Team Data:")
            print(cleaned_teams.head())

            print("\nCleaning Nicknames...")
            data_cleaner.clean_nick_names(nicknames_file_path)

            print("\nData Collection and Cleaning Pipeline Completed Successfully!")
        elif choice == "2":
            print("\nStep 1: Scraping MVP Data...")
            scrape_mvp()
        elif choice == "3":
            print("\nStep 2: Parsing MVP Data...")
            parse_mvp()
        elif choice == "4":
            print("\nStep 3: Scraping Player Statistics...")
            scrape_player()
        elif choice == "5":
            print("\nStep 4: Parsing Player Statistics...")
            parse_player()
        elif choice == "6":
            print("\nStep 5: Scraping Team Statistics...")
            scrape_team()
        elif choice == "7":
            print("\nStep 6: Parsing Team Statistics...")
            parse_team()
        elif choice == "8":
            print("\nCleaning MVP Data...")
            data_cleaner.clean_mvp(mvp_file_path)
        elif choice == "9":
            print("\nCleaning Player Data...")
            cleaned_players = data_cleaner.clean_players(players_file_path)
            print("\nPreview of Cleaned Player Data:")
            print(cleaned_players.head())
        elif choice == "10":
            print("\nCleaning Team Data...")
            cleaned_teams = data_cleaner.clean_teams(teams_file_path)
            print("\nPreview of Cleaned Team Data:")
            print(cleaned_teams.head())
        elif choice == "11":
            print("\nCleaning Nicknames...")
            data_cleaner.clean_nick_names(nicknames_file_path)
        elif choice == "0":
            print("\nExiting the pipeline. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 0 and 11.")


if __name__ == "__main__":
    main()
