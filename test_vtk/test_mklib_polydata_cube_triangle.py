#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 13:51:30 2018

@author: Marek

https://www.vtk.org/Wiki/VTK/Examples/Python/DataManipulation/Cube.py


C: 2018.01.16
M: 2025.04.26 - działa, ale zapis do pliu vtk nie działa

"""
import os
import vtk
import numpy as np
import mklib_vtkrendering as mkr
import mklib_vtkpolydata_visualization as mkpdv
import mklib_vtkpolydata_sources as mkpds
import mklib_vtkpolydata_utils as mkpdu
import mklib_vtkpolydata_io as mkpdio

renderer, renWin, iren = mkr.createMainVTKWindow()
mkr.displayAxesWXYZ0(renderer)
mkr.displayUnitSphereWXY0(renderer, rad=0.2)
mkr.displayPlaneWXY0(renderer)
mkr.setActiveCamera(renderer, pos=(0, 0, 25))

# ### 2019.06.14 ###
if 1:
    c = mkpds.cubeFromSource(4, 0, 1, [1, 2, 1])

    t = mkpdu.triangulatePolyData(c)
    t = mkpdu.deleteCellFromPolyData(t, 0)
    t = mkpdu.deleteCellFromPolyData(t, 2)

    c1 = np.random.randint(0, 255, size=(t.GetNumberOfCells(), 3))
    mkpdu.setRGBColorToPolyData(t, 'CELLS', c1, toCells=True)

    c2 = np.random.randint(0, 255, size=(t.GetNumberOfPoints(), 3))
    mkpdu.setRGBColorToPolyData(t, 'POINTS', c2, toPoints=True)

    mkpdv.displayPolyData(renderer, t, backCulling=1, scalarVisibility=True)

    ce = mkpdu.extractCellEdges(c)
    mkpdv.displayPolyData(renderer, ce, color=[0, 0, 1])

    # mkpdio.writePolyData('xxx.vtk', t)
    gl = mkpdv.sphereGlyphPoints(ce, 0.1)
    mkpdv.displayPolyData(renderer, gl, color=[0, 1, 0])

    c2 = mkpdu.cleanPolyData(c)
    mkpdu.polyDataInfo(c2, printCellsAndPoints=True, name="Wyczyszczone")
    mkpdu.labelPolyData(renderer, c2)

    mkpdio.writePolyData('xxx-100.vtk', t)
    mkpdio.writeSTL('yyy-100.stl', t )


if 1:
    Colors2 = vtk.vtkUnsignedCharArray()
    Colors2.SetNumberOfComponents(3)
    Colors2.SetName("Colors2")
    Colors2.InsertNextTuple3(0, 0, 125)
    Colors2.InsertNextTuple3(0, 125, 0)
    Colors2.InsertNextTuple3(125, 0, 0)

    p1 = [1.0, 0.0, 1.0]
    p2 = [0.0, 0.0, 1.0]
    p3 = [0.0, 1.0, 1.0]
    tr = mkpds.triangleFromPoints(p1, p2, p3)

    #c1 = [0, 125, 255]
    #col1 = mkpdu.setRGBColorToPolyData(tr, 'PTS', c1, toCells=True)

    c2 = [(0, 0, 125), (0, 125, 0), (125, 0, 0)]
    col2 =mkpdu.setRGBColorToPolyData(tr, "CELLS", c2, toPoints=True)

    mkpdv.displayPolyData(renderer, tr, scalarVisibility=True)
    mkpdu.labelPolyData(renderer, tr)


renWin.Render()
iren.Start()

del renderer
del renWin
del iren

print("EoF: %s" % os.path.basename(__file__))
