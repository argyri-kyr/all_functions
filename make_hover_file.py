

import os
import shutil

from globalVars import folder1, folder2, textends

def make_hover_file(text):
    if os.path.exists(folder1 + 'texts/'+ text + textends + '_hover/'):
        return
    else:
        os.makedirs(folder1 + 'texts/'+ text + textends + '_hover/')
        sourcefile = folder1 + 'texts/'+ text + textends + "/alltext.txt"
        destfile = folder1 + 'texts/'+ text + textends + '_hover/alltext.txt'
        shutil.copyfile(sourcefile, destfile)

        sourcefile = folder1 + 'texts/'+ text + textends + "/alltext_true_lines.txt"
        destfile = folder1 + 'texts/'+ text + textends + '_hover/alltext_true_lines.txt'
        shutil.copyfile(sourcefile, destfile)

        return