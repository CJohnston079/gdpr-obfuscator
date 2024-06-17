import csv
import io


def format_csv_data(data):
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
