'''
Created on Nov 14, 2010

@author: pekka
'''
import unittest
from shallowspace.eventmanager import EventManager
from shallowspace.event import CharactorPlaceEvent, FreeSectorAction
from shallowspace.map import Sector, MapState
from shallowspace.constants import DIRECTION_UP, DIRECTION_LEFT, DIRECTION_DOWN, DIRECTION_RIGHT
from shallowspace.actors import Charactor

class MapTests(unittest.TestCase):
    pass

class MapStateTests(unittest.TestCase):
    
    def setUp(self):
        self.event_manager = EventManager()
    
    def testInit(self):
        """Test map state initalisation"""
        map_state = MapState(self.event_manager)
        self.assertEqual(map_state.event_manager, self.event_manager)
        self.assertTrue(map_state in self.event_manager.listener_groups["default"].listeners)
        self.assertEqual(map_state.occupied_sectors_by_actor_id, {})
        self.assertEqual(map_state.actors_by_sector_id, {})
        
    def testCharactorPlaceNotification(self):
        """Test charactor place notification"""
        map_state = MapState(self.event_manager)
        charactor = Charactor(self.event_manager)
        charactor.sector = Sector()
        charactor_place_event = CharactorPlaceEvent(charactor)
        self.event_manager.post(charactor_place_event)
        self.assertEqual(map_state.actors_by_sector_id[charactor.sector.charactor_id], charactor)
        self.assertEqual(map_state.occupied_sectors_by_actor_id[charactor.charactor_id], charactor.sector)
        
    def testFreeSectorActionNotification(self):
        """Test free section action notification"""
        map_state = MapState(self.event_manager)
        sector = Sector()
        
        self.actionExecuted = False #TODO: this is no good
        def function(sector_is_free):
            if sector_is_free:
                self.actionExecuted = True
        callback_function = function
        free_sector_action = FreeSectorAction(sector, callback_function)
        self.event_manager.post(free_sector_action)
        self.assertTrue(self.actionExecuted)
        
        self.actionExecuted = False
        charactor = Charactor(self.event_manager)
        charactor.sector = sector
        map_state.occupied_sectors_by_actor_id[charactor.charactor_id] = charactor.sector
        self.event_manager.post(free_sector_action)
        self.assertFalse(self.actionExecuted)

class SectorTests(unittest.TestCase):

    def testInit(self):
        """Test sector initialisation"""
        sector = Sector()
        self.assertEqual(len(sector.neighbors), 4)
        self.assertEqual(len(sector.corners), 4)
        for neighbor in sector.neighbors:
            self.assertEqual(neighbor, None)
        for neighbor in sector.corners:
            self.assertEqual(neighbor, None)
        
    def testMoveNotPossible(self):
        """Test illegal moves"""
        sector = Sector()
        self.assertFalse(sector.move_possible(DIRECTION_UP))
        self.assertFalse(sector.move_possible(DIRECTION_RIGHT))
        self.assertFalse(sector.move_possible(DIRECTION_DOWN))
        self.assertFalse(sector.move_possible(DIRECTION_LEFT))
        
    def testMovePossible(self):
        """Test legal moves"""
        sector = Sector()
        sector.neighbors = [Sector() for x in xrange(4)]
        self.assertTrue(sector.move_possible(DIRECTION_UP))
        self.assertTrue(sector.move_possible(DIRECTION_RIGHT))
        self.assertTrue(sector.move_possible(DIRECTION_DOWN))
        self.assertTrue(sector.move_possible(DIRECTION_LEFT))

if __name__ == "__main__":
    unittest.main()
