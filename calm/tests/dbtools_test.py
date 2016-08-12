'''
    calm.tests.test_dbtools.py

    jason corso

    Unit tests for the calm.dbtools module
'''

import unittest
import tempfile
import os.path
import shutil

from .. import dbtools

class testBasicMethods(unittest.TestCase):

    def test_count(self):

        size = dbtools.countDB('/tmp/calm_simple3.lmdb')

        self.assertEquals(size,3)

    def test_glob(self):

        td = tempfile.mkdtemp()
        dbo = os.path.join(td,"test_glob.lmdb")
        dbtools.createDB_glob('/tmp/calm_imtree/*/image_*.png',dbo)

        size = dbtools.countDB(dbo)

        self.assertEquals(size,6)

        shutil.rmtree(td)



if __name__ == '__main__':
    unittest.main()

