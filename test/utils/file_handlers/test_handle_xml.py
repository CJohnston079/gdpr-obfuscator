import boto3
import unittest

from moto import mock_aws
from src.utils.file_handlers.handle_xml import handle_xml


@mock_aws
class TestHandleXML(unittest.TestCase):
    def setUp(self):
        self.sample_data = [
            {"name": "George", "age": "44", "city": "York"},
            {"name": "Lindsay", "age": "40", "city": "Leeds"},
            {"name": "Michael", "age": "37", "city": "Sheffield"}
        ]

        sample_xml_data = (
            "<root>"
            "<person><name>George</name><age>44</age><city>York</city></person>"
            "<person><name>Lindsay</name><age>40</age><city>Leeds</city></person>"
            "<person><name>Michael</name><age>37</age><city>Sheffield</city></person>"
            "</root>"
        )

        bucket_name = "test-bucket"
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        s3.put_object(Bucket=bucket_name, Key="test/empty-file.xml", Body="")
        s3.put_object(
            Bucket=bucket_name,
            Key="test/test.xml",
            Body=sample_xml_data
        )
        s3.put_object(
            Bucket=bucket_name,
            Key="test/no-children.xml",
            Body="<root></root>"
        )

    def test_returns_list_of_dicts(self):
        result = handle_xml("s3://test-bucket/test/test.xml")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(row, dict) for row in result))

    def test_returns_list_of_expected_length(self):
        result = handle_xml("s3://test-bucket/test/test.xml")
        self.assertEqual(len(result), 3)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_xml("s3://test-bucket/test/empty-file.xml")
        self.assertEqual(result, [])

    def test_returns_expected_data(self):
        result = handle_xml("s3://test-bucket/test/test.xml")
        self.assertEqual(result, self.sample_data)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
