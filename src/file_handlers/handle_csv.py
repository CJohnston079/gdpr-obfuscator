import csv


def handle_csv(csv_file):
    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        return [dict(row) for row in csv_reader]
