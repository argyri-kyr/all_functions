

import tkinter as tk
import matplotlib.pyplot as plt


from globalVars import folder1, textends


def totalshift_askbox(text, pageno, setmycollections_ref, getParam_ref):
    global root, x_entry, y_entry, xstart_entry, xend_entry, ystart_entry, yend_entry
    
    root = tk.Tk()
    root.resizable(True, True)
    
    w = 300                            # my width
    h = 500                            # my height
    ws = root.winfo_screenwidth()      # width of the screen
    hs = root.winfo_screenheight()     # height of the screen
    x = (ws/2) - (w/2) + 520
    y = (hs/2) - (h/2) - 80
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    
    # x-shift
    label = tk.Label(root, text="Enter a value to move x:")
    label.pack(pady = (10,0))

    x_entry = tk.Entry(root)
    x_entry.pack(pady = (0,5))
    
    # y-shift
    label = tk.Label(root, text="Enter a value to move y:")
    label.pack(pady = (5,0))
    
    y_entry = tk.Entry(root)
    y_entry.pack(pady = (0,5))

    # select rectangle xstart
    label = tk.Label(root, text="Enter xstart")
    label.pack(pady = (5,0))
    
    xstart_entry = tk.Entry(root)
    xstart_entry.pack(pady = (0,5))
    
    # select rectangle xend
    label = tk.Label(root, text="Enter xend")
    label.pack(pady = (5,0))
    
    xend_entry = tk.Entry(root)
    xend_entry.pack(pady = (0,5))

    # select rectangle ystart
    label = tk.Label(root, text="Enter ystart")
    label.pack(pady = (5,0))
    
    ystart_entry = tk.Entry(root)
    ystart_entry.pack(pady = (0,5))
    
    # select rectangle yend
    label = tk.Label(root, text="Enter yend")
    label.pack(pady = (5,0))
    
    yend_entry = tk.Entry(root)
    yend_entry.pack(pady = (0,5))
    

    # Pack the update button into the tkinter frame
    button = tk.Button(root, text="Update plot", command=lambda: update_plot(text, pageno, x_entry.get(), y_entry.get(), xstart_entry.get(), xend_entry.get(), ystart_entry.get(), yend_entry.get(), setmycollections_ref, getParam_ref))
    button.pack(pady = (15,5))
    
    # Pack the update button into the tkinter frame
    button = tk.Button(root, text="Next", command=lambda: nextPage(getParam_ref))
    button.pack(pady = (10,5))   
    
    return  root, xstart_entry, ystart_entry, xend_entry, yend_entry




def clear_entry_fields():
    x_entry.delete(0, tk.END)
    y_entry.delete(0, tk.END)
    xstart_entry.delete(0, tk.END)
    xend_entry.delete(0, tk.END)
    ystart_entry.delete(0, tk.END)
    yend_entry.delete(0, tk.END)




def update_plot(text, pageno, x_value, y_value, xstart, xend, ystart, yend, setmycollections_ref, getParam_ref):
    # ext = (0,0,0,0)
    # getParam_ref("rect_selector").draw_shape(ext)
    # getParam_ref("rect_selector").set_visible(False)
    
    
    x, y = getParam_ref("mypagecollection")[1], getParam_ref("mypagecollection")[2]
    
    clear_entry_fields()
    
    if(x_value==""):
        x_value = 0
        
    if(y_value==""):
        y_value = 0
        
        
    x_value = float(x_value)
    y_value = float(y_value)
    xstart = float(xstart)
    xend = float(xend)
    ystart = float(ystart)
    yend = float(yend)
    
    for i in range(len(x)):
        if( xstart<=x[i]<=xend  and  ystart<=y[i]<=yend ):
            x[i] += x_value
            y[i] += y_value

    setmycollections_ref(x, 1)
    setmycollections_ref(y, 2)
    
    # Clean and Update the plot
    getParam_ref("ax").clear()
    
    image = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
    getParam_ref("ax").margins(x=0)
    plt.title("Test Attention - Gazes Preview\n")
    
    getParam_ref("ax").scatter(x, y, marker='x')
    getParam_ref("ax").imshow(img)
    plt.axis('off')
    
    getParam_ref("fig").canvas.draw()
    # getParam_ref("rect_selector").set_visible(True)



def nextPage(getParam_ref):
    plt.close('all')
    root.destroy()



