from src.exceptions import ObfuscationError


def obfuscate_fields(data, fields):
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
            obfuscated_field = {}

            for key, val in record.items():
                if isinstance(val, list):
                    obfuscated_field[key] = obfuscate_fields(val, fields)
                elif isinstance(val, dict):
                    obfuscated_field[key] = obfuscate_fields([val], fields)[0]
                else:
                    obfuscated_field[key] = "***" if key in fields else val

            obfuscated_data.append(obfuscated_field)

        return obfuscated_data

    except AttributeError as e:
        raise AttributeError(e)
    except RecursionError:
        raise RecursionError("maximum recursion depth exceeded.")
    except Exception as e:
        raise ObfuscationError(e)
