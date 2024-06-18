import boto3
import pytest
from generate_test_data import generate_data
from moto import mock_aws


@pytest.fixture(scope="module", autouse=True)
def s3_bucket():
    with mock_aws():
        bucket_name = "test-bucket"
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=bucket_name)

        yield s3, bucket_name


@pytest.fixture(scope="session")
def test_shallow_data():
    return generate_data(
        "shallow_list_based",
        "shallow_list_based_obfuscated",
        "shallow_dict_based",
        "shallow_dict_based_obfuscated",
    )


@pytest.fixture(scope="session")
def test_deep_data():
    return generate_data(
        "deep_list_based",
        "deep_list_based_obfuscated",
        "deep_dict_based",
        "deep_dict_based_obfuscated",
    )


@pytest.fixture(scope="session")
def test_xml_data():
    return generate_data(
        "shallow_dict_based",
        "shallow_xml_str",
        "deep_dict_based",
        "deep_xml_str",
    )


@pytest.fixture(scope="session")
def test_large_data():
    return generate_data(
        "shallow_list_based",
        "shallow_dict_based",
        "shallow_xml_str",
        num_records=10000,
    )
