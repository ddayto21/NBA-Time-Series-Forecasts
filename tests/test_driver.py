import os
import unittest
from unittest.mock import patch, MagicMock
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from data_collection.driver import get_chrome_driver, verify_proxy
from dotenv import load_dotenv
import requests


# Load environment variables from .env file
load_dotenv()


class TestChromeDriver(unittest.TestCase):
    @patch("data_collection.driver.Service")
    @patch("data_collection.driver.webdriver.Chrome")
    @patch("data_collection.driver.os.getenv")
    def test_get_chrome_driver_success(self, mock_getenv, mock_chrome, mock_service):
        """Test that get_chrome_driver returns a configured WebDriver instance."""
        # Arrange
        mock_getenv.side_effect = lambda key: (
            "/mock/path/to/chromedriver" if key == "CHROMEDRIVER_PATH" else None
        )
        mock_driver_instance = MagicMock(spec=WebDriver)
        mock_chrome.return_value = mock_driver_instance

        # Act
        driver = get_chrome_driver()

        # Assert
        mock_getenv.assert_any_call("CHROMEDRIVER_PATH")
        mock_service.assert_called_once_with("/mock/path/to/chromedriver")
        mock_chrome.assert_called_once()
        self.assertEqual(driver, mock_driver_instance)

    @patch("data_collection.driver.os.getenv")
    def test_get_chrome_driver_no_env_variable(self, mock_getenv):
        """Test that get_chrome_driver raises a ValueError if CHROMEDRIVER_PATH is not set."""
        # Arrange
        mock_getenv.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            get_chrome_driver()

        self.assertEqual(
            str(context.exception), "CHROMEDRIVER_PATH is not set in the .env file."
        )

    @patch("data_collection.driver.requests.get")
    def test_verify_proxy_success(self, mock_requests_get):
        """Test that verify_proxy returns True for a working proxy."""
        # Arrange
        proxy_address = os.getenv("PROXY_ADDRESS")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"origin": "123.45.67.89"}
        mock_requests_get.return_value = mock_response

        # Act
        result = verify_proxy(proxy_address)

        # Assert
        mock_requests_get.assert_called_once_with(
            "https://httpbin.org/ip",
            proxies={"http": proxy_address, "https": proxy_address},
            timeout=10,
        )
        self.assertTrue(result)

    @patch("data_collection.driver.requests.get")
    def test_verify_proxy_failure(self, mock_requests_get):
        """Test that verify_proxy returns False for a non-working proxy."""
        # Arrange
        proxy_address = os.getenv("PROXY_ADDRESS")
        mock_requests_get.side_effect = requests.exceptions.RequestException(
            "Connection error"
        )

        # Act
        result = verify_proxy(proxy_address)

        # Assert
        mock_requests_get.assert_called_once_with(
            "https://httpbin.org/ip",
            proxies={"http": proxy_address, "https": proxy_address},
            timeout=10,
        )
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
