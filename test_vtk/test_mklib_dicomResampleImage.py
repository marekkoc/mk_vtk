#!/usr/bin/env python3
#vim: set ff=unix:
"""
C: 2018.05.01
M: 2025.04.26 - działa
"""
import os
import vtk
import numpy as np

import mklib_vtkrendering as mkr
import mklib_vtkimage as mkimg
import mklib_vtk as mkpd
import imp
imp.reload(mkimg)
imp.reload(mkpd)

from mk_add_path_dropbox import MK_DROPBOX_DANE


if __name__ == '__main__':
	
	PathDicom ='./1.3.12.2.1107.5.2.30.27640.2017070314003110363513030.0.0.0'
	path = os.path.join(MK_DROPBOX_DANE,PathDicom)
	reader = mkimg.dicomImageReader(path)
	
	# convert to vtkImage
	image = vtk.vtkImageData()
	image = reader.GetOutput()
	orig = image.GetOrigin()
	spc = image.GetSpacing()
	print(spc)
		
	# get info about image
	mkimg.getVtkImageInfo(image, 'oryg')
	# Write ImageData to file
	mkimg.writeVtkImageData(image,'oryg.vtk')
	
	sp = spc[0]
	resampledImage = mkimg.resampleVtkImage(image,spacing=[sp, sp, sp])
	mkimg.getVtkImageInfo(resampledImage, 'resampled')
	mkimg.writeVtkImageData(resampledImage, 'resampled.vtk')