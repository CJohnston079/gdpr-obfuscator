import json

import boto3


def handle_json(bucket, key):
    """
    Reads the contents of a JSON file from an AWS S3 bucket and returns a list
    of dictionaries.

    Args:
        file_path (str): The S3 bucket path to the JSON file to be read. The
            path should be in the format "s3://bucket_name/path/to/file.json".

    Returns:
        list:
            A list of dictionaries representing the data in the JSON file.
    """
    s3 = boto3.client("s3", region_name="eu-west-2")

    response = s3.get_object(Bucket=bucket, Key=key)
    content = response["Body"].read().decode("utf-8")

    data = json.loads(content) if content else []

    return data
