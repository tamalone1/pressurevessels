# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 tamalone1

A collection of conversion factors for the units supported in the Vessel class.

"""
US = {'pressure': {'name': 'psi',
                   'factor': 0.006895},
      'length': {'name': 'in',
                 'factor': 25.4}}

SI = {'pressure': {'name': 'MPa',
                   'factor': 1/25.4},
      'length': {'name': 'mm',
                 'factor': 1/0.006895}}

other = {'inch': ('mm', 25.4), 'psi': ('MPa', 0.006895)}

otherSI = {'mm': ('inch', 1/25.4),
      'MPa': ('psi', 1/0.0068947)}

# Data descriptor object
class VesselParameter:
    ''' A physical parameter with units describing a pressure vessel.
    '''

    def __init__(self, unit_type):
        self.unit_type = unit_type

    def __set_name__(self, obj, name):
        # stores the name assigned to this object in the owning object
        # i.e. attribute from obj.attribute
        self.name = name

    def __get__(self, obj, objtype):
        # Gets the value from the owner's dictionary directly
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        # Sets the value in the owner's dictionary directly
        obj.__dict__[self.name] = value
