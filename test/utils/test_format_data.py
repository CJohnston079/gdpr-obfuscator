import pytest

from src.exceptions import FormatDataError
from src.utils.format_data import format_data


class TestFormatData:
    def test_format_data_calls_serialise_data(self, mocker):
        serialise_data = mocker.patch("src.utils.format_data.serialise_data")
        format_data(["data"])
        serialise_data.assert_called_once_with(["data"])


class TestFormatDataErrorHandling:
    def test_raises_format_data_error_for_exceptions(self, mocker):
        serialise_data = mocker.patch("src.utils.format_data.serialise_data")
        serialise_data.side_effect = Exception

        with pytest.raises(FormatDataError):
            format_data("erroneous-data")
