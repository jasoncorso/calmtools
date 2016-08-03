'''
    maketestdata.py

    jason corso

    Currently, these functions are expected to be run during setup to generate the test data.
'''

import numpy as np
from ..dbtools import createDB


def make_simple3():
    
    O  = np.ones([3,3])
    Z  = np.zeros([3,3])
    A1 = np.asarray([O,Z,Z])
    A2 = np.asarray([Z,O,Z])
    A3 = np.asarray([Z,Z,O])
    
    createDB([A1,A2,A2],range(3),'/tmp/calm_simple3.lmdb')


def main():
    make_simple3()


if __name__ == '__main__':

    main()

