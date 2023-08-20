import os
import json
from typing import Dict, Any


def load_json(file_path: str) -> Dict[str, Any]:
    if not os.path.isfile(file_path):
        raise Exception(f"File {file_path} does not exist")

    with open(file_path, 'r', encoding='utf-8') as file:
        result = json.load(file)

    return result

def write_json(obj: Any, file_path: str) -> None:
    with open(file_path, mode='w', encoding='utf-8') as file:
        json.dump(obj, file, ensure_ascii=True, indent=4)
