import json
import os

def get_config():
    addon_dir = os.path.dirname(__file__)
    return os.path.join(addon_dir, "user_files", "settings.json")


def check_json_config(note_type_id: int):
    config_file = get_config()

    if not os.path.exists(config_file):
        return None

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}

    return data.get(str(note_type_id))
