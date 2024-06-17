import pytest

from src.exceptions import FormatDataError
from src.exceptions import GetDataError
from src.exceptions import ObfuscationError
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

    @pytest.mark.xfail
    def test_obfuscator_calls_helper_functions(self, mocker):
        get_data = mocker.patch("src.obfuscator.get_data")
        obfuscate_fields = mocker.patch("src.obfuscator.obfuscate_fields")
        format_data = mocker.patch("src.obfuscator.format_data")

        get_data.return_value = self.original_data
        obfuscate_fields.return_value = self.obfuscated_data
        format_data.return_value = self.serialized_data

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.csv",
            "pii_fields": ["name"],
        }

        result = obfuscator(event)

        get_data.assert_called_once_with("s3://bucket/data/file.csv")
        obfuscate_fields.assert_called_once_with(self.original_data, ["name"])
        format_data.assert_called_once_with(self.obfuscated_data)

        assert result == self.serialized_data


@pytest.mark.error_handling
class TestObfuscatorErrorHandling:
    def test_raises_critical_exception_for_unknown_error(self, mocker, caplog):
        get_data = mocker.patch("src.obfuscator.get_data")
        get_data.side_effect = Exception

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.txt",
            "pii_fields": ["name"],
        }

        with pytest.raises(Exception):
            obfuscator(event)

        assert "An unexpected error occurred" in caplog.text
        assert any(record.levelname == "CRITICAL" for record in caplog.records)


@pytest.mark.error_handling
class TestObfuscatorHandlesPropagatedUtilExceptions:
    def test_raises_get_data_error(self, mocker, caplog):
        get_data = mocker.patch("src.obfuscator.get_data")
        get_data.side_effect = GetDataError("Error loading data")

        event = {
            "file_to_obfuscate": "s3://erroneous-file",
            "pii_fields": ["name"],
        }

        with pytest.raises(GetDataError):
            obfuscator(event)

        assert "Error loading data from" in caplog.text

    def test_raises_obfuscate_fields_error(self, mocker, caplog):
        mocker.patch("src.obfuscator.get_data")
        obfuscate_fields = mocker.patch("src.obfuscator.obfuscate_fields")
        obfuscate_fields.side_effect = ObfuscationError(
            "Error obfuscating fields"
        )

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.csv",
            "pii_fields": ["name"],
        }

        with pytest.raises(ObfuscationError):
            obfuscator(event)

        assert "Error obfuscating fields" in caplog.text

    def test_raises_format_data_error(self, mocker, caplog):
        mocker.patch("src.obfuscator.get_data")
        mocker.patch("src.obfuscator.obfuscate_fields")
        format_data = mocker.patch("src.obfuscator.format_data")
        format_data.side_effect = FormatDataError("Error serialising data")

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.csv",
            "pii_fields": ["name"],
        }

        with pytest.raises(FormatDataError):
            obfuscator(event)

        assert "Error formatting obfuscated data" in caplog.text
