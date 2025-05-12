#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A module with I/O functions on PolyData objects.

@author: marek
Created on Fri Jun 14 15:14:01 2019

Created: 2019.06.14
Modified: 2019.06.28
"""

import vtk
all = []


def writeSTL(filename, polydata, toASCII=True):
    """
    C: 2019.06.14
    M: 2019.06.28
    """
    stlWriter = vtk.vtkSTLWriter()
    stlWriter.SetFileName(filename)
    stlWriter.SetInputData(polydata)
    if toASCII:
        stlWriter.SetFileTypeToASCII()
    else:
        stlWriter.SetFileTypeToBinary()
    stlWriter.Update()
    stlWriter.Write()


all.append('writeSTL')


def readSTL(filename):
    """
    C: 2019.02.20
    M: 2019.02.20
    """
    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
    reader.Update()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(reader.GetOutput())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor


all.append('readSTL')


def readSTLAsPolyData(filename):
    """
    C: 2019.02.20
    M: 2019.02.20
    """
    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()


all.append('readSTLAsPolyData')


def writePolyData(filename, polydata, toASCII=True):
    """
    formaty: VTK
    """
    writer = vtk.vtkPolyDataWriter()
    writer.SetInputData(polydata)
    writer.SetFileName(filename)
    if toASCII:
        writer.SetFileTypeToASCII()
    else:
        writer.SetFileTypeToBinary()
    writer.Update()
    writer.Write()


all.append('writePolyData')


def readVTKGeometry(filename):
    """
    Reads VTK file format

    Input: filename.vtk
    Output: actor

    C: 2019.02.20
    M: 2019.02.20
    """
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()  # Needed because of GetScalarRange
    output = reader.GetOutput()
    scalar_range = output.GetScalarRange()

    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(output)
    mapper.SetScalarRange(scalar_range)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor


all.append('readVTKGeometry')


def readVTKGeometryAsPolyData(filename):
    """
    Reads VTK file format

    Input: filename.vtk
    Output: polydata

    C: 2019.02.20
    M: 2019.02.20
    """
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()  # Needed because of GetScalarRange
    output = reader.GetOutput()

    usg = vtk.vtkGeometryFilter()
    usg.SetInputData(output)
    usg.Update()
    return usg.GetOutput()


all.append('readVTKGeometryAsPolyData')
