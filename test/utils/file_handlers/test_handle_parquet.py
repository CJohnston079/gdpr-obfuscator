import boto3
import unittest
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

from moto import mock_aws
from src.utils.file_handlers.handle_parquet import handle_parquet


@mock_aws
class TestHandleParquet(unittest.TestCase):
    def setUp(self):
        self.sample_data = [
            {"name": "George", "age": 44, "city": "York"},
            {"name": "Lindsay", "age": 40, "city": "Leeds"},
            {"name": "Michael", "age": 37, "city": "Sheffield"}
        ]

        df = pd.DataFrame(self.sample_data)
        table = pa.Table.from_pandas(df)
        parquet_buffer = pa.BufferOutputStream()
        pq.write_table(table, parquet_buffer)
        parquet_data = parquet_buffer.getvalue().to_pybytes()

        self.bucket_name = "test-bucket"
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        s3.put_object(
            Bucket=self.bucket_name,
            Key="test/test.parquet",
            Body=parquet_data
        )
        s3.put_object(
            Bucket=self.bucket_name,
            Key="test/test.pq",
            Body=parquet_data
        )

    def test_returns_list_of_dicts(self):
        result = handle_parquet("s3://test-bucket/test/test.parquet")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(row, dict) for row in result))

    def test_returns_list_of_expected_length(self):
        result = handle_parquet("s3://test-bucket/test/test.parquet")
        self.assertEqual(len(result), 3)

    def test_returns_empty_list_when_passed_empty_file(self):
        empty_df = pd.DataFrame()
        empty_table = pa.Table.from_pandas(empty_df)
        empty_buffer = pa.BufferOutputStream()
        pq.write_table(empty_table, empty_buffer)
        empty_parquet_data = empty_buffer.getvalue().to_pybytes()

        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=self.bucket_name)
        s3.put_object(
            Bucket=self.bucket_name,
            Key="test/empty-file.parquet",
            Body=empty_parquet_data
        )

        result = handle_parquet("s3://test-bucket/test/empty-file.parquet")
        self.assertEqual(result, [])

    def test_returns_expected_data(self):
        result = handle_parquet("s3://test-bucket/test/test.parquet")
        self.assertEqual(result, self.sample_data)

    def test_handles_files_with_pq_extension(self):
        result = handle_parquet("s3://test-bucket/test/test.pq")
        self.assertEqual(result, self.sample_data)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
