'''
Created on Nov 11, 2010

@author: pekka
'''
import unittest
from shallowspace.eventmanager import EventManager
from shallowspace.event import Event  
from event_tester import EventTester 

class BasicTests(unittest.TestCase):

    def testRegister(self):
        """Test registering a listener"""
        ev = EventManager()
        et = EventTester()
        ev.register_listener(et)
        self.assertTrue(et in ev.listener_groups["default"].listeners)
        
    def testUnregister(self):
        """Test unregistering a listener"""
        ev = EventManager()
        et = EventTester()
        ev.register_listener(et)
        ev.unregister_listener(et)
        self.assertFalse(et in ev.listener_groups["default"].listeners)
        
    def testPost(self):
        """Test posting an event"""
        ev = EventManager()
        et = EventTester()
        ev.register_listener(et)
        event = Event()
        ev.post(event)
        self.assertEqual(et.last_event(), event)

if __name__ == "__main__":
    unittest.main()