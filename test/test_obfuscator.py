import json
import textwrap
import timeit

import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from moto import mock_aws

from src.exceptions import FormatDataError
from src.exceptions import GetDataError
from src.exceptions import ObfuscationError
from src.obfuscator import obfuscator


def create_event(s3_uri, pii_fields=["name"]):
    return {
        "file_to_obfuscate": f"s3://{s3_uri}",
        "pii_fields": pii_fields,
    }


@pytest.mark.smoke
class TestObfuscator:
    @pytest.fixture(scope="module", autouse=True)
    def place_test_files(self, s3_bucket, test_shallow_data, test_xml_data):
        s3, bucket_name = s3_bucket

        data = test_shallow_data["shallow_list_based"]
        xml_data = test_xml_data["shallow_xml_str"]
        json_data = json.dumps(data)

        headers = data[0].keys()
        rows = [",".join([row[key] for key in headers]) for row in data]
        csv_data = ",".join(headers) + "\n" + "\n".join(rows)

        df = pd.DataFrame(test_shallow_data["shallow_list_based"])
        table = pa.Table.from_pandas(df)
        parquet_buffer = pa.BufferOutputStream()
        pq.write_table(table, parquet_buffer)
        pq_data = parquet_buffer.getvalue().to_pybytes()

        s3.put_object(Bucket=bucket_name, Key="file.csv", Body=csv_data)
        s3.put_object(Bucket=bucket_name, Key="file.json", Body=json_data)
        s3.put_object(Bucket=bucket_name, Key="file.parquet", Body=pq_data)
        s3.put_object(Bucket=bucket_name, Key="file.xml", Body=xml_data)

    def test_returns_obfuscated_csv_data(self, test_shallow_data):
        data = test_shallow_data["shallow_list_based_obfuscated"]
        headers = data[0].keys()
        rows = [",".join([row[key] for key in headers]) for row in data]
        csv_data_obf = ",".join(headers) + "\n" + "\n".join(rows)

        event = create_event("test-bucket/file.csv")
        result = obfuscator(event)

        result = textwrap.dedent(result).strip().replace("\r\n", "\n")
        expected = textwrap.dedent(csv_data_obf).strip()

        assert result == expected

    def test_returns_obfuscated_json_data(self, test_shallow_data):
        obf_data = test_shallow_data["shallow_list_based_obfuscated"]
        json_data_obf = json.dumps(obf_data)

        event = create_event("test-bucket/file.json")
        result = obfuscator(event)

        assert result == json_data_obf

    def test_returns_obfuscated_parquet_data(self, test_shallow_data):
        df = pd.DataFrame(test_shallow_data["shallow_list_based_obfuscated"])
        table_obf = pa.Table.from_pandas(df)
        parquet_buffer_obf = pa.BufferOutputStream()
        pq.write_table(table_obf, parquet_buffer_obf)
        parquet_data_obf = parquet_buffer_obf.getvalue().to_pybytes()

        event = create_event("test-bucket/file.parquet")
        result = obfuscator(event)

        assert result == parquet_data_obf

    def test_returns_obfuscated_xml_data(self, test_xml_data):
        xml_data_obf = test_xml_data["shallow_xml_str_obfuscated"]
        event = create_event("test-bucket/file.xml")
        result = obfuscator(event)
        assert result == xml_data_obf


class TestObfuscatorCallsHelpersFunctions:
    def test_calls_helper_functions(self, mocker, test_shallow_data):
        original_data = test_shallow_data["shallow_list_based"]
        obfuscated_data = test_shallow_data["shallow_list_based_obfuscated"]

        get_file_type = mocker.patch("src.obfuscator.get_file_type")
        get_data = mocker.patch("src.obfuscator.get_data")
        obfuscate_fields = mocker.patch("src.obfuscator.obfuscate_fields")
        format_data = mocker.patch("src.obfuscator.format_data")

        get_file_type.return_value = "csv"
        get_data.return_value = original_data
        obfuscate_fields.return_value = obfuscated_data

        obfuscator(create_event("bucket/data/file.csv"))

        get_file_type.assert_called_once_with("s3://bucket/data/file.csv")
        get_data.assert_called_once_with("s3://bucket/data/file.csv", "csv")
        obfuscate_fields.assert_called_once_with(original_data, ["name"])
        format_data.assert_called_once_with(obfuscated_data, "csv")


@pytest.mark.error_handling
class TestObfuscatorErrorHandling:
    def test_raises_critical_exception_for_unknown_error(self, mocker, caplog):
        get_file_type = mocker.patch("src.obfuscator.get_file_type")
        get_file_type.side_effect = Exception

        event = create_event("bucket/data/file.txt")

        with pytest.raises(Exception):
            obfuscator(event)

        assert "An unexpected error occurred" in caplog.text
        assert any(record.levelname == "CRITICAL" for record in caplog.records)


@pytest.mark.error_handling
class TestObfuscatorHandlesPropagatedUtilExceptions:
    def test_raises_attribute_error(self, mocker, caplog):
        get_file_type = mocker.patch("src.obfuscator.get_file_type")
        get_file_type.side_effect = AttributeError

        event = create_event("bucket/data/file")

        with pytest.raises(AttributeError):
            obfuscator(event)

        assert "Error extracting file type" in caplog.text

    def test_raises_get_data_error(self, mocker, caplog):
        mocker.patch("src.obfuscator.get_file_type")
        get_data = mocker.patch("src.obfuscator.get_data")
        get_data.side_effect = GetDataError("Error loading data")

        event = create_event("erroneous-file")

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

        event = create_event("test-bucket/data/file.csv")

        with pytest.raises(ObfuscationError):
            obfuscator(event)

        assert "Error obfuscating fields" in caplog.text

    def test_raises_format_data_error(self, mocker, caplog):
        mocker.patch("src.obfuscator.get_file_type")
        mocker.patch("src.obfuscator.get_data")
        mocker.patch("src.obfuscator.obfuscate_fields")
        format_data = mocker.patch("src.obfuscator.format_data")
        format_data.side_effect = FormatDataError("Error serialising data")

        event = create_event("bucket/file.csv")

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

        event = create_event("test-bucket/dir/large-file.xml")

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
