

import os


from globalVars import folder1, textends



def findnumberoftextpages(text):
    folder_path = folder1 + 'texts/' + text + textends 
    file_prefix = "Slide"
    file_extension = ".png"

    # List all files in the directory
    files = os.listdir(folder_path)

    # Filter files based on the naming pattern
    slides = [file for file in files if file.startswith(file_prefix) and file.endswith(file_extension) and file[len(file_prefix):-len(file_extension)].isdigit()]

    # Count the number of matching files
    number_of_slides = len(slides)
    
    return number_of_slides