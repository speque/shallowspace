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
    OccupiedSectorAction, CharactorShootRequest, CharactorMoveRequest,\
    FreeSectorAction
from shallowspace.constants import *
from tests.event_tester import EventTester
from types import FunctionType
from shallowspace.map import Sector


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
        
    def testCharactorShootRequest(self):
        """Test notifying the player about a CharactorChoorReuquest"""
        player = Player(self.event_manager, self.id_manager)
        request = CharactorShootRequest()
        self.event_tester.clear()
        def register_shoot_call():
            register_shoot_call.called = True
        self.shoot_called = False
        player.active_charactor.shoot = register_shoot_call
        player.notify(request)
        self.assertTrue(player.active_charactor.shoot.called)
    
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
        
    def testNotifyCharatorMoveRequest(self):
        """Test notifying the player about a CharactorMoveRequest"""
        player = Player(self.event_manager, self.id_manager)
        request = CharactorMoveRequest(DIRECTION_DOWN)
        player.active_charactor.direction = DIRECTION_UP
        def register_turn_call(direction):
            register_turn_call.called = True
        player.active_charactor.turn = register_turn_call
        self.event_tester.clear()
        player.notify(request)
        self.assertTrue(player.active_charactor.turn.called)
        
        request = CharactorMoveRequest(DIRECTION_UP)
        player.notify(request)
        # the active charactor does not have a sector yet
        self.assertIsNone(self.event_tester.last_event())
        
        request = CharactorMoveRequest(DIRECTION_UP, True)
        player.active_charactor.turn.called = False
        player.notify(request)
        # the active charactor does not have a sector yet
        self.assertIsNone(self.event_tester.last_event())
        self.assertFalse(player.active_charactor.turn.called)
        
        player.active_charactor.sector = Sector()
        player.notify(request)
        self.assertTrue(isinstance(self.event_tester.last_event(), FreeSectorAction))
        self.assertIsNone(self.event_tester.last_event().sector)

if __name__ == "__main__":
    unittest.main()