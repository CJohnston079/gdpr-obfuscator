import io
import pickle

from src.utils.file_formatters.serialise_data import serialise_data


class TestSerialiseDicts:
    def test_serialise_data_does_not_mutate_input(self, test_shallow_data):
        original_dicts = test_shallow_data["shallow_list_based"]
        copied_dicts = original_dicts.copy()

        serialised_data = serialise_data(original_dicts)

        buffer = io.BytesIO(serialised_data)
        deserialised_dicts = pickle.load(buffer)

        assert deserialised_dicts == original_dicts
        assert copied_dicts == original_dicts

    def test_serialises_empty_list(self):
        dicts = []

        serialised_data = serialise_data(dicts)

        buffer = io.BytesIO(serialised_data)
        deserialised_data = pickle.load(buffer)

        assert deserialised_data == dicts

    def test_serialises_shallow_data(self, test_shallow_data):
        data = test_shallow_data["shallow_list_based"]

        serialised_data = serialise_data(data)

        buffer = io.BytesIO(serialised_data)
        deserialised_data = pickle.load(buffer)

        assert deserialised_data == data

    def test_serialises_deep_array_based_data(self, test_deep_data):
        data = test_deep_data["deep_list_based"]

        serialised_data = serialise_data(data)

        buffer = io.BytesIO(serialised_data)
        deserialised_data = pickle.load(buffer)

        assert deserialised_data == data

    def test_serialises_deep_object_based_data(self, test_deep_data):
        data = test_deep_data["deep_dict_based"]

        serialised_data = serialise_data(data)

        buffer = io.BytesIO(serialised_data)
        deserialised_data = pickle.load(buffer)

        assert deserialised_data == data
