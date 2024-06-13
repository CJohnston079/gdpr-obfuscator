import pytest
from data_generation import (
    generate_shallow_data_sets,
    generate_shallow_data_old,
    generate_deep_array_based_data,
    generate_deep_object_based_data
)


@pytest.fixture(scope="session")
def generate_shallow_data():
    return generate_shallow_data_sets()


@pytest.fixture(scope="class")
def test_shallow_data(generate_shallow_data):
    return generate_shallow_data["data"]


@pytest.fixture(scope="class")
def ts_shallow_data():
    return generate_shallow_data_old()


@pytest.fixture(scope="class")
def ts_deep_array_based_data():
    return generate_deep_array_based_data()


@pytest.fixture(scope="class")
def ts_deep_object_based_data():
    return generate_deep_object_based_data()
