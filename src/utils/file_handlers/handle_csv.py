import csv


def handle_csv(csv_file):
    """
    Reads the contents of a CSV file and returns a list of dictionaries,

    Args:
        csv_file (str): The path to the CSV file to be read.

    Returns:
        list: A list of dictionaries representing the rows in the CSV file.
              Each dictionary contains key-value pairs where the keys are
              column headers and the values are the corresponding values
              from each row in the CSV file.

    Raises:
        FileNotFoundError: If the specified CSV file cannot be found.
    """

    with open(csv_file, 'r', newline='') as file:
        return [dict(row) for row in csv.DictReader(file)]
