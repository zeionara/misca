import os
from yaml import load, dump, FullLoader


def read_state_from_yaml_file(path: str, default = None):
    if os.path.exists(path):
        with open(path, 'r', encoding = 'utf-8') as file:
            return load(file, Loader = FullLoader)
    return default


def write_state_to_yaml_file(path: str, state: dict):
    if not os.path.exists(path):
        os.makedirs(os.path.abspath(os.path.join(path, os.pardir)), exist_ok = True)

    with open(path, 'w', encoding = 'utf-8') as file:
        return dump(state, file)
