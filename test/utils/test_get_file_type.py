import pytest

from src.utils.get_file_type import get_file_type


class TestGetFileType:
    def test_returns_a_string(self):
        result = get_file_type("s3://bucket/data/file.csv")
        assert isinstance(result, str)

    def test_returns_csv_for_csv_files(self):
        result = get_file_type("s3://bucket/data/file.csv")
        assert result == "csv"

    def test_returns_json_for_json_files(self):
        result = get_file_type("s3://bucket/data/file.json")
        assert result == "json"

    def test_returns_pq_and_parquet_for_pq_and_parquet_files(self):
        short_extension = get_file_type("s3://bucket/data/file.pq")
        long_extension = get_file_type("s3://bucket/data/file.parquet")
        assert short_extension == "pq"
        assert long_extension == "parquet"

    def test_handles_files_with_multiple_dots(self):
        result = get_file_type("s3://bucket/data/file.name.csv")
        assert result == "csv"

    def test_handles_urls_with_query_parameters(self):
        result = get_file_type("s3://bucket/data/file.csv?versionId=12345")
        assert result == "csv"

    def test_handles_urls_with_fragments(self):
        result = get_file_type("s3://bucket/data/file.csv#section")
        assert result == "csv"


@pytest.mark.error_handling
class TestGetFileTypeErrorHandling:
    def test_handles_files_without_extension(self):
        with pytest.raises(ValueError) as e:
            get_file_type("s3://bucket/data/file")

        assert str(e.value) == (
            "Unable to get file extension from s3://bucket/data/file"
        )
