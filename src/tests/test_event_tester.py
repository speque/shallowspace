'''
Created on Nov 11, 2010

@author: pekka
'''
import unittest
from event_tester import EventTester   
from shallowspace.event import Event

class BasicTests(unittest.TestCase):

    def testNotify(self):
        et = EventTester()
        ev = Event()
        et.notify(ev)
        self.assertEqual(ev, et.lastEvent)
        
    def testCheckLastEvent(self):
        et = EventTester()
        ev = Event()
        et.notify(ev)
        self.assertEqual(et.check_last_event(), ev)
        self.assertEqual(et.check_last_event(), None)

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(BasicTests)
    return suite

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()