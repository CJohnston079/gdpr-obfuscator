import copy
import sys

import pytest

from exceptions import ObfuscationError
from src.utils.obfuscate_fields import obfuscate_fields
from src.utils.obfuscation_methods.anonymise import anonymise
from src.utils.obfuscation_methods.tokenise import tokenise


def create_options(pii_fields=["name"], obf_method=tokenise):
    return {
        "pii_fields": pii_fields,
        "obfuscation_method": obf_method,
        "options": {},
        "anonymous_pii_fields": {"name": "Aaron Baker"},
    }


class TestObfuscateFields:
    def test_returns_list_of_dictionaries(self, test_shallow_data):
        data = test_shallow_data["shallow_list_based"]
        result = obfuscate_fields(data, create_options())

        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_input_data_not_mutated(self, test_shallow_data):
        data = test_shallow_data["shallow_list_based"]
        original_data = copy.deepcopy(data)
        obfuscate_fields(data, create_options())

        assert data == original_data

    @pytest.mark.smoke
    def test_obfuscates_targeted_fields_in_shallow_data(
        self, test_shallow_data
    ):
        data = test_shallow_data["shallow_list_based"]
        obfuscated_data = test_shallow_data["shallow_list_based_obfuscated"]
        result = obfuscate_fields(data, create_options())

        assert result == obfuscated_data

    @pytest.mark.smoke
    def test_obfuscates_targeted_fields_in_deep_list_based_data(
        self, test_deep_data
    ):
        data = test_deep_data["deep_list_based"]
        obfuscated_data = test_deep_data["deep_list_based_obfuscated"]
        options = create_options(["name", "email", "phone"])
        result = obfuscate_fields(data, options)

        assert result == obfuscated_data

    @pytest.mark.smoke
    def test_obfuscates_targeted_fields_in_deep_dict_based_data(
        self, test_deep_data
    ):
        data = test_deep_data["deep_dict_based"]
        obfuscated_data = test_deep_data["deep_dict_based_obfuscated"]
        options = create_options(["name", "email", "phone"])
        result = obfuscate_fields(data, options)

        assert result == obfuscated_data


class TestObfuscateFieldsAnonymisesData:
    def test_calls_anonymise_if_obf_method_is_anonymise(
        self, mocker, test_shallow_data
    ):
        data = test_shallow_data["shallow_list_based"]
        anonymise = mocker.patch("src.utils.obfuscate_fields.anonymise")
        obfuscate_fields(data, create_options(obf_method=anonymise))
        anonymise.assert_called

    def test_obfuscate_fields_calls_generate_pii_if_obf_method_is_anonymise(
        self, mocker, test_shallow_data
    ):
        data = test_shallow_data["shallow_list_based"]
        generate_pii = mocker.patch("src.utils.obfuscate_fields.generate_pii")
        obfuscate_fields(data, create_options(obf_method=anonymise))
        generate_pii.assert_called


@pytest.mark.error_handling
class TestObfuscateFieldsErrorHandling:
    def test_raises_attribute_error(self):
        with pytest.raises(AttributeError):
            obfuscate_fields("invalid input", create_options())

    def test_raises_recursion_error(self):
        recursion_limit = sys.getrecursionlimit()
        nested_data = []

        for _ in range(recursion_limit):
            nested_data = [{"nested": nested_data}]

        with pytest.raises(RecursionError):
            obfuscate_fields(nested_data, create_options(["nested"]))

    def test_raises_obfuscation_error_for_other_exceptions(self, mocker):
        with pytest.raises(ObfuscationError):
            obfuscate_fields(Exception, create_options())


@pytest.mark.performance
class TestObfuscateFieldsPerformance:
    def test_obfuscate_fields_performance(self, benchmark, test_large_data):
        data = test_large_data["shallow_dict_based"]
        benchmark(obfuscate_fields, data, create_options())
