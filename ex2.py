


import matplotlib.pyplot as plt
# import tkinter as tk
# from matplotlib.patches import Rectangle
# from matplotlib.widgets import RectangleSelector
# import numpy as np

# from movefigure import movefigure


# def main_plot():
#     global fig, ax, x, y, totalclicks, rect_selector
#     fig, ax = plt.subplots()
#     fig.set_size_inches(8, 5)
#     movefigure(fig, 350, 280)
    
    
    
#     totalclicks = 0
    
#     # Initialize the RectangleSelector object outside of the main_plot() function
#     rect_selector = RectangleSelector(
#         ax, line_select_callback, useblit=True, button=[1], interactive=True)


#     fig.canvas.mpl_connect('key_press_event', on_key_press)
        
        
#     x = [1, 2, 3, 4, 5, 8, 10, 12, 6, 14]
#     y = [2, 4, 6, 8, 10, 2, 5, 10, 6, 7]
    
    
#     ax.scatter(x, y)
#     ax.set_xlim(0, 15)
#     ax.set_ylim(0, 20)
#     plt.show()
    


# def on_key_press(event):
#     if event.key == 'enter':
#         x_value = 0
#         y_value = 2
#         xstart = float(x1)
#         xend = float(x2)
#         ystart = float(y1)
#         yend = float(y2)
        
#         for i in range(len(x)):
#             if( xstart<=x[i]<=xend  and  ystart<=y[i]<=yend ):
#                 x[i] += x_value
#                 y[i] += y_value

#         # Clean and Update the plot
#         ax.clear()
#         ax.set_xlim(0, 15)
#         ax.set_ylim(0, 20)
#         ax.scatter(x, y)
#         fig.canvas.draw()
 

            
        

# def line_select_callback(eclick, erelease):
#     global x1,x2,y1,y2
#     x1, y1 = eclick.xdata, eclick.ydata
#     x2, y2 = erelease.xdata, erelease.ydata
#     print("\n\nx1 = ", x1)
#     print("x2 = ", x2)
#     print("y1 = ", y1)
#     print("y2 = ", y2)
#     return x1,y1,x2,y2


# def main():
#     main_plot()

# main()
 
 
# ###################################################################


# import matplotlib.pyplot as plt
# import tkinter as tk
# from matplotlib.patches import Rectangle
# from matplotlib.widgets import RectangleSelector
# import numpy as np

# from movefigure import movefigure


# def clear_entry_fields():
#     x_entry.delete(0, tk.END)
#     y_entry.delete(0, tk.END)
#     xstart_entry.delete(0, tk.END)
#     xend_entry.delete(0, tk.END)
#     ystart_entry.delete(0, tk.END)
#     yend_entry.delete(0, tk.END)
    

# def update_plot(x, y, x_value, y_value, xstart, xend, ystart, yend):
#     ext = (0,0,0,0)
#     rect_selector.draw_shape(ext)
#     rect_selector.set_visible(False)
    
#     clear_entry_fields()
    
#     if(x_value==""):
#         x_value = 0
        
#     if(y_value==""):
#         y_value = 0
        
        
#     x_value = float(x_value)
#     y_value = float(y_value)
#     xstart = float(xstart)
#     xend = float(xend)
#     ystart = float(ystart)
#     yend = float(yend)
    
#     for i in range(len(x)):
#         if( xstart<=x[i]<=xend  and  ystart<=y[i]<=yend ):
#             x[i] += x_value
#             y[i] += y_value

#     # Clean and Update the plot
#     ax.clear()
#     ax.set_xlim(0, 15)
#     ax.set_ylim(0, 20)
#     ax.scatter(x, y)
#     fig.canvas.draw()
#     rect_selector.set_visible(True)
    


# def main_plot():
#     global fig, ax,  rect_selector
#     fig, ax = plt.subplots()
#     fig.set_size_inches(8, 5)
#     movefigure(fig, 350, 280)
    
    
#     # Initialize the RectangleSelector object outside of the main_plot() function
#     rect_selector = RectangleSelector(
#         ax, line_select_callback, useblit=True, drawtype='box', button=[1], interactive=True)


