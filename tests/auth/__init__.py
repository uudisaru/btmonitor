import os


def read_key(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, filename)) as f:
        return f.read()
