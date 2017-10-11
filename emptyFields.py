"""Copyright: Arthur Milchior arthur@milchior.fr
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
Feel free to contribute to this code on https://github.com/Arthur-Milchior/anki-delete-empty-fields
Anki Add-on number: 215304215


WARNING: IF for some reason, you want notes with a field being entirely whitespaces (i.e. space, tab, newline,...) DO NOT USE THIS ADD-ON

Usage: sometime a field which appears empty in the browser is not considered as empty by anki. 
This add-on ensures that notes with an empty are considered empty by anki.

This fact is ensured only for new cards and cards which are edited. A button "empty fields" in the main window allow you to apply this add-on to already existing notes.


Technical notes:
Usually, the empty fields, not considered empty by anki, contains some html. This can be seen using sqlitebrowser (or any other tool to check the database) or ankidroid. This add-ons checks whether 
"""
#Note that the code could be simpler. However, I do prefer to use more
#generic function that I could then copy paste into other
#add-ons. Waiting for a day where add-ons can uses code in common ?


from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, showWarning, askUser
from anki.notes import Note
import re
import aqt
import cgi

def askUserPerso(text):
    return askUser("""escaped:
    ========
    """+cgi.escape(text)+"""========
    Unescaped
    ========
    """+text)


tag =r"<\s*(?!img)[^<>]*>"
"""Recognizing a tag which is not img"""

space_tag = r"(?:"+tag+r"|\s)"
"""Either a non_img tage, or a space"""

emptyField=re.compile(r"^"+space_tag+r"*$")
"""Regexp recognizing a text containing only whitespace and non img
tags"""

def run():
    """transform empty fields into really empty fields"""
    col = mw.col
    nids = col.db.list("""select id from notes""")
    for nid in nids:
        note = Note(col, id=nid)
        if remove (note,emptyField):
            #If some change really did happen
            oldFlush(note)


def checkRemove(note,regexp):
    #Not used in this addons. Replacing remove by checkRemove allows
    #to check what is edited before changing the note.
        changes= remove(note, emptyField)
        someChange=False
        for (name,before,after) in changes:
            if askUser("""Allow edition from:
            ----------
            """+ before+ """
            ----------
            Into:
            ----------
            """ + after):
                note.__setitem__(name, after)
                someChange=True
        return someChange

def remove(note,regexp,doChange=False):
    """Remove the text recognized by regexp if doChange is true. Return the changes that (would) happens"""
    return editNote(note,regexp,"",doChange=doChange)

def editNote(note,regexp,repl, doChange=False):
    """Apply changeIter(regexp,repl) to every field of this note.
    Return the list of changes.

    Return the list of changed fields, with before/after"""
    changer = changeIter(regexp,repl)
    changes = []
    for (name,value) in note.items():
        (after,is_changed)= changer(value)
        if is_changed:
            changes.append((name,value,after))
            if  doChange:
                note.__setitem__(name, after)
    return changes
            
def changeIter(regexp,repl):
    """A function which applies: substituting regexp by repl, until doing so does not change anything. This function also returns whether a changed occured."""
    def aux(text):
        text_ = text
        changed= ""
        while changed!=text_:
            # if not askUserPerso("Considering "+ text_+"."):
            #     return
            changed=text_
            text_= regexp.sub(repl,text_)
        return (changed, changed!=text)
    return aux

# def changeIter(regexp,repl,text):
#     """A function which applies: substituting regexp by repl, until doing so does not change anything. This function also returns whether a changed occured."""
#     text_ = text
#     changed= ""
#     while changed!=text_:
#         print("Considering "+ text_+".")
#         changed=text_
#         text_= regexp.sub(repl,text_)
#     return (changed, changed!=text)


oldFlush = Note.flush
def noteFlush(note, mod=None):
    remove(note, emptyField)
    oldFlush(note,mod=mod)

Note.flush = noteFlush



action = QAction(aqt.mw)
action.setText("Empty fields")
mw.form.menuTools.addAction(action)
action.triggered.connect(run)
