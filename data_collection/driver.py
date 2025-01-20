# data_collection/driver.py

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_chrome_driver():
    """
    Configures and returns a Selenium WebDriver for Chrome in headless mode.
    The ChromeDriver path is loaded from an environment variable in the .env file.
    """
    chrome_driver_path = os.getenv("CHROMEDRIVER_PATH")
    if not chrome_driver_path:
        raise ValueError("CHROMEDRIVER_PATH is not set in the .env file.")

    chrome_service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument(
        "--disable-gpu"
    )  # Disable GPU for consistent headless performance
    options.add_argument(
        "--no-sandbox"
    )  # Required for some environments like CI/CD pipelines
    options.add_argument(
        "--disable-dev-shm-usage"
    )  # Overcome limited resource problems

    driver = webdriver.Chrome(service=chrome_service, options=options)
    return driver
