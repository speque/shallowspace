'''
Created on Oct 31, 2010

@author: pekka
'''
import unittest
import shallowspace.constants
from event_tester import EventTester   
from shallowspace.actors import Charactor
from shallowspace.eventmanager import EventManager
from shallowspace.game import Game
from shallowspace.event import CharactorMoveEvent

class BasicTests(unittest.TestCase):

    def setUp(self):
        em = EventManager()
        self.eventManager = em
        self.game = Game(em)
        self.eventTester = EventTester()
        self.eventManager.register_listener(self.eventTester)


    def tearDown(self):
        pass


    def testMove(self):
        c = Charactor(self.eventManager)
        map = self.game.map
        map.build()
        c.place(map.sectors[map.startSectorIndex])
        c.move(shallowspace.constants.DIRECTION_RIGHT)
        self.assertTrue(isinstance(self.eventTester.check_last_event(), CharactorMoveEvent))
        c.move(shallowspace.constants.DIRECTION_DOWN) 
        self.assertTrue(isinstance(self.eventTester.check_last_event(), CharactorMoveEvent))
        c.move(shallowspace.constants.DIRECTION_LEFT) 
        self.assertTrue(isinstance(self.eventTester.check_last_event(), CharactorMoveEvent))
        c.move(shallowspace.constants.DIRECTION_UP) 
        self.assertTrue(isinstance(self.eventTester.check_last_event(), CharactorMoveEvent))
        sec = map.sectors[map.startSectorIndex]
        newSec = c.sector
        self.assertEqual(map.sectors.index(sec), map.sectors.index(newSec))

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(BasicTests)
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
