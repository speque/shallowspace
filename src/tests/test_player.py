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
    CharactorMoveToRequest, CalculatePathRequest, ActiveCharactorChangeRequest, \
    OccupiedSectorAction
from tests.event_tester import EventTester
from types import FunctionType


class PlayerTests(unittest.TestCase):
    
    def setUp(self):
        self.event_manager = EventManager()
        self.id_manager = ObjectIdGenerator()
        self.event_tester = EventTester()
        self.event_manager.register_listener(self.event_tester, ("default"))
        class C():
            pass
        self.game = C()
        self.game.map = C()

    def testInit(self):
        """Test player initialisation"""
        player = Player(self.event_manager, self.id_manager)
        self.assertEqual(player.event_manager, self.event_manager)
        self.assertEqual(player.game, None)
        self.assertEqual(player.name, "")
        self.assertTrue(player in self.event_manager.listener_groups["default"].listeners)
        for charactor in player.charactors:
            self.assertTrue(isinstance(charactor, Charactor))
            #TODO check id
        self.assertEqual(player.active_charactor, player.charactors[3])
        
    def testNotifyGameStartedEvent(self):
        """Test notifying the player abot a GameStartedEvent"""
        player = Player(self.event_manager, self.id_manager)
        game_started_event = GameStartedEvent()
        self.event_tester.clear()
        player.notify(game_started_event)
        for index, charactor in enumerate(player.charactors):
            self.assertTrue(isinstance(self.event_tester.events[index], CharactorPlaceRequest))
            self.assertEqual(charactor, self.event_tester.events[index].charactor)
            
    def testNotifyCharactorMoveToRequest(self):
        """Test notifying the player abot a CharactorMoveToRequest"""
        player = Player(self.event_manager, self.id_manager)
        request = CharactorMoveToRequest(None)
        self.event_tester.clear()
        player.notify(request)
        self.assertTrue(isinstance(self.event_tester.last_event(), CalculatePathRequest))
        self.assertEqual(None, self.event_tester.last_event().pos)
        
    #TODO test notify CharactorShootRequest
    
    def testNotifyActiveCharactorChangeRequest(self):
        """Test notifying the player abot a ActiveCharactorChangeRequest"""
        player = Player(self.event_manager, self.id_manager)
        request = ActiveCharactorChangeRequest(None)
        self.event_tester.clear()
        player.notify(request)
        self.assertTrue(isinstance(self.event_tester.last_event(), OccupiedSectorAction))
        self.assertEqual(None, self.event_tester.last_event().pos)
        self.assertTrue(type(self.event_tester.last_event().function) is FunctionType)
        #TODO check for function

if __name__ == "__main__":
    unittest.main()