'''
Created on Oct 31, 2010

@author: pekka
'''

import unittest
import test_charactor

if __name__=="__main__":
    print ''
    print '*******************************************'
    print '* Test suite for Shallow Space initiated: *'
    print '*******************************************'
    print ''

    charactorSuite = test_charactor.suite()
    allTestSuites = unittest.TestSuite([charactorSuite])
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(allTestSuites)
