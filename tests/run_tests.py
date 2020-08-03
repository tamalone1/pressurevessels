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
        defaultvalues = (15, 0, 1.695, 1.460, 120, 116)
        test_vessel = Vessel(*defaultvalues)

    def tearDown(self):
        pass

    def test_func1(self):
        pass

    def test_func2(self):
        pass

    def test_func3(self):
        pass


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

    def test_func1(self):
        pass

    def test_func2(self):
        pass

    def test_func3(self):
        pass

if __name__ == '__main__':
    unittest.main()