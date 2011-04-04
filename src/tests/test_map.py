'''
Created on Nov 14, 2010

@author: pekka
'''
import unittest
from shallowspace.eventmanager import EventManager
from shallowspace.event import CharactorPlaceEvent, FreeSectorAction
from shallowspace.map import Sector, MapState
from shallowspace.constants import *
from shallowspace.actors import Charactor

class MapTests(unittest.TestCase):
    pass

class MapStateTests(unittest.TestCase):
    
    def setUp(self):
        self.eventManager = EventManager()
    
    def testInit(self):
        """Test map state initalisation"""
        ms = MapState(self.eventManager)
        self.assertEqual(ms.event_manager, self.eventManager)
        self.assertTrue(ms in self.eventManager.listener_groups["default"].listeners)
        self.assertEqual(ms.occupied_sectors_by_actor_id, {})
        self.assertEqual(ms.actors_by_sector_id, {})
        
    def testCharactorPlaceNotification(self):
        """Test charactor place notification"""
        ms = MapState(self.eventManager)
        c = Charactor(self.eventManager)
        c.sector = Sector()
        cpe = CharactorPlaceEvent(c)
        self.eventManager.post(cpe)
        self.assertEqual(ms.actors_by_sector_id[c.sector.charactor_id], c)
        self.assertEqual(ms.occupied_sectors_by_actor_id[c.charactor_id], c.sector)
        
    def testFreeSectorActionNotification(self):
        """Test free section action notification"""
        ms = MapState(self.eventManager)
        s = Sector()
        
        self.actionExecuted = False
        def function(sectorIsFree):
            if sectorIsFree:
                self.actionExecuted = True
        f = function
        ev = FreeSectorAction(s, f)
        self.eventManager.post(ev)
        self.assertTrue(self.actionExecuted)
        
        self.actionExecuted = False
        c = Charactor(self.eventManager)
        c.sector = s
        ms.occupied_sectors_by_actor_id[c.charactor_id] = c.sector
        self.eventManager.post(ev)
        self.assertFalse(self.actionExecuted)

class SectorTests(unittest.TestCase):

    def testInit(self):
        """Test sector initialisation"""
        s = Sector()
        self.assertEqual(len(s.neighbors), 4)
        self.assertEqual(len(s.corners), 4)
        for n in s.neighbors:
            self.assertEqual(n, None)
        for n in s.corners:
            self.assertEqual(n, None)
        
    def testMoveNotPossible(self):
        """Test illegal moves"""
        s = Sector()
        self.assertFalse(s.move_possible(DIRECTION_UP))
        self.assertFalse(s.move_possible(DIRECTION_RIGHT))
        self.assertFalse(s.move_possible(DIRECTION_DOWN))
        self.assertFalse(s.move_possible(DIRECTION_LEFT))
        
    def testMovePossible(self):
        """Test legal moves"""
        s = Sector()
        s.neighbors = [Sector() for x in xrange(4)]
        self.assertTrue(s.move_possible(DIRECTION_UP))
        self.assertTrue(s.move_possible(DIRECTION_RIGHT))
        self.assertTrue(s.move_possible(DIRECTION_DOWN))
        self.assertTrue(s.move_possible(DIRECTION_LEFT))

if __name__ == "__main__":
    unittest.main()
