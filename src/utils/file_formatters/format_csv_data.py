import csv
import io


def format_csv_data(data):
    """
    Formats a data structure into a CSV string ready for writing.

    Args:
        data (str): The data to be formatted

    Returns:
        str: A CSV formatted string.
    """
    if data == []:
        return ""

    fieldnames = data[0].keys()
    output = io.StringIO()

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

    csv_contents = output.getvalue()
    output.close()

    return csv_contents
