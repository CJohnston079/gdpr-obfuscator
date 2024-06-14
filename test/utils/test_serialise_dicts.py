import io
import pickle
import pytest
from src.utils.serialise_dicts import serialise_dicts


class TestSerialiseDicts:
    def test_serialise_dicts_does_not_mutate_input(self, generate_shallow_data):
        original_dicts = generate_shallow_data["shallow_list_based"]
        copied_dicts = original_dicts.copy()

        serialised_data = serialise_dicts(original_dicts)

        buffer = io.BytesIO(serialised_data)
        deserialised_dicts = pickle.load(buffer)

        assert deserialised_dicts == original_dicts
        assert copied_dicts == original_dicts

    def test_serialises_empty_list(self):
        dicts = []

        serialised_data = serialise_dicts(dicts)

        buffer = io.BytesIO(serialised_data)
        deserialised_data = pickle.load(buffer)

        assert deserialised_data == dicts

    def test_serialises_shallow_data(self, generate_shallow_data):
        data = generate_shallow_data["shallow_list_based"]

        serialised_data = serialise_dicts(data)

        buffer = io.BytesIO(serialised_data)
        deserialised_data = pickle.load(buffer)

        assert deserialised_data == data

    def test_serialises_deep_array_based_data(self, generate_deep_data):
        data = generate_deep_data["deep_list_based"]

        serialised_data = serialise_dicts(data)

        buffer = io.BytesIO(serialised_data)
        deserialised_data = pickle.load(buffer)

        assert deserialised_data == data

    def test_serialises_deep_object_based_data(
        self,
        generate_deep_data
    ):
        data = generate_deep_data["deep_object_based"]

        serialised_data = serialise_dicts(data)

        buffer = io.BytesIO(serialised_data)
        deserialised_data = pickle.load(buffer)

        assert deserialised_data == data


if __name__ == "__main__":  # pragma: no cover
    pytest.main()
