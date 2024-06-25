def mask(field, options):
    """
    Returns a token intended to be used as an obfuscation for a field in a data
    set. The token is a triple asterisk ("***") by default.

    Args:
        field (string): The field to be obfuscated.
        options (dict): A dictionary containing obfuscation options. It should
            containt the key "_val" whose length determines the number of
            repetitions of the token. If val is None then the function will
            return a single token. If the key "token" is in options, then this
            will be used as the token.

    Returns:
        str: A string of repeated tokens, corresponding to the length of
            options["val"].
    """
    mask_length = len(options.get("_val") or "_")
    token = options.get("token", "*")
    return token * mask_length
