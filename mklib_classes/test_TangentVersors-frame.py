#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Wektory.

https://vtk.org/Wiki/VTK/Examples/Python/GeometricObjects/Display/OrientedArrow

Created on Wed Jul 31 14:32:12 2019
@author: marek

C: 2019.07.31
M: 2019.08.01
"""

import os
import vtk
import numpy as np

from mkReader import mkReader
from mkRenderer import mkRenderer
from mkPolyDataSources import mkPolyDataSources


def _arrow(startPoint, Tangent, arDir='t'):
    """
    C: 2019.07.31
    M: 2019.08.01
    """

    tx, ty, tz = Tangent
    # Basis is: Tx, Ty, Tz
    Tx = [tx, 0, 0]
    Ty = [0, ty, 0]
    Tz = [0, 0, tz]

    if arDir == 't':
        endPoint = startPoint + np.r_[tx, ty, tz]
        arbitrary = [tx, 0, -1]
        col = (1, 1, .1)
    elif arDir == 'x':
        endPoint = startPoint + np.r_[tx, 0, 0]
        arbitrary = Ty
        col = (1, 0, 0)
    elif arDir == 'y':
        endPoint = startPoint + np.r_[0, ty, 0]
        arbitrary = [-1, ty, 0]
        col = (0, 1, 0)
    elif arDir == 'z':
        arbitrary = [-1, 0, tz]
        col = (0, 0, 1)
        endPoint = startPoint + np.r_[0, 0, tz]
    else:
        print('Wrong flag!')
        return

    # Create an arrow.
    arrowSource = vtk.vtkArrowSource()

    # The X axis is a vector from start to end
    math = vtk.vtkMath()
    math.Subtract(endPoint, startPoint, Tx)
    length = math.Norm(Tx)
    math.Normalize(Tx)

    # Z - Wektor prostopadly do plaszczyzny w ktorej sa Tx i arbitrary
    math.Cross(Tx, arbitrary, Tz)
    math.Normalize(Tz)

    # The Y axis is Z cross X
    math.Cross(Tz, Tx, Ty)
    matrix = vtk.vtkMatrix4x4()

    # Create the direction cosine matrix
    matrix.Identity()
    for i in range(3):
        matrix.SetElement(i, 0, Tx[i])
        matrix.SetElement(i, 1, Ty[i])
        matrix.SetElement(i, 2, Tz[i])

    # Apply the transforms
    transform = vtk.vtkTransform()
    transform.Translate(startPoint)
    transform.Concatenate(matrix)
    transform.Scale(length, length, length)

    # Transform the polydata
    transformPD = vtk.vtkTransformPolyDataFilter()
    transformPD.SetTransform(transform)
    transformPD.SetInputConnection(arrowSource.GetOutputPort())
    transformPD.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transformPD.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(*col)
    return actor, arrowSource.GetShaftRadius()

def allTangents(spList, tangList):
    """
    C: 2019.08.01
    M: 2019.08.01
    """
    SP = spList
    T = tangList

    assembly = vtk.vtkAssembly()
    for k in range(T.shape[0]):
        ac, rc = _arrow(SP[k, :], T[k, :], 't')
        ax, rx = _arrow(SP[k, :], T[k, :], 'x')
        ay, ry = _arrow(SP[k, :], T[k, :], 'y')
        az, rz = _arrow(SP[k, :], T[k, :], 'z')

        sphere = mkPolyDataSources()
        sphere.sphereFromSource(pos=SP[k, :], rad=rc)


        assembly.AddPart(ac)
        assembly.AddPart(ax)
        assembly.AddPart(ay)
        assembly.AddPart(az)
        assembly.AddPart(sphere.asActor(col=(1, 1, 0.1)))
    return assembly

if __name__ == '__main__':

    import time

    rd = mkRenderer()
    # rd.displayAxesWXYZ0()
    # rd.displayPlaneWXYZ0(xRng=[-2, 2], yRng=[-2, 2], delXY=[8, 8])
    # rd.displayUnitSphereWXYZ()

    f1 = '../../all_data/tof_58.mat'
    reader1 = mkReader(f1)
    reader1.setMatDcitName('xList')
    data1 = reader1.loadData()
    T1 = data1[:, 6:9]
    SP1 = data1[:, 3:6]

    f2  = '../../all_data/tof_66.mat'
    reader2 = mkReader(f2)
    reader2.setMatDcitName('xList')
    data2 = reader2.loadData()
    T2 = data2[:, 6:9]
    SP2 = data2[:, 3:6]

    # Add the actor to the scene
    rd.ren = allTangents(SP1, T1)
    rd.ren = allTangents(SP2, T2)

    if 0:
        for k in range(T1.shape[0]):
            rd.setActiveCamera(SP1[k, :]+np.r_[-10, 5, -15], SP1[k, :])
            print(k, flush=True)
            time.sleep(0.8)
            rd.iren.GetRenderWindow().Render()


rd.renWin.Render()
rd.iren.Start()
del rd
print("\nEoF: %s" % os.path.basename(__file__))

