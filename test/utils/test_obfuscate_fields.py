import copy
import unittest
from src.utils.obfuscate_fields import obfuscate_fields


class TestObfuscateFields():
    def test_returns_list_of_dictionaries(self, ts_shallow_data):
        shallow_data, obfc_shallow_data = ts_shallow_data
        result = obfuscate_fields(shallow_data, ["name"])

        assert isinstance(result, list), "Expected a list"
        assert result, "The returned list is empty"
        assert all(
            isinstance(row, dict)
            for row in result
        ), "Returned list should contain dictionaries"

    def test_input_data_not_mutated(self, ts_shallow_data):
        shallow_data, obfc_shallow_data = ts_shallow_data
        original_data = copy.deepcopy(shallow_data)
        obfuscate_fields(shallow_data, ["name"])

        assert shallow_data == original_data, (
            "Input data should not be mutated"
        )

    def test_obfuscates_targeted_fields_in_shallow_data(self, ts_shallow_data):
        shallow_data, obfc_shallow_data = ts_shallow_data
        result = obfuscate_fields(shallow_data, ["name"])

        assert result == obfc_shallow_data

    def test_obfuscates_targeted_fields_in_deep_array_based_data(
        self, ts_deep_array_based_data
    ):
        deep_data, obfc_deep_data = ts_deep_array_based_data
        result = obfuscate_fields(deep_data, ["name", "email", "phone"])

        assert result == obfc_deep_data

    def test_obfuscates_targeted_fields_in_deep_object_based_data(
        self, ts_deep_object_based_data
    ):
        deep_data, obfc_deep_data = ts_deep_object_based_data
        result = obfuscate_fields(deep_data, ["name", "email", "phone"])

        assert result == obfc_deep_data


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
