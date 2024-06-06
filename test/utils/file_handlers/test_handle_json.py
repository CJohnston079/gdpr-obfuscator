import json
import boto3
import unittest

from moto import mock_aws
from unittest.mock import patch, mock_open
from src.utils.file_handlers.handle_json import handle_json


@mock_aws
class TestHandleJson(unittest.TestCase):
    def setUp(self):
        self.sample_data = [
            {'name': 'George', 'age': '44', 'city': 'York'},
            {'name': 'Lindsay', 'age': '40', 'city': 'Leeds'},
            {'name': 'Michael', 'age': '37', 'city': 'Sheffield'}
        ]

        sample_json_data = json.dumps(self.sample_data)

        bucket_name = 'test-bucket'
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        s3.put_object(Bucket=bucket_name, Key='test/empty-file.json', Body="")
        s3.put_object(
            Bucket=bucket_name,
            Key='test/test.json',
            Body=sample_json_data
        )

    def test_returns_list_of_dicts(self):
        result = handle_json("s3://test-bucket/test/test.json")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(row, dict) for row in result))

    def test_returns_list_of_expected_length(self):
        result = handle_json("s3://test-bucket/test/test.json")
        self.assertEqual(len(result), 3)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_json("s3://test-bucket/test/empty-file.json")

        print(result)
        self.assertEqual(result, [])

    def test_returns_expected_data(self):
        result = handle_json("s3://test-bucket/test/test.json")
        self.assertEqual(result, self.sample_data)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
