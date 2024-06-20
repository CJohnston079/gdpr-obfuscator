def tokenise(field, options):
    """
    Returns a token intended to be used as an obfuscation for a field in a data
    set. The token is a triple asterisk ("***") by default.

    Args:
        field (string): The field to be obfuscated.
        options (dict): A dictionary containing obfuscation options. If the key
            "token" is in options, then this will be returned.

    Returns:
        str: "***" or a custom token from options["token"].
    """
    return options.get("token", "***")
