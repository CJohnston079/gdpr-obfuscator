import timeit

import pytest

from src.utils.file_readers.get_csv_data import get_csv_data


class TestGetCSVData:
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
        result = get_csv_data("test-bucket", "dir/test-csv.csv")
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_returns_list_of_expected_length(self, set_up_s3_data):
        data = set_up_s3_data
        result = get_csv_data("test-bucket", "dir/test-csv.csv")
        assert len(result) == len(data)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = get_csv_data("test-bucket", "dir/empty-file.csv")
        assert result == []

    @pytest.mark.smoke
    def test_returns_expected_data(self, set_up_s3_data):
        data = set_up_s3_data
        result = get_csv_data("test-bucket", "dir/test-csv.csv")
        assert result == data


@pytest.mark.performance
class TestGetCSVDataPerformance:
    @pytest.fixture(scope="class", autouse=True)
    def set_up_s3_data(self, s3_bucket, test_large_data):
        s3, bucket_name = s3_bucket
        data = test_large_data["shallow_list_based"]

        headers = data[0].keys()
        rows = [",".join([row[key] for key in headers]) for row in data]
        csv_data = ",".join(headers) + "\n" + "\n".join(rows)

        s3.put_object(
            Bucket=bucket_name, Key="dir/large-csv.csv", Body=csv_data
        )

    def test_get_csv_data_performance(self):
        num_of_executions = 50

        execution_time = timeit.timeit(
            lambda: get_csv_data("test-bucket", "dir/large-csv.csv"),
            number=num_of_executions,
        )

        print(
            "\nAverage execution time for get_csv_data on 10,000 records: "
            f"{round(execution_time / num_of_executions, 4)} seconds"
        )
