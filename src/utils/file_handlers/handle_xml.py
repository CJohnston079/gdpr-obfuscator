import xml.etree.ElementTree as ET
import boto3
import io


def handle_xml(file_path):
    bucket_name = file_path.split('/')[2]
    key = '/'.join(file_path.split('/')[3:])

    s3 = boto3.client("s3", region_name="eu-west-2")

    response = s3.get_object(Bucket=bucket_name, Key=key)
    content = response['Body'].read().decode('utf-8')

    if not content:
        return []

    root = ET.fromstring(content)
    data_tag = root[0].tag

    data = [
        {child.tag: child.text for child in element}
        for element in root.findall(f".//{data_tag}")
    ]

    return data
