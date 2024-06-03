import io
import pickle
import pytest
from src.utils.serialise_dicts import serialise_dicts


class TestSerialiseDicts:
    def test_serialise_dicts_does_not_mutate_input(self):
        original_dicts = [{"a": 1, "b": 2}, {"c": 3, "d": 4}]
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

    def test_serialises_single_dict(self):
        dicts = [{"a": 1, "b": 2}]

        serialised_data = serialise_dicts(dicts)

        buffer = io.BytesIO(serialised_data)
        deserialised_data = pickle.load(buffer)

        assert deserialised_data == dicts

    def test_serialises_multiple_dicts(self):
        dicts = [{"a": 1, "b": 2}, {"c": 3, "d": 4}]

        serialised_data = serialise_dicts(dicts)

        buffer = io.BytesIO(serialised_data)
        deserialised_data = pickle.load(buffer)

        assert deserialised_data == dicts

    def test_serialise_nested_dicts(self):
        dicts = [{"a": {"b": 1, "c": 2}}, {"d": {"e": 3, "f": 4}}]

        serialised_data = serialise_dicts(dicts)

        buffer = io.BytesIO(serialised_data)
        deserialised_data = pickle.load(buffer)

        assert deserialised_data == dicts


if __name__ == '__main__':
    pytest.main()
