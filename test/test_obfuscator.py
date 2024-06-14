import unittest
from unittest.mock import patch

from src.obfuscator import obfuscator


class TestObfuscator(unittest.TestCase):
    def setUp(self):
        self.original_data = [
            {"name": "George", "age": "44", "city": "York"},
            {"name": "Lindsay", "age": "40", "city": "Leeds"},
            {"name": "Michael", "age": "37", "city": "Sheffield"},
        ]
        self.obfuscated_data = [
            {"name": "***", "age": "***", "city": "York"},
            {"name": "***", "age": "***", "city": "Leeds"},
            {"name": "***", "age": "***", "city": "Sheffield"},
        ]
        self.serialized_data = """[
            {"name": "***", "age": "***", "city": "York"},
            {"name": "***", "age": "***", "city": "Leeds"},
            {"name": "***", "age": "***", "city": "Sheffield"}
        ]"""

    @patch("src.obfuscator.serialise_dicts")
    @patch("src.obfuscator.obfuscate_fields")
    @patch("src.obfuscator.get_data")
    def test_obfuscator_calls_helper_functions(
        self, mock_get_data, mock_obfuscate_fields, mock_serialise_dicts
    ):
        mock_get_data.return_value = self.original_data
        mock_obfuscate_fields.return_value = self.obfuscated_data
        mock_serialise_dicts.return_value = self.serialized_data

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.csv",
            "pii_fields": ["name", "age"],
        }

        result = obfuscator(event)

        mock_get_data.assert_called_once_with("s3://bucket/data/file.csv")
        mock_obfuscate_fields.assert_called_once_with(
            self.original_data, event["pii_fields"]
        )
        mock_serialise_dicts.assert_called_once_with(self.obfuscated_data)

        assert result == self.serialized_data


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
