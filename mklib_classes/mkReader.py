#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Klasa do wczytywania obrazow.

Created on Thu May 30 09:13:47 2019
@author: mk

(C) MK & AM

C: 2019.05.30
M: 2019.11.15

v 0.01
"""

import nibabel as nib
import numpy as np
import scipy.io as sio

class mkReader(object):
    """
    C: 2019.05.30
    M: 2019.07.04
    """
    def __init__(self, fileName):
        self._filename = fileName
        self._data = None
        self.nii = None

    def setFileName(self, fileName):
        self._filename = fileName

    def getFileName(self):
        return self._filename

    def getData(self):
        return self._data

    def getNiiStructure(self):
        if self.nii is not None:
            return self.nii
        else:
            print('There is no Nii structure! Try to load data first!')
            return None

    def getPixDimFromNiiHeader(self):
        if self.nii is not None:
            nii = self.getNiiStructure()
            h = nii.header
            pixdim = h['pixdim']
            return pixdim
        else:
            print('There is no Nii structure! Try to load data first!')
            return None


    def loadData(self):
        # NIFTI
        if self._filename.endswith('.nii') or self._filename.endswith('.nii.gz'):
            self.nii = nib.load(self._filename)
            self._data = self.nii.get_data()
        # NPY
        elif self._filename.endswith('.npy'):
            self._data = np.load(self._filename)
        # RAW
        elif self._filename.endswith('.raw'):
            if  hasattr(self, '_rawDtype') and hasattr(self, '_rawShape'):
                self._data = np.fromfile(self._filename, dtype=self._rawDtype)
                self._data.shape = self._rawShape
            else:
                print('\nmkReader ---> Set RAW image dtype and/or shape!!!\n')
                return
        # MAT
        elif self._filename.endswith('.mat'):
            if hasattr(self, '_matDictName'):
                self._data = sio.loadmat(self._filename)[self._matDictName]
            else:
                print('\nmkReader ---> Set MAT file dictionary name FIRST!!!')
                return
        # VES
        elif self._filename.endswith('.ves'):
            self._data = np.loadtxt(self._filename, dtype=np.float, delimiter=' ', skiprows=1)
        else:
            print("mkReader ---> Can't read this file ({})!!!".format(self._filename))
            self._data = None
        return self._data


    def setRawParams(self, dtype='uint8', shape=(256, 256, 256)):
        self._rawDtype = dtype
        self._rawShape = shape

    def setMatDcitName(self, dictName):
        self._matDictName = dictName

    def getMatDictKeys(self):
        if self._filename.endswith('.mat'):
            return sio.loadmat(self._filename).keys()

    def reshapeDataOrder(self, order='F'):
        """
        order = 'C' or 'F' (Fortran)
        """
        self._data = self._data.reshape(self._data.shape, order)
        return self._data


if __name__ == '__main__':
    # MAT file
    if 0:
        reader = mkReader('tof_66.mat')
        print(reader.getMatDictKeys())
        reader.setMatDcitName('xList')
        img = reader.loadData()
    # VES file
    if 1:
        reader = mkReader('vtree_tra.ves')
        ves = reader.loadData()
        print(ves.shape)


