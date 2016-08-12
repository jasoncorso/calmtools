'''
    maketestdata.py

    jason corso

    Currently, these functions are expected to be run during setup to generate the test data.
'''

import numpy as np
import os
import cv2
from ..dbtools import createDB


def make_simple3():
    
    O  = np.ones([3,3])
    Z  = np.zeros([3,3])
    A1 = np.asarray([O,Z,Z])
    A2 = np.asarray([Z,O,Z])
    A3 = np.asarray([Z,Z,O])
    
    createDB([A1,A2,A2],range(3),'/tmp/calm_simple3.lmdb')

def make_tree():

    if not os.path.exists('/tmp/calm_tree'):
        os.mkdir('/tmp/calm_tree')
    if not os.path.exists('/tmp/calm_tree/1'):
        os.mkdir('/tmp/calm_tree/1')
    if not os.path.exists('/tmp/calm_tree/2'):
        os.mkdir('/tmp/calm_tree/2')

    O1  = np.ones([3,3,3])*0.25*255
    O2  = np.ones([3,3,3])*0.5*255
    O3  = np.ones([3,3,3])*0.75*255

    createDB([O1,O2,O3],range(3),'/tmp/calm_tree/1/db_001.lmdb')
    createDB([O1,O2,O3],range(3),'/tmp/calm_tree/1/db_002.lmdb')
    createDB([O1,O2,O3],range(3),'/tmp/calm_tree/1/db_003.lmdb')
    createDB([O1,O2,O3],range(3),'/tmp/calm_tree/1/db_004.lmdb')

    createDB([O1,O2,O3],range(3),'/tmp/calm_tree/2/db_001.lmdb')
    createDB([O1,O2,O3],range(3),'/tmp/calm_tree/2/db_002.lmdb')
    createDB([O1,O2,O3],range(3),'/tmp/calm_tree/2/db_003.lmdb')
    createDB([O1,O2,O3],range(3),'/tmp/calm_tree/2/db_004.lmdb')

def make_imtree():

    if not os.path.exists('/tmp/calm_imtree'):
        os.mkdir('/tmp/calm_imtree')
    if not os.path.exists('/tmp/calm_imtree/1'):
        os.mkdir('/tmp/calm_imtree/1')
    if not os.path.exists('/tmp/calm_imtree/2'):
        os.mkdir('/tmp/calm_imtree/2')

    O1  = np.ones([3,3,3])*0.25*255
    O2  = np.ones([3,3,3])*0.5*255
    O3  = np.ones([3,3,3])*0.75*255

    cv2.imwrite('/tmp/calm_imtree/1/image_001.png',O1)
    cv2.imwrite('/tmp/calm_imtree/1/image_002.png',O2)
    cv2.imwrite('/tmp/calm_imtree/1/image_003.png',O3)

    cv2.imwrite('/tmp/calm_imtree/2/image_001.png',O1)
    cv2.imwrite('/tmp/calm_imtree/2/image_002.png',O2)
    cv2.imwrite('/tmp/calm_imtree/2/image_003.png',O3)
    cv2.imwrite('/tmp/calm_imtree/2/image_004.jpg',O1)
    cv2.imwrite('/tmp/calm_imtree/2/image_005.jpg',O2)
    cv2.imwrite('/tmp/calm_imtree/2/image_006.jpg',O3)


def main():
    make_simple3()
    make_tree()
    make_imtree()


if __name__ == '__main__':

    main()

