import boto3
import unittest

from moto import mock_aws
from unittest.mock import patch, mock_open
from src.utils.file_handlers.handle_csv import handle_csv


@mock_aws
class TestHandleCSV(unittest.TestCase):
    def setUp(self):
        self.sample_data = [
            {'name': 'George', 'age': '44', 'city': 'York'},
            {'name': 'Lindsay', 'age': '40', 'city': 'Leeds'},
            {'name': 'Michael', 'age': '37', 'city': 'Sheffield'}
        ]

        sample_csv_data = (
            "name,age,city\n"
            "George,44,York\n"
            "Lindsay,40,Leeds\n"
            "Michael,37,Sheffield"
        )

        bucket_name = 'test-bucket'
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        s3.put_object(Bucket=bucket_name, Key='test/empty-file.csv', Body="")
        s3.put_object(
            Bucket=bucket_name,
            Key='test/test.csv',
            Body=sample_csv_data
        )

    def test_returns_list_of_dicts(self):
        result = handle_csv("s3://test-bucket/test/test.csv")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(row, dict) for row in result))

    def test_returns_list_of_expected_length(self):
        result = handle_csv("s3://test-bucket/test/test.csv")
        self.assertEqual(len(result), 3)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_csv("s3://test-bucket/test/empty-file.csv")
        self.assertEqual(result, [])

    def test_returns_expected_data(self):
        result = handle_csv("s3://test-bucket/test/test.csv")
        self.assertEqual(result, self.sample_data)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
