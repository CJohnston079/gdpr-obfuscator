import timeit

import pytest

from src.utils.file_readers.get_xml_data import get_xml_data


class TestGetXMLData:
    @pytest.fixture(scope="class", autouse=True)
    def set_up_s3_data(self, s3_bucket, test_xml_data):
        s3, bucket_name = s3_bucket

        shallow_xml_data = test_xml_data["shallow_xml_str"]
        deep_xml_data = test_xml_data["deep_xml_str"]

        s3.put_object(Bucket=bucket_name, Key="dir/empty-file.xml", Body="")
        s3.put_object(
            Bucket=bucket_name,
            Key="dir/shallow-data.xml",
            Body=shallow_xml_data,
        )
        s3.put_object(
            Bucket=bucket_name, Key="dir/deep-data.xml", Body=deep_xml_data
        )

    def test_returns_list_of_dicts(self):
        result = get_xml_data("test-bucket", "dir/shallow-data.xml")
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_returns_list_of_expected_length(self, test_xml_data):
        shallow_data = test_xml_data["shallow_xml_data"]
        result = get_xml_data("test-bucket", "dir/shallow-data.xml")
        assert len(result) == len(shallow_data)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = get_xml_data("test-bucket", "dir/empty-file.xml")
        assert result == []

    def test_returns_expected_shallow_data(self, test_xml_data):
        shallow_data = test_xml_data["shallow_xml_data"]
        result = get_xml_data("test-bucket", "dir/shallow-data.xml")

        assert result == shallow_data

    def test_returns_expected_deep_data(self, test_xml_data):
        deep_data = test_xml_data["deep_xml_data"]
        result = get_xml_data("test-bucket", "dir/deep-data.xml")

        assert result == deep_data


@pytest.mark.performance
class TestGetXMLDataPerformance:
    @pytest.fixture(scope="class", autouse=True)
    def set_up_s3_data(self, s3_bucket, test_large_data):
        s3, bucket_name = s3_bucket
        data = test_large_data["shallow_xml_str"]

        s3.put_object(
            Bucket=bucket_name,
            Key="dir/large-data.xml",
            Body=data,
        )

    def test_get_xml_data_performance(self):
        num_of_executions = 50

        execution_time = timeit.timeit(
            lambda: get_xml_data("test-bucket", "dir/large-data.xml"),
            number=num_of_executions,
        )

        print(
            "\nAverage execution time for get_xml_data on 10,000 records: "
            f"{round(execution_time / num_of_executions, 4)} seconds"
        )
