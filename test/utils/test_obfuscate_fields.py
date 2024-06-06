import copy
import pytest
import unittest
from src.utils.obfuscate_fields import obfuscate_fields


class TestObfuscateFields():
    @pytest.fixture
    def sample_args(self):
        sample_data = [
            {'name': 'George', 'age': '44', 'city': 'York'},
            {'name': 'Michael', 'age': '40', 'city': 'Leeds'},
            {'name': 'Lindsay', 'age': '37', 'city': 'Sheffield'}
        ]
        sample_fields = ["name"]
        expected_return = [
            {'name': '***', 'age': '44', 'city': 'York'},
            {'name': '***', 'age': '40', 'city': 'Leeds'},
            {'name': '***', 'age': '37', 'city': 'Sheffield'}
        ]

        return sample_data, sample_fields, expected_return

    def test_returns_list_of_dictionaries(self, sample_args):
        sample_data, sample_fields, expected_return = sample_args
        result = obfuscate_fields(sample_data, sample_fields)

        assert isinstance(result, list), "Expected a list"
        assert result, "The returned list is empty"
        assert all(
            isinstance(row, dict)
            for row in result
        ), "Returned list should contain dictionaries"

    def test_input_data_not_mutated(self, sample_args):
        sample_data, sample_fields, expected_return = sample_args
        original_data = copy.deepcopy(sample_data)
        obfuscate_fields(sample_data, sample_fields)

        assert sample_data == original_data, "Input data should not be mutated"

    def test_returns_data_with_targeted_fields_obfuscated(self, sample_args):
        sample_data, sample_fields, expected_return = sample_args
        result = obfuscate_fields(sample_data, sample_fields)

        assert result == expected_return


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
