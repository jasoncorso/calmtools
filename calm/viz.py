'''
    calm.viz.py
    jason corso

    Tools for caffe and lmdb visualization
    Functions here are of the following forms
       DB     --> Images

'''

import lmdb
import caffe
import cv2
import numpy as np



def dbToImages(DB,format,isRGB=True):
    '''!@brief Converts all the images in the DB to png files on disk.

    It is assumed that the path specified in the format string actually exists on disk

    We note that the images are assumed stored in RGB in the LMDB.  OpenCV is
    used to write to disk and hence if isRGB is True, then we convert to BGR
    when writing.  The original database is not affected by this.

    @author: jason corso
    @param DB path to input LMDB (readOnly)
    @param format a printf-style format string, including a %s to write the key.png
    '''

    env = lmdb.open(DB, readonly = True)

    with env.begin() as txn:
        cursor = txn.cursor()

        if not cursor.first():
            print "empty database"
            return

        while True:
            k = cursor.key()
            print k

            raw_datum = cursor.value()

            datum = caffe.proto.caffe_pb2.Datum()
            datum.ParseFromString(raw_datum)
            flat_x = np.fromstring(datum.data, dtype=np.uint8)
            x = flat_x.reshape(datum.channels, datum.height, datum.width)
            fn = format % k
            if isRGB:
                cv2.imwrite(fn,cv2.cvtColor(np.rollaxis(x,0,3),cv2.COLOR_RGB2BGR))
            else:  #isBGR
                cv2.imwrite(fn,np.rollaxis(x,0,3))

            if not cursor.next():
                break


