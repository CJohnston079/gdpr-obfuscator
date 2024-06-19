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

    def dict_to_xml(tag, dictionary):
        children = []

        for key, val in dictionary.items():
            if isinstance(val, dict):
                children.append(dict_to_xml(key, val))
            else:
                children.append(f"<{key}>{val}</{key}>")

        return f"<{tag}>{''.join(children)}</{tag}>"

    root = list(data[0].keys())[0]
    children = []

    for entry in data:
        child = list(entry[root].keys())[0]
        children.append(dict_to_xml(child, entry[root][child]))

    xml_str = f"<{root}>{''.join(children)}</{root}>"

    return xml_str
