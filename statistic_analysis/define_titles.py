


def define_titles(exercise):
    title = []
    if(exercise=='Raven Score'):
        title.append('Raven')
    if(exercise=='Memory Short Audit Verb'):
        title.append('Βραχύχρονη Ακουστική Λεκτική Μνήμη')
        title.append('Βραχύχρονη Ακουστική Φωνολογική Μνήμη')
    if(exercise=='Memory Work Audit Verb'):
        title.append('Εργαζόμενη Ακουστική Μνήμη')
    if(exercise=='Phonological Rhymes'):
        title.append('Ρίμες')
    if(exercise=='Phonological Syllables'):
        title.append('Αντικατάσταση Συλλαβών')
    if(exercise=='Phonological Phonemes'):
        title.append('Απαλοιφή Φωνήματος')
    if(exercise=='Decode Words Pseudo'):
        title.append('Αποκωδικοποίηση Πραγματικών Λέξεων')
        title.append('Αποκωδικοποίηση Ψευδο-Λέξεων')
    if(exercise=='Visual Orthographic Rec'):
        title.append('Οπτική Αναγνώριση')
        title.append('Οπτική Ορθογραφία')
    if(exercise=='Decode Sentences'):
        title.append('Κατανόηση Προτάσεων')
    
    return title
        
    