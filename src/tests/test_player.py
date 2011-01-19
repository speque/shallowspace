'''
Created on Jan 17, 2011

@author: pekka
'''
import unittest
from shallowspace.player import Player
from shallowspace.eventmanager import EventManager
from shallowspace.game import ObjectIdGenerator
from shallowspace.actors import Charactor
from shallowspace.event import GameStartedEvent, CharactorPlaceRequest,\
    CharactorMoveToRequest, CalculatePathRequest, ActiveCharactorChangeRequest,\
    OccupiedSectorAction
from tests.event_tester import EventTester
from types import FunctionType


class PlayerTests(unittest.TestCase):
    
    def setUp(self):
        self.eventManager = EventManager()
        self.idManager = ObjectIdGenerator()
        self.evt = EventTester()
        self.eventManager.register_listener(self.evt, ["default"])
        class C():
            pass
        self.game = C()
        self.game.map = C()

    def testInit(self):
        """Test player initialisation"""
        p = Player(self.eventManager, self.idManager)
        self.assertEqual(p.evManager, self.eventManager)
        self.assertEqual(p.game, None)
        self.assertEqual(p.name, "")
        self.assertTrue(p in self.eventManager.listenerGroups["default"].listeners)
        for c in p.charactors:
            self.assertTrue(isinstance(c, Charactor))
            #TODO check id
        self.assertEqual(p.active_charactor, p.charactors[3])
        
    def testNotifyGameStartedEvent(self):
        """Test notifying the player abot a GameStartedEvent"""
        p = Player(self.eventManager, self.idManager)
        ev = GameStartedEvent()
        self.evt.clear()
        p.notify(ev)
        for index, charactor in enumerate(p.charactors):
            self.assertTrue(isinstance(self.evt.events[index], CharactorPlaceRequest))
            self.assertEqual(charactor, self.evt.events[index].charactor)
            
    def testNotifyCharactorMoveToRequest(self):
        """Test notifying the player abot a CharactorMoveToRequest"""
        p = Player(self.eventManager, self.idManager)
        ev = CharactorMoveToRequest(None)
        self.evt.clear()
        p.notify(ev)
        self.assertTrue(isinstance(self.evt.last_event(), CalculatePathRequest))
        self.assertEqual(None, self.evt.last_event().pos)
        
    #TODO test notify CharactorShootRequest
    
    def testNotifyActiveCharactorChangeRequest(self):
        """Test notifying the player abot a ActiveCharactorChangeRequest"""
        p = Player(self.eventManager, self.idManager)
        ev = ActiveCharactorChangeRequest(None)
        self.evt.clear()
        p.notify(ev)
        self.assertTrue(isinstance(self.evt.last_event(), OccupiedSectorAction))
        self.assertEqual(None, self.evt.last_event().pos)
        self.assertTrue(type(self.evt.last_event().f) is FunctionType)
        #TODO check for f

if __name__ == "__main__":
    unittest.main()