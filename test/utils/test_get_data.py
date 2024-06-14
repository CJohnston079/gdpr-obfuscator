from unittest.mock import patch

import pytest

from src.utils.get_data import get_data


class TestGetData:
    @pytest.fixture(autouse=True)
    def setup(self, test_shallow_data):
        self.data = test_shallow_data["shallow_list_based"]

    @patch("src.utils.get_data.handle_csv")
    @patch("src.utils.get_data.get_file_type")
    def test_get_data_calls_get_file_type(
        self, mock_get_file_type, mock_handle_csv
    ):
        mock_get_file_type.return_value = "csv"
        get_data("s3://bucket/data/file.csv")
        mock_get_file_type.assert_called_once_with("s3://bucket/data/file.csv")

    @patch("src.utils.get_data.handle_csv")
    @patch("src.utils.get_data.get_file_type")
    def test_get_data_calls_handle_csv_when_file_type_is_csv(
        self, mock_get_file_type, mock_handle_csv
    ):
        mock_get_file_type.return_value = "csv"
        get_data("s3://bucket/data/file.csv")
        mock_handle_csv.assert_called_once_with("s3://bucket/data/file.csv")

    @patch("src.utils.get_data.handle_json")
    @patch("src.utils.get_data.get_file_type")
    def test_get_data_calls_handle_csv_when_file_type_is_json(
        self, mock_get_file_type, mock_handle_json
    ):
        mock_get_file_type.return_value = "json"
        get_data("s3://bucket/data/file.json")
        mock_handle_json.assert_called_once_with("s3://bucket/data/file.json")

    @patch("src.utils.get_data.handle_parquet")
    @patch("src.utils.get_data.get_file_type")
    def test_get_data_calls_handle_csv_when_file_type_is_parquet(
        self, mock_get_file_type, mock_handle_parquet
    ):
        mock_get_file_type.return_value = "parquet"
        get_data("s3://bucket/data/file.parquet")
        mock_handle_parquet.assert_called_once_with(
            "s3://bucket/data/file.parquet"
        )

    @patch("src.utils.get_data.handle_xml")
    @patch("src.utils.get_data.get_file_type")
    def test_get_data_calls_handle_csv_when_file_type_is_xml(
        self, mock_get_file_type, mock_handle_xml
    ):
        mock_get_file_type.return_value = "xml"
        get_data("s3://bucket/data/file.xml")
        mock_handle_xml.assert_called_once_with("s3://bucket/data/file.xml")

    @patch("src.utils.get_data.handle_csv")
    @patch("src.utils.get_data.get_file_type")
    def test_get_data_calls_returns_expected_data(
        self, mock_get_file_type, mock_handle_csv
    ):
        mock_get_file_type.return_value = "csv"
        mock_handle_csv.return_value = self.data
        result = get_data("s3://bucket/data/file.csv")

        assert result == self.data

    @patch("src.utils.get_data.get_file_type")
    def test_get_data_handles_unsupported_file_type(self, mock_get_file_type):
        mock_get_file_type.return_value = "txt"

        with pytest.raises(ValueError) as e:
            get_data("s3://bucket/data/file.txt")

        assert str(e.value) == "File type .txt is not supported."
