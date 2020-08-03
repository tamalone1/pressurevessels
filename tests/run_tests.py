# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 tamalone1
"""

import unittest
from pressurevessels.PressureVessels import Vessel

class Test_Vessel(unittest.TestCase):
    ''' Subclass of TestCase, which is executed by unittest.main

    Each test is a method with a name starting with 'test'.
    The setUp method is run prior to each test.
    The tearDown method is run after each test.
    '''

    def setUp(self):
        self.defaultvalues = (15, 0, 1.695, 1.460, 120, 116)
        self.test_vessel = Vessel(*self.defaultvalues)

    def tearDown(self):
        pass

    def test_vonmises(self):
        vm = self.test_vessel._vonmises
        self.assertEqual(vm(80,80,0), 80)
        self.assertEqual(vm(80,-80,80), 160)


class Test_GUI(unittest.TestCase):
    ''' Subclass of TestCase, which is executed by unittest.main

    Each test is a method with a name starting with 'test'.
    The setUp method is run prior to each test.
    The tearDown method is run after each test.
    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()