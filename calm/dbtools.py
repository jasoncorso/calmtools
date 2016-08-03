'''
    calm.dbtools.py
    jason corso

    Tools for caffe-related lmdb management

'''

import lmdb
import numpy as np



def computeMV(DB,ODB):
    '''!@brief Compute the mean and variance of all images in a database.

    @author: jason corso
    @param DB path to input LMDB with images
    :return:
    '''

    # open the database
    env = lmdb.open(DB,readonly = True)

    env.close()


def countDB(DB):
    '''!@brief Counts number of keys in the lmdb and returns it

    @author: jason corso
    @param DB path to input LMDB
    '''

    # open the database
    env = lmdb.open(DB,readonly = True)

    with env.begin() as txn:
        dbsize = txn.stat()['entries']

    return dbsize

    env.close()
