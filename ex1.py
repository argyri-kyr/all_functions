

# data = pd.read_excel(folder1 + 'texts/' + text + textends + '/py/mytext/allwordspure.xlsx', header=None)
# allwords = []
# allwords = data.iloc[:,0]
# allwords = allwords.to_list()


# import tkinter as tk
# from tkinter import messagebox
# import threading

# def show_warning():
#     messagebox.showwarning("Warning", "This is a warning message")

# def f():
#     for i in range(10):
#         if i == 5:
#             # Open warning window in a separate thread
#             warning_thread = threading.Thread(target=show_warning)
#             warning_thread.start()
#         print(f"Processing iteration {i}")
#     print("Terminate")

# f()


    
import numpy as np

# Define arrays A and B
A = np.array([[1, 2], [3, 4], [5, 6]])
B = np.array([[7, 8], [9, 10], [11, 12]])

# Stack arrays A and B along a new axis
C = np.stack((A, B), axis=1)

print(C)
    

