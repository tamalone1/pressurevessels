# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 tamalone1
"""
import math
# from .conversions import VesselParameter

class Vessel():
    '''A cylindrical vessel subjected to internal and external pressure
    '''
    # pExt = VesselParameter('pressure')
    # pInt = VesselParameter('pressure')
    # OD = VesselParameter('length')
    # ID = VesselParameter('length')
    # yieldstress = VesselParameter('pressure')

    def __init__(self, pExt, pInt, OD, ID, yieldstress):
        ''' Set the vessel's design parameters, and calculate the stresses,
        safety factors, and pressure ratings'''
        self.pExt = pExt
        self.pInt = pInt
        self.OD = OD
        self.ID = ID
        self.yieldstress = yieldstress

        self.units = 'US'

        self._inputs = ('pExt',
                        'pInt',
                        'OD',
                        'ID',
                        'yieldstress')

        # Call all of the calculation methods
        self.calculate()

    def __repr__(self):
        r = [f'{parameter}: {getattr(self, parameter)}' for parameter in self._inputs]
        return '\n'.join(r)

    @staticmethod
    def _principalstressINT(OD, ID, pInt, pExt):
        """ Calculate the principal stresses on the internal surface."""
        hoop = pInt*(OD**2+ID**2)/(OD**2-ID**2) - 2*pExt*(OD**2)/(OD**2-ID**2)
        axial = pInt*(ID**2)/(OD**2-ID**2) - pExt*(OD**2)/(OD**2-ID**2)
        radial = -pInt
        return hoop, axial, radial

    @staticmethod
    def _principalstressEXT(OD, ID, pInt, pExt):
        """ Calculate the principal stresses on the external surface."""
        hoop = 2*pInt*(ID**2)/(OD**2-ID**2) - pExt*(OD**2+ID**2)/(OD**2-ID**2)
        axial = pInt*(ID**2)/(OD**2-ID**2) - pExt*(OD**2)/(OD**2-ID**2)
        radial = -pExt
        return hoop, axial, radial

    @staticmethod
    def _vonmises(s1, s2, s3):
        """ Calculate von Mises stress given 3 principal stresses."""
        vm = math.sqrt(0.5 * ((s1 - s2)**2 + (s2 - s3)**2 + (s3 - s1)**2))
        return vm

    @staticmethod
    def _safetyfactor(value, allowable):
        """ Calculate the safety factor, compared to the allowable value."""
        return allowable / value

    def calculate(self):
        ''' Update the stresses, safety factors, and pressure ratings.'''
        # Set a flag if the net pressure is external
        self.external = (self.pExt > self.pInt)
        self.get_stresses()
        self.get_safetyfactors()
        self.get_maxpressures()

    def get_stresses(self):
        # Calculate the von Mises stress on the outer and inner surfaces

        vmExt = self._vonmises(*self._principalstressEXT(self.OD,
                                                         self.ID,
                                                         self.pInt,
                                                         self.pExt))

        vmInt = self._vonmises(*self._principalstressINT(self.OD,
                                                         self.ID,
                                                         self.pInt,
                                                         self.pExt))
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

        self.SF_room = min(self._safetyfactor(maxstress, yieldstress),
                           self._safetyfactor(averagestress, yieldstress*self.k))

    def get_maxpressures(self):
        '''Calculate the maximum pressures.

        Multiply the differential pressure by the minimum safety factor (for
        external and internal), and add the result external pressure (internal
        case) and subtract from the internal pressure (external case).'''
        differentialpressure = abs(self.pExt - self.pInt)
        self.maxExtroom = self.SF_room * differentialpressure
        self.maxIntroom = self.SF_room * differentialpressure

    def modify_parameters(self, *, pExt=None, pInt=None, OD=None, ID=None,
                          yieldstress=None):
        '''Change any of the parameters, and recalculate everything'''
        # For each keyword argument, if a new value is passed, update the 
        # associated parameter
        if pExt:
            self.pExt = pExt
        if pInt:
            self.pInt = pInt
        if OD:
            self.OD = OD
        if ID:
            self.ID = ID
        if yieldstress:
            self.yieldstress = yieldstress

        # Call all of the calculation methods
        self.calculate()

    def change_units(self, system):
        ''' Convert the vessel parameters to another unit system.'''
        self.units = system

    def _change_with_SF(self, **kwargs):
        ''' Change parameter(s) and return min safety factor. '''
        self.modify_parameters(**kwargs)
        SF = self.SF_room
        return SF

    @staticmethod
    def _barlow_thickness(P_diff, diameter, allowable_stress):
        ''' Estimate the thickness using Barlow's formula.
        
        Barlow's formula is a common method of determining the pressure rating
        for thin-walled pressure vessels, using one of the diameters, the wall
        thickness, and the allowable stress. If the wall is thin, the radial 
        stress is small and can be neglected, so both diameters are not needed.
        '''
        thickness = P_diff * diameter / (2 * allowable_stress)
        return thickness

    def minimize_OD(self):
        ''' Return the smallest OD with safety factor >= 1, all else equal.
        
        The vessel will be updated with this new value automatically.'''
        # Starting value of safety factor
        SF = self.SF_room
        # if the current SF is greater than 1.0, use the current diameters as 
        # brackets for bisection method
        a = self.ID + 0.001
        if SF > 1.0:
            # Use current diameters as the starting range
            b = self.OD
        else:
            # Use Barlow's method to adjust the thickness
            # Estimate the upper bound on the wall thickness using Barlow's formula
            diff_pressure = abs(self.pExt - self.pInt)
            allowable_stress = self.yieldstress
            new_thickness = self._barlow_thickness(diff_pressure, 
                                                   self.ID, 
                                                   allowable_stress)
            new_OD = self.ID + 2*new_thickness                                 
            # Check if Barlow's method gives SF < 1
            new_SF = self._change_with_SF(OD=new_OD)
            if  new_SF > 1.0:
                b = new_OD
            else:
                b = new_OD + 2*new_thickness/new_SF

        # Bisection method: find the optimum point inside a bracketed range
        while abs(b - a) >= 0.00001:
            # Get SF for each value of OD and subtract 1.00
            SF_a = self._change_with_SF(OD=a) - 1.0
            SF_b = self._change_with_SF(OD=b) - 1.0
            midpoint = (a+b)/2
            SF_mid = self._change_with_SF(OD=midpoint) - 1.0
            if SF_a * SF_mid < 0:
                # Change range to these points
                b = midpoint
            else:
                a = midpoint 

    def minimize_ID(self):
        ''' Return the largest ID with safety factor >=1, all else equal.

        The vessel will be updated with this new value automatically.'''
        # Starting value of safety factor
        SF = self.SF_room
        # if the current SF is greater than 1.0, use the current diameters as 
        # brackets for bisection method
        a = self.OD - 0.001
        if SF > 1.0:
            # Use current diameters as the starting range
            b = self.ID
        else:
            # Use Barlow's method to adjust the thickness
            # Estimate the upper bound on the wall thickness using Barlow's formula
            diff_pressure = abs(self.pExt - self.pInt)
            allowable_stress = self.yieldstress
            new_thickness = self._barlow_thickness(diff_pressure, 
                                                   self.OD, 
                                                   allowable_stress)
            new_ID = max(0, self.OD - 2*new_thickness)                                 
            # Check if Barlow's method gives SF < 1
            new_SF = self._change_with_SF(ID=new_ID)
            if  new_SF > 1.0:
                b = new_ID
            else:
                b = new_ID + 2*new_thickness/new_SF

        # Bisection method: find the optimum point inside a bracketed range
        while abs(b - a) >= 0.0001:
            # Get SF for each value of OD and subtract 1.00
            SF_a = self._change_with_SF(ID=a) - 1.0
            SF_b = self._change_with_SF(ID=b) - 1.0
            midpoint = (a+b)/2
            SF_mid = self._change_with_SF(ID=midpoint) - 1.0
            if SF_a * SF_mid < 0:
                # Change range to these points
                b = midpoint
            else:
                a = midpoint 
