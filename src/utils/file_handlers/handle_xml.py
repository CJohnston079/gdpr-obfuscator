import xml.etree.ElementTree as ET
import boto3
import io


def handle_xml(file_path):
    """
    Reads the contents of a XML file from an AWS S3 bucket and returns a
    list of dictionaries of the same structure as the XML file.

    Args:
        file_path (str): The S3 bucket path to the XML file to be read. The
            path should be in the format "s3://bucket_name/path/to/file.xml".

    Returns:
        list:
            A list of dictionaries representing the data in the XML file. Each
            dictionary represents a tag in the XML file containing any child
            elements of that tag in the same format.
    """

    bucket_name = file_path.split("/")[2]
    key = "/".join(file_path.split("/")[3:])

    s3 = boto3.client("s3", region_name="eu-west-2")

    response = s3.get_object(Bucket=bucket_name, Key=key)
    content = response["Body"].read().decode("utf-8")

    if not content:
        return []

    root = ET.fromstring(content)

    def parse_element(element):
        if len(element) == 0:
            return {element.tag: element.text}
        else:
            children = {}
            for child in element:
                children.update(parse_element(child))
            return {element.tag: children}

    data = [parse_element(child) for child in root]

    return data
