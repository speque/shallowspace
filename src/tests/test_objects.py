'''
Created on Jun 2, 2011

@author: pekka
'''
import unittest
from shallowspace.eventmanager import EventManager
from shallowspace.objects import Bullets
from shallowspace.map import Sector
from tests.event_tester import EventTester
from shallowspace.event import BulletDestroyedEvent, BulletsMoveEvent, TickEvent

class BulletsTests(unittest.TestCase):
    
    def setUp(self):
        self.event_manager = EventManager()
        self.event_tester = EventTester()
        self.event_manager.register_listener(self.event_tester, ("default"))
        
    def testInit(self):
        """Test bullets initialisation"""
        bullets = Bullets(self.event_manager)
        self.assertEqual(self.event_manager, bullets.event_manager)
        self.assertEqual([], bullets.bullets)
        self.assertTrue(bullets in self.event_manager.listener_groups["default"].listeners)
        
    def testCreateBullet(self):
        """Test creating bullet"""
        bullets = Bullets(self.event_manager)
        sector = Sector()
        direction = 0
        bullets.create_bullet(sector, direction)
        self.assertTrue(len(bullets.bullets) == 1)
        self.assertEquals(bullets.bullets[0].sector, sector)
        self.assertEqual(bullets.bullets[0].direction, direction)
        
    def testDestroyBullet(self):
        """Test destroying bullet"""
        bullets = Bullets(self.event_manager)
        sector = Sector()
        direction = 0
        bullets.create_bullet(sector, direction)
        bullets.destroy_bullet(bullets.bullets[0])
        self.assertTrue(len(bullets.bullets) == 0)
        self.assertTrue(isinstance(self.event_tester.last_event(), BulletDestroyedEvent))
        
    def testMoveBullets(self):
        """Test moving bullets"""
        bullets = Bullets(self.event_manager)
        bullets.move_bullets()
        self.assertTrue(isinstance(self.event_tester.last_event(), BulletsMoveEvent))
        
    def testNotifyTickEvent(self):
        """Test notifying bullets about tick event"""
        bullets = Bullets(self.event_manager)
        def register_move_bullets_call():
            register_move_bullets_call.called = True
        bullets.move_bullets = register_move_bullets_call
        bullets.move_bullets.called = False
        event = TickEvent()
        bullets.notify(event)
        #there are no bullets -> False
        self.assertFalse(bullets.move_bullets.called)
        bullets.create_bullet(Sector(), 0)
        bullets.notify(event)
        self.assertTrue(bullets.move_bullets.called)
        