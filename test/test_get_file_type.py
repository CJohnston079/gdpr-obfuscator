from src.get_file_type import get_file_type


class TestGetFileType():
    def test_returns_a_string(self):
        result = get_file_type("s3://bucket/data/file.csv")
        assert isinstance(result, str)

    def test_returns_csv_for_csv_files(self):
        result = get_file_type("s3://bucket/data/file.csv")
        assert result == 'csv'

    def test_returns_json_for_json_files(self):
        result = get_file_type("s3://bucket/data/file.json")
        assert result == 'json'

    def test_returns_parquet_for_parquet_files(self):
        short_file = get_file_type("s3://bucket/data/file.pqt")
        long_file = get_file_type("s3://bucket/data/file.parquet")
        assert short_file == 'parquet'
        assert long_file == 'parquet'

    def test_returns_none_for_unsupported_files(self):
        result = get_file_type("s3://bucket/data/file.txt")
        assert result is None

    def test_handles_files_without_extension(self):
        result = get_file_type("s3://bucket/data/file")
        assert result is None

    def test_handles_files_with_multiple_dots(self):
        result = get_file_type("s3://bucket/data/file.name.csv")
        assert result == 'csv'

    def test_handles_urls_with_query_parameters(self):
        result = get_file_type("s3://bucket/data/file.csv?versionId=12345")
        assert result == 'csv'

    def test_handles_urls_with_fragments(self):
        result = get_file_type("s3://bucket/data/file.csv#section")
        assert result == 'csv'
