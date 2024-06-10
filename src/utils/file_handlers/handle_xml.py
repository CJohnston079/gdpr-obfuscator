import xml.etree.ElementTree as ET
import boto3
import io


def handle_xml(file_path):
    """
    Reads the contents of a XML file from an AWS S3 bucket and returns a
    list of dictionaries. XML data must be in the format
    <root>
        <parent_tag>data</parent_tag>
        <parent_tag>data</parent_tag>
        <parent_tag>data</parent_tag>
    </root>

    Args:
        file_path (str): The S3 bucket path to the XML file to be read. The
            path should be in the format "s3://bucket_name/path/to/file.xml".

    Returns:
        list:
            A list of dictionaries representing the data in the XML file. Each
            dictionary contains key-value pairs where the keys are direct
            children of the root element and the values are the children of each
            key.
    """

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
