#!/usr/bin/env python3
#vim: set ff=unix:
"""
C: 2018.04.18
M: 2025.04.26 - działa
"""


import vtk
import os
import numpy as np

import matplotlib.pyplot as plt
plt.gray()

import mklib_vtkrendering as mkr
import mklib_vtkimage as mkimg
import mklib_vtk.mklib_vtkpolydata_visualization as mkpd
#import imp
#imp.reload(mkimg)
#imp.reload(mkpd)

from mk_add_path_dropbox import MK_DROPBOX_DANE

if __name__ == '__main__':

	# RAW Image test
	if 1:
		# VISUALIZATION - Main window


		fname = 'normal01_4000_036_5_256_N00.raw'
		pth = os.path.join(MK_DROPBOX_DANE,"trees-drzewa",fname)
		reader = mkimg.rawImageReader(pth)
		img = vtk.vtkImageData()
		img = reader.GetOutput()
		#npimg = mkimg.convertVtkImageDataToNumpy(img)
		#mkimg.getNumpyArrayInfo(npimg)
		#mkimg.writeVtkImageData(img,'aaa.vtk')

		voi1 = mkimg.vtkVoiExtractor(img, region=[100,150,100,160,100,180])
		#mkimg.writeVtkImageData(voi1.GetOutput(),'voi.vtk')

		renderer, renWin, iren = mkr.createMainVTKWindow()
		mkpd.marchingCubes1(renderer, voi1.GetOutput(), 30)




		# Plane Widget X
		if 1:
			planeWidgetX = vtk.vtkImagePlaneWidget()
			planeWidgetX.DisplayTextOn()
			planeWidgetX.SetInputData(voi1.GetOutput())
			planeWidgetX.SetPlaneOrientationToXAxes()
			planeWidgetX.SetSliceIndex(128)
			planeWidgetX.RestrictPlaneToVolumeOn()
			planeWidgetX.SetKeyPressActivationValue("x")
			planeWidgetX.GetPlaneProperty().SetColor(1,0,0)
			planeWidgetX.SetResliceInterpolateToNearestNeighbour()
			planeWidgetX.SetInteractor(iren)
			planeWidgetX.On()

		iren.Start()

		del renderer
		del renWin
		del iren





	# DICOM TEST
	if 0:
		PathDicom ='./1.3.12.2.1107.5.2.30.27640.2017070314003110363513030.0.0.0'
		pth = os.path.join(MK_DROPBOX_DANE,PathDicom)
		reader = mkimg.dicomImageReader(pth)

		# convert to vtkImage
		image = vtk.vtkImageData()
		image = reader.GetOutput()
		orig = image.GetOrigin()
		spc = image.GetSpacing()

		# get info about image
		mkimg.getVtkImageInfo(image)

		# Write ImageData to file
		mkimg.writeVtkImageData(image)

		# Convert to Numpy
		nparray = mkimg.convertVtkImageDataToNumpy(image)

		#print("Display numpy image")
		#plt.imshow(nparray[:,:,20],interpolation='None',origin='lower')
		#plt.show()

		vtkarray = 2**16-1 - nparray
		#plt.figure()
		#plt.imshow(vtkarray[:,:,20],interpolation='None',origin='lower')
		#plt.show()

		img = mkimg.convertNumpyArrayToVtkImage(vtkarray,origin=orig, spacing=spc)
		mkimg.writeVtkImageData(img,'zzz.vtk')

print('EOF')