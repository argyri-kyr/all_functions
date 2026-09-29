from PIL import Image
import glob
from globalVars import folder1, folder2

#Load and Appear at the end of the programme, all the fixation images that are stored in all_graphs file
def LoadFixationFiles(text, sub1):

    #create list of files
    files = glob.glob(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + '1/fixations*.png')

    #loop over list
    for f in files:
        im = Image.open(f)
        im.show()

