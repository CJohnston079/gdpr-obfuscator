import pytest


@pytest.fixture
def ts_shallow_data():
    shallow_data = [
        {"name": "George", "age": "44", "city": "York"},
        {"name": "Michael", "age": "40", "city": "Leeds"},
        {"name": "Lindsay", "age": "37", "city": "Sheffield"}
    ]
    obfuscated_shallow_data = [
        {"name": "***", "age": "44", "city": "York"},
        {"name": "***", "age": "40", "city": "Leeds"},
        {"name": "***", "age": "37", "city": "Sheffield"}
    ]

    return shallow_data, obfuscated_shallow_data


@pytest.fixture
def ts_deep_data():
    deep_data = [
        {
            "name": "George",
            "age": "44",
            "city": "York",
            "contact": [
                    {"email": "george@bluthcompany.com"},
                    {"phone": "01904 123456"}
            ],
        },
        {
            "name": "Lindsay",
            "age": "40",
            "city": "Leeds",
            "contact": [
                    {"email": "lindsay@bluthcompany.com"},
                    {"phone": "0113 123456"}
            ],
        },
        {
            "name": "Michael",
            "age": "37",
            "city": "Sheffield",
            "contact": [
                    {"email": "michael@bluthcompany.com"},
                    {"phone": "0114 123456"}
            ],
        }
    ]
    obfuscated_deep_data = [
        {
            "name": "***",
            "age": "44",
            "city": "York",
            "contact": [
                    {"email": "***"},
                    {"phone": "***"}
            ],
        },
        {
            "name": "***",
            "age": "40",
            "city": "Leeds",
            "contact": [
                    {"email": "***"},
                    {"phone": "***"}
            ],
        },
        {
            "name": "***",
            "age": "37",
            "city": "Sheffield",
            "contact": [
                    {"email": "***"},
                    {"phone": "***"}
            ],
        }
    ]

    return deep_data, obfuscated_deep_data
