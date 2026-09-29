
from PIL import ImageOps
from PIL import Image

from globalVars import folder1, folder2, pyimagepath

def fixationsCropped(sub1, exam, text, pageno):
    path = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/fixations' + str(pageno) + '.png'
    img = Image.open(path)

    # Image Dimesions , before Crop
    w = 1366
    h= 768

    # Image Dimensions , after Crop
    cw = 800     # 950 , before change
    ch = 500     # 600 , before change

    # Center Coord
    wdif, hdif = (w-cw)//2, (h-ch)//2

    # Box Dimensions ( Part of Image I want to Crop )
    border = wdif, hdif, wdif, hdif  # left, top, right, bottom

    cropped_img = ImageOps.crop(img, border)
    newpath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/fixations' + str(pageno) + '_cropped.png'
    cropped_img.save(newpath)
