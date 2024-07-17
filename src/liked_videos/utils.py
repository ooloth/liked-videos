import json


def pretty_print_json(json_data: dict | list[dict]) -> None:
    print(json.dumps(json_data, indent=4))
