

from asyncio.windows_events import NULL
import matplotlib.pyplot as plt
from matplotlib import transforms


from globalVars import folder1, folder2, textends
from findROIbounds import main
from make_hover_file import make_hover_file


def rainbow_text(x,y,ls,lc,**kw):
    """
    Take a list of strings ``ls`` and colors ``lc`` and place them next to each
    other, with text ls[i] being shown in color lc[i].

    This example shows how to do both vertical and horizontal text, and will
    pass all keyword arguments to plt.text, so you can set the font size,
    family, etc.
    """

    t = plt.gca().transData
    fig = plt.gcf()

    space_between_words = 20

    #horizontal version
    for s,c in zip(ls,lc):
        text = plt.text(x,y,s+" ",color=c, transform=t, **kw)
        text.draw(fig.canvas.get_renderer())
        ex = text.get_window_extent()
        t = transforms.offset_copy(text._transform, x=ex.width+space_between_words, units='dots')



def plotrainbow(text, colors, photopath):
    global f, ax
    f, ax = plt.subplots(figsize=(10, 9.5))
    plt.rcParams["figure.figsize"] = [10, 9.5] #[12, 9.5]
    

    # plot 2
    make_hover_file(text)

    # find true lines
    textpath = folder1 + 'texts/'+ text + textends + '_hover/alltext_true_lines.txt'
    texts = open(textpath,'r').readlines()[0]
    texts = texts.replace("-|", "\n" )


    """
    plt.text(0.09, 0.5, texts, color="black", fontsize=12, va='center') # plt.text(0.05, 0.5, texts, color="black", fontsize=12, va='center')
    """

    # split text into lines
    stringlines = []
    index = 0
    while(index<len(texts)):
        s=''
        while(index<len(texts) and texts[index]!="\n"):
            s += texts[index]
            index+=1
        index+=1
        stringlines.append(s)
    
    
    countline = 0
    countcolors = 0
    for line in stringlines:
        # choose colors per line
        line_length = len( line[1:].split(" ") )
        start = countcolors
        end = countcolors+line_length
        colorpicker = colors[start:end]

        # call rainbow for each line
        rainbow_text(0, 1.05-countline*0.04, line.split(), colorpicker, size=12)

        # change line increases
        countline += 1
        countcolors += line_length


    plt.axis('off')

    plt.savefig(photopath)  # plt.text(0.05, 0.5, texts, color="black", fontsize=12, va='center', dpi=500)
    
    # plt.show()



def main_textplot(sub1, text, colors):

    if(sub1==NULL):
        photopath = folder1 + 'texts/'+ text + textends + '_hover/Slide1.png'
    
    else:
        photopath = folder1 + folder2 + '/subject_' + str(sub1) + '/all_graphs/' + text + '1/py/Slide1.png'
    

    plotrainbow(text, colors, photopath)


    # Only when I have no subject means that I want to find bounds for text, otherwise bounds have been found
    if(sub1==NULL):
        # text for roi analysis
        text = text+"_1920_hover"
        main(text)

    plt.close('all')


def main_for_texts():
    texts = ['visit', 'zoo', 'island', 'olympia']
    colors = 30 * ['magenta', 'purple', 'red', 'lawngreen', 'lightseagreen', 'royalblue', 'blueviolet']
    
    for text in texts:
        main_textplot(NULL, text, colors)



# main_for_texts()