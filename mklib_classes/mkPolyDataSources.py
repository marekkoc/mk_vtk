#!/usr/bin/env python
# -*- coding: utf-8 -*-
#vim: set ff=unix:
"""
Poly data sources.

Created on Fri Jul 12 16:52:15 2019
@author: marek

(C) MK & AM

C: 2019.07.12
M: 2019.07.12

v: 0.01
"""
import vtk
from mkPolyData import mkPolyData

class mkPolyDataSources(mkPolyData):
    """
    C: 2019.07.12
    M: 2019.07.12
    """
    def __init__(self, poly = False, name = 'Some Poly Data source'):
        super(mkPolyDataSources, self).__init__(poly, name)

    def cuberFromSource(self, pos=[0, 0, 0], sideLen = [1, 1, 1]):
        """
        C: 2019.07.12
        M: 2019.07.12
        """
        cube = vtk.vtkCubeSource()
        cube.SetCenter(*pos)
        cube.SetXLength(sideLen[0])
        cube.SetYLength(sideLen[1])
        cube.SetZLength(sideLen[2])
        cube.Update()
        self.poly = cube.GetOutput()
        return self.poly

    def sphereFromSource(self, pos=[0, 0, 0], rad=1):
        """
        C: 2019.07.12
        M: 2019.07.12
        """
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(rad)
        sphere.SetCenter(*pos)
        sphere.Update()
        self.poly = sphere.GetOutput()
        return self.poly

