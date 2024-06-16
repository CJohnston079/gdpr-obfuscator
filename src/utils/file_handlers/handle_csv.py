import csv
import io

import boto3


def handle_csv(bucket, key):
    """
    Reads the contents of a CSV file from an AWS S3 bucket and returns a list
    of dictionaries.

    Args:
        bucket (str): The name of S3 bucket in which the CSV file is located.
        key (str): The file path of the CSV file within its bucket.

    Returns:
        list:
            A list of dictionaries representing the rows in the CSV file.
            Each dictionary contains key-value pairs where the keys are
            column headers and the values are the corresponding values
            from each row in the CSV file.
    """
    s3 = boto3.client("s3", region_name="eu-west-2")

    response = s3.get_object(Bucket=bucket, Key=key)
    content = response["Body"].read().decode("utf-8")
    file_content = io.StringIO(content)

    return [dict(row) for row in csv.DictReader(file_content)]
