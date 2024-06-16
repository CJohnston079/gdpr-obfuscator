from src.exceptions import UnsupportedFile
from src.utils.file_handlers import handle_csv
from src.utils.file_handlers import handle_json
from src.utils.file_handlers import handle_parquet
from src.utils.file_handlers import handle_xml
from src.utils.get_file_type import get_file_type


def get_data(file_path):
    """
    Reads the contents of a file and returns a list of dictionaries,

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        list: A list of dictionaries representing the data in the file.
              Each dictionary contains key-value pairs where the keys are
              column headers and the values are the corresponding values
              from each row.

    Raises:
        UnsupportedFile: If no function exists to handle file_type
    """
    try:
        file_type = get_file_type(file_path)

        handlers = {
            "csv": handle_csv,
            "json": handle_json,
            "pqt": handle_parquet,
            "parquet": handle_parquet,
            "xml": handle_xml,
        }

        handler = handlers.get(file_type)
        data = handler(file_path)

        return data

    except TypeError:
        raise UnsupportedFile(file_type)
