import os

from aqt import mw
from aqt.utils import showInfo, tooltip
from .logic import setup_from_note
from .utils import load_settings


def add_buttons(buttons, editor):
    copy_icon = os.path.join(os.path.dirname(__file__), "resources", "copy.png")
    copy_button = editor.addButton(
        copy_icon,
        "select fields",
        copy_action,
        tip="select fields to copy"
    )

    paste_icon = os.path.join(os.path.dirname(__file__), "resources", "paste.png")
    paste_button = editor.addButton(
        paste_icon,
        "paste fields",
        paste_action,
        tip="paste from same note"
    )
    buttons.append(copy_button)
    buttons.append(paste_button)

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

    settings = load_settings(model_id)
    if not settings:
        showInfo(f"No config found for {model_name}")
        return

    fields_to_copy = settings.get("fields", [])
    tags = settings.get("tags", False)

    if not fields_to_copy and not tags:
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

    # copy tags
    if tags:
        note.tags = list(set(note.tags) | set(prev_note.tags))

    editor.loadNote()
    if copied and not tags:
        tooltip("Fields Pasted!")
    elif copied and tags:
        tooltip("Fields and Tags Pasted!")
    else:
        tooltip("Tags Pasted!")

