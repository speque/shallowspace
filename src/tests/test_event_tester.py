'''
Created on Nov 11, 2010

@author: pekka
'''
import unittest
from event_tester import EventTester   
from shallowspace.event import Event

class BasicTests(unittest.TestCase):

    def testInit(self):
        """Test initialising event tester"""
        event_tester = EventTester()
        self.assertEqual(event_tester.events, [])
        
    def testCheckLastEvent(self):
        """Test checking the last event"""
        event_tester = EventTester()
        event = Event()
        event_tester.notify(event)
        self.assertEqual(event_tester.last_event(), event)
        
    def testCheckLastTwoEvents(self):
        """Test checking last two events"""
        event_tester = EventTester()
        event1 = Event()
        event2 = Event()
        event3 = Event()
        event_tester.notify(event1)
        event_tester.notify(event2)
        event_tester.notify(event3)
        self.assertEqual([event1, event2], event_tester.last_n_events(2))
        
    def testClear(self):
        event_tester = EventTester()
        event = Event()
        event_tester.notify(event)
        event_tester.clear()
        self.assertEqual(event_tester.events, [])

if __name__ == "__main__":
    unittest.main()