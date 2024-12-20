import csv


def read_file(path: str) -> list[list[str]]:
    rows: list[list[str]] = []

    # open csv file
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row in reader:
            # add row to rows
            rows.append(row)
        return rows
