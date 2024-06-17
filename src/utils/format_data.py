from src.exceptions import FormatDataError
from src.utils.file_formatters.serialise_data import serialise_data


def format_data(data):
    try:
        formatted_data = serialise_data(data)

        return formatted_data

    except Exception as e:
        raise FormatDataError(e)
