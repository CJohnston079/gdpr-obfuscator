import unittest
from unittest.mock import patch, mock_open
from src.utils.file_handlers.handle_csv import handle_csv


class TestHandleCSV(unittest.TestCase):
    sample_data = [
        {'name': 'George', 'age': '44', 'city': 'York'},
        {'name': 'Lindsay', 'age': '40', 'city': 'Leeds'},
        {'name': 'Michael', 'age': '37', 'city': 'Sheffield'}
    ]

    sample_csv_content = (
        "name,age,city\n"
        "George,44,York\n"
        "Lindsay,40,Leeds\n"
        "Michael,37,Sheffield"
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
