import boto3
import pytest

from src.utils.file_handlers.handle_xml import handle_xml


class TestHandleXML():
    @pytest.fixture(scope="class", autouse=True)
    def set_up_s3_data(self, s3_bucket, test_xml_data):
        s3, bucket_name = s3_bucket

        shallow_data = test_xml_data["shallow_object_based"]
        shallow_xml_data = test_xml_data["shallow_xml_str"]
        deep_data = test_xml_data["deep_object_based"]
        deep_xml_data = test_xml_data["deep_xml_str"]

        s3.put_object(Bucket=bucket_name, Key="dir/empty-file.xml", Body="")
        s3.put_object(
            Bucket=bucket_name,
            Key="dir/shallow-data.xml",
            Body=shallow_xml_data
        )
        s3.put_object(
            Bucket=bucket_name,
            Key="dir/deep-data.xml",
            Body=deep_xml_data
        )

    def test_returns_list_of_dicts(self):
        result = handle_xml("s3://test-bucket/dir/shallow-data.xml")
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_returns_list_of_expected_length(self, test_xml_data):
        shallow_data = test_xml_data["shallow_object_based"]
        result = handle_xml("s3://test-bucket/dir/shallow-data.xml")
        assert len(result) == len(shallow_data)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_xml("s3://test-bucket/dir/empty-file.xml")
        assert result == []

    def test_returns_expected_shallow_data(self, test_xml_data):
        shallow_data = test_xml_data["shallow_object_based"]
        result = handle_xml("s3://test-bucket/dir/shallow-data.xml")

        assert result == shallow_data

    def test_returns_expected_deep_data(self, test_xml_data):
        deep_data = test_xml_data["deep_object_based"]
        result = handle_xml("s3://test-bucket/dir/deep-data.xml")
        assert result == deep_data
