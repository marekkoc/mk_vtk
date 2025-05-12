#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Plik z funckajmi do etykietowania obiektow binarnych w obrazach 3D.

Plik wykorzysuje biblioteki scipy.ndimage i nibabel.

Created on Tue Jun 18 14:34:37 2019
@author: marek

(C) MK & AM

C: 2019.06.18
M: 2019.06.18
"""
import numpy as np
import scipy.ndimage as ndimage
import nibabel as nib

def label3DImage(im, rank=3, connectivity=3):
    """
    Returns:
        - labeled array
        - num_features
    """
    # structuring element and labeling
    s = ndimage.generate_binary_structure(rank, connectivity)
    # labeled image and number of features
    labeled_array, num_features = ndimage.label(im,s)
    return labeled_array, num_features


def label3DImageAndGetTheBiggestObjects(im, bigObjectsNumber = 3, rank=3, connectivity=3):
    """
    Labels objects and returns the bigest object(s).

    Returns:
        - labeled array with chosen number of selected objests
        - num_features
    """
    # structuring element and labeling
    s = ndimage.generate_binary_structure(rank, connectivity)
    # labeled image and number of features
    labeled_array, num_features = ndimage.label(im,s)

    # identify the biggest object in the image
    lab_size = []
    for i in range(labeled_array.max()):
    	lab_size.append(len(labeled_array[labeled_array==i]))
    # find the biggest object and its index
    maxobj = max(lab_size[1:])
    maxobjidx = lab_size.index(maxobj)
    print("The biggest element has index equalled to %i and contains %i voxels.\n"%(maxobjidx, maxobj))


    # get the indices of the biggest object
    idx = np.where(labeled_array==maxobjidx)
    nim = np.zeros_like(im)
    nim[idx] = im[idx]
