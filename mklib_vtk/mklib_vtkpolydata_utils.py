#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: marek
Created on Fri Jun 14 15:14:01 2019

Created: 2019.06.14
Modified: 2019.06.14
A modul with utlitly functions to deal with poly data.

@author: marek
Created on Fri Jun 14 17:09:55 2019

Created: 2019.06.14
Modified: 2019.06.14
"""

import vtk
import numpy as np
all = []


def polyDataInfo(polydata, printCellsAndPoints=False, printPoints=False,
                 name="PolyData"):
    print('*** %s ***' % name)
    num_points = polydata.GetNumberOfPoints()
    num_cells = polydata.GetNumberOfCells()
    print('num_points = %d' % num_points)
    print('num_cells = %d' % num_cells)

    if printPoints:
        print("\t*** Points:")
        for i in range(num_points):
            print("\tPoint: {} --> {}".format(i, polydata.GetPoint(i)))
    if printCellsAndPoints:
        print("\t*** Cells And Points:")
        for i in range(num_cells):
            c = polydata.GetCell(i)
            print("\tCell id = {}, ({}) ".format(i, c.GetClassName()))
            pnts_num = c.GetNumberOfPoints()
            for k in range(pnts_num):
                print("\t    {} ---> {}".format(k, c.GetPoints().GetPoint(k)))


all.append('polyDataInfo')


def setRGBColorToPolyData(poly, name, valList, toPoints=False, toCells=False):
    Colors = vtk.vtkUnsignedCharArray()
    Colors.SetNumberOfComponents(3)
    Colors.SetName(name)

    if not isinstance(valList[0], list) and not isinstance(valList[0], tuple) and not isinstance(valList[0], np.ndarray):
        Colors.InsertNextTuple3(*valList)
    else:
        for col in valList:
            Colors.InsertNextTuple3(*col)

    if toPoints:
        poly.GetPointData().SetScalars(Colors)
    elif toCells:
        poly.GetCellData().SetScalars(Colors)
    else:
        "setRGBColorToPolyData ---> Wrong Cell Type"
        return None
    # gdy jest ta linie nie musimy zwracac poly,
    # bo oryginal zostanie zaktualizowany
    poly.Modified()
    return poly



def cleanPolyData(poly, tolerance=0.01):
    clean2 = vtk.vtkCleanPolyData()
    clean2.SetInputData(poly)
    clean2.SetTolerance(tolerance)
    clean2.PointMergingOn()
    clean2.Update()
    return clean2.GetOutput()


all.append('cleanPolyData')


def triangulatePolyData(poly):
    t = vtk.vtkTriangleFilter()
    t.SetInputData(poly)
    t.Update()
    return t.GetOutput()


all.append('triangulatePolyData')


def labelPolyData(ren, polydata):
    """
    """
    labelMapper = vtk.vtkLabeledDataMapper()
    labelMapper.SetInputData(polydata)
    labelMapper.SetLabelModeToLabelIds()
    # labelMapper.SetLabelModeToLabelFieldData()
    labelActor = vtk.vtkActor2D()
    labelActor.SetMapper(labelMapper)
    ren.AddActor(labelActor)


all.append('labelPolyData')


def outlineFilter(vtkdata):
    outline = vtk.vtkOutlineFilter()
    outline.SetInputData(vtkdata)
    outline.Update()

    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInputData(outline.GetOutput())

    outlineActor = vtk.vtkActor()
    outlineActor.SetMapper(outlineMapper)
    outlineActor.GetProperty().SetColor(1, 1, 1)
    # ren.__add__(outlineActor)


all.append('outlineFilter')


def extractCellEdges(polydata, opa=0.2):
    """
    Extracts edges and renders only these extracted edges
    (framework of an object in polydata).
    """
    edges = vtk.vtkExtractEdges()
    edges.SetInputData(polydata)
    edges.Update()
    return edges.GetOutput()


all.append('extractCellEdges')


def deleteCellFromPolyData(poly, cellId=0):
    # Tell the polydata to build 'upward' links from points to cells.
    poly.BuildLinks()
    # Mark a cell as deleted.
    poly.DeleteCell(cellId)
    # Remove the marked cell.
    poly.RemoveDeletedCells()
    return poly


all.append('deleteCellFromPolyData')


def appendPolyDatas(polyDataList):
    """
    Appends a few poly datas into one data set.

    C: 2019.06.14
    M: 2019.06.14
    """
    nr = len(polyDataList)
    append = vtk.vtkAppendPolyData()
    append.UserManagedInputsOn()
    append.SetNumberOfInputs(nr)
    for k in range(nr):
        append.SetInputDataByNumber(k, polyDataList[k])
    append.Update()
    return append


all.append('appendPolyDataList')
