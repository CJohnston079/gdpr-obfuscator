import json
import textwrap
import xml.etree.ElementTree as ET

import pandas as pd
import pyarrow.parquet as pq
import pytest

from src.utils.file_formatters.format_csv_data import format_csv_data
from src.utils.file_formatters.format_json_data import format_json_data
from src.utils.file_formatters.format_parquet_data import format_parquet_data
from src.utils.file_formatters.format_xml_data import format_xml_data


class TestFileFormatters:
    @pytest.mark.parametrize(
        "format_func, expected_output",
        [
            (format_csv_data, ""),
            (format_json_data, "[]"),
            (format_parquet_data, b""),
            (format_xml_data, "<data></data>"),
        ],
    )
    def test_empty_data(self, format_func, expected_output):
        assert format_func([]) == expected_output

    def test_format_csv_data(self, test_shallow_data):
        data = test_shallow_data["shallow_list_based"]
        result = format_csv_data(data)

        headers = data[0].keys()
        rows = [",".join([row[key] for key in headers]) for row in data]
        expected_csv = ",".join(headers) + "\n" + "\n".join(rows)

        expected_csv = textwrap.dedent(expected_csv).strip()
        result = textwrap.dedent(result).strip().replace("\r\n", "\n")

        assert result == expected_csv

    @pytest.mark.parametrize(
        "data_key", ["deep_list_based", "shallow_list_based"]
    )
    def test_format_json_data(
        self, test_deep_data, test_shallow_data, data_key
    ):
        if "deep" in data_key:
            data = test_deep_data[data_key]
        else:
            data = test_shallow_data[data_key]

        result = format_json_data(data)
        expected_json = json.dumps(data)

        assert result == expected_json

    def test_format_parquet_data(self, test_shallow_data, tmp_path):
        data = test_shallow_data["shallow_list_based"]
        parquet_file = tmp_path / "test.parquet"

        serialized_parquet = format_parquet_data(data)
        with open(parquet_file, "wb") as f:
            f.write(serialized_parquet)

        table_read = pq.read_table(parquet_file)
        df_read = table_read.to_pandas()

        expected_df = pd.DataFrame(data)
        pd.testing.assert_frame_equal(df_read, expected_df)

    @pytest.mark.parametrize(
        "data_key", ["deep_dict_based", "shallow_dict_based"]
    )
    def test_format_xml_data(
        self, test_deep_data, test_shallow_data, data_key
    ):
        if "deep" in data_key:
            data = test_deep_data[data_key]
        else:
            data = test_shallow_data[data_key]

        result = format_xml_data(data)

        root = ET.fromstring(result)
        entries = root.findall("entry")

        assert len(entries) == len(data)

        for entry, item in zip(entries, data):
            for key, value in item.items():
                assert entry.find(key).text == str(value)
