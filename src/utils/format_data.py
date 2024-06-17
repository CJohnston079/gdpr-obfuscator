from src.exceptions import FormatDataError
from src.utils.file_formatters.format_csv_data import format_csv_data
from src.utils.file_formatters.format_json_data import format_json_data
from src.utils.file_formatters.format_parquet_data import format_parquet_data
from src.utils.file_formatters.format_xml_data import format_xml_data
from src.utils.file_formatters.serialise_data import serialise_data


def format_data(data, file_type=None):
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
