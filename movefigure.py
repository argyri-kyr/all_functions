import matplotlib

def movefigure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend().lower()  # normalize to lowercase
    if 'tkagg' in backend:
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif 'wxagg' in backend:
        f.canvas.manager.window.SetPosition((x, y))
    elif hasattr(f.canvas.manager.window, 'move'):
        # Qt and GTK
        f.canvas.manager.window.move(x, y)
    elif hasattr(f.canvas.manager.window, 'wm_geometry'):
        # Fallback for Tk-like backends not caught above
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    else:
        print(f"movefigure: unsupported backend '{backend}', skipping window move")