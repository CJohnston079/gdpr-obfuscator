from botocore.exceptions import ClientError

from src.exceptions import GetDataError
from src.utils.file_readers import get_csv_data
from src.utils.file_readers import get_json_data
from src.utils.file_readers import get_parquet_data
from src.utils.file_readers import get_xml_data
from src.utils.get_file_type import get_file_type


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
            "csv": get_csv_data,
            "json": get_json_data,
            "pqt": get_parquet_data,
            "parquet": get_parquet_data,
            "xml": get_xml_data,
        }

        handler = handlers.get(file_type)

        if handler is None:
            raise TypeError(f"file type .{file_type} is not supported")

        data = handler(bucket, key)

        return data

    except TypeError:
        raise
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchKey":
            raise FileNotFoundError(
                f"The file at {file_path} was not found in S3."
            )
        elif error_code == "AccessDenied":
            raise PermissionError(
                f"Permission denied for file {file_path} in S3."
            )
        else:
            raise OSError(
                f"An error occurred while accessing file {file_path} in S3: "
                f"{e}"
            )
    except Exception as e:
        raise GetDataError(e)
