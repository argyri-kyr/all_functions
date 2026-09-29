


def saveAudioNotes(notes, notespath):
    text_file = open(notespath, "w")
    text_file.write(notes)
    text_file.close()