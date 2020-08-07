## Pressure Vessel stress calculator

Use this code to calculate the stresses in cylindrical pressure vessels. A calculator class, `Vessel`, and a GUI class, `PV_GUI`, are provided.

Given the dimensions of the pressure vessel, the material strength, and the applied pressure, the von Mises stresses in the wall are calculated. A safety factor is determined using both the maximum von Mises stress and the average stress between the inner and outer wall surface. The average stress is limited to a smaller proportion of the maximum allowable stress, which requires that vessels with thinner walls have larger margins of safety.
___
## Getting Started

### Prerequisites

* tkinter (included in Python Standard Library)

___
## Usage
For direct use of the `Vessel` class, you can import the module:
```python
import pressurevessels
```
and create a `Vessel` instance:
```python
v = Vessel(pExt, pInt, OD, ID, yieldstress, deratedyieldstress)
```

To use the GUI from tkinter, you can execute the module with 
`python -m pressurevessels`
___
## Roadmap
* Unit conversions (US and SI)
* Optimizing the wall thickness to minimize material
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
