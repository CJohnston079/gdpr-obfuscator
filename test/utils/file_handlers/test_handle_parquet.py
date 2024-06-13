import boto3
import pytest
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

from moto import mock_aws
from src.utils.file_handlers.handle_parquet import handle_parquet


@mock_aws
class TestHandleParquet:
    @pytest.fixture(autouse=True)
    def setup_method(self, s3_bucket, ts_shallow_data):
        s3, bucket_name = s3_bucket
        shallow_data, _ = ts_shallow_data

        df = pd.DataFrame(shallow_data)
        table = pa.Table.from_pandas(df)
        parquet_buffer = pa.BufferOutputStream()
        pq.write_table(table, parquet_buffer)
        parquet_data = parquet_buffer.getvalue().to_pybytes()

        s3.put_object(
            Bucket=bucket_name,
            Key="dir/test_parquet.parquet",
            Body=parquet_data
        )
        s3.put_object(
            Bucket=bucket_name,
            Key="dir/test_pq.pq",
            Body=parquet_data
        )

    def test_returns_list_of_dicts(self):
        result = handle_parquet("s3://test-bucket/dir/test_parquet.parquet")
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_returns_list_of_expected_length(self, ts_shallow_data):
        shallow_data, _ = ts_shallow_data
        result = handle_parquet("s3://test-bucket/dir/test_parquet.parquet")
        assert len(result) == len(shallow_data)

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
            Body=empty_parquet_data
        )

        result = handle_parquet("s3://test-bucket/dir/empty_parquet.parquet")
        assert result == []

    def test_returns_expected_data(self, ts_shallow_data):
        shallow_data, _ = ts_shallow_data
        result = handle_parquet("s3://test-bucket/dir/test_parquet.parquet")
        assert result == shallow_data

    def test_handles_files_with_pq_extension(self, ts_shallow_data):
        shallow_data, _ = ts_shallow_data
        result = handle_parquet("s3://test-bucket/dir/test_pq.pq")
        assert result == shallow_data
