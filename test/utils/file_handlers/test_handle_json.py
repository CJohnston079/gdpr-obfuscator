import json

import pytest

from src.utils.file_handlers.handle_json import handle_json


class TestHandleJSON:
    @pytest.fixture(scope="class", autouse=True)
    def set_up_s3_data(self, s3_bucket, test_shallow_data, test_deep_data):
        s3, bucket_name = s3_bucket
        shallow_data = test_shallow_data["shallow_list_based"]
        deep_data = test_deep_data["deep_list_based"]

        s3.put_object(Bucket=bucket_name, Key="dir/empty.json", Body="")
        s3.put_object(
            Bucket=bucket_name,
            Key="dir/shallowData.json",
            Body=json.dumps(shallow_data),
        )
        s3.put_object(
            Bucket=bucket_name,
            Key="dir/deepData.json",
            Body=json.dumps(deep_data),
        )

    def test_returns_list_of_dicts(self):
        result = handle_json("test-bucket", "dir/shallowData.json")
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_returns_list_of_expected_length(self, test_shallow_data):
        shallow_data = test_shallow_data["shallow_list_based"]
        result = handle_json("test-bucket", "dir/shallowData.json")
        assert len(result) == len(shallow_data)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_json("test-bucket", "dir/empty.json")
        assert result == []

    def test_returns_expected_shallow_data(self, test_shallow_data):
        shallow_data = test_shallow_data["shallow_list_based"]
        result = handle_json("test-bucket", "dir/shallowData.json")
        assert result == shallow_data

    def test_returns_expected_deep_data(self, test_deep_data):
        deep_data = test_deep_data["deep_list_based"]
        result = handle_json("test-bucket", "dir/deepData.json")
        assert result == deep_data
