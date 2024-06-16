import logging

from src.exceptions import GetDataError
from src.utils.file_handlers import handle_csv
from src.utils.file_handlers import handle_json
from src.utils.file_handlers import handle_parquet
from src.utils.file_handlers import handle_xml
from src.utils.get_file_type import get_file_type


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_data(file_path):
    """
    Reads the contents of a file and returns a list of dictionaries,

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        list: A list of dictionaries representing the data structure in
            the file.

    Raises:
        TypeError: If no function exists to handle file_type.
        GetDataError: If any other Exception is raised.
    """
    try:
        file_type = get_file_type(file_path)
        bucket = file_path.split("/")[2]
        key = "/".join(file_path.split("/")[3:])

        handlers = {
            "csv": handle_csv,
            "json": handle_json,
            "pqt": handle_parquet,
            "parquet": handle_parquet,
            "xml": handle_xml,
        }

        handler = handlers.get(file_type)

        if handler is None:
            raise TypeError(f"file type .{file_type} is not supported")

        data = handler(bucket, key)

        return data

    except TypeError:
        raise
    except Exception as e:
        raise GetDataError(e)
