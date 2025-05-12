#!/usr/bin/env python3
#vim: set ff=unix:
"""
(C) MK & AM

C: 2018.04.24
M: 2018.04.24
"""

import os
import vtk

import mklib_vtkrendering as mkr
import mklib_vtkimage as mkimg
import mklib_vtkpolydata_visualization as mkpd
#import imp
#imp.reload(mkimg)
#imp.reload(mkpd)
#imp.reload(mkr)

from mk_add_path_dropbox import MK_DROPBOX_DANE

if __name__ == '__main__':

	fname = 'trees-drzewa/normal01_4000_036_5_256_N00.raw'
	pth = os.path.join(MK_DROPBOX_DANE, fname)
	reader = mkimg.rawImageReader(pth)
	img = vtk.vtkImageData()
	img = reader.GetOutput()

	voi1 = mkimg.vtkVoiExtractor(img, region=[100,150,100,160,100,180])
	#mkimg.writeVtkImageData(voi1.GetOutput(),'voi.vtk')
	voi1data = vtk.vtkImageData()
	voi1data = voi1.GetOutput()


	renderer, renWin, iren = mkr.createMainVTKWindow()
	mkpd.marchingCubes1(renderer, voi1data, 30)
	planeX = mkpd.planeWidget(renderer, voi1data, 'x')
	planeY = mkpd.planeWidget(renderer, voi1data, 'y')
	planeZ = mkpd.planeWidget(renderer, voi1data, 'z')
	for plane in [planeX, planeY, planeZ]:
		plane.SetInteractor(iren)
		plane.On()


	iren.Start()

	del renderer
	del renWin
	del iren


print('EOF')
