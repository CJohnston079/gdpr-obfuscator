from src.exceptions import ObfuscationError


def obfuscate_fields(data, options):
    """
    Obfuscates targeted fields in a list of dictionaries.

    Takes a list of dictionaries representing records (data) and an options
    dictionary. The options dictionary should container the key "pii_fields",
    which are the fields to be obfuscated. Returns a new list of dictionaries
    where the pii_fields have been obfuscated, which by default tokenises them
    with a triple asterisk string ("***").

    Args:
        data (list of dict): A list of dictionaries representing records, where
            each dict contains key-value pairs for the fields of the record.
        options (dict): A dictionary containing the following keys:
            pii_fields (str): A list of strings of the fields to obfuscated.
            obfuscation_method (func): The method to call on fields to be
                obfuscated.
            options (dict): A dictionary containing options for the obfuscation
                method.

    Returns:
        list of dict: A new list of dictionaries where the targeted fields are
        obfuscated using the obfuscation_method in options.
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
