from PyQt6.QtGui import QAction
from aqt import mw, gui_hooks
from .editor import add_buttons
from .logic import setup_from_menu

# menu
action = QAction("Copy Fields", mw)

# triggers
action.triggered.connect(setup_from_menu)

mw.form.menuTools.addAction(action)
gui_hooks.editor_did_init_buttons.append(add_buttons)
