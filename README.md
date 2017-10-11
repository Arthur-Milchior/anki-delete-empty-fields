Copyright: Arthur Milchior arthur@milchior.fr
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
Feel free to contribute to this code on https://github.com/Arthur-Milchior/anki-delete-empty-fields
Anki Add-on number: 215304215

WARNING: IF for some reason, you want notes with a field being entirely whitespaces (i.e. space, tab, newline,...) DO NOT USE THIS ADD-ON

Usage: sometime a field which appears empty in the browser is not considered as empty by anki. 
This add-on ensures that notes with an empty are considered empty by anki.

This fact is ensured only for new cards and cards which are edited. A button "empty fields" in the main window allow you to apply this add-on to already existing notes.


Technical notes:
Usually, the empty fields, not considered empty by anki, contains some html. This can be seen using sqlitebrowser (or any other tool to check the database) or ankidroid. This add-ons checks whether 