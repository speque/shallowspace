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
        ev = EventManager()
        et = EventTester()
        ev.register_listener(et)
        self.assertTrue(et in ev.listenerGroups["default"].listeners)
        
    def testUnregister(self):
        ev = EventManager()
        et = EventTester()
        ev.register_listener(et)
        ev.unregister_listener(et)
        self.assertFalse(et in ev.listenerGroups["default"].listeners)
        
    def testPost(self):
        ev = EventManager()
        et = EventTester()
        ev.register_listener(et)
        event = Event()
        ev.post(event)
        self.assertEqual(et.check_last_event(), event)

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(BasicTests)
    return suite

if __name__ == "__main__":
    unittest.main()