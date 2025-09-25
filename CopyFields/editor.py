import json
import os

from aqt import mw
from aqt.utils import showInfo, tooltip
from .logic import setup_from_note
from .utils import get_config

def add_buttons(buttons, editor):
    copy_icon = os.path.join(os.path.dirname(__file__), "resources", "copy.png")
    copy_button = editor.addButton(
        copy_icon,
        "copy fields",
        copy_action,
        tip="copy fields"
    )

    paste_icon = os.path.join(os.path.dirname(__file__), "resources", "paste.png")
    paste_button = editor.addButton(
        paste_icon,
        "paste fields",
        paste_action,
        tip="paste selected fields"
    )
    buttons.append(copy_button)
    buttons.append(paste_button)

def load_fields_for_note_type(model_id: int):
    config_file = get_config()

    if not os.path.exists(config_file) or os.path.getsize(config_file) == 0:
        return None

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    return data.get(str(model_id))

def copy_action(editor):
    note = editor.note
    model = note.model()
    model_id = model["id"]
    setup_from_note(model_id)

def paste_action(editor):
    from aqt.editor import Editor

    if not isinstance(editor, Editor):
        return

    note = editor.note
    if not note:
        showInfo("No note selected")
        return

    model = note.model()
    model_id = model["id"]
    model_name = model["name"]

    fields_to_copy = load_fields_for_note_type(model_id)
    if not fields_to_copy:
        showInfo(f"No config found for {model_name} note type")
        return

    # exclude the current note if it already exists in DB
    current_id = note.id if getattr(note, "id", None) else None

    if current_id:
        prev_nid = mw.col.db.scalar(
            """
            SELECT id FROM notes 
            WHERE mid = ? AND id < ?
            ORDER BY id DESC LIMIT 1
            """,
            model_id,
            current_id,
        )
    else:
        # in Add Cards (note not saved yet), just grab latest of this type
        prev_nid = mw.col.db.scalar(
            """
            SELECT id FROM notes 
            WHERE mid = ? 
            ORDER BY id DESC LIMIT 1
            """,
            model_id,
        )

    if not prev_nid:
        showInfo(f"No previously saved note found for {model_name}")
        return

    prev_note = mw.col.get_note(prev_nid)
    if not prev_note:
        showInfo("Previous note could not be loaded")
        return

    prev_fields = {k.strip(): k for k in prev_note.keys()}
    new_fields = {k.strip(): k for k in note.keys()}

    copied = []
    for fname in fields_to_copy:
        if not isinstance(fname, str):
            continue
        key = fname.strip()
        if key in prev_fields and key in new_fields:
            prev_key = prev_fields[key]
            new_key = new_fields[key]
            note[new_key] = prev_note[prev_key]
            copied.append(new_key)

    # also copy tags
    note.tags = list(set(note.tags) | set(prev_note.tags))

    editor.loadNote()

    if copied:
        tooltip(f"Pasted fields: {', '.join(copied)} + tags")
    else:
        tooltip("0 fields pasted.")
