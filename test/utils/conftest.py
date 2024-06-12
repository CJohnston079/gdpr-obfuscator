import pytest
from data_generation import generate_shallow_data, generate_deep_data


@pytest.fixture
def ts_shallow_data():
    return generate_shallow_data()


@pytest.fixture
def ts_deep_data():
    return generate_deep_data()
