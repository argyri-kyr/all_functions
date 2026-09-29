

import tkinter as tk
from tkinter import filedialog
import os


# -------- Globals -------- #
path_value = None
id_start_value = None
id_end_value = None
dob_value = None

path_entry = None
id_start_entry = None
id_end_entry = None
dob_entry = None
root = None


def browse_path():
    folder = filedialog.askdirectory()
    if folder:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder)


def load_last_path():
    pathfile = os.path.join(os.path.dirname(__file__), 'last_used_path.txt')
    if os.path.exists(pathfile):
        try:
            with open(pathfile, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except:
            return ""
    return ""


def submit():
    global path_value, id_start_value, id_end_value, dob_value
    path_value = path_entry.get().strip()
    id_start_value = id_start_entry.get().strip()
    id_end_value = id_end_entry.get().strip()
    dob_value = dob_entry.get().strip()
    root.destroy()


def move_focus(event):
    widgets = [path_entry, id_start_entry, id_end_entry, dob_entry]
    current = root.focus_get()

    if current not in widgets:
        return

    idx = widgets.index(current)

    if event.keysym == "Down":
        next_idx = (idx + 1) % len(widgets)
    elif event.keysym == "Up":
        next_idx = (idx - 1) % len(widgets)
    else:
        return

    widgets[next_idx].focus_set()


def placeholder_focus_in(entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def placeholder_focus_out(entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg="gray")



def gui_for_profiles():
    global root, path_entry, id_start_entry, id_end_entry, dob_entry

    # ---------------- GUI ---------------- #
    root = tk.Tk()
    root.title("Input Form")
    root.geometry("520x240")

    # Path
    tk.Label(root, text="Path:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    path_entry = tk.Entry(root, width=45)
    path_entry.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=browse_path).grid(row=0, column=2, padx=5)

    # ID Start
    tk.Label(root, text="ID Start:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    id_start_entry = tk.Entry(root, width=20)
    id_start_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # ID End
    tk.Label(root, text="ID End:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    id_end_entry = tk.Entry(root, width=20)
    id_end_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # DOB 
    tk.Label(root, text="DOB:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    dob_entry = tk.Entry(root, width=20)
    dob_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    placeholder = "YYYY-MM-DD"
    dob_entry.insert(0, placeholder)
    dob_entry.config(fg="gray")
    dob_entry.bind("<FocusIn>", lambda e: placeholder_focus_in(dob_entry, placeholder))
    dob_entry.bind("<FocusOut>", lambda e: placeholder_focus_out(dob_entry, placeholder))

    # Load default path if file exists
    last_path = load_last_path()
    if last_path:
        path_entry.insert(0, last_path)
        id_start_entry.focus_set()   # cursor goes to ID Start, if path exists
    else:
        path_entry.focus_set()       # cursor goes to Path, if path not exists


    # Submit Button
    tk.Button(root, text="Submit", width=20, height=2, command=submit).grid(row=4, column=1, pady=25)
    
    root.bind('<Return>', lambda event: submit())
    root.bind("<Down>", move_focus)
    root.bind("<Up>", move_focus)

    root.mainloop()

    return path_value, id_start_value, id_end_value, dob_value
