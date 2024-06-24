import json
import textwrap

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from src.exceptions import FormatDataError
from src.exceptions import GetDataError
from src.exceptions import ObfuscationError
from src.obfuscator import Obfuscator
from src.utils.obfuscation_methods.tokenise import tokenise


def create_event(s3_uri, pii_fields=["name"]):
    return {
        "file_to_obfuscate": f"s3://{s3_uri}",
        "pii_fields": pii_fields,
    }


@pytest.fixture(scope="module", autouse=True)
def obfuscator():
    return Obfuscator()


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

    def test_returns_obfuscated_csv_data(self, obfuscator, test_shallow_data):
        data = test_shallow_data["shallow_list_based_obfuscated"]
        headers = data[0].keys()
        rows = [",".join([row[key] for key in headers]) for row in data]
        csv_data_obf = ",".join(headers) + "\n" + "\n".join(rows)

        event = create_event("test-bucket/file.csv")
        result = obfuscator.obfuscate(event)

        result = textwrap.dedent(result).strip().replace("\r\n", "\n")
        expected = textwrap.dedent(csv_data_obf).strip()

        assert result == expected

    def test_returns_obfuscated_json_data(self, obfuscator, test_shallow_data):
        obf_data = test_shallow_data["shallow_list_based_obfuscated"]
        json_data_obf = json.dumps(obf_data, indent=2)

        event = create_event("test-bucket/file.json")
        result = obfuscator.obfuscate(event)

        assert result == json_data_obf

    def test_returns_obfuscated_pq_data(self, obfuscator, test_shallow_data):
        df = pd.DataFrame(test_shallow_data["shallow_list_based_obfuscated"])
        table_obf = pa.Table.from_pandas(df)
        parquet_buffer_obf = pa.BufferOutputStream()
        pq.write_table(table_obf, parquet_buffer_obf)
        parquet_data_obf = parquet_buffer_obf.getvalue().to_pybytes()

        event = create_event("test-bucket/file.parquet")
        result = obfuscator.obfuscate(event)

        assert result == parquet_data_obf

    def test_returns_obfuscated_xml_data(self, obfuscator, test_xml_data):
        xml_data_obf = test_xml_data["shallow_xml_str_obfuscated"]
        event = create_event("test-bucket/file.xml")
        result = obfuscator.obfuscate(event)
        assert result == xml_data_obf


class TestObfuscatorCallsUtilFunctions:
    def test_calls_util_functions(self, obfuscator, mocker, test_shallow_data):
        data = test_shallow_data["shallow_list_based"]
        obfuscated_data = test_shallow_data["shallow_list_based_obfuscated"]
        obfuscation_options = {
            "pii_fields": ["name"],
            "obfuscation_method": tokenise,
            "options": {},
        }

        get_file_type = mocker.patch("src.obfuscator.get_file_type")
        get_data = mocker.patch("src.obfuscator.get_data")
        obfuscate_fields = mocker.patch("src.obfuscator.obfuscate_fields")
        format_data = mocker.patch("src.obfuscator.format_data")

        get_file_type.return_value = "csv"
        get_data.return_value = data
        obfuscate_fields.return_value = obfuscated_data

        obfuscator.obfuscate(create_event("bucket/data/file.csv"))

        get_file_type.assert_called_once_with("s3://bucket/data/file.csv")
        get_data.assert_called_once_with("s3://bucket/data/file.csv", "csv")
        obfuscate_fields.assert_called_once_with(data, obfuscation_options)
        format_data.assert_called_once_with(obfuscated_data, "csv")


@pytest.mark.error_handling
class TestObfuscatorErrorHandling:
    def test_raises_critical_exception_for_unknown_error(
        self, obfuscator, mocker, caplog
    ):
        get_file_type = mocker.patch("src.obfuscator.get_file_type")
        get_file_type.side_effect = Exception

        event = create_event("bucket/data/file.txt")

        with pytest.raises(Exception):
            obfuscator.obfuscate(event)

        assert "An unexpected error occurred" in caplog.text
        assert any(record.levelname == "CRITICAL" for record in caplog.records)


@pytest.mark.error_handling
class TestObfuscatorHandlesPropagatedUtilExceptions:
    def test_raises_attribute_error(self, obfuscator, mocker, caplog):
        get_file_type = mocker.patch("src.obfuscator.get_file_type")
        get_file_type.side_effect = AttributeError

        event = create_event("bucket/data/file")

        with pytest.raises(AttributeError):
            obfuscator.obfuscate(event)

        assert "Error extracting file type" in caplog.text

    def test_raises_get_data_error(self, obfuscator, mocker, caplog):
        mocker.patch("src.obfuscator.get_file_type")
        get_data = mocker.patch("src.obfuscator.get_data")
        get_data.side_effect = GetDataError("Error loading data")

        event = create_event("erroneous-file")

        with pytest.raises(GetDataError):
            obfuscator.obfuscate(event)

        assert "Error loading data from" in caplog.text

    def test_raises_obfuscate_fields_error(self, obfuscator, mocker, caplog):
        mocker.patch("src.obfuscator.get_file_type")
        mocker.patch("src.obfuscator.get_data")
        obfuscate_fields = mocker.patch("src.obfuscator.obfuscate_fields")
        obfuscate_fields.side_effect = ObfuscationError(
            "Error obfuscating fields"
        )

        event = create_event("test-bucket/data/file.csv")

        with pytest.raises(ObfuscationError):
            obfuscator.obfuscate(event)

        assert "Error obfuscating fields" in caplog.text

    def test_raises_format_data_error(self, obfuscator, mocker, caplog):
        mocker.patch("src.obfuscator.get_file_type")
        mocker.patch("src.obfuscator.get_data")
        mocker.patch("src.obfuscator.obfuscate_fields")
        format_data = mocker.patch("src.obfuscator.format_data")
        format_data.side_effect = FormatDataError("Error serialising data")

        event = create_event("bucket/file.csv")

        with pytest.raises(FormatDataError):
            obfuscator.obfuscate(event)

        assert "Error formatting obfuscated data" in caplog.text


@pytest.mark.performance
class TestObfuscatorPerformance:
    @pytest.fixture(scope="module", autouse=True)
    def s3_bucket(self, s3_bucket, test_large_data):
        s3, bucket_name = s3_bucket
        data = test_large_data["shallow_xml_str"]
        s3.put_object(Bucket=bucket_name, Key="large-file.xml", Body=data)

    def test_obfuscator_performance(self, obfuscator, benchmark):
        event = create_event("test-bucket/large-file.xml")
        benchmark(obfuscator.obfuscate, event)
