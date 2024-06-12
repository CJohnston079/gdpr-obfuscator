import boto3
import pytest
from moto import mock_aws


@pytest.fixture(scope="class", autouse=True)
def s3_bucket():
    with mock_aws():
        bucket_name = "test-bucket"
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=bucket_name)

        yield s3, bucket_name
