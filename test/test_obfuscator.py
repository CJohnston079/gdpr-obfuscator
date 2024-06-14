import pytest

from src.obfuscator import obfuscator


class TestObfuscator:
    @pytest.fixture(autouse=True)
    def setup(self, test_shallow_data):
        self.original_data = test_shallow_data["shallow_list_based"]
        self.obfuscated_data = test_shallow_data[
            "shallow_list_based_obfuscated"
        ]
        self.serialized_data = (
            f'{test_shallow_data["shallow_list_based_obfuscated"]}'
        )

    def test_obfuscator_calls_helper_functions(self, mocker):
        get_data = mocker.patch("src.obfuscator.get_data")
        obfuscate_fields = mocker.patch("src.obfuscator.obfuscate_fields")
        serialise_dicts = mocker.patch("src.obfuscator.serialise_dicts")

        get_data.return_value = self.original_data
        obfuscate_fields.return_value = self.obfuscated_data
        serialise_dicts.return_value = self.serialized_data

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.csv",
            "pii_fields": ["name"],
        }

        result = obfuscator(event)

        get_data.assert_called_once_with("s3://bucket/data/file.csv")
        obfuscate_fields.assert_called_once_with(
            self.original_data, event["pii_fields"]
        )
        serialise_dicts.assert_called_once_with(self.obfuscated_data)

        assert result == self.serialized_data
