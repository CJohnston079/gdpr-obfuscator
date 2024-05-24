from unittest.mock import patch, mock_open
import pytest
from src.file_handlers.handle_csv import handle_csv

sample_data = [
    {'name': 'Alice', 'age': '30', 'city': 'York'},
    {'name': 'Bob', 'age': '25', 'city': 'Leeds'},
    {'name': 'Charlie', 'age': '21', 'city': 'Sheffield'}
]

sample_csv_content = """name,age,city
Alice,30,York
Bob,25,Leeds
Charlie,21,Sheffield
"""


def test_returns_list_of_dicts():
    with patch("builtins.open", mock_open(read_data=sample_csv_content)):
        data = handle_csv("dummy.csv")
        assert isinstance(data, list)
        assert all(isinstance(row, dict) for row in data)


def test_returns_list_of_expected_length():
    with patch("builtins.open", mock_open(read_data=sample_csv_content)):
        data = handle_csv("dummy.csv")
        assert len(data) == 3


def test_returns_expected_data():
    with patch("builtins.open", mock_open(read_data=sample_csv_content)):
        data = handle_csv("dummy.csv")
        assert data == sample_data


def test_handles_empty_file():
    with patch("builtins.open", mock_open(read_data="")):
        data = handle_csv("empty_file.csv")
        assert data == []


def test_handles_missing_file():
    with pytest.raises(FileNotFoundError):
        handle_csv("non_existent_file.csv")
