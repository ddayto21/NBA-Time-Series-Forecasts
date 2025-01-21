# data_collection/constants.py
import os

# Base directory for saving scraped and parsed data files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directories for different data types
DIRECTORIES = {
    "mvp": os.path.join(BASE_DIR, "mvp"),
    "player": os.path.join(BASE_DIR, "player"),
    "team": os.path.join(BASE_DIR, "team"),
}

# Ensure directories exist
for path in DIRECTORIES.values():
    os.makedirs(path, exist_ok=True)

# Years of data to scrape and parse
YEARS = range(1991, 2025)
