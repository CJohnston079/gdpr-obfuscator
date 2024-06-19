import json
import textwrap

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
            (format_xml_data, ""),
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

    @pytest.mark.parametrize("depth", ["shallow", "deep"])
    def test_format_json_data(self, test_deep_data, test_shallow_data, depth):
        if depth == "shallow":
            data = test_shallow_data[f"{depth}_list_based"]
        else:
            data = test_deep_data[f"{depth}_list_based"]

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

    @pytest.mark.parametrize("depth", ["shallow", "deep"])
    def test_format_xml_data(self, test_xml_data, depth):
        data = test_xml_data[f"{depth}_xml_data"]
        expexted_xml = test_xml_data[f"{depth}_xml_str"]
        result = format_xml_data(data)

        assert result == expexted_xml
