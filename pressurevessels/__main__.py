# make the module executable
# at which point, the GUI version is run
import tkinter as tk
from .gui import PV_GUI

root = tk.Tk()
root.title('Pressure Vessels')
PV_GUI(root).grid(row=0, column=0, padx=2, pady=2)
root.mainloop()