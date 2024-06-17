import xml.etree.ElementTree as ET


def format_xml_data(data):
    if data == []:
        return "<data></data>"

    root = ET.Element("data")
    for item in data:
        entry = ET.SubElement(root, "entry")
        for key, value in item.items():
            ET.SubElement(entry, key).text = str(value)

    return ET.tostring(root, encoding="unicode", method="xml")
