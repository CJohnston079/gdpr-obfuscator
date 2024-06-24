import json


def format_json_data(data):
    """
    Formats a data structure into a JSON string ready for writing.

    Args:
        data (str): The data to be formatted.

    Returns:
        str: A JSON formatted string.
    """
    if data == []:
        return "[]"

    return json.dumps(data, indent=2)
