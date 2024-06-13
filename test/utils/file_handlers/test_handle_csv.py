import boto3
import pytest

from src.utils.file_handlers.handle_csv import handle_csv


class TestHandleCSV():
    @pytest.fixture(scope="class", autouse=True)
    def setup_method(self, s3_bucket, ts_shallow_data):
        s3, bucket_name = s3_bucket
        data, _ = ts_shallow_data

        headers = data[0].keys()
        rows = [",".join([row[key] for key in headers]) for row in data]
        csv_data = ",".join(headers) + "\n" + "\n".join(rows)

        s3.put_object(Bucket=bucket_name, Key="dir/empty-file.csv", Body="")
        s3.put_object(
            Bucket=bucket_name,
            Key="dir/test-csv.csv",
            Body=csv_data
        )

        return data

    def test_returns_list_of_dicts(self):
        result = handle_csv("s3://test-bucket/dir/test-csv.csv")
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_returns_list_of_expected_length(self, setup_method):
        data = setup_method
        result = handle_csv("s3://test-bucket/dir/test-csv.csv")
        assert len(result) == len(data)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_csv("s3://test-bucket/dir/empty-file.csv")
        assert result == []

    def test_returns_expected_data(self, setup_method):
        data = setup_method
        result = handle_csv("s3://test-bucket/dir/test-csv.csv")
        assert result == data
