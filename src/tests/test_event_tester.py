'''
Created on Nov 11, 2010

@author: pekka
'''
import unittest
from event_tester import EventTester   
from shallowspace.event import Event

class BasicTests(unittest.TestCase):

    def testNotify(self):
        """Test notifying"""
        et = EventTester()
        ev = Event()
        et.notify(ev)
        self.assertEqual(ev, et.last_event())
        
    def testCheckLastEvent(self):
        """Test checking the last event"""
        et = EventTester()
        ev = Event()
        et.notify(ev)
        self.assertEqual(et.last_event(), ev)

if __name__ == "__main__":
    unittest.main()