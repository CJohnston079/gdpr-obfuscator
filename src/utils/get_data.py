from src.utils.get_file_type import get_file_type
from src.file_handlers.handle_csv import handle_csv


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
        ValueError: If no function exists to handle the file_type
    """
    file_type = get_file_type(file_path)

    if file_type == 'csv':
        data = handle_csv(file_path)
        data = 'poo'
    else:
        raise ValueError(
            f"File type .{file_type} is not supported."
        )

    return data
