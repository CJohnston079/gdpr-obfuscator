import io

import boto3
import pyarrow.parquet as pq


def get_paruqet_data(bucket, key):
    """
    Reads the contents of a Parquet file from an AWS S3 bucket and returns a
    list of dictionaries.

    Args:
        bucket (str): The name of S3 bucket where the Parquet file is located.
        key (str): The file path of the Parquet file within its bucket.

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
