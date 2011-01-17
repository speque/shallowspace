'''
Created on Jan 17, 2011

@author: pekka
'''
import unittest
from shallowspace.player import Player
from shallowspace.eventmanager import EventManager
from shallowspace.game import ObjectIdGenerator
from shallowspace.actors import Charactor


class PlayerTests(unittest.TestCase):
    
    def setUp(self):
        self.eventManager = EventManager()
        self.idManager = ObjectIdGenerator()

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

if __name__ == "__main__":
    unittest.main()