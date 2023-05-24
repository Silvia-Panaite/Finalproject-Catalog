from unittest import TestCase
from unittest.mock import patch

from src.presentation import get_new_catalog_data


class PresentationTest(TestCase):
    def test_get_new_catalog_data(self):
        with patch("builtins.input", side_effect=["mock_subject", "mock_grade1", "mock_grade2"]):
            result = get_new_catalog_data()
            self.assertEqual(
                result,
                {
                    "title": "mock_subject",
                    "url": "mock_grade1",
                    "notes": "mock_grade2"
                }
            )