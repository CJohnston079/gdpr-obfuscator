import boto3
import io
import pyarrow.parquet as pq


def handle_parquet(file_path):
    bucket_name = file_path.split('/')[2]
    key = '/'.join(file_path.split('/')[3:])

    s3 = boto3.client("s3", region_name="eu-west-2")

    response = s3.get_object(Bucket=bucket_name, Key=key)
    content = response['Body'].read()
    file_content = io.BytesIO(content)

    table = pq.read_table(file_content)
    data = table.to_pandas().to_dict(orient='records')

    return data
