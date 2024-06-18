import timeit

import boto3
import pytest
from moto import mock_aws

from src.exceptions import FormatDataError
from src.exceptions import GetDataError
from src.exceptions import ObfuscationError
from src.obfuscator import obfuscator


class TestObfuscator:
    def test_obfuscator_calls_helper_functions(
        self, mocker, test_shallow_data
    ):
        original_data = test_shallow_data["shallow_list_based"]
        obfuscated_data = test_shallow_data["shallow_list_based_obfuscated"]

        get_file_type = mocker.patch("src.obfuscator.get_file_type")
        get_data = mocker.patch("src.obfuscator.get_data")
        obfuscate_fields = mocker.patch("src.obfuscator.obfuscate_fields")
        format_data = mocker.patch("src.obfuscator.format_data")

        get_file_type.return_value = "csv"
        get_data.return_value = original_data
        obfuscate_fields.return_value = obfuscated_data

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.csv",
            "pii_fields": ["name"],
        }

        obfuscator(event)

        get_file_type.assert_called_once_with("s3://bucket/data/file.csv")
        get_data.assert_called_once_with("s3://bucket/data/file.csv", "csv")
        obfuscate_fields.assert_called_once_with(original_data, ["name"])
        format_data.assert_called_once_with(obfuscated_data, "csv")

    def test_obfuscator_returns_expected_value(self, mocker, test_xml_data):
        original_data = test_xml_data["shallow_dict_based"]
        obfuscated_data = test_xml_data["shallow_dict_based"]
        expected_return = test_xml_data["shallow_xml_str"]

        get_file_type = mocker.patch("src.obfuscator.get_file_type")
        get_data = mocker.patch("src.obfuscator.get_data")
        obfuscate_fields = mocker.patch("src.obfuscator.obfuscate_fields")
        format_data = mocker.patch("src.obfuscator.format_data")

        get_file_type.return_value = "xml"
        get_data.return_value = original_data
        obfuscate_fields.return_value = obfuscated_data
        format_data.return_value = expected_return

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.xml",
            "pii_fields": ["name"],
        }

        result = obfuscator(event)

        assert result == expected_return


@pytest.mark.error_handling
class TestObfuscatorErrorHandling:
    def test_raises_critical_exception_for_unknown_error(self, mocker, caplog):
        get_file_type = mocker.patch("src.obfuscator.get_file_type")
        get_file_type.side_effect = Exception

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.txt",
            "pii_fields": ["name"],
        }

        with pytest.raises(Exception):
            obfuscator(event)

        assert "An unexpected error occurred" in caplog.text
        assert any(record.levelname == "CRITICAL" for record in caplog.records)


@pytest.mark.error_handling
class TestObfuscatorHandlesPropagatedUtilExceptions:
    def test_raises_attribute_error(self, mocker, caplog):
        get_file_type = mocker.patch("src.obfuscator.get_file_type")
        get_file_type.side_effect = AttributeError

        event = {
            "file_to_obfuscate": "s3://data/file",
            "pii_fields": ["name"],
        }

        with pytest.raises(AttributeError):
            obfuscator(event)

        assert "Error extracting file type" in caplog.text

    def test_raises_get_data_error(self, mocker, caplog):
        mocker.patch("src.obfuscator.get_file_type")
        get_data = mocker.patch("src.obfuscator.get_data")
        get_data.side_effect = GetDataError("Error loading data")

        event = {
            "file_to_obfuscate": "s3://erroneous-file",
            "pii_fields": ["name"],
        }

        with pytest.raises(GetDataError):
            obfuscator(event)

        assert "Error loading data from" in caplog.text

    def test_raises_obfuscate_fields_error(self, mocker, caplog):
        mocker.patch("src.obfuscator.get_file_type")
        mocker.patch("src.obfuscator.get_data")
        obfuscate_fields = mocker.patch("src.obfuscator.obfuscate_fields")
        obfuscate_fields.side_effect = ObfuscationError(
            "Error obfuscating fields"
        )

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.csv",
            "pii_fields": ["name"],
        }

        with pytest.raises(ObfuscationError):
            obfuscator(event)

        assert "Error obfuscating fields" in caplog.text

    def test_raises_format_data_error(self, mocker, caplog):
        mocker.patch("src.obfuscator.get_file_type")
        mocker.patch("src.obfuscator.get_data")
        mocker.patch("src.obfuscator.obfuscate_fields")
        format_data = mocker.patch("src.obfuscator.format_data")
        format_data.side_effect = FormatDataError("Error serialising data")

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.csv",
            "pii_fields": ["name"],
        }

        with pytest.raises(FormatDataError):
            obfuscator(event)

        assert "Error formatting obfuscated data" in caplog.text


@pytest.mark.performance
class TestObfuscatorPerformance:
    @pytest.fixture(scope="module", autouse=True)
    def s3_bucket(self, test_large_data):
        with mock_aws():
            bucket_name = "test-bucket"
            s3 = boto3.client("s3", region_name="us-east-1")
            s3.create_bucket(Bucket=bucket_name)

            yield s3, bucket_name

    def test_obfuscator_performance(self, s3_bucket, test_large_data):
        s3, bucket_name = s3_bucket

        s3.put_object(
            Bucket=bucket_name,
            Key="dir/large-file.xml",
            Body=test_large_data["shallow_xml_str"],
        )

        event = {
            "file_to_obfuscate": "s3://test-bucket/dir/large-file.xml",
            "pii_fields": ["name"],
        }

        num_of_executions = 50
        average_execution_time = round(
            timeit.timeit(lambda: obfuscator(event), number=num_of_executions)
            / num_of_executions,
            4,
        )

        print(
            "\nAverage execution time for obfuscator on 10,000 records: "
            f"{average_execution_time} seconds"
        )

        assert average_execution_time < 1
