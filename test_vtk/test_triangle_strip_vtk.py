#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 16:09:15 2019

@author: marek
"""
import os
import vtk
import numpy as np
import mklib_vtkrendering as mkr
import mklib_vtk as mkpd
import mklib_vtktrianglestrip as mkts

vec = np.r_[0, 1, 0]
p0 = np.array([1, 1, 1])
p1 = np.array([2, 2, 2])

v1 = mkts.setTriangleStripVerticles(p0, p1, vec)
pd1 = mkts.triangleStripPolyData(v1)


v2 = mkts.setTriangleStripVerticles([1, 2, 1], [2, 3, 2], [0, 0.1, 0])
pd2 = mkts.triangleStripPolyData(v2)

pd = vtk.vtkAppendPolyData()
pd.AddInputData(pd1)
pd.AddInputData(pd2)
pd.Update()
polyd = pd.GetOutput()


ren, renWin, iren = mkr.createMainVTKWindow()
mkts.displayTriangleStrip(ren, polyd, rep='wire')

# mkpd.writeSTL('xxx.stl', polyd)

mkr.displayAxesWXYZ0(ren, pos=(0, 0, 0))
renWin.Render()
iren.Start()

del ren
del renWin
del iren
print('EOF: %s' % os.path.basename(__file__))
