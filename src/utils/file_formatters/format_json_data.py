import json


def format_json_data(data):
    if data == []:
        return "[]"

    return json.dumps(data)
