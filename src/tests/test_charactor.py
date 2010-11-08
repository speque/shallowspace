'''
Created on Oct 31, 2010

@author: pekka
'''
import unittest
import shallowSpace.constants
from eventTester import EventTester   
from shallowSpace.actors import Charactor
from shallowSpace.eventManager import EventManager
from shallowSpace.game import Game

class BasicTests(unittest.TestCase):

    def setUp(self):
        em = EventManager()
        self.eventManager = em
        self.game = Game(em)
        self.eventTester = EventTester()


    def tearDown(self):
        pass


    def testMove(self):
        c = Charactor(self.eventManager)
        map = self.game.map
        map.Build()
        c.Place(map.sectors[map.startSectorIndex])
        c.Move(shallowSpace.constants.DIRECTION_RIGHT)
        
        c.Move(shallowSpace.constants.DIRECTION_DOWN) 
        c.Move(shallowSpace.constants.DIRECTION_LEFT) 
        c.Move(shallowSpace.constants.DIRECTION_UP) 
        sec = map.sectors[map.startSectorIndex]
        newSec = c.sector
        self.assertEqual(map.sectors.index(sec), map.sectors.index(newSec))

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(BasicTests)
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
