'''
Created on Oct 31, 2010

@author: pekka
'''

import unittest
import test_charactor
import test_eventmanager
import test_event_tester

if __name__=="__main__":
    suites = []
    suites.append(test_event_tester.suite())
    suites.append(test_charactor.suite())
    suites.append(test_eventmanager.suite())
    allTestSuites = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(allTestSuites)
