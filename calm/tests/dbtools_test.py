'''
    calm.tests.test_dbtools.py

    jason corso

    Unit tests for the calm.dbtools module
'''

import unittest

from .. import dbtools

class testBasicMethods(unittest.TestCase):

    def test_count(self):

        size = dbtools.countDB('/tmp/calm_simple3.lmdb')

        self.assertEquals(size,3)




if __name__ == '__main__':
    unittest.main()

