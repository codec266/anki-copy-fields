# Anki Copy Fields

**Copy Fields** is a simple [Anki](https://apps.ankiweb.net/) add-on that allows you to quickly copy fields from the previously added card into your current note.

## Features
- Copy fields from the previous note of the same type.
- Automatically include tags
- Configure which fields to copy per note type
- Easy setup via **Tools → Copy Fields**

## Installation
**AnkiWeb**

**Source**

## Demo

## Usage

**Configuring Fields to Copy**
1. In Anki, go to **Tools → Copy Fields**.
2. Pick the deck you want to configure.
3. Select which note type you want to use.
4. Choose the fields you want to automatically copy.
5. Click `OK` to save your configuration.

📂 Your note type configurations are stored in `user_files/note_type_fields.json`

**Pasting Fields from Previous Note**
1. Open **Add** or edit an existing note.
2. Click the `paste selected fields` button in the editor's toolbar.
3. The configured fields and tags from the note before the current one will be copied.

⚠️ If no previous note exists or no configuration is set for the current note type, a pop-up will notify you instead of pasting.
