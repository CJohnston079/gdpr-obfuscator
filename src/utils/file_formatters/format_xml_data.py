def format_xml_data(data):
    """
    Formats a data structure into an XML string ready for writing.

    Args:
        data (str): The data to be formatted

    Returns:
        str: An XML formatted string.
    """
    if data == []:
        return ""

    def dict_to_xml(tag, dictionary, level=1):
        indent = "  " * level
        child_indent = "  " * (level + 1)
        children = []

        for key, val in dictionary.items():
            if isinstance(val, dict):
                children.append(dict_to_xml(key, val, level + 1))
            else:
                children.append(f"{child_indent}<{key}>{val}</{key}>\n")

        return f"{indent}<{tag}>\n{''.join(children)}{indent}</{tag}>\n"

    root = list(data[0].keys())[0]
    children = []

    for entry in data:
        child = list(entry[root].keys())[0]
        children.append(dict_to_xml(child, entry[root][child], level=1))

    xml_str = f"<{root}>\n{''.join(children)}</{root}>"

    return xml_str
