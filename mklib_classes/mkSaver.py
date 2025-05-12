#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Klasa do zapisywania obrazow.

Created on Wed Jun 26 11:15:54 2019
@author: marek

(C) MK & AM

C: 2019.06.26
M: 2019.06.26

v: 0.01
"""
import time
import numpy as np
import nibabel as nib


class mkSaver(object):
    """

    C: 2019.06.26
    M: 2019.06.26
    """
    def __init__(self, data, rootName, ext='.nii.gz', nii=None):
        self._data = data
        self._filename = rootName
        self._ext = ext
        self.nii = nii

#    def setData(self, data):
#        self._data = data
#
#    def setNiiStructure(self, nii):
#        self.nii = nii

    def saveDataAsNPY(self, suff=''):
        saveName = self._filename + suff + '.npy'
        np.save(saveName, self._data)

    def saveDataAsNIFTI(self, suff='', spacing=[1,1,1]):

        nii = self.nii
        data = self._data
        name = self._filename
        ext = self._ext

        if nii is not None:
            hdr = nii.header
            hdr['descrip'] = 'MK: nibabel-' + nib.__version__ + ' ({})'.format(time.strftime("%Y-%m-%d"))
            img = nib.Nifti1Image(data, affine=nii.affine, header=hdr)
        else:

            hdr = nib.Nifti1Header()
            hdr['descrip'] = 'MK: nibabel-' + nib.__version__ + ' ({})'.format(time.strftime("%Y-%m-%d"))
            img = nib.Nifti1Image(data, affine=np.eye(4), header=hdr)
            img.header['pixdim'][1:4]= spacing
        img.set_data_dtype(data.dtype)

        saveName = name +  str(suff) + ext
        img.to_filename(saveName)
        print("Image saved as %s" % saveName)


if __name__== '__main__':
    nii = nib.load('bg01cm_x1_vef_0o50_1o75q_tho14.nii')
    d = nii.get_data()

    saver = mkSaver(d, 'xxx', ext='.nii', nii=nii)
    #saver.saveDataAsNPY()
    saver.saveDataAsNIFTI()
