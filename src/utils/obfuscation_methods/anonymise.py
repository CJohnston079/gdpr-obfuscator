import re

from .tokenise import tokenise


def anonymise(field, options):
    """
    Returns an randomly generated value intended to be used as an obfuscation
    for a field in a data set.

    Args:
        field (string): The field to be obfuscated, used to look up an
            appropriate value in pii_fields.
        options (dict): A dictionary containing obfuscation options. If the key
            "token" is in options, then the value will be returned in the
            event that field is not found in pii_fields.

    Returns:
        str: A randomly generated value from pii_fields, or a token if a value
            is not found in pii_fields.
    """
    pii_fields = options["_anonymous_pii_fields"]
    cleaned_field = re.sub(r"[ \-_]", "", field).lower()
    value = pii_fields.get(cleaned_field, tokenise(field, options))
    return value
