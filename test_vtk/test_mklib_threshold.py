#!/usr/bin/env python3
#vim: set ff=unix:
"""
C: 2018.05.03
M: 2025.04.26 - działa zapis, ale nie działa odczyt pliku nii.gz
"""


import vtk
import os
import numpy as np

import matplotlib.pyplot as plt
plt.gray()

import mklib_vtkrendering as mkr
import mklib_vtkimage as mki
import mklib_vtk as mkp
#import imp
#imp.reload(mki)
#imp.reload(mkp)

from mk_add_path_dropbox import MK_DROPBOX_DANE

if __name__ == '__main__':

	fname = 'normal01_4000_036_5_256_N00.vtk'
	pth = os.path.join(MK_DROPBOX_DANE, 'trees-drzewa',fname)
	reader = mki.vtkImageReader(pth)
	img = vtk.vtkImageData()
	img = reader.GetOutput()

	th = mki.thresholdVtkImageByUpper(img,115,255,0)

	mki.writeVtkImageData(th.GetOutput(),'2th.vtk')


	print("EOF: %s" % os.path.basename(__file__))