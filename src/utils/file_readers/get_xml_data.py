import xml.etree.ElementTree as ET

import boto3


def get_xml_data(bucket, key):
    """
    Reads the contents of a XML file from an AWS S3 bucket and returns a
    list of dictionaries of the same structure as the XML file.

    Args:
        bucket (str): The name of S3 bucket in which the XML file is located.
        key (str): The file path of the XML file within its bucket.

    Returns:
        list:
            A list of dictionaries representing the data in the XML file. Each
            dictionary represents a tag in the XML file containing any child
            elements of that tag in the same format. The root element of the
            XML file is preserved as the parent dictionary.
    """
    s3 = boto3.client("s3", region_name="eu-west-2")

    response = s3.get_object(Bucket=bucket, Key=key)
    content = response["Body"].read().decode("utf-8")

    if not content:
        return []

    root = ET.fromstring(content)

    def parse_element(element):
        if len(element) == 0:
            return element.text
        return {child.tag: parse_element(child) for child in element}

    data = [{root.tag: {child.tag: parse_element(child)}} for child in root]

    return data
