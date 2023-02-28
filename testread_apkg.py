# Import the necessary Anki modules
import os
from anki.collection import Collection

# Get the path of the .apkg file
apkg_file_path = os.path.join("./","myapkg/SelectedNotes.apkg")

# Load the collection from the .apkg file
collection = Collection(apkg_file_path)

# Get the list of notes in the collection
notes = collection.findNotes("")

# Loop through the notes and print their fields and tags
for note_id in notes:
    note = collection.getNote(note_id)
    fields = note.fields
    tags = note.tags
    # Do something with the note data, such as printing it to the console
    print("Fields:", fields)
    print("Tags:", tags)

# Close the collection
collection.close()
