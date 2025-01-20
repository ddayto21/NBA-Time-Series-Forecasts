# src/data_collection/utils.py
import os

def save_html(content, directory, filename):
    """Saves HTML content to a specified file in the given directory."""
    with open(os.path.join(directory, filename), "w", encoding="utf-8") as file:
        file.write(content)

def load_html(directory, filename):
    """Loads and returns HTML content from a specified file."""
    with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
        return file.read()
