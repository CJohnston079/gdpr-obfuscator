def obfuscate_fields(data, fields):
    """
    Obfuscates targeted fields in a list of dictionaries.

    This function takes a list of dictionaries representing records (data) and
    a list of fields to obfuscate. It returns a new list of dictionaries where
    the specified fields are replaced with '***'.

    Args:
        data (list of dict): A list of dictionaries representing records, where
            each dict contains key-value pairs for the fields of the record.
        fields (list of str): A list of strings of the fields to obfuscate.

    Returns:
        list of dict: A new list of dictionaries where the targeted fields are
        replaced with '***'.
    """

    obfuscated_data = []

    for record in data:
        obfuscated_record = {}

        for key, value in record.items():
            if (isinstance(value, list)):
                obfuscated_record[key] = obfuscate_fields(value, fields)
            else:
                obfuscated_record[key] = "***" if key in fields else value

        obfuscated_data.append(obfuscated_record)

    return obfuscated_data
