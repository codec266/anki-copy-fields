# Anki Copy Fields
**Copy Fields** is a simple [Anki](https://apps.ankiweb.net/) add-on that allows you to quickly copy fields from your previous note.

## Features
- Copy fields from the previous note of the same type.
- Automatically includes tags.
- Configure which fields to copy per note type
- Easy setup via **Tools → Copy Fields**

## Installation
**AnkiWeb**
1. Open Anki.
2. Go to **Tools → Add-ons → Get Add-ons**
3. Enter the add-on code: `1097703658`
4. Click `OK` and restart Anki.

**Source**
1. Go to the [Releases](https://github.com/codec266/anki-copy-fields/releases) tab of this repository.
2. Download the latest `.ankiaddon` file.
3. Double-click the `.ankiaddon` file to install.
4. Restart Anki.
## Demo
![Demo](assets/demo.gif)
## Usage

**Configuring Fields to Copy**
1. In Anki, go to **Tools → Copy Fields**.
2. Pick the deck you want to configure.
3. Select which note type you want to use.
4. Choose the fields you want to automatically copy.
5. Click `OK` to save your configuration.

📂 Your note type configurations are stored in `user_files/settings.json`

**Pasting Fields from Previous Note**
1. Open **Add** or edit an existing note.
2. Click the `paste selected fields` button in the editor's toolbar.
3. The configured fields and tags from the note before the current one will be copied.

⚠️ If no previous note exists or no configuration is set for the current note type, a pop-up will notify you instead of pasting.
___
