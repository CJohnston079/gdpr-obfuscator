import csv
import boto3
import io


def handle_csv(file_path):
    """
    Reads the contents of a CSV file from an AWS S3 bucket and returns a list
    of dictionaries.

    Args:
        file_path (str): The S3 bucket path to the CSV file to be read. The path
            should be in the format 's3://bucket_name/path/to/file.csv'.

    Returns:
        list:
            A list of dictionaries representing the rows in the CSV file.
            Each dictionary contains key-value pairs where the keys are
            column headers and the values are the corresponding values
            from each row in the CSV file.
    """

    bucket_name = file_path.split('/')[2]
    key = '/'.join(file_path.split('/')[3:])

    s3 = boto3.client("s3", region_name="eu-west-2")

    response = s3.get_object(Bucket=bucket_name, Key=key)
    content = response['Body'].read().decode('utf-8')
    file_content = io.StringIO(content)

    return [dict(row) for row in csv.DictReader(file_content)]
