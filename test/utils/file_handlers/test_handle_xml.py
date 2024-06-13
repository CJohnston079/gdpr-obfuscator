import boto3
import pytest

from src.utils.file_handlers.handle_xml import handle_xml


class TestHandleXML():
    @pytest.fixture(scope="class", autouse=True)
    def set_up_s3_data(self, s3_bucket, test_xml_data):
        s3, bucket_name = s3_bucket

        sample_shallow_data = test_xml_data["shallow_object_based"]
        sample_shallow_xml_data = test_xml_data["shallow_xml_str"]
        sample_deep_data = test_xml_data["deep_object_based"]
        sample_deep_xml_data = test_xml_data["deep_xml_str"]

        s3.put_object(Bucket=bucket_name, Key="dir/empty-file.xml", Body="")
        s3.put_object(
            Bucket=bucket_name,
            Key="dir/shallow-data.xml",
            Body=sample_shallow_xml_data
        )
        s3.put_object(
            Bucket=bucket_name,
            Key="dir/deep-data.xml",
            Body=sample_deep_xml_data
        )

        return sample_shallow_data, sample_deep_data

    def test_returns_list_of_dicts(self):
        result = handle_xml("s3://test-bucket/dir/shallow-data.xml")
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_returns_list_of_expected_length(self, set_up_s3_data):
        sample_shallow_data, _ = set_up_s3_data
        result = handle_xml("s3://test-bucket/dir/shallow-data.xml")
        assert len(result) == len(sample_shallow_data)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_xml("s3://test-bucket/dir/empty-file.xml")
        assert result == []

    def test_returns_expected_shallow_data(self, set_up_s3_data):
        sample_shallow_data, _ = set_up_s3_data
        result = handle_xml("s3://test-bucket/dir/shallow-data.xml")

        assert result == sample_shallow_data

    def test_returns_expected_deep_data(self, set_up_s3_data):
        _, sample_deep_data = set_up_s3_data
        result = handle_xml("s3://test-bucket/dir/deep-data.xml")
        assert result == sample_deep_data
