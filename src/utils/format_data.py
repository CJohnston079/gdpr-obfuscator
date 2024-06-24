from .file_formatters.format_csv_data import format_csv_data
from .file_formatters.format_json_data import format_json_data
from .file_formatters.format_parquet_data import format_parquet_data
from .file_formatters.format_xml_data import format_xml_data
from .file_formatters.serialise_data import serialise_data
from exceptions import FormatDataError


def format_data(data, file_type=None):
    """
    Formats a list of data into a string ready to be written to a specified
    file type. If no file type is specified, a generic serialised string is
    returned.

    Args:
        data (list): the data to be formatted
        file_type (str): The extension with which to look up correct handler

    Returns:
        formatted_data (str): A string of data formatted ready for writing to
            the specified file_type.

    Raises:
        FormatDataError: If an Exception is raised while formatting the data.
    """
    try:
        handlers = {
            "csv": format_csv_data,
            "json": format_json_data,
            "pqt": format_parquet_data,
            "parquet": format_parquet_data,
            "xml": format_xml_data,
        }

        handler = handlers.get(file_type)

        if handler is None:
            formatted_data = serialise_data(data)
        else:
            formatted_data = handler(data)

        return formatted_data

    except Exception as e:
        raise FormatDataError(e)
