import re


def get_file_type(file_path):
    """
    Returns the file type as a string from a given file path.

    Args:
        file_path (str): The file path from which to extract the file type.

    Returns:
        str or None: The file type corresponding to the file extension found
        in the file path, or None if the file type is not supported or no
        extesion is found.
    """

    extension_map = {
        "csv": "csv",
        "json": "json",
        "pqt": "parquet",
        "parquet": "parquet"
    }

    extension_pattern = r"\.(\w+)(?:\?.*|#.*)?$"
    extension = re.search(extension_pattern, file_path)

    if not extension:
        return None

    file_type = extension_map.get(extension.group(1))

    return file_type
