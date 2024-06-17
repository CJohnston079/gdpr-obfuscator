import pytest
from botocore.exceptions import ClientError

from src.exceptions import GetDataError
from src.utils.get_data import get_data


class TestGetData:
    @pytest.mark.parametrize(
        "file_type, file_path, file_handler",
        [
            ("csv", "s3://bucket/data/file.csv", "get_csv_data"),
            ("json", "s3://bucket/data/file.json", "get_json_data"),
            ("parquet", "s3://bucket/data/file.parquet", "get_parquet_data"),
            ("xml", "s3://bucket/data/file.xml", "get_xml_data"),
        ],
    )
    def test_get_data_calls_correct_function(
        self, mocker, file_type, file_path, file_handler
    ):
        mock_file_handler = mocker.patch(f"src.utils.get_data.{file_handler}")

        get_data(file_path, file_type)

        bucket, key = file_path.replace("s3://", "").split("/", 1)
        mock_file_handler.assert_called_once_with(bucket, key)


@pytest.mark.error_handling
class TestGetDataErrorHandling:
    def test_get_data_handles_unsupported_file_type(self):
        with pytest.raises(TypeError) as e:
            get_data("s3://bucket/data/file.txt", "txt")

        assert str(e.value) == ("file type .txt is not supported")

    def test_raises_get_data_error_for_caught_exceptions(self, mocker):
        get_csv_data = mocker.patch("src.utils.get_data.get_csv_data")
        get_csv_data.side_effect = Exception

        with pytest.raises(GetDataError):
            get_data("s3://bucket/data/file.csv", "csv")


@pytest.mark.error_handling
class TestClientErrorResponses:
    @pytest.mark.parametrize(
        "file_path, exception",
        [
            ("s3://test-bucket/missing_file.csv", FileNotFoundError),
            ("s3://test-bucket/protected_file.csv", PermissionError),
            ("s3://test-bucket/other_file.csv", IOError),
            ("s3://test-bucket/invalid_data.csv", GetDataError),
        ],
    )
    def test_get_data_client_errors(self, mocker, file_path, exception):
        get_csv_data = mocker.patch("src.utils.get_data.get_csv_data")

        if exception == FileNotFoundError:
            get_csv_data.side_effect = ClientError(
                {"Error": {"Code": "NoSuchKey"}}, "operation_name"
            )
        elif exception == PermissionError:
            get_csv_data.side_effect = ClientError(
                {"Error": {"Code": "AccessDenied"}}, "operation_name"
            )
        elif exception == IOError:
            get_csv_data.side_effect = ClientError(
                {"Error": {"Code": "OtherError"}}, "operation_name"
            )
        elif exception == GetDataError:
            get_csv_data.side_effect = ValueError("Invalid CSV")

        with pytest.raises(exception):
            get_data(file_path, "csv")
