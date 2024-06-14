from unittest.mock import patch

import pytest

from src.obfuscator import obfuscator


class TestObfuscator:
    @pytest.fixture(autouse=True)
    def setup(self, test_shallow_data):
        self.original_data = test_shallow_data["shallow_list_based"]
        self.obfuscated_data = test_shallow_data["shallow_list_based"]
        self.serialized_data = f'{test_shallow_data["shallow_list_based"]}'

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
