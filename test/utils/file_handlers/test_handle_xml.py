import boto3
import pytest

from src.utils.file_handlers.handle_xml import handle_xml


class TestHandleXML():
    @pytest.fixture(scope="class", autouse=True)
    def set_up_s3_data(self, s3_bucket):
        s3, bucket_name = s3_bucket

        sample_shallow_data = [
            {"person": {"name": "George", "age": "44", "city": "York"}},
            {"person": {"name": "Lindsay", "age": "40", "city": "Leeds"}},
            {"person": {"name": "Michael", "age": "37", "city": "Sheffield"}}
        ]

        sample_deep_data = [
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

        s3.put_object(Bucket=bucket_name, Key="dir/empty-file.xml", Body="")
        s3.put_object(
            Bucket=bucket_name,
            Key="dir/shallow-data.xml",
            Body=sample_shallow_xml_data
        )
        s3.put_object(
            Bucket=bucket_name,
            Key="dir/deep-data.xml",
            Body=sample_deep_xml_data
        )

        return sample_shallow_data, sample_deep_data

    def test_returns_list_of_dicts(self):
        result = handle_xml("s3://test-bucket/dir/shallow-data.xml")
        assert isinstance(result, list)
        assert all(isinstance(row, dict) for row in result)

    def test_returns_list_of_expected_length(self, set_up_s3_data):
        sample_shallow_data, _ = set_up_s3_data
        result = handle_xml("s3://test-bucket/dir/shallow-data.xml")
        assert len(result) == len(sample_shallow_data)

    def test_returns_empty_list_when_passed_empty_file(self):
        result = handle_xml("s3://test-bucket/dir/empty-file.xml")
        assert result == []

    def test_returns_expected_shallow_data(self, set_up_s3_data):
        sample_shallow_data, _ = set_up_s3_data
        result = handle_xml("s3://test-bucket/dir/shallow-data.xml")
        assert result == sample_shallow_data

    def test_returns_expected_deep_data(self, set_up_s3_data):
        _, sample_deep_data = set_up_s3_data
        result = handle_xml("s3://test-bucket/dir/deep-data.xml")
        assert result == sample_deep_data
