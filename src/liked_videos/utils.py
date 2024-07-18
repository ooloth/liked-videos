import json


def pretty_json(json_data: dict | list[dict]) -> str:
    return json.dumps(json_data, indent=2, sort_keys=True)


def pretty_print_json(json_data: dict | list[dict]) -> None:
    print(json.dumps(json_data, indent=2, sort_keys=True))
