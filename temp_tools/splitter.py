import json


def split_json(json_file: str) -> None:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    upper_keys = {k: v for k, v in data.items() if k[0].isupper()}
    lower_keys = {k: v for k, v in data.items() if k[0].islower()}

    with open('uppercase_forward.json', 'w', encoding='utf-8') as f:
        json.dump(upper_keys, f, indent=4, ensure_ascii=False)

    with open('forward_map.json', 'w', encoding='utf-8') as f:
        json.dump(lower_keys, f, indent=4, ensure_ascii=False)


path: str = ''
split_json(path)
