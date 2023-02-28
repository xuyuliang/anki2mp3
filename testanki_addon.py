# an anki addon to exprot a deck to a csv file
#
# Copyright: (c) 2012-2014 Robert Baruch <robert.c.baruch@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os
import csv
import codecs
import anki
import anki.importing
from anki.utils import stripHTML
from anki.hooks import addHook
from aqt import mw
from aqt.utils import showInfo, showWarning, askUser, getOnlyText
from aqt.qt import *
from aqt import QAction, QMenu
from PyQt5.QtWidgets import QMessageBox
def export_csv(self):
    # get the path to the file
    file_path = getOnlyText(_("./outputmp3/"), default="deck.csv")
    if not file_path:
        return

    # get the deck
    deck = self.deck

    # get the models
    models = deck.models

    # get the cards
    cards = deck.cards()

    # get the notes
    notes = deck.notes()

    # get the fields
    fields = models

# Define a function to add the new menu item
def addMenuItem(browser):
    # Create a new QAction object with a label
    action = QAction("My Add-on", browser)
    # Connect the QAction to a function that will be called when the menu item is clicked
    action.triggered.connect(myFunction)
    # Add the QAction to the browser's Tools menu
    browser.menuTools.addAction(action)

# Define the function that will be called when the menu item is clicked
def myFunction():
    # Display a message box with a message
    QMessageBox.information(None, "My Add-on", "Hello from my add-on!")

# Register the add-on with Anki
addHook("browser.setupMenus", addMenuItem)