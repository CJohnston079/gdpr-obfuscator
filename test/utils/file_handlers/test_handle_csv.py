import pytest

from src.utils.file_handlers.handle_csv import handle_csv


class TestHandleCSV:
    @pytest.fixture(scope="class", autouse=True)
    def set_up_s3_data(self, s3_bucket, test_shallow_data):
        s3, bucket_name = s3_bucket
        data = test_shallow_data["shallow_list_based"]

        headers = data[0].keys()
        rows = [",".join([row[key] for key in headers]) for row in data]
        csv_data = ",".join(headers) + "\n" + "\n".join(rows)

        s3.put_object(Bucket=bucket_name, Key="dir/empty-file.csv", Body="")
        s3.put_object(
            Bucket=bucket_name, Key="dir/test-csv.csv", Body=csv_data
        )

        return data

    def test_returns_list_of_dicts(self):
        result = handle_csv("test-bucket", "dir/test-csv.csv")
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_returns_list_of_expected_length(self, set_up_s3_data):
        data = set_up_s3_data
        result = handle_csv("test-bucket", "dir/test-csv.csv")
        assert len(result) == len(data)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_csv("test-bucket", "dir/empty-file.csv")
        assert result == []

    def test_returns_expected_data(self, set_up_s3_data):
        data = set_up_s3_data
        result = handle_csv("test-bucket", "dir/test-csv.csv")
        assert result == data
