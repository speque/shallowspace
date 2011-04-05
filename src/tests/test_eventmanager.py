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
        event = EventManager()
        event_tester = EventTester()
        event.register_listener(event_tester)
        self.assertTrue(event_tester in event.listener_groups["default"].listeners)
        
    def testUnregister(self):
        """Test unregistering a listener"""
        event = EventManager()
        event_tester = EventTester()
        event.register_listener(event_tester)
        event.unregister_listener(event_tester)
        self.assertFalse(event_tester in event.listener_groups["default"].listeners)
        
    def testPost(self):
        """Test posting an event"""
        event = EventManager()
        event_tester = EventTester()
        event.register_listener(event_tester)
        event = Event()
        event.post(event)
        self.assertEqual(event_tester.last_event(), event)

if __name__ == "__main__":
    unittest.main()