import os
import json


def write(filename: str, object):
    filePath = 'output/' + filename + '.json'
    os.makedirs(os.path.dirname(filePath), exist_ok=True)

    with open(filePath, 'w', newline='', encoding='utf-8') as file:
        json.dump(object, file, ensure_ascii=False, indent=4)
