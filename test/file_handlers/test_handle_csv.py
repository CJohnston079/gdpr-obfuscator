import unittest
from unittest.mock import patch, mock_open
import pytest
from src.file_handlers.handle_csv import handle_csv


class TestHandleCSV(unittest.TestCase):
    sample_data = [
        {'name': 'Alice', 'age': '30', 'city': 'York'},
        {'name': 'Bob', 'age': '25', 'city': 'Leeds'},
        {'name': 'Charlie', 'age': '21', 'city': 'Sheffield'}
    ]

    sample_csv_content = (
        "name,age,city\n"
        "Alice,30,York\n"
        "Bob,25,Leeds\n"
        "Charlie,21,Sheffield"
    )

    @patch("builtins.open", mock_open(read_data=sample_csv_content))
    def test_returns_list_of_dicts(self):
        result = handle_csv("dummy.csv")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(row, dict) for row in result))

    @patch("builtins.open", mock_open(read_data=sample_csv_content))
    def test_returns_list_of_expected_length(self):
        result = handle_csv("dummy.csv")
        self.assertEqual(len(result), 3)

    @patch("builtins.open", mock_open(read_data=sample_csv_content))
    def test_returns_expected_data(self):
        result = handle_csv("dummy.csv")
        self.assertEqual(result, self.sample_data)

    @patch("builtins.open", mock_open(read_data=""))
    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_csv("dummy.csv")
        self.assertEqual(result, [])

    def test_handles_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            handle_csv("non_existent_file.csv")


if __name__ == '__main__':
    unittest.main()
