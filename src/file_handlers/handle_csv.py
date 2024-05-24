import csv


def handle_csv(csv_file):
    data = []

    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(dict(row))

    return data
