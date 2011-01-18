'''
Created on Oct 31, 2010

@author: pekka
'''
import unittest
import shallowspace.constants
from event_tester import EventTester   
from shallowspace.actors import Charactor
from shallowspace.eventmanager import EventManager
from shallowspace.map import Sector
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
        self.assertTrue(c in self.eventManager.listenerGroups["default"].listeners)
        self.assertEqual(c.sector, None)
        self.assertEqual(c.id, 0)
        self.assertEqual(c.radius, 2)
        self.assertEqual(c.direction, shallowspace.constants.DIRECTION_DOWN)

    def testTurn(self):
        """Test turning"""
        c = Charactor(self.eventManager)
        c.turn(shallowspace.constants.DIRECTION_RIGHT)
        self.assertEqual(c.direction, shallowspace.constants.DIRECTION_RIGHT)
        lastEvent = self.eventTester.last_event()
        self.assertTrue(isinstance(lastEvent, CharactorTurnEvent))
        self.assertEqual(lastEvent.charactor, c)
        
    def testShoot(self):
        """Test shooting"""
        c = Charactor(self.eventManager)
        c.shoot()
        lastEvent = self.eventTester.last_event()
        self.assertTrue(isinstance(lastEvent, CharactorShootEvent))
        self.assertEqual(lastEvent.charactor, c)

    def testPlace(self):
        """Test placing"""
        c = Charactor(self.eventManager)
        s = Sector()
        c.place(s)
        lastEvent = self.eventTester.last_event()
        self.assertTrue(isinstance(lastEvent, CharactorPlaceEvent))
        self.assertEqual(lastEvent.charactor, c)

    def testSuccesfullMove(self):
        """Test moving to a non-blocked direction"""
        c = Charactor(self.eventManager)
        s = Sector()
        c.place(s)
        n = Sector()
        s.neighbors[shallowspace.constants.DIRECTION_UP] = n 
        c.move(shallowspace.constants.DIRECTION_UP)
        self.assertTrue(isinstance(self.eventTester.last_event(), CharactorMoveEvent))
        self.assertEqual(c.sector, n)
        
    def testUnsuccesfullMove(self):
        """Test moving to a blocked direction"""
        c = Charactor(self.eventManager)
        s = Sector()
        c.place(s)
        e = self.eventTester.last_event()
        c.move(shallowspace.constants.DIRECTION_UP)
        self.assertEqual(self.eventTester.last_event(), e)
        self.assertEqual(c.sector, s)

if __name__ == "__main__":
    unittest.main()
