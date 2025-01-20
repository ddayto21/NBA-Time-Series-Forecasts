# main.py
from data_collection.scraping import scrape_mvp, scrape_player, scrape_team
from data_collection.parsing import parse_mvp, parse_player, parse_team


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
    print("0: Exit")


def main():
    """Main function to execute the data collection workflow."""
    while True:
        display_menu()
        choice = input("\nEnter your choice (0-7): ")

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

            print("\nData Collection Pipeline Completed Successfully!")
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
        elif choice == "0":
            print("\nExiting the pipeline. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 0 and 7.")


if __name__ == "__main__":
    main()
