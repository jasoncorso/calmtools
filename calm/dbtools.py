'''
    calm.dbtools.py
    jason corso

    Tools for caffe-related lmdb management

'''

import lmdb
import caffe
import numpy as np
import scipy as sp



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

    env.close()

    return dbsize



def createDB(A,Y,DBO):
    '''!@brief Create an LMDB at DBO from parallel lists of arrays A (2D images)
    and Y (1D vector of labels).

    Each array is encoded as a standard caffe datum and indexed starting from 0

    @author: jason corso
    @param A list of arrays.
    @param A list of integers (1D)
    @param File path at which to save the data
    '''

    assert(len(A) == len(Y))

    imshape = A[0].shape
    map_size = max(1677216,np.prod(imshape)*len(A)*10)  # the *10 is to bc I do not know how to size the caffe datum version of these data samples

    env = lmdb.open(DBO, map_size=map_size)

    with env.begin(write=True) as txn:
        for i,image in enumerate(A):
            # resizes the image and then rolls it to be channels-first like caffe needs
            rmage = np.rollaxis(sp.misc.imresize(image,imshape,interp='bilinear'),2)

            datum          = caffe.proto.caffe_pb2.Datum()
            datum.channels = imshape[2]
            datum.height   = imshape[0]
            datum.width    = imshape[1]
            datum.data     = rmage.tobytes()
            datum.label    = int(Y[i])

            str_id = '{:08}'.format(i)

            # the encode is only essential in Python 3
            txn.put(str_id.encode('ascii'),datum.SerializeToString())

        env.sync()

    env.close()
