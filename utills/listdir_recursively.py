import os


def listdir(dir: str):
    result = []
    for root, _, files in os.walk(dir):
        for file in files:
            result.append(os.path.join(root, file))
    return result
