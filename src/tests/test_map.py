'''
Created on Nov 14, 2010

@author: pekka
'''
import unittest
from shallowspace.map import Sector
from shallowspace.constants import *

class SectorTests(unittest.TestCase):

    def testNumberOfNeighbors(self):
        s = Sector()
        self.assertEqual(len(s.neighbors), 4)
        
    def testInitialNeighbors(self):
        s = Sector()
        self.assertFalse(s.move_possible(DIRECTION_UP))
        self.assertFalse(s.move_possible(DIRECTION_RIGHT))
        self.assertFalse(s.move_possible(DIRECTION_DOWN))
        self.assertFalse(s.move_possible(DIRECTION_LEFT))
        
def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(SectorTests)
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
