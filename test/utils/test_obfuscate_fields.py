import copy

from src.utils.obfuscate_fields import obfuscate_fields


class TestObfuscateFields:
    def test_returns_list_of_dictionaries(self, test_shallow_data):
        data = test_shallow_data["shallow_list_based"]
        result = obfuscate_fields(data, ["name"])

        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_input_data_not_mutated(self, test_shallow_data):
        data = test_shallow_data["shallow_list_based"]
        original_data = copy.deepcopy(data)
        obfuscate_fields(data, ["name"])

        assert data == original_data

    def test_obfuscates_targeted_fields_in_shallow_data(
        self, test_shallow_data
    ):
        data = test_shallow_data["shallow_list_based"]
        obfuscated_data = test_shallow_data["shallow_list_based_obfuscated"]
        result = obfuscate_fields(data, ["name"])

        assert result == obfuscated_data

    def test_obfuscates_targeted_fields_in_deep_array_based_data(
        self, test_deep_data
    ):
        data = test_deep_data["deep_list_based"]
        obfuscated_data = test_deep_data["deep_list_based_obfuscated"]
        result = obfuscate_fields(data, ["name", "email", "phone"])

        assert result == obfuscated_data

    def test_obfuscates_targeted_fields_in_deep_object_based_data(
        self, test_deep_data
    ):
        data = test_deep_data["deep_dict_based"]
        obfuscated_data = test_deep_data["deep_dict_based_obfuscated"]
        result = obfuscate_fields(data, ["name", "email", "phone"])

        assert result == obfuscated_data
