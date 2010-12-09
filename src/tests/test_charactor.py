'''
Created on Oct 31, 2010

@author: pekka
'''
import unittest
import shallowspace.constants
from event_tester import EventTester   
from shallowspace.actors import Charactor
from shallowspace.eventmanager import EventManager
from shallowspace.map import Map, Sector
from shallowspace.event import CharactorMoveEvent, CharactorTurnEvent, CharactorShootEvent, CharactorPlaceEvent

class BasicTests(unittest.TestCase):

    def setUp(self):
        em = EventManager()
        self.eventManager = em
        self.eventTester = EventTester()
        self.eventManager.register_listener(self.eventTester)


    def tearDown(self):
        pass
        
    def testInit(self):
        """Test character initialisation"""
        c = Charactor(self.eventManager)
        self.assertTrue(c in self.eventManager.listeners)
        self.assertEqual(c.sector, None)
        self.assertEqual(c.direction, shallowspace.constants.DIRECTION_DOWN)

    def testTurn(self):
        c = Charactor(self.eventManager)
        c.turn(shallowspace.constants.DIRECTION_RIGHT)
        self.assertEqual(c.direction, shallowspace.constants.DIRECTION_RIGHT)
        lastEvent = self.eventTester.check_last_event()
        self.assertTrue(isinstance(lastEvent, CharactorTurnEvent))
        self.assertEqual(lastEvent.charactor, c)
        

    def testShoot(self):
        c = Charactor(self.eventManager)
        c.shoot()
        lastEvent = self.eventTester.check_last_event()
        self.assertTrue(isinstance(lastEvent, CharactorShootEvent))
        self.assertEqual(lastEvent.charactor, c)

    def testPlace(self):
        c = Charactor(self.eventManager)
        s = Sector()
        c.place(s)
        lastEvent = self.eventTester.check_last_event()
        self.assertTrue(isinstance(lastEvent, CharactorPlaceEvent))
        self.assertEqual(lastEvent.charactor, c)

    def testSuccesfullMove(self):
        c = Charactor(self.eventManager)
        s = Sector()
        c.place(s)
        n = Sector()
        s.neighbors[shallowspace.constants.DIRECTION_UP] = n 
        c.move(shallowspace.constants.DIRECTION_UP)
        self.assertTrue(isinstance(self.eventTester.check_last_event(), CharactorMoveEvent))
        self.assertEqual(c.sector, n)
        

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(BasicTests)
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
