'''
    calm.dbtools.py
    jason corso

    Tools for caffe-related image management
    Functions here are of the following forms
       ImageData --> ImageData
       ImageData --> Params

'''

import glob
import numpy as np
import scipy as sp
import scipy.ndimage



def computeMean_glob(globString,resize=None,interp='bilinear',
                     imReader=scipy.ndimage.imread):
    '''!@brief Compute the mean of an image set (via a glob string) and return it.

    This is present because the default Caffe compute_image_mean tool, while helpful, does not handle
    floating point data.  This function should be used when you want to handle floating data and do it
    outside of caffe.

    You can use a custom imReader in the event you have to preprocess the image data in an atypical way.
    Otherwise, the standard scipy.ndimage.imread function is used.

    Currently the mean is already returned as numpy.float64 for processing outside of this function.

    @author: jason corso
    @param: globString is the string passed to the glob function (e.g., '/tmp/image*.png')
    @param: resize is a [rows by columns] array to resize the image to, or it is None if no resizing (default is None) Resize is still considered if a different imReader is set.
    @param: interp is the string to use in the resizing function call (scipy.misc.imresize)
    @param: imReader is a function that takes the path to an image and returns a numpy ndarray with the data (r,c,d)
    @return: the mean image as an numpy array
    '''

    files = glob.glob(globString)
    scale = 1.0/len(files)

    shape = resize
    if resize is None:
        image = imReader(files[0])
        shape = image.shape

    A = np.zeros(shape,dtype=np.float64)

    for i in files:
        image = imReader(i)

        if resize is not None:
            image = sp.misc.imresize(image,resize,interp=interp)

        A = A + scale*image

    return A