import json
import boto3
import unittest

from moto import mock_aws
from unittest.mock import patch, mock_open
from src.utils.file_handlers.handle_json import handle_json


@mock_aws
class TestHandleJson(unittest.TestCase):
    def setUp(self):
        self.sample_shallow_data = [
            {"name": "George", "age": "44", "city": "York"},
            {"name": "Lindsay", "age": "40", "city": "Leeds"},
            {"name": "Michael", "age": "37", "city": "Sheffield"}
        ]

        self.sample_deep_data = [
            {
                "name": "George",
                "age": "44",
                "city": "York",
                "contact": [
                    {"email": "george@bluthcompany.com"},
                    {"phone": "01904 123456"}
                ],
            },
            {
                "name": "Lindsay",
                "age": "40",
                "city": "Leeds",
                "contact": [
                    {"email": "lindsay@bluthcompany.com"},
                    {"phone": "0113 123456"}
                ],
            },
            {
                "name": "Michael",
                "age": "37",
                "city": "Sheffield",
                "contact": [
                    {"email": "michael@bluthcompany.com"},
                    {"phone": "0114 123456"}
                ],
            }
        ]

        sample_shallow_json_data = json.dumps(self.sample_shallow_data)
        sample_deep_json_data = json.dumps(self.sample_deep_data)

        bucket_name = "test-bucket"
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        s3.put_object(Bucket=bucket_name, Key="test/test-empty.json", Body="")
        s3.put_object(
            Bucket=bucket_name,
            Key="test/shallow-data.json",
            Body=sample_shallow_json_data
        )
        s3.put_object(
            Bucket=bucket_name,
            Key="test/deep-data.json",
            Body=sample_deep_json_data
        )

    def test_returns_list_of_dicts(self):
        result = handle_json("s3://test-bucket/test/shallow-data.json")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(row, dict) for row in result))

    def test_returns_list_of_expected_length(self):
        result = handle_json("s3://test-bucket/test/shallow-data.json")
        self.assertEqual(len(result), 3)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_json("s3://test-bucket/test/test-empty.json")

        print(result)
        self.assertEqual(result, [])

    def test_returns_expected_shallow_data(self):
        result = handle_json("s3://test-bucket/test/shallow-data.json")
        self.assertEqual(result, self.sample_shallow_data)

    def test_returns_expected_deep_data(self):
        result = handle_json("s3://test-bucket/test/deep-data.json")
        self.assertEqual(result, self.sample_deep_data)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
