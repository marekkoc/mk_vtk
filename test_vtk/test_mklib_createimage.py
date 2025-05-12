#!/usr/bin/env python3
#vim: set ff=unix:
"""
C: 2018.05.03
M: 2025.04.26 - plik vtk dzała, plik nii nie działa
"""


import vtk
import os
import numpy as np

#import matplotlib.pyplot as plt
#plt.gray()

import mklib_vtkrendering as mkr
import mklib_vtkimage as mki
import mklib_vtk as mkp
#import imp
#imp.reload(mki)
#imp.reload(mkp)

from mk_add_path_dropbox import MK_DROPBOX_DANE

if __name__ == '__main__':

	vol = vtk.vtkImageData()
	vol.SetDimensions(26,26,26)
	vol.SetOrigin(-0.5, -0.5, -0.5)
	sp = 1/25
	vol.SetSpacing(sp, sp, sp)

	scalars = vtk.vtkFloatArray()
	for k in range(26):
		z = -0.5 + k*sp
		kOffset = k * 26 * 26

		for j in range(26):
			y = -0.5 + j * sp
			jOffset = j * 26

			for i in range(26):
				x = -0.5 + i * sp
				s = x*x + y*y + z*z - (0.4*0.4)
				#print(s)
				offset = i + jOffset + kOffset
				scalars.InsertTuple1(offset,s)

	vol.GetPointData().SetScalars(scalars)

	mki.writeVtkImageData(vol,'vol.vtk')
	mki.writeVtkImageData(vol,'vol.nii')


	print("EOF: %s" % os.path.basename(__file__))
