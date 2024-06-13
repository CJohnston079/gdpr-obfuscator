import pytest
from data_generation import (
    generate_data,
    generate_shallow_data_old,
    generate_deep_array_based_data,
    generate_deep_object_based_data
)


@pytest.fixture(scope="session")
def generate_shallow_data():
    return generate_data(
        "shallow_list_based",
        "shallow_list_based_obfuscated",
        "shallow_object_based",
        "shallow_object_based_obfuscated",
    )


@pytest.fixture(scope="session")
def test_xml_data():
    data = generate_data(
        "shallow_object_based",
        "shallow_xml_str",
        "deep_object_based",
        "deep_xml_str"
    )
    data["shallow_xml_str"] = f'<root>{data["shallow_xml_str"]}</root>'
    data["deep_xml_str"] = f'<root>{data["deep_xml_str"]}</root>'

    return data


@pytest.fixture(scope="class")
def test_shallow_data(generate_shallow_data):
    return generate_shallow_data["shallow_list_based"]


@pytest.fixture(scope="class")
def test_shallow_object_based_data(generate_shallow_data):
    return generate_shallow_data["shallow_object_based_obfuscated"]


@pytest.fixture(scope="class")
def ts_shallow_data():
    return generate_shallow_data_old()


@pytest.fixture(scope="class")
def ts_deep_array_based_data():
    return generate_deep_array_based_data()


@pytest.fixture(scope="class")
def ts_deep_object_based_data():
    return generate_deep_object_based_data()
