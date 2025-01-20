# tests/test_utils.py
import os
import unittest
from src.data_collection.utils import save_html, load_html
from src.data_collection.constants import BASE_DIR

class TestUtils(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory for testing."""
        self.test_dir = os.path.join(BASE_DIR, "test")
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file = "test.html"
        self.test_content = "<html><body>Test Content</body></html>"

    def tearDown(self):
        """Remove the temporary directory and its contents."""
        os.remove(os.path.join(self.test_dir, self.test_file))
        os.rmdir(self.test_dir)

    def test_save_and_load_html(self):
        """Test saving and loading HTML files."""
        save_html(self.test_content, self.test_dir, self.test_file)
        loaded_content = load_html(self.test_dir, self.test_file)
        self.assertEqual(self.test_content, loaded_content)

if __name__ == "__main__":
    unittest.main()
