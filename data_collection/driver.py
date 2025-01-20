import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()


def verify_proxy(proxy_address):
    """
    Verifies if the provided proxy is working by making a request to https://httpbin.org/ip.

    Parameters:
        proxy_address (str): The proxy address (e.g., http://username:password@proxy.example.com:8080)

    Returns:
        bool: True if the proxy is working, False otherwise.
    """
    url = "https://httpbin.org/ip"
    proxies = {"http": proxy_address, "https": proxy_address}

    try:
        print(f"Testing proxy: {proxy_address}")
        response = requests.get(url, proxies=proxies, timeout=10)
        response.raise_for_status()
        print(f"Proxy is working. Response: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Proxy failed: {e}")
        return False


def get_chrome_driver():
    """
    Configures and returns a Selenium WebDriver for Chrome in headless mode.
    The ChromeDriver path and proxy settings are loaded from environment variables in the .env file.
    """
    chrome_driver_path = os.getenv("CHROMEDRIVER_PATH")
    proxy_address = os.getenv(
        "PROXY_ADDRESS"
    )  # Proxy server address (e.g., "http://proxy.example.com:8080")

    if not chrome_driver_path:
        raise ValueError("CHROMEDRIVER_PATH is not set in the .env file.")

    if proxy_address:
        if not verify_proxy(proxy_address):
            raise ValueError("The proxy address is invalid or not working.")

    chrome_service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()

    # Headless mode and performance options
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Configure proxy if set
    if proxy_address:
        options.add_argument(f"--proxy-server={proxy_address}")

    driver = webdriver.Chrome(service=chrome_service, options=options)
    return driver
