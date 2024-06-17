import xml.etree.ElementTree as ET


def format_xml_data(data):
    """
    Formats a data structure into an XML string ready for writing.

    Args:
        data (str): The data to be formatted

    Returns:
        str: An XML formatted string.
    """
    if data == []:
        return "<data></data>"

    root = ET.Element("data")
    for item in data:
        entry = ET.SubElement(root, "entry")
        for key, value in item.items():
            ET.SubElement(entry, key).text = str(value)

    return ET.tostring(root, encoding="unicode", method="xml")
