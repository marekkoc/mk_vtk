#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A module with function sources to create 3D objects.

@author: marek
Created on Fri Jun 14 14:44:22 2019

Created: 2019.06.14
Modified: 2019.06.14
"""
import vtk
all = []

def triangleFromPoints(p1, p2, p3):
    """
    p1, p2 and p3 are lists of coordinates.
    """
    # create points
    points = vtk.vtkPoints()
    points.InsertNextPoint(*p1)
    points.InsertNextPoint(*p2)
    points.InsertNextPoint(*p3)

    triangle = vtk.vtkTriangle()
    triangle.GetPointIds().SetId(0, 0)
    triangle.GetPointIds().SetId(1, 1)
    triangle.GetPointIds().SetId(2, 2)

    triangles = vtk.vtkCellArray()
    triangles.InsertNextCell(triangle)

    # polydata object
    tr = vtk.vtkPolyData()
    tr.SetPoints(points)
    tr.SetPolys(triangles)
    return tr


all.append('triangleFromPoints')


def cubeFromSource(x, y, z, side=[1, 1, 1]):
    """
    previous name: createCube
    """
    # create cube
    cube = vtk.vtkCubeSource()
    cube.SetCenter(x, y, z)
    cube.SetXLength(side[0])
    cube.SetYLength(side[1])
    cube.SetZLength(side[2])
    cube.Update()

    poly = cube.GetOutput()
    return poly


all.append('cubeFromSource')


def cubeFromScratch(coords, side=1):
    d = side/2.0
    x, y, z = coords

    a = [(x-d, y-d, z-d), (x+d, y-d, z-d),
         (x+d, y+d, z-d), (x-d, y+d, z-d),
         (x-d, y-d, z+d), (x+d, y-d, z+d),
         (x+d, y+d, z+d), (x-d, y+d, z+d)]
    pts = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
           (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]

    cube = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    polys = vtk.vtkCellArray()
    scalars = vtk.vtkFloatArray()

    for i in range(8):
        points.InsertPoint(i, a[i])
    for i in range(6):
        polys.InsertNextCell(_mkVtkIdList(pts[i]))
    for i in range(8):
        scalars.InsertTuple1(i, i)

    cube.SetPoints(points)
    cube.SetPolys(polys)
    cube.GetPointData().SetScalars(scalars)
    return cube


all.append('cubeFromScratch')


def _mkVtkIdList(it):
    vil = vtk.vtkIdList()
    for i in it:
        vil.InsertNextId(int(i))
    return vil


def cubesFromVerticelsAndFaces(ren, vert_list, face_list, opa=1.0,
                               col=[0, 1, 1]):
    """
    previous name: createPolyData
    """
    cube = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    polys = vtk.vtkCellArray()
    scalars = vtk.vtkFloatArray()

    for i in range(len(vert_list)):
        points.InsertPoint(i, vert_list[i])
        scalars.InsertTuple1(i, 1)
    for i in range(len(face_list)):
        polys.InsertNextCell(_mkVtkIdList(face_list[i]))

    cube.SetPoints(points)
    cube.SetPolys(polys)
    cube.GetPointData().SetScalars(scalars)

    cubeMapper = vtk.vtkPolyDataMapper()
    cubeMapper.SetInputData(cube)
    # cubeMapper.SetScalarRange(0,len(vert_list))
    cubeMapper.ScalarVisibilityOff()

    cubeActor = vtk.vtkActor()
    cubeActor.GetProperty().SetOpacity(opa)

    cubeActor.GetProperty().SetColor(*col)
    cubeActor.SetMapper(cubeMapper)
    ren.AddActor(cubeActor)

    del points
    del polys
    del scalars
    return cube


all.append('cubesFromVerticelsAndFaces')


def cubesFromPointsList(coords_list, VOX=1.0, scale=0.1, opa=1.0,
                        color=[1, 0, 0]):
    """
    previous name: voxelsMidPoints
    previous name: drawPolyDataFromPointsList
    """
    sc = scale * VOX
    side = [sc, sc, sc]

    appendedpolys = vtk.vtkAppendPolyData()
    appendedpolys.UserManagedInputsOn()
    appendedpolys.SetNumberOfInputs(len(coords_list))

    for k, coor in enumerate(coords_list):
        x, y, z = coor
        polyCube = cubeFromSource(x, y, z, side)
        appendedpolys.SetInputDataByNumber(k, polyCube)
    appendedpolys.Update()
    # polydata = vtk.vtkPolyData()
    polydata = appendedpolys.GetOutput()

    # mapper
    # cubeMapper = vtk.vtkPolyDataMapper()
    # cubeMapper.SetInputData(cleaned_polydata)
    # actor
    # cubeActor = vtk.vtkActor()
    # cubeActor.GetProperty().SetColor(*color)
    # assign actor to the renderer
    # cubeActor.SetMapper(cubeMapper)
    # ren.AddActor(cubeActor)
    return polydata


all.append('cubesFromPointsList')