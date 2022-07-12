import csv
import os


def write(filename: str, process):
    filePath = 'output/' + filename + '.csv'
    os.makedirs(os.path.dirname(filePath), exist_ok=True)

    with open(filePath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        process(writer)


def read(filename: str, extract) -> list:
    filePath = 'output/' + filename + '.csv'

    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        return extract(reader)
