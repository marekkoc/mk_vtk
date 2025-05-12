#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Binary objects labelling class.

Created on Tue Jun 18 15:27:28 2019
@author: marek

(C) MK & AM

C: 2019.06.18
M: 2019.08.22

v: 0.01
"""
import sys
#sys.path.append('../../../../00/all_python/mklib_classes')
#sys.path.append('../../../../00/all_python/mklib_utils')

sys.path.append('/media/marek/p1ext4/work/00/all_python/mklib_classes')
sys.path.append('/media/marek/p1ext4/work/00/all_python/mklib_utils')

import os
import time
import numpy as np
import nibabel as nib
import scipy.ndimage as ndimage

from mklib_utils1 import imgInfo
from mkSaver import mkSaver

class mkLabeller(object):
    """
    C: 2019.06.18
    M: 2019.06.22
    """
    def __init__(self, data3D, rank=3, connectivity=3):
        self._img = data3D
        self._label3DImage(rank, connectivity)

    def Info(self):
        im = self._img  # zeby bylo krocej
        print("Loaded Image:")
        print("  *** max = {}, min={}, type={}, shape={}".
              format(im.max(), im.min(), im.dtype, im.shape))

    def InfoLabeledImage(self):
        im = self._labImg_  # zeby bylo krocej
        print("Labeled Image:")
        print("  *** max = {}, min={}, type={}, shape={}".
              format(im.max(), im.min(), im.dtype, im.shape))

    def getImage(self):
        return self._img

    def getLabeledImage(self):
        return self._labImg_

    def getTotalNumberOfObjects(self):
        return self._objNumber_

    def _label3DImage(self, rank, connectivity):
        print("Labelling...")
        # structuring element and labeling
        s = ndimage.generate_binary_structure(rank, connectivity)
        # labeled image and number of features
        labeled_array, num_features = ndimage.label(self._img, s)

        # domyslnie zwracana macierz jest typu int32,
        # jesli obiektow jest mniej niz 255 to zamieniam macierz na uint8
        if num_features < 256:
            labeled_array = np.asarray(labeled_array, dtype=self._img.dtype)

        # quantify the the size objects in the image
        lab_size = []
        for i in range(labeled_array.max()+1):
            lab_size.append(len(labeled_array[labeled_array == i]))

        self._labImg_ = labeled_array
        self._objNumber_ = num_features

        print("Object size sorting in descending order...")
        # tworzymy macierz 2D - bez pierwszego wiersza (tam jest tlo)
        # kol1 - kolejny objekt (etykieta/jasnosc)
        # kol2 - licznosc obiektu (w wokselach)
        arr = np.array(list(enumerate(lab_size)))[1:]
        arr = arr[arr[:, 1].argsort(), :]
        self._labels_ = arr[::-1, :]

    def printLabelAndItsVoxelNumber(self):
        print("Object -> voxels")
        labs = self._labels_
        for r in range(labs.shape[0]):
            print("   {} ---> {}".format(*labs[r, :]))

    def selectObjectsBiggerThanNVoxels(self, N=10):
        labs = self._labels_
        idx = np.where(labs[:, 1] > N)
        self._labels_ = labs[idx]

    def selectNTheBiggestObjects(self, N=5):
        self._labels_ = self._labels_[:N, :]

    def relableObjectsInAscendingOrder(self):
        print("\nObject relabeling (starts from 1) in ascending order...")
        im = self._labImg_
        labs = self._labels_
        rows = labs.shape[0]
        nim = np.zeros_like(im)

        for r in range(rows):
            newVal = r + 1
            o = labs[r, 0]
            idx = np.where(im==o)
            nim[idx] = newVal
            labs[r, 0] = newVal
        self._labImg_ = nim

    def getCurrentLabeledImage(self, convertToBinaryValue=0):

        im = self._labImg_  # obraz
        labs = self._labels_  # etykiety i ich woksele
        nim = np.zeros_like(im)
        for k in range(labs.shape[0]):
            o = labs[k,0]
            idx = np.where(im==o)
            nim[idx] = im[idx]

        if convertToBinaryValue:
            nim = np.where(nim > 0, convertToBinaryValue, 0)
            nim = np.asarray(nim, dtype=self._img.dtype)
        return nim

    def saveEachObjectSeparately(self, name, ext, niioryg):
        """
        M: 2019.08.22
        """
        labs = self._labels_
        im = self._labImg_

        rows = labs.shape[0]
        for k in range(rows):
            data = np.zeros_like(im)
            o, vox = labs[k]
            idx = np.where(im==o)
            data[idx] = o
            suff = '-lb-o%d' % o
            saver = mkSaver(data, name, ext, niioryg)
            saver.saveDataAsNIFTI(suff)

    def saveImageAsNIFTI(self, name, ext, niioryg, convertToBinaryValue=0):
        """
        M: 2019.08.22
        """
        im = self._labImg_
        if convertToBinaryValue:
            im = np.where(im>0, convertToBinaryValue, 0)
            im = np.asarray(im, dtype=self._img.dtype)
        saver = mkSaver(im, name, ext, niioryg)
        saver.saveDataAsNIFTI()


if __name__ == '__main__':
    from mkReader import mkReader

    # name = '../../all_data/bg01cm_x1_vef_0o50_1o75q_tho14'
    name = '/media/marek/p1ext4/work/19/nitrc_2019/bg01_x1_analiza_20190517/SKEL/qth14/bg01cm_x1_vef_0o50_1o75q_tho14_g10_sk'
    reader = mkReader(name + '.nii.gz')
    data = reader.loadData()
    nii = reader.getNiiStructure()

    lb = mkLabeller(data)
    #lb.selectNTheBiggestObjects(5)
    #lb.printLabelAndItsVoxelNumber()
    #lb.relableObjectsInAscendingOrder()
    lb.printLabelAndItsVoxelNumber()
    b = lb.getCurrentLabeledImage()
    print(b.shape, b.max())

    # lb.saveImageAsNIFTI(name, '.nii.gz', nii)
    # lb.saveEachObjectSeparately(name, '.nii.gz', nii)
    print("\nEoF: %s" % os.path.basename(__file__))
