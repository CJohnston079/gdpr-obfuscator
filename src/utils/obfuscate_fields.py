from src.exceptions import ObfuscationError


def obfuscate_fields(data, options):
    """
    Obfuscates targeted fields in a list of dictionaries.

    This function takes a list of dictionaries representing records (data) and
    a list of fields to obfuscate. It returns a new list of dictionaries where
    the specified fields are replaced with "***", retaining the original
    structure of the data.

    Args:
        data (list of dict): A list of dictionaries representing records, where
            each dict contains key-value pairs for the fields of the record.
        fields (list of str): A list of strings of the fields to obfuscate.

    Returns:
        list of dict: A new list of dictionaries where the targeted fields are
        replaced with "***".
    """
    try:
        obfuscated_data = []

        for record in data:
            obfuscated_record = obfuscate_record(record, options)
            obfuscated_data.append(obfuscated_record)

        return obfuscated_data

    except AttributeError as e:
        raise AttributeError(e)
    except RecursionError:
        raise RecursionError("maximum recursion depth exceeded.")
    except Exception as e:
        raise ObfuscationError(e)


def obfuscate_record(record, options):
    obfuscated_record = {}

    for field, val in record.items():
        obfuscated_record[field] = obfuscate_field(field, val, options)

    return obfuscated_record


def obfuscate_field(field, val, options):
    pii_fields = options["pii_fields"]
    obfuscation_method = options["obfuscation_method"]
    obfuscation_options = options["options"]

    if isinstance(val, list):
        return obfuscate_fields(val, options)
    elif isinstance(val, dict):
        return obfuscate_record(val, options)
    elif field in pii_fields:
        return obfuscation_method(field, obfuscation_options)
    else:
        return val
