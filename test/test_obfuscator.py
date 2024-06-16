import pytest

from src.exceptions import GetDataError
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
        obfuscate_fields.assert_called_once_with(self.original_data, ["name"])
        serialise_dicts.assert_called_once_with(self.obfuscated_data)

        assert result == self.serialized_data


@pytest.mark.error_handling
class TestObfuscatorErrorHandling:
    def test_raises_generic_exception(self, mocker):
        get_data = mocker.patch("src.obfuscator.get_data")
        get_data.side_effect = Exception

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.txt",
            "pii_fields": ["name"],
        }

        with pytest.raises(Exception) as e:
            obfuscator(event)

        assert str(e.value) == "An unknown error occurred."


@pytest.mark.error_handling
class TestObfuscatorHandlesGetDataError:
    @pytest.mark.parametrize(
        "event, expected_message",
        [
            (
                {
                    "file_to_obfuscate": "s3://bucket/data/file.txt",
                    "pii_fields": ["name"],
                },
                "GetDataError: error fetching data from "
                "s3://bucket/data/file.txt: "
                "UnsupportedFile: file type .txt is not supported.",
            ),
            (
                {
                    "file_to_obfuscate": "s3://bucket/data/file",
                    "pii_fields": ["name"],
                },
                "GetDataError: error fetching data from "
                "s3://bucket/data/file: "
                "FileTypeExtractionError: unable to get file extension from "
                "s3://bucket/data/file",
            ),
        ],
    )
    def test_handles_get_data_errors(self, event, expected_message, caplog):
        with pytest.raises(GetDataError):
            obfuscator(event)

        assert expected_message in caplog.text
