import json
import os


def resolve_path_to_test_file(filename: str) -> str:
    data_directory_path = os.path.join(os.path.dirname(__file__), "data")
    return os.path.join(data_directory_path, filename)


def load_test_json_data(filename: str) -> dict:
    with open(resolve_path_to_test_file(filename)) as json_file:
        return json.loads(json_file.read())
