Use this code to calculate the stresses in cylindrical pressure vessels. A calculator class, `PressureVessel`, and a GUI class, `PV_GUI`, are provided.
Given the dimensions of the pressure vessel, the material strength, and the applied pressure, the von Mises stresses in the wall are calculated. A safety factor is determined using both the maximum von Mises stress and the average stress between the inner and outer wall surface. The average stress is limited to a smaller proportion of the maximum allowable stress, which requires that vessels with thinner walls have larger margins of safety.

# Dependencies
* numpy
* tkinter
* matplotlib (used in incomplete features)

# Usage
For direct use of the `pressurevessel` class, you can import the class:
```python
from pressurevessels import PressureVessel
```
To use the GUI from tkinter, import the module and create:
```python
root = tk.Tk()
root.title('Pressure Vessels')
PV_GUI(root).grid(row=0, column=0, padx=2, pady=2)
root.mainloop()
```

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

# License
[MIT](https://choosealicense.com/licenses/mit/)
