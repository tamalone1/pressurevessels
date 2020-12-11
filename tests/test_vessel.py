# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 tamalone1
"""

import unittest
from pressurevessels.PressureVessels import Vessel
from pressurevessels import conversions

class Test_Vessel(unittest.TestCase):

    def setUp(self):
        self.defaultvalues = (15, 0, 1.695, 1.460, 120)
        self.test_vessel = Vessel(*self.defaultvalues)

    def test_vonmises(self):
        vm = self.test_vessel._vonmises
        self.assertEqual(vm(80,80,0), 80)
        self.assertEqual(vm(80,-80,80), 160)

    def test_defaultvessel(self):
        self.assertAlmostEqual(self.test_vessel.maxstress, 100.676, 3)
        self.assertAlmostEqual(self.test_vessel.averagestress, 87.685, 3)
    
    def test_externalcheck(self):
        self.assertTrue(self.test_vessel.external)

    def test_modify_parameters(self):
        # Check initial value
        self.assertEqual(self.test_vessel.pExt, 15)
        # Take note of the current safety factor
        sf_0 = self.test_vessel.SF_room
        # Change external pressure value
        self.test_vessel.modify_parameters(pExt=20)
        # Take note of the current safety factor
        sf_0 = self.test_vessel.maxstress
        # Check that the value changed
        self.assertEqual(self.test_vessel.pExt, 20)
        # Check that the safety factor decreased
        self.assertLess(self.test_vessel.SF_room, sf_0)

    def test_change_units(self):
        starting_parameters = self.test_vessel.__dict__
        vessel_parameters = [('pExt', 'pressure'),
                        ('pInt', 'pressure'),
                        ('OD', 'length'),
                        ('ID', 'length'),
                        ('yieldstress', 'pressure')]
        if starting_parameters['units'] == 'US':
            # Convert to SI
            self.test_vessel.change_units('SI')
            # Confirm the conversion label happened
            self.assertEqual(self.test_vessel.units, 'SI')
            # Check each vessel parameter was converted properly
            for param_name, unit_type in vessel_parameters:
                    # subTest context identifies which parameter failed
                    with self.subTest(parameter=param_name):
                        starting_value = starting_parameters[param_name]
                        if unit_type == 'length':
                            factor = 25.4   # mm
                        elif unit_type == 'pressure':
                            factor = 0.006895   # MPa
                        # Determine the correct converted value
                        expected_value = starting_value * factor
                        # Actual test statement
                        new_value = self.test_vessel.__dict__[param_name]
                        self.assertAlmostEqual(new_value, expected_value, 3)
                        
        elif starting_parameters['units'] == 'SI':
            # Convert to US
            self.test_vessel.change_units('US')
            # Confirm the conversion label happened
            self.assertEqual(self.test_vessel.units, 'US')
            # Check each vessel parameter was converted properly
            for param_name, unit_type in vessel_parameters:
                    # subTest context identifies which parameter failed
                    with self.subTest(parameter=param_name):
                        starting_value = starting_parameters[param_name]
                        if unit_type == 'length':
                            factor = 1/25.4   # mm
                        elif unit_type == 'pressure':
                            factor = 1/0.006895   # MPa
                        # Determine the correct converted value
                        expected_value = starting_value * factor
                        # Actual test statement
                        new_value = self.test_vessel.__dict__[param_name]
                        self.assertAlmostEqual(new_value, expected_value, 3)

if __name__ == '__main__':
    unittest.main()
