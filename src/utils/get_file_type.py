import re


def get_file_type(file_path):
    """
    Returns the file type as a string from a given file path.

    Args:
        file_path (str): The file path from which to extract the file type.

    Returns:
        str: The file extension found at the end of the file path.

    Raises:
        AttributeError: If unable to retrieve extension from file path.
    """
    try:
        extension_pattern = r"\.(\w+)(?:\?.*|#.*)?$"
        extension = re.search(extension_pattern, file_path)

        file_type = extension.group(1)

        return file_type

    except AttributeError:
        raise AttributeError(f"unable to get file extension from {file_path}")
