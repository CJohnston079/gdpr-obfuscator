import unittest
from unittest.mock import patch

from src.obfuscator import obfuscator


class TestObfuscator(unittest.TestCase):
    @patch("src.obfuscator.serialise_dicts")
    @patch("src.obfuscator.obfuscate_fields")
    @patch("src.obfuscator.handle_csv")
    @patch("src.obfuscator.get_file_type")
    def test_obfuscator_calls_helper_functions(
            self,
            mock_get_file_type,
            mock_handle_csv,
            mock_obfuscate_fields,
            mock_serialise_dicts
    ):
        mock_get_file_type.return_value = 'csv'
        mock_handle_csv.return_value = [
            {'name': 'George', 'age': '44', 'city': 'York'},
            {'name': 'Lindsay', 'age': '40', 'city': 'Leeds'},
            {'name': 'Michael', 'age': '37', 'city': 'Sheffield'}
        ]
        mock_obfuscate_fields.return_value = [
            {'name': '***', 'age': '***', 'city': 'York'},
            {'name': '***', 'age': '***', 'city': 'Leeds'},
            {'name': '***', 'age': '***', 'city': 'Sheffield'}
        ]
        mock_serialise_dicts.return_value = '''[
            {'name': '***', 'age': '***', 'city': 'York'},
            {'name': '***', 'age': '***', 'city': 'Leeds'},
            {'name': '***', 'age': '***', 'city': 'Sheffield'}
        ]'''

        event = {
            "file_to_obfuscate": "s3://bucket/data/file.csv",
            "pii_fields": ["name", "age"]
        }

        result = obfuscator(event)

        mock_get_file_type.assert_called_once_with("s3://bucket/data/file.csv")
        mock_handle_csv.assert_called_once_with("s3://bucket/data/file.csv")
        mock_obfuscate_fields.assert_called_once_with(
            [
                {'name': 'George', 'age': '44', 'city': 'York'},
                {'name': 'Lindsay', 'age': '40', 'city': 'Leeds'},
                {'name': 'Michael', 'age': '37', 'city': 'Sheffield'}
            ],
            event["pii_fields"]
        )
        mock_serialise_dicts.assert_called_once_with([
            {'name': '***', 'age': '***', 'city': 'York'},
            {'name': '***', 'age': '***', 'city': 'Leeds'},
            {'name': '***', 'age': '***', 'city': 'Sheffield'}
        ])

        assert result == '''[
            {'name': '***', 'age': '***', 'city': 'York'},
            {'name': '***', 'age': '***', 'city': 'Leeds'},
            {'name': '***', 'age': '***', 'city': 'Sheffield'}
        ]'''


if __name__ == '__main__':
    unittest.main()
