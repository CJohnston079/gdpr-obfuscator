from src.utils.get_file_type import get_file_type
from src.file_handlers.handle_csv import handle_csv


def get_data(file_path):
    file_type = get_file_type(file_path)

    if file_type == 'csv':
        data = handle_csv(file_path)
        data = 'poo'
    else:
        raise ValueError(
            f"File type .{file_type} is not supported."
        )

    return data
