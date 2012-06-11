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
        event_maanger = EventManager()
        self.event_manager = event_maanger
        self.event_tester = EventTester()
        self.event_manager.register_listener(self.event_tester)

    def tearDown(self):
        pass
        
    def testInit(self):
        """Test character initialisation"""
        charactor = Charactor(self.event_manager)
        self.assertTrue(charactor in self.event_manager.listener_groups["default"].listeners)
        self.assertEqual(charactor.sector, None)
        self.assertEqual(charactor.charactor_id, 0)
        self.assertEqual(charactor.radius, 2)
        self.assertEqual(charactor.direction, shallowspace.constants.DIRECTION_DOWN)

    def testTurn(self):
        """Test turning"""
        charactor = Charactor(self.event_manager)
        charactor.turn(shallowspace.constants.DIRECTION_RIGHT)
        self.assertEqual(charactor.direction, shallowspace.constants.DIRECTION_RIGHT)
        lastEvent = self.event_tester.last_event()
        self.assertTrue(isinstance(lastEvent, CharactorTurnEvent))
        self.assertEqual(lastEvent.charactor, charactor)
        
    def testShoot(self):
        """Test shooting"""
        charactor = Charactor(self.event_manager)
        charactor.shoot()
        lastEvent = self.event_tester.last_event()
        self.assertTrue(isinstance(lastEvent, CharactorShootEvent))
        self.assertEqual(lastEvent.charactor, charactor)

    def testPlace(self):
        """Test placing"""
        charactor = Charactor(self.event_manager)
        sector = Sector()
        charactor.place(sector)
        lastEvent = self.event_tester.last_event()
        self.assertTrue(isinstance(lastEvent, CharactorPlaceEvent))
        self.assertEqual(lastEvent.charactor, charactor)

    def testSuccesfullMove(self):
        """Test moving to a non-blocked direction"""
        charactor = Charactor(self.event_manager)
        sector = Sector()
        charactor.place(sector)
        neighboring_sector = Sector()
        sector.neighbors[shallowspace.constants.DIRECTION_UP] = neighboring_sector 
        charactor.move(shallowspace.constants.DIRECTION_UP)
        self.assertTrue(isinstance(self.event_tester.last_event(), CharactorMoveEvent))
        self.assertEqual(charactor.sector, neighboring_sector)
        
    def testUnsuccesfullMove(self):
        """Test moving to a blocked direction"""
        charactor = Charactor(self.event_manager)
        sector = Sector()
        charactor.place(sector)
        event = self.event_tester.last_event()
        charactor.move(shallowspace.constants.DIRECTION_UP)
        self.assertEqual(self.event_tester.last_event(), event)
        self.assertEqual(charactor.sector, sector)

if __name__ == "__main__":
    unittest.main()
