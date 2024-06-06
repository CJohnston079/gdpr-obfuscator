import unittest
from unittest.mock import patch
from src.utils.get_data import get_data


class TestGetData(unittest.TestCase):
    @patch("src.utils.get_data.handle_csv")
    @patch("src.utils.get_data.get_file_type")
    def test_get_data_calls_get_file_type(
            self,
            mock_get_file_type,
            mock_handle_csv
    ):
        mock_get_file_type.return_value = 'csv'
        get_data("s3://bucket/data/file.csv")
        mock_get_file_type.assert_called_once_with("s3://bucket/data/file.csv")

    @patch("src.utils.get_data.handle_csv")
    @patch("src.utils.get_data.get_file_type")
    def test_get_data_calls_handle_csv_when_file_type_is_csv(
            self,
            mock_get_file_type,
            mock_handle_csv
    ):
        mock_get_file_type.return_value = 'csv'
        get_data("s3://bucket/data/file.csv")
        mock_handle_csv.assert_called_once_with("s3://bucket/data/file.csv")

    @patch("src.utils.get_data.handle_json")
    @patch("src.utils.get_data.get_file_type")
    def test_get_data_calls_handle_csv_when_file_type_is_json(
            self,
            mock_get_file_type,
            mock_handle_json
    ):
        mock_get_file_type.return_value = 'json'
        get_data("s3://bucket/data/file.json")
        mock_handle_json.assert_called_once_with("s3://bucket/data/file.json")

    @patch("src.utils.get_data.get_file_type")
    def test_get_data_handles_unsupported_file_type(self, mock_get_file_type):
        mock_get_file_type.return_value = 'txt'

        with self.assertRaises(ValueError) as context:
            get_data("s3://bucket/data/file.txt")

        self.assertEqual(
            str(context.exception),
            "File type .txt is not supported."
        )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
