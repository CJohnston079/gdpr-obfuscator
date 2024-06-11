import boto3
import unittest

from moto import mock_aws
from src.utils.file_handlers.handle_xml import handle_xml


@mock_aws
class TestHandleXML(unittest.TestCase):
    def setUp(self):
        self.sample_shallow_data = [
            {"person": {"name": "George", "age": "44", "city": "York"}},
            {"person": {"name": "Lindsay", "age": "40", "city": "Leeds"}},
            {"person": {"name": "Michael", "age": "37", "city": "Sheffield"}}
        ]

        self.sample_deep_data = [
            {"person":
                {"name": "George", "age": "44", "city": "York", "contact":
                    {"email": "george@bluthcompany.com", "phone": "01904 123456"}
                 }
             },
            {"person":
                {"name": "Lindsay", "age": "40", "city": "Leeds", "contact":
                    {"email": "lindsay@bluthcompany.com", "phone": "0113 123456"}
                 }
             },
            {"person":
                {"name": "Michael", "age": "37", "city": "Sheffield", "contact":
                    {"email": "michael@bluthcompany.com", "phone": "0114 123456"}
                 }
             },
        ]

        sample_shallow_xml_data = (
            "<root>"
            "<person><name>George</name><age>44</age><city>York</city></person>"
            "<person><name>Lindsay</name><age>40</age><city>Leeds</city></person>"
            "<person><name>Michael</name><age>37</age><city>Sheffield</city></person>"
            "</root>"
        )

        sample_deep_xml_data = (
            """
          <root>
            <person>
              <name>George</name>
              <age>44</age>
              <city>York</city>
              <contact>
                <email>george@bluthcompany.com</email>
                <phone>01904 123456</phone>
              </contact>
            </person>
            <person>
              <name>Lindsay</name>
              <age>40</age>
              <city>Leeds</city>
              <contact>
                <email>lindsay@bluthcompany.com</email>
                <phone>0113 123456</phone>
              </contact>
            </person>
            <person>
              <name>Michael</name>
              <age>37</age>
              <city>Sheffield</city>
              <contact>
                <email>michael@bluthcompany.com</email>
                <phone>0114 123456</phone>
              </contact>
            </person>
          </root>
          """
        )

        bucket_name = "test-bucket"
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        s3.put_object(Bucket=bucket_name, Key="test/empty-file.xml", Body="")
        s3.put_object(
            Bucket=bucket_name,
            Key="test/shallow-data.xml",
            Body=sample_shallow_xml_data
        )
        s3.put_object(
            Bucket=bucket_name,
            Key="test/deep-data.xml",
            Body=sample_deep_xml_data
        )

    def test_returns_list_of_dicts(self):
        result = handle_xml("s3://test-bucket/test/shallow-data.xml")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(row, dict) for row in result))

    def test_returns_list_of_expected_length(self):
        result = handle_xml("s3://test-bucket/test/shallow-data.xml")
        self.assertEqual(len(result), 3)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_xml("s3://test-bucket/test/empty-file.xml")
        self.assertEqual(result, [])

    def test_returns_expected_shallow_data(self):
        result = handle_xml("s3://test-bucket/test/shallow-data.xml")
        self.assertEqual(result, self.sample_shallow_data)

    def test_returns_expected_deep_data(self):
        result = handle_xml("s3://test-bucket/test/deep-data.xml")
        self.assertEqual(result, self.sample_deep_data)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
