from src.file_handlers.handle_csv import handle_csv
from src.utils.get_file_type import get_file_type
from src.utils.obfuscate_fields import obfuscate_fields
from src.utils.serialise_dicts import serialise_dicts


def obfuscator(event):
    file_path = event["file_to_obfuscate"]
    fields_to_obfuscate = event["pii_fields"]

    file_type = get_file_type(file_path)

    if file_type == 'csv':
        data = handle_csv(file_path)
    else:
        return

    obfuscated_data = obfuscate_fields(data, fields_to_obfuscate)
    serialized_data = serialise_dicts(obfuscated_data)

    return serialized_data
