import pytest
from data_generation import generate_data


@pytest.fixture(scope="session")
def test_shallow_data():
    return generate_data(
        "shallow_list_based",
        "shallow_list_based_obfuscated",
        "shallow_object_based",
        "shallow_object_based_obfuscated",
    )


@pytest.fixture(scope="session")
def test_deep_data():
    return generate_data(
        "deep_list_based",
        "deep_list_based_obfuscated",
        "deep_object_based",
        "deep_object_based_obfuscated",
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
