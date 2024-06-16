import io

import boto3
import pyarrow.parquet as pq


def handle_parquet(bucket, key):
    """
    Reads the contents of a Parquet file from an AWS S3 bucket and returns a
    list of dictionaries.

    Args:
        file_path (str): The S3 bucket path to the Parquet file to be read.
        file_path should be in the format "s3://bucket_name/path/to/file.pq"
        or "s3://bucket_name/path/to/file.parquet".

    Returns:
        list:
            A list of dictionaries representing the rows in the Parquet file.
            Each dictionary contains key-value pairs where the keys are
            column headers and the values are the corresponding values from
            each row in the Parquet file.
    """
    s3 = boto3.client("s3", region_name="eu-west-2")

    response = s3.get_object(Bucket=bucket, Key=key)
    content = response["Body"].read()
    file_content = io.BytesIO(content)

    table = pq.read_table(file_content)
    data = table.to_pandas().to_dict(orient="records")

    return data
