'''
Created on Oct 31, 2010

@author: pekka
'''
import unittest
from shallowSpace.actors import Charactor
from shallowSpace.shallowSpace import EventManager
from shallowSpace.game import Game
from shallowSpace.map import Map 

class BasicTests(unittest.TestCase):

    def setUp(self):
        em = EventManager()
        self.eventManager = em
        self.game = Game(em)


    def tearDown(self):
        pass


    def testMove(self):
        c = Charactor(self.eventManager)
        map = self.game.map
        map.Build()
        sec = map.sectors[0]
        c.Place(map.sectors[map.startSectorIndex])
        c.Move(Map.DIRECTION_RIGHT) 
        c.Move(Map.DIRECTION_DOWN) 
        c.Move(Map.DIRECTION_LEFT) 
        c.Move(Map.DIRECTION_UP) 
        newSec = c.sector
        self.assertEqual(map.sectors.index(sec), map.sectors.index(newSec))

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(BasicTests)
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()