#     fig.canvas.mpl_connect('key_press_event', on_key_press)
        
        
#     x = [1, 2, 3, 4, 5, 8, 10, 12, 6, 14]
#     y = [2, 4, 6, 8, 10, 2, 5, 10, 6, 7]
    
    
#     ax.scatter(x, y)
#     ax.set_xlim(0, 15)
#     ax.set_ylim(0, 20)
#     plt.show()



# def line_select_callback(eclick, erelease):
#     global x1,x2,y1,y2
#     x1, y1 = eclick.xdata, eclick.ydata
#     x2, y2 = erelease.xdata, erelease.ydata
#     print("\n\nx1 = ", x1)
#     print("x2 = ", x2)
#     print("y1 = ", y1)
#     print("y2 = ", y2)
#     return x1,y1,x2,y2





# def main_win(xtemp, ytemp):
#     global root, x_entry, y_entry, xstart_entry, xend_entry, ystart_entry, yend_entry
    
#     root = tk.Tk()
#     root.resizable(True, True)
    
#     w = 300                            # my width
#     h = 450                            # my height
#     ws = root.winfo_screenwidth()      # width of the screen
#     hs = root.winfo_screenheight()     # height of the screen
#     x = (ws/2) - (w/2) + 380
#     y = (hs/2) - (h/2)
#     root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    
#     # x-shift
#     label = tk.Label(root, text="Enter a value to move x:")
#     label.pack(pady = (10,0))

#     x_entry = tk.Entry(root)
#     x_entry.pack(pady = (0,5))
    
#     # y-shift
#     label = tk.Label(root, text="Enter a value to move y:")
#     label.pack(pady = (5,0))
    
#     y_entry = tk.Entry(root)
#     y_entry.pack(pady = (0,5))

#     # select rectangle xstart
#     label = tk.Label(root, text="Enter xstart")
#     label.pack(pady = (5,0))
    
#     xstart_entry = tk.Entry(root)
#     xstart_entry.pack(pady = (0,5))
    
#     # select rectangle xend
#     label = tk.Label(root, text="Enter xend")
#     label.pack(pady = (5,0))
    
#     xend_entry = tk.Entry(root)
#     xend_entry.pack(pady = (0,5))

#     # select rectangle ystart
#     label = tk.Label(root, text="Enter ystart")
#     label.pack(pady = (5,0))
    
#     ystart_entry = tk.Entry(root)
#     ystart_entry.pack(pady = (0,5))
    
#     # select rectangle yend
#     label = tk.Label(root, text="Enter yend")
#     label.pack(pady = (5,0))
    
#     yend_entry = tk.Entry(root)
#     yend_entry.pack(pady = (0,5))



#     # Pack the update button into the tkinter frame
#     button = tk.Button(root, text="Update plot", command=lambda: update_plot(xtemp, ytemp, x_entry.get(), y_entry.get(), xstart_entry.get(), xend_entry.get(), ystart_entry.get(), yend_entry.get()))
#     button.pack(pady = (10,5))
    


# def on_key_press(event):
#     if event.key == 'enter':
#         # Enter the click x index into the x_entry entry field
#         xstart_entry.delete(0, tk.END)
#         xstart_entry.insert(0, str(x1))


#         # Enter the click y index into the y_entry entry field
#         ystart_entry.delete(0, tk.END)
#         ystart_entry.insert(0, str(y1))
    
#         # Enter the click x index into the x_entry entry field
#         xend_entry.delete(0, tk.END)
#         xend_entry.insert(0, str(x2))


#         # Enter the click y index into the y_entry entry field
#         yend_entry.delete(0, tk.END)
#         yend_entry.insert(0, str(y2))
            
    
    
    
# def main():
#     x,y = main_plot()
#     main_win(x, y)
#     root.mainloop()



# main()

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
    
x_axis_points = [1, 2, 3, 1, 2, 3]
y_axis_points = [1, 2, 3, 4, 5, 6]

# Create a custom tick locator
tick_locator = mticker.MultipleLocator(base=1.0)

# Set the x-axis ticks explicitly
plt.xticks(ticks=tick_locator.get_locator().tick_values())

# Plot the points using the scatter() function
plt.scatter(x_axis_points, y_axis_points)

# Add axis labels and title
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.title("My Plot")

# Show the plot
plt.show()