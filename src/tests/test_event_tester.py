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
        et = EventTester()
        self.assertEqual(et.events, [])
        
    def testCheckLastEvent(self):
        """Test checking the last event"""
        et = EventTester()
        ev = Event()
        et.notify(ev)
        self.assertEqual(et.last_event(), ev)
        
    def testCheckLastTwoEvents(self):
        """Test checking last two events"""
        et = EventTester()
        ev1 = Event()
        ev2 = Event()
        ev3 = Event()
        et.notify(ev1)
        et.notify(ev2)
        et.notify(ev3)
        self.assertEqual([ev1, ev2], et.last_n_events(2))
        
    def testClear(self):
        et = EventTester()
        ev = Event()
        et.notify(ev)
        et.clear()
        self.assertEqual(et.events, [])

if __name__ == "__main__":
    unittest.main()