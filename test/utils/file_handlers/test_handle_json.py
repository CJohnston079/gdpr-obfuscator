import json
import boto3
import pytest

from moto import mock_aws
from src.utils.file_handlers.handle_json import handle_json


class TestHandleJson:
    @pytest.fixture(scope="class", autouse=True)
    def set_up_s3_data(
        self, s3_bucket, ts_shallow_data, ts_deep_array_based_data
    ):
        s3, bucket_name = s3_bucket
        shallow_data, _ = ts_shallow_data
        deep_data, _ = ts_deep_array_based_data

        s3.put_object(Bucket=bucket_name, Key="test/empty.json", Body="")
        s3.put_object(
            Bucket=bucket_name,
            Key="test/shallow-data.json",
            Body=json.dumps(shallow_data)
        )
        s3.put_object(
            Bucket=bucket_name,
            Key="test/deep-data.json",
            Body=json.dumps(deep_data)
        )

    def test_returns_list_of_dicts(self):
        result = handle_json("s3://test-bucket/test/shallow-data.json")
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_returns_list_of_expected_length(self, ts_shallow_data):
        shallow_data, _ = ts_shallow_data
        result = handle_json("s3://test-bucket/test/shallow-data.json")
        assert len(result) == len(shallow_data)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_json("s3://test-bucket/test/empty.json")
        assert result == []

    def test_returns_expected_shallow_data(self, ts_shallow_data):
        shallow_data, _ = ts_shallow_data
        result = handle_json("s3://test-bucket/test/shallow-data.json")
        assert result == shallow_data

    def test_returns_expected_deep_data(self, ts_deep_array_based_data):
        deep_data, _ = ts_deep_array_based_data
        result = handle_json("s3://test-bucket/test/deep-data.json")
        assert result == deep_data


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
