import timeit

import pytest

from src.exceptions import FormatDataError
from src.utils.format_data import format_data


class TestFormatData:
    @pytest.mark.parametrize(
        "file_type, file_handler",
        [
            ("csv", "src.utils.format_data.format_csv_data"),
            ("json", "src.utils.format_data.format_json_data"),
            ("parquet", "src.utils.format_data.format_parquet_data"),
            ("xml", "src.utils.format_data.format_xml_data"),
            (None, "src.utils.format_data.serialise_data"),
        ],
    )
    def test_calls_format_data_with_expected_function(
        self, mocker, file_type, file_handler
    ):
        mock_file_handler = mocker.patch(file_handler)
        format_data(["data"], file_type)
        mock_file_handler.assert_called_once_with(["data"])

    @pytest.mark.smoke
    def test_calls_returns_expected_data(self, mocker, test_xml_data):
        data = test_xml_data["shallow_xml_data"]
        xml_string = test_xml_data["shallow_xml_str"]

        format_xml_data = mocker.patch("src.utils.format_data.format_xml_data")
        format_xml_data.return_value = xml_string
        result = format_data(data, "xml")

        assert result == xml_string


@pytest.mark.error_handling
class TestFormatDataErrorHandling:
    def test_raises_format_data_error_for_exceptions(self, mocker):
        serialise_data = mocker.patch("src.utils.format_data.serialise_data")
        serialise_data.side_effect = Exception

        with pytest.raises(FormatDataError):
            format_data("erroneous-data")


@pytest.mark.performance
class TestFormatDataPerformance:
    def test_format_data_performance(self, test_large_data):
        data = test_large_data["shallow_dict_based"]
        num_of_executions = 50

        execution_time = timeit.timeit(
            lambda: format_data(data), number=num_of_executions
        )

        print(
            "\nAverage execution time for format_data on 10,000 records: "
            f"{round(execution_time / num_of_executions, 4)} seconds"
        )
