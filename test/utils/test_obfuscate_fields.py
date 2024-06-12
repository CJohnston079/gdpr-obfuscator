import copy
import pytest
import unittest
from src.utils.obfuscate_fields import obfuscate_fields


class TestObfuscateFields():
    @pytest.fixture
    def sample_args(self):
        shallow_data = [
            {"name": "George", "age": "44", "city": "York"},
            {"name": "Michael", "age": "40", "city": "Leeds"},
            {"name": "Lindsay", "age": "37", "city": "Sheffield"}
        ]
        deep_data = [
            {
                "name": "George",
                "age": "44",
                "city": "York",
                "contact": [
                    {"email": "george@bluthcompany.com"},
                    {"phone": "01904 123456"}
                ],
            },
            {
                "name": "Lindsay",
                "age": "40",
                "city": "Leeds",
                "contact": [
                    {"email": "lindsay@bluthcompany.com"},
                    {"phone": "0113 123456"}
                ],
            },
            {
                "name": "Michael",
                "age": "37",
                "city": "Sheffield",
                "contact": [
                    {"email": "michael@bluthcompany.com"},
                    {"phone": "0114 123456"}
                ],
            }
        ]
        obfc_shallow_data = [
            {"name": "***", "age": "44", "city": "York"},
            {"name": "***", "age": "40", "city": "Leeds"},
            {"name": "***", "age": "37", "city": "Sheffield"}
        ]
        obfc_deep_data = [
            {
                "name": "***",
                "age": "44",
                "city": "York",
                "contact": [
                    {"email": "***"},
                    {"phone": "***"}
                ],
            },
            {
                "name": "***",
                "age": "40",
                "city": "Leeds",
                "contact": [
                    {"email": "***"},
                    {"phone": "***"}
                ],
            },
            {
                "name": "***",
                "age": "37",
                "city": "Sheffield",
                "contact": [
                    {"email": "***"},
                    {"phone": "***"}
                ],
            }
        ]

        return shallow_data, deep_data, obfc_shallow_data, obfc_deep_data

    def test_returns_list_of_dictionaries(self, sample_args):
        shallow_data, deep_data, obfc_shallow_data, obfc_deep_data = sample_args
        result = obfuscate_fields(shallow_data, ["name"])

        assert isinstance(result, list), "Expected a list"
        assert result, "The returned list is empty"
        assert all(
            isinstance(row, dict)
            for row in result
        ), "Returned list should contain dictionaries"

    def test_input_data_not_mutated(self, sample_args):
        shallow_data, deep_data, obfc_shallow_data, obfc_deep_data = sample_args
        original_data = copy.deepcopy(shallow_data)
        obfuscate_fields(shallow_data, ["name"])

        assert shallow_data == original_data, "Input data should not be mutated"

    def test_obfuscates_targeted_fields_in_shallow_data(self, sample_args):
        shallow_data, deep_data, obfc_shallow_data, obfc_deep_data = sample_args
        result = obfuscate_fields(shallow_data, ["name"])

        assert result == obfc_shallow_data

    def test_obfuscates_targeted_fields_in_deep_data(self, sample_args):
        shallow_data, deep_data, obfc_shallow_data, obfc_deep_data = sample_args
        result = obfuscate_fields(deep_data, ["name", "email", "phone"])

        assert result == obfc_deep_data


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
