import tkinter as tk
from PIL import ImageGrab
from pathlib import Path

def Screenshot(filename: str):
    coords = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}
    
    snip = tk.Tk()
    snip.attributes("-fullscreen", True)
    snip.attributes("-alpha", 0.5)
    snip.attributes("-topmost", True)
    snip.configure(bg="black")
    
    canvas = tk.Canvas(snip, cursor="cross", bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)
    rect = None
    
    def onpress(event):
        nonlocal rect
        
        coords["x1"] = event.x_root
        coords["y1"] = event.y_root
        
        rect = canvas.create_rectangle(coords["x1"], coords["y1"], coords["x1"], coords["y1"], outline="red", width=2)
        
    def ondrag(event):
        canvas.coords(rect, coords["x1"], coords["y1"], event.x_root, event.y_root)
        
    def onrelease(event):
        coords["x2"] = event.x_root
        coords["y2"] = event.y_root
        snip.destroy()
    
    canvas.bind("<ButtonPress-1>", onpress)
    canvas.bind("<B1-Motion>", ondrag)
    canvas.bind("<ButtonRelease-1>", onrelease)
    
    snip.grab_set()
    snip.wait_window()
    
    x1 = min(coords["x1"], coords["x2"])
    y1 = min(coords["y1"], coords["y2"])
    x2 = max(coords["x1"], coords["x2"])
    y2 = max(coords["y1"], coords["y2"])
    
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img.save(Path.cwd() / filename)