import timeit

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from moto import mock_aws

from src.utils.file_readers.get_parquet_data import get_parquet_data


@mock_aws
class TestGetParquetData:
    @pytest.fixture(autouse=True)
    def set_up_s3_data(self, s3_bucket, test_shallow_data):
        s3, bucket_name = s3_bucket
        data = test_shallow_data["shallow_list_based"]

        df = pd.DataFrame(data)
        table = pa.Table.from_pandas(df)
        parquet_buffer = pa.BufferOutputStream()
        pq.write_table(table, parquet_buffer)
        parquet_data = parquet_buffer.getvalue().to_pybytes()

        s3.put_object(
            Bucket=bucket_name,
            Key="dir/test_parquet.parquet",
            Body=parquet_data,
        )
        s3.put_object(
            Bucket=bucket_name, Key="dir/test_pq.pq", Body=parquet_data
        )

    def test_returns_list_of_dicts(self):
        result = get_parquet_data("test-bucket", "dir/test_parquet.parquet")
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_returns_list_of_expected_length(self, test_shallow_data):
        data = test_shallow_data["shallow_list_based"]
        result = get_parquet_data("test-bucket", "dir/test_parquet.parquet")
        assert len(result) == len(data)

    def test_returns_empty_list_when_passed_empty_file(self, s3_bucket):
        s3, bucket_name = s3_bucket

        empty_df = pd.DataFrame()
        empty_table = pa.Table.from_pandas(empty_df)
        empty_buffer = pa.BufferOutputStream()
        pq.write_table(empty_table, empty_buffer)
        empty_parquet_data = empty_buffer.getvalue().to_pybytes()

        s3.put_object(
            Bucket=bucket_name,
            Key="dir/empty_parquet.parquet",
            Body=empty_parquet_data,
        )

        result = get_parquet_data("test-bucket", "dir/empty_parquet.parquet")
        assert result == []

    def test_returns_expected_data(self, test_shallow_data):
        data = test_shallow_data["shallow_list_based"]
        result = get_parquet_data("test-bucket", "dir/test_parquet.parquet")
        assert result == data

    def test_handles_files_with_pq_extension(self, test_shallow_data):
        data = test_shallow_data["shallow_list_based"]
        result = get_parquet_data("test-bucket", "dir/test_pq.pq")
        assert result == data


@pytest.mark.performance
class TestGetParquetDataPerformance:
    @pytest.fixture(scope="class", autouse=True)
    def set_up_s3_data(self, s3_bucket, test_large_data):
        s3, bucket_name = s3_bucket
        data = test_large_data["shallow_list_based"]

        df = pd.DataFrame(data)
        table = pa.Table.from_pandas(df)
        parquet_buffer = pa.BufferOutputStream()
        pq.write_table(table, parquet_buffer)
        parquet_data = parquet_buffer.getvalue().to_pybytes()

        s3.put_object(
            Bucket=bucket_name,
            Key="dir/large_parquet.pq",
            Body=parquet_data,
        )

    def test_get_parquet_data_performance(self):
        num_of_executions = 50

        execution_time = timeit.timeit(
            lambda: get_parquet_data("test-bucket", "dir/large_parquet.pq"),
            number=num_of_executions,
        )

        print(
            "\nAverage execution time for get_parquet_data on 10,000 records: "
            f"{round(execution_time / num_of_executions, 4)} seconds"
        )
