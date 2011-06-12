'''
Created on Jun 2, 2011

@author: pekka
'''
import unittest
from shallowspace.eventmanager import EventManager
from shallowspace.objects import Bullets
from shallowspace.map import Sector

class BulletsTests(unittest.TestCase):
    
    def setUp(self):
        self.event_manager = EventManager()
        
    def testInit(self):
        """Test bullets initialisation"""
        bullets = Bullets(self.event_manager)
        self.assertEqual(self.event_manager, bullets.event_manager)
        self.assertEqual([], bullets.bullets)
        self.assertTrue(bullets in self.event_manager.listener_groups["default"].listeners)
        
    def testCreateBullet(self):
        """Test create bullet"""
        bullets = Bullets(self.event_manager)
        sector = Sector()
        direction = 0
        bullets.create_bullet(sector, direction)
        self.assertTrue(len(bullets.bullets) == 1)
        self.assertEquals(bullets.bullets[0].sector, sector)
        self.assertEqual(bullets.bullets[0].direction, direction)