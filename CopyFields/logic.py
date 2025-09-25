import json
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QListWidget, QDialogButtonBox, QVBoxLayout, QCheckBox
from aqt import mw
from aqt.utils import tooltip, showInfo

def chooseItemDialog(msg, choices,startrow=0):
    dialog = QDialog(mw.app.activeWindow())
    dialog.setWindowModality(Qt.WindowModality.WindowModal)
    layout = QVBoxLayout(dialog)
    dialog.setLayout(layout)

    label = QLabel(msg)
    layout.addWidget(label)

    # options
    list_widget = QListWidget()
    list_widget.addItems(choices)
    list_widget.setCurrentRow(startrow)
    layout.addWidget(list_widget)

    # buttons
    buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    layout.addWidget(buttons)

    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)

    if dialog.exec() == 0:
        return None
    return list_widget.currentRow()

def select_fields(note_type_id):
    model = mw.col.models.get(note_type_id)
    model_name = model["name"]
    field_names = [f['name'] for f in model['flds']]

    dialog = QDialog(mw.app.activeWindow())
    dialog.setWindowModality(Qt.WindowModality.WindowModal)
    layout = QVBoxLayout(dialog)
    dialog.setLayout(layout)

    label = QLabel(f"Select fields for {model_name}")
    layout.addWidget(label)

    checkboxes = {}
    for field in field_names:
        cb = QCheckBox(field)
        layout.addWidget(cb)
        checkboxes[field] = cb

    # buttons
    buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    layout.addWidget(buttons)

    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)

    if dialog.exec() == 0:
        return None
    selected_fields = [f for f, cb in checkboxes.items() if cb.isChecked()]

    # save note type fields
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

    data[str(note_type_id)] = selected_fields

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return selected_fields


def get_deck(msg="Select a Deck"):
    decks = mw.col.decks.all_names()
    index = chooseItemDialog(msg, decks)

    if index is None:
        return None

    deck_name = decks[index]
    deck_id = mw.col.decks.id(deck_name)
    return deck_id

def get_note_type_id(deck_id):
    cids = mw.col.decks.cids(deck_id)
    note_type_ids = set([mw.col.get_card(cid).note_type()['id'] for cid in cids])
    if note_type_ids is None:
        return
    return list(note_type_ids)


def select_note_types(note_type_ids):
    note_types = mw.col.models.all()
    choices = [nt['name'] for nt in note_types if nt['id'] in note_type_ids]
    index = chooseItemDialog("Select a Note Type", choices)
    if index is None:
        return None
    selected_nt = choices[index]
    for nt in note_types:
        if nt['name'] == selected_nt:
            return nt['id']
    return None

def setup_from_note(note_id):
    selected_fields = select_fields(note_id)
    if selected_fields is not None:
        tooltip(f"Fields saved: {selected_fields}!")
    else:
        tooltip("No fields selected")

def setup_from_menu(editor):
    deck_id = get_deck()
    if deck_id is None:
        return

    note_type_ids = get_note_type_id(deck_id)
    if not note_type_ids:
        tooltip("No notes found")
        return

    note_type_id = note_type_ids[0] if len(note_type_ids) == 1 else select_note_types(note_type_ids)
    if not note_type_id:
        return
    selected_fields = select_fields(note_type_id)

    if selected_fields is not None:
        tooltip(f"Fields saved: {selected_fields}!")
    else:
        tooltip("No fields selected")