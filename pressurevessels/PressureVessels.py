# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 tamalone1
"""

import math
import numpy as np

# Pressure vessel class to handle calculations
class Vessel():
    '''A class to keep together the design parameters and the analysis methods

    '''
    def __init__(self, pExt, pInt, OD, ID, yieldstress, deratedyieldstress):
        ''' Set the vessel's design parameters, and calculate the stresses,
        safetyfactors, and pressure ratings'''
        # Design parameters (inputs)
        self.pExt = pExt
        self.pInt = pInt
        self.OD = OD
        self.ID = ID
        self.yieldstress = yieldstress
        self.deratedyieldstress = deratedyieldstress

        # Set a flag if the net pressure is external
        if self.pExt > self.pInt:
            self.external = True
        else:
            self.external = False
        # Call all of the calculation methods
        self.calculate()

    def _principalstressINT(self):
        """ Calculate the principal stresses on the internal surface."""
        OD, ID, pInt, pExt = self.OD, self.ID, self.pInt, self.pExt
        hoop = pInt*(OD**2+ID**2)/(OD**2-ID**2) - 2*pExt*(OD**2)/(OD**2-ID**2)
        axial = pInt*(ID**2)/(OD**2-ID**2) - pExt*(OD**2)/(OD**2-ID**2)
        radial = -pInt
        return hoop, axial, radial

    def _principalstressEXT(self):
        """ Calculate the principal stresses on the external surface."""
        OD, ID, pInt, pExt = self.OD, self.ID, self.pInt, self.pExt
        hoop = 2*pInt*(ID**2)/(OD**2-ID**2) - pExt*(OD**2+ID**2)/(OD**2-ID**2)
        axial = pInt*(ID**2)/(OD**2-ID**2) - pExt*(OD**2)/(OD**2-ID**2)
        radial = -pExt
        return hoop, axial, radial

    def _vonmises(self, s1, s2, s3):
        """ Calculate von Mises stress given 3 principal stresses."""
        vm = math.sqrt(0.5 * ((s1 - s2)**2 + (s2 - s3)**2 + (s3 - s1)**2))
        return vm

    def _safetyfactor(self, value, allowable):
        """ Calculate the safety factor, compared to the allowable value."""
        return allowable / value

    def calculate(self):
        ''' Update the stresses, safety factors, and pressure ratings.'''
        self.get_stresses()
        self.get_safetyfactors()
        self.get_maxpressures()

    def get_stresses(self):
        # Calculate the von Mises stress on the outer and inner surfaces

        vmExt = self._vonmises(*self._principalstressEXT())
        vmInt = self._vonmises(*self._principalstressINT())
        maxstress = max(vmExt, vmInt)
        averagestress = (vmExt + vmInt) / 2

        # Store the relevant results for later
        self.maxstress = maxstress
        self.averagestress = averagestress

    def get_safetyfactors(self):
        '''Calculate the minimum safety factors for internal and external pressure
        Compare average stress to adjusted yield stress, where the adjustment
        factor is 2/3 for internal pressure or 4/5 for external pressure'''
        if self.external:
            self.k = 0.80
        else:
            self.k = 0.666666

        maxstress = self.maxstress
        averagestress = self.averagestress
        yieldstress = self.yieldstress
        deratedyieldstress = self.deratedyieldstress
        self.SF_room = min(self._safetyfactor(maxstress, yieldstress),
                                    self._safetyfactor(averagestress, yieldstress*self.k))
        self.SF_derated = min(self._safetyfactor(maxstress, deratedyieldstress),
                                       self._safetyfactor(averagestress, deratedyieldstress*self.k))

    def get_maxpressures(self):
        '''Calculate the maximum pressures.

        Multiply the differential pressure by the minimum safety factor (for
        external and internal), and add the result external pressure (internal
        case) and subtract from the internal pressure (external case).'''
        differentialpressure = abs(self.pExt - self.pInt)
        self.maxExtroom = self.SF_room * differentialpressure
        self.maxIntroom = self.SF_room * differentialpressure
        self.maxExtderated = self.SF_derated * differentialpressure
        self.maxIntderated = self.SF_derated * differentialpressure

    def modify_parameters(self, *, pExt=None, pInt=None, OD=None, ID=None,
                          yieldstress=None, deratedyieldstress=None):
        '''Change any of the parameters, and recalculate everything'''
        # For each keyword argument, if a new value is not passed, use the old
        # value:
        if pExt is None:
            pExt = self.pExt
        if pInt is None:
            pInt = self.pInt
        if OD is None:
            OD = self.OD
        if ID is None:
            ID = self.ID
        if yieldstress is None:
            yieldstress = self.yieldstress
        if deratedyieldstress is None:
            deratedyieldstress = self.deratedyieldstress

        # Call the init function again with the modified parameters included
        self.__init__(pExt, pInt, OD, ID, yieldstress, deratedyieldstress)
