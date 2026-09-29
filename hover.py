

import os
import scipy.io
from asyncio.windows_events import NULL
import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('TkAgg')

from globalVars import folder1, folder2, textends, guiflag
from basic_function_gui import basic_function_gui
from texttoplot import main_textplot
from colorbar import colorbar
from movefigure import movefigure
from zoomimage import zoomimage


def check_indiv_structure(sub1, text):
    path1 = folder1 + folder2 + 'subject_' + str(sub1) + '/'
    path2 = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + '1/py/bubbledata.xlsx'

    paths = [path1, path2]
    for p in paths:
        if( not os.path.exists(p) ):
            print("Not appropriate folder structure for sub = %d in text = %s" %(sub1, text))
            return NULL
            



def read_column(bubbledata, columnname):
    data = bubbledata[columnname]
    data = data.to_list()
    return data



def define_points(wordno):
    first_x = data.iloc[0, 0]

    roibounds = data.iloc[wordno, :]
    roibounds = roibounds.to_list()

    start_x = int( roibounds[0] )
    if(start_x != first_x):
        start_x = start_x + 10

    start_y = int( roibounds[1] )
    width = int( roibounds[2] )
    height  = int( roibounds[3] )

    end_x = start_x + width - 13
    end_y = start_y + height - 4

    return start_x, start_y, end_x, end_y



def choose_points(start_x, start_y, end_x, end_y):
    step = 5

    dividedpart = (end_x - start_x)/5
    find_x = start_x
    ix = [start_x]

    for i in range(5):
        find_x += dividedpart
        ix.append(find_x)

    iy = [i for i in range(start_y, end_y, step)]

    x = []
    for pointx in range(len(ix)):
        for pointy in range(len(iy)):
            x.append(ix[pointx])
    
    y = []
    for point in ix:    
        y += iy

    return x, y


def main_hover(sub1, text):
    global visits, maxvisittime, dweltime, gazedur, familiarity_fv, familiarity_all
    global fig, ax, scatter

    fig, ax = plt.subplots(figsize=(10, 9.5))
    movefigure(fig, 500, 10)


    fig.suptitle("sub = " + str(sub1) , x = 0.1, y = 0.95, fontsize=10)
    plt.axis('off')

    path1 = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + '1/py/Slide1.png'
    img = plt.imread(path1)
    ax.imshow(img)

    path = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + '1/py/bubbledata.xlsx'
    bubbledata = pd.read_excel(path)

    visits = read_column(bubbledata, "visits")
    gazedur = read_column(bubbledata, "gazedur")
    maxvisittime = read_column(bubbledata, "maxvisittime")
    dweltime = read_column(bubbledata, "dweltime")
    familiarity_all = read_column(bubbledata, 'familiarity_all')
    familiarity_fv = read_column(bubbledata, 'familiarity_fv')
    

    # Step 1. Create Annotation Object
    global annotation
    annotation = ax.annotate(
        text='',
        xy=(0, 0),
        xytext=(15, 15), # distance from x, y
        textcoords='offset points',
        bbox={'boxstyle': 'round', 'fc': 'w'},
        arrowprops={'arrowstyle': '->'}
    )
    annotation.set_visible(False)

    fig.canvas.mpl_connect('motion_notify_event', motion_hover)

    # Step 2. Create a scatter chart
    global wordno, scatter
    scatter = []

    global lines, data
    data = pd.read_excel(folder1 + 'texts/' + text + textends + '_hover/py/ROIbounds/mytext.page_1.ROIbounds.xlsx')
    lines = data.iloc[:,0]
    lines = lines.to_list()

    for wordno in range(len(lines)):
        start_x, start_y, end_x, end_y = define_points(wordno)
        x, y = choose_points(start_x, start_y, end_x, end_y)

        # colors = np.random.randint(1, 5, size=len(x))
        # norm = plt.Normalize(1, 4)
        # cmap = plt.cm.PiYG

        scatter.append( plt.scatter(
            x=x,
            y=y,
            # c=colors,
            alpha=0,
            s=3,
            # cmap=cmap,
            # norm=norm
        ) )



# Step 3. Implement the hover event to display annotations
def motion_hover(event):
    wordno = None

    if(event.xdata is not None):
        for wo in range(len(lines)):
            start_x, start_y, end_x, end_y = define_points(wo)
            if(start_x <= event.xdata <= end_x  and  start_y <= event.ydata <= end_y ):
                wordno = wo

    annotation_visbility = annotation.get_visible()

    if(wordno is not None):
        if event.inaxes == ax:
            is_contained, annotation_index = scatter[wordno].contains(event)
            if is_contained:
                data_point_location = scatter[wordno].get_offsets()[annotation_index['ind'][0]]
                annotation.xy = data_point_location

                # set text
                text_label = "visits: " + str(visits[wordno]) + "\n" + \
                             "gazedur: " + str(gazedur[wordno]) + "\n" + \
                             "maxvisittime: " + str(maxvisittime[wordno]) + "\n" + \
                             "dweltime: " + str(dweltime[wordno]) + "\n" + \
                             "familiarity_all: " + str(familiarity_all[wordno]) + "\n" + \
                             "familiarity_fv: " + str(familiarity_fv[wordno])


                annotation.set_text(text_label)

                annotation.get_bbox_patch().set_facecolor('pink')
                annotation.set_alpha(1)

                annotation.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if annotation_visbility:
                    annotation.set_visible(False)
                    fig.canvas.draw_idle()

    if(wordno is None):
        annotation.set_visible(False)
        fig.canvas.draw_idle()       
    




def read_colors(sub1, text):
    colorpath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + '1/py/color_triplet_gaze_duration.mat'
    colorpalette = scipy.io.loadmat(colorpath, simplify_cells=True)

    colorpalette = colorpalette['color_triplet_final']
    colorpalette = [list(colorpalette[i]) for i in range(len(colorpalette))]

    for i in range(len(colorpalette)):
        for j in range(len(colorpalette[i])):
            colorpalette[i][j] = int(colorpalette[i][j])/255
        colorpalette[i] = tuple(colorpalette[i])
    
    return colorpalette


def main():
    if( guiflag ):
        textcheckedflag = 1
        subs = NULL
        while( subs==NULL ):
            subs, texts, firstchoices = basic_function_gui(textcheckedflag)
            bypass, hardcases, onlylefteye, onlyrighteye = firstchoices[0], firstchoices[1], firstchoices[2], firstchoices[3]
    
    else:
        subs = [13001]
        texts=['visit']
        bypass = 0
        hardcases = 0
        onlylefteye = 0
        onlyrighteye = 0
        firstchoices = [bypass, hardcases, onlylefteye, onlyrighteye]

    
    for sub in subs:
        sub = int(sub)
        for text in texts:
            run = check_indiv_structure(sub, text)
            if(run==NULL):
                continue
            
            # Create Colored Text, accornig to sub's reading
            colors = read_colors(sub, text)
            main_textplot(sub, text, colors)
            plt.close('all')

            # Create annotations into colored text
            main_hover(sub, text)

            # Zoom text
            x_column = data.iloc[:, 0].tolist()
            y_column = data.iloc[:, 1].tolist()
            width_column = data.iloc[:, 2].tolist()
            height_column = data.iloc[:, 3].tolist()
            zoomimage(x_column, y_column, width_column, height_column)

            # Insert colorbar to plot
            colorbar(fig, ax)

            # Save again the plot zoomed
            photopath = folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + '1/py/Slide1.png'
            plt.savefig(photopath)
            plt.tight_layout(pad=3.3)
            plt.show()


main()

# main_hover(1480, 'island')
# zoomimage()
# plt.show()

