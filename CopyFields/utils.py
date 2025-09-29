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

def load_settings(model_id: int):
    config_file = get_config()

    if not os.path.exists(config_file) or os.path.getsize(config_file) == 0:
        return None

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    return data.get(str(model_id))


def save_settings(note_type_id, selected_fields, tags):
    user_files = os.path.join(os.path.dirname(__file__), "user_files")
    os.makedirs(user_files, exist_ok=True)

    config_file = os.path.join(user_files, "settings.json")

    data = {}
    if os.path.exists(config_file) and os.path.getsize(config_file) > 0:
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    data[str(note_type_id)] = {
        "fields": selected_fields,
        "tags": tags
    }

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
