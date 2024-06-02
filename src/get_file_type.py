import re


def get_file_type(file_path):
    extension_map = {
        'csv': 'csv',
        'json': 'json',
        'pqt': 'parquet',
        'parquet': 'parquet'
    }

    extension_pattern = r'\.(\w+)(?:\?.*|#.*)?$'
    extension = re.search(extension_pattern, file_path)

    if not extension:
        return None

    file_type = extension_map.get(extension.group(1))

    return file_type
