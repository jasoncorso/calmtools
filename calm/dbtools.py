'''
    calm.dbtools.py
    jason corso

    Tools for caffe-related lmdb management
    Functions here are of the following forms
       DB     --> information about the db
       DB     --> new DB
       Data   --> DB
       Params --> DB

'''

import lmdb
import caffe
import numpy as np
import scipy as sp




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


def dropPixels(DB,DBO,DBD,droprate=0.1,duprate=1):
    '''!@brief Take an LMDB of images at DB and drop droprate pixels from each image and save the output into a new db.

    @author: jason corso
    @param DB path to the original (readOnly) data
    @param DBO path to the output database with dropped pixels
    @param DBD path to the output database with the original images (only outputted when duprate > 1
    @param float droprate rate at which to drop pixels (0,1)
    @param int duprate how many times to duplicate the whole data (augmentation)
    '''

    assert(isinstance(duprate,int))

    print "dropPixels at %f drop rate and %d duprate"%(droprate,duprate)

    env = lmdb.open(DB, readonly = True)
    txn = env.begin()

    map_size = env.info()['map_size']*duprate

    envO = lmdb.open(DBO, map_size=map_size)

    envD = None
    if duprate > 1:
        envD = lmdb.open(DBD, map_size=map_size)

    gi = 0
    for i in range(duprate):

        print "dup %d starting output index %d"%(i,gi)
        cur = txn.cursor()

        if not cur.first():
            print "empty database"  # handle this better
            return

        while (True):
            # get datum (use caffe tools for this)
            raw_datum = cur.value()
            datum = caffe.proto.caffe_pb2.Datum()
            datum.ParseFromString(raw_datum)
            flat_x = np.fromstring(datum.data, dtype=np.uint8)
            x = flat_x.reshape(datum.channels, datum.height, datum.width)

            # x is a uint8 channels*height*width image
            n = (int)(datum.height*datum.width*droprate)

            # generate random indices for rows (row-random-indices) and columns to drop
            rri = np.random.randint(0,datum.height,size=n)
            cri = np.random.randint(0,datum.width,size=n)

            o = np.copy(x)
            o[:,rri,cri] = 0

            str_id = '{:08}'.format(gi)

            # write out to dbs
            datumO          = caffe.proto.caffe_pb2.Datum()
            datumO.channels = datum.channels
            datumO.height   = datum.height
            datumO.width    = datum.width
            datumO.data     = o.tobytes()
            datumO.label    = datum.label
            with envO.begin(write=True) as txnO:
                txnO.put(str_id.encode('ascii'),datumO.SerializeToString())

            if envD is not None:
                datumD          = caffe.proto.caffe_pb2.Datum()
                datumD.channels = datum.channels
                datumD.height   = datum.height
                datumD.width    = datum.width
                datumD.data     = datum.data
                datumD.label    = datum.label
                with envD.begin(write=True) as txnD:
                    txnD.put(str_id.encode('ascii'),datumD.SerializeToString())

            gi += 1
            if not cur.next():
                break

    env.close()

    envO.sync()
    envO.close()

    if envD is not None:
        envD.sync()
        envD.close()


