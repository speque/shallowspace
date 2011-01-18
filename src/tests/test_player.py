'''
Created on Jan 17, 2011

@author: pekka
'''
import unittest
from shallowspace.player import Player
from shallowspace.eventmanager import EventManager
from shallowspace.game import ObjectIdGenerator
from shallowspace.actors import Charactor
from shallowspace.event import GameStartedEvent, CharactorPlaceRequest
from tests.event_tester import EventTester


class PlayerTests(unittest.TestCase):
    
    def setUp(self):
        self.eventManager = EventManager()
        self.idManager = ObjectIdGenerator()
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
        evt = EventTester()
        self.eventManager.register_listener(evt, ["default"])
        p.notify(ev)
        for index, charactor in enumerate(p.charactors):
            self.assertTrue(isinstance(evt.events[index], CharactorPlaceRequest))
            self.assertEqual(charactor, evt.events[index].charactor)

if __name__ == "__main__":
    unittest.main()