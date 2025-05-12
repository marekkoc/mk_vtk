#!/usr/bin/env python
# -*- coding: utf-8 -*-
#vim: set ff=unix:
"""
A module with implemented basic and the most common poly data operations.

Created on Thu Jul  4 11:26:57 2019
@author: marek

(C) MK & AM

C: 2019.07.04
M: 2019.07.04

v: 0.01
"""
import vtk
import numpy as np


class mkPolyData(object):
    """
    C: 2019.07.04
    M: 2019.07.04
    """

    def __init__(self, poly=None, name="Poly Data"):
        self.poly = poly
        self.name = name

    @property
    def poly(self):
        return self._poly

    @poly.setter
    def poly(self, poly):
        self._poly = poly

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def asActor(self, scalarVisibility=True, col=(.9,.1,.1), opa=1, withEdges= False, lineWidth=False, backCulling=False):
        """
        Returns polydata as an actor.

        based on: .../mklib_vtkpolydata_visualization.py

        C: 2019.07.04
        M: 2019.07.04
        """
        mapper = vtk.vtkPolyDataMapper()
        if scalarVisibility:
            mapper.ScalarVisibilityOn()
            mapper.SetScalarRange(0, self.poly.GetPointData().GetNumberOfTuples())
        else:
            mapper.ScalarVisibilityOff()

        mapper.SetInputData(self.poly)

        actor = vtk.vtkActor()
        actor.GetProperty().SetColor(*col)  # ( 0.5, 0.5, 0.5 )
        actor.GetProperty().SetOpacity(opa)
        if backCulling:
            actor.GetProperty().BackfaceCullingOn()
        if lineWidth:
            actor.GetProperty().SetLineWidth(lineWidth)
        actor.SetMapper(mapper)
        if withEdges:
            actor.GetProperty().SetEdgeColor(1.0, 1.0, 1.0)  # (0.0, 0.0, 0.0)
            actor.GetProperty().EdgeVisibilityOn()
        return actor

    def info(self, printCellsAndPoints=False, printPoints=False):
        """
        based on: .../mklib_vtkpolydata_utils.py

        C: 2019.07.04
        M: 2019.07.04
        """
        print('*** %s ***' % self.name)
        num_points = self.poly.GetNumberOfPoints()
        num_cells = self.poly.GetNumberOfCells()
        print('num_points = %d' % num_points)
        print('num_cells = %d' % num_cells)

        if printPoints:
            print("\t*** Points:")
            for i in range(num_points):
                print("\tPoint: {} --> {}".format(i, self.poly.GetPoint(i)))
        if printCellsAndPoints:
            print("\t*** Cells And Points:")
            for i in range(num_cells):
                c = self.poly.GetCell(i)
                print("\tCell id = {}, ({}) ".format(i, c.GetClassName()))
                pnts_num = c.GetNumberOfPoints()
                for k in range(pnts_num):
                    print("\t    {} ---> {}".format(k, c.GetPoints().GetPoint(k)))

    def outlineActor(self):
        """
        based on: .../mklib_vtkpolydata_utils.py

        C: 2019.07.04
        M: 2019.07.04
        """
        outline = vtk.vtkOutlineFilter()
        outline.SetInputData(self.poly)
        outline.Update()
        outlineMapper = vtk.vtkPolyDataMapper()
        outlineMapper.SetInputData(outline.GetOutput())
        outlineActor = vtk.vtkActor()
        outlineActor.SetMapper(outlineMapper)
        outlineActor.GetProperty().SetColor(1, 1, 1)
        return outlineActor

    def labelActor(self):
        """
        based on: .../mklib_vtkpolydata_utils.py

        C: 2019.07.04
        M: 2019.07.04
        """
        labelMapper = vtk.vtkLabeledDataMapper()
        labelMapper.SetInputData(self.poly)
        labelMapper.SetLabelModeToLabelIds()
        # labelMapper.SetLabelModeToLabelFieldData()
        labelActor = vtk.vtkActor2D()
        labelActor.SetMapper(labelMapper)
        return labelActor

    def appendPolyDatas(self, polyList):
        """
        Appends a few poly datas into one data set.

        based on: .../mklib_vtkpolydata_utils.py

        C: 2019.07.04
        M: 2019.07.04
        """
        polyDataList = [self.poly]
        polyDataList.extend(polyList)

        nr = len(polyDataList)
        append = vtk.vtkAppendPolyData()
        append.UserManagedInputsOn()
        append.SetNumberOfInputs(nr)
        for k in range(nr):
            append.SetInputDataByNumber(k, polyDataList[k])
        append.Update()
        self.poly = append.GetOutput()

    def cleanPolyData(self, tolerance=0.01):
        """
        based on: .../mklib_vtkpolydata_utils.py

        C: 2019.07.04
        M: 2019.07.04
        """
        clean2 = vtk.vtkCleanPolyData()
        clean2.SetInputData(self.poly)
        clean2.SetTolerance(tolerance)
        clean2.PointMergingOn()
        clean2.Update()
        self.poly = clean2.GetOutput()

    def triangulatePolyData(self):
        """
        based on: .../mklib_vtkpolydata_utils.py

        C: 2019.07.04
        M: 2019.07.04
        """
        t = vtk.vtkTriangleFilter()
        t.SetInputData(self.poly)
        t.Update()
        self.poly = t.GetOutput()

    def deleteCellFromPolyData(self, cellId=0):
        """
        based on: .../mklib_vtkpolydata_utils.py

        C: 2019.07.04
        M: 2019.07.04
        """
        # Tell the polydata to build 'upward' links from points to cells.
        self.poly.BuildLinks()
        # Mark a cell as deleted.
        self.poly.DeleteCell(cellId)
        # Remove the marked cell.
        self.poly.RemoveDeletedCells()

    def cellEdgesActor(self, col=(.9, .9, .9), opa=0.2):
        """
        Extracts edges and renders only these extracted edges
        (framework of an object in polydata).

        based on: .../mklib_vtkpolydata_utils.py

        C: 2019.07.04
        M: 2019.07.04

        """
        edges = vtk.vtkExtractEdges()
        edges.SetInputData(self.poly)
        edges.Update()
        eMapper = vtk.vtkPolyDataMapper()
        eMapper.SetInputData(edges.GetOutput())
        eActor = vtk.vtkActor()
        eActor.SetMapper(eMapper)
        eActor.GetProperty().SetColor(*col)
        return eActor

    def setRGBColorToPolyData(self, name, valList, toPoints=False, toCells=False):
        Colors = vtk.vtkUnsignedCharArray()
        Colors.SetNumberOfComponents(3)
        Colors.SetName(name)

        if not isinstance(valList[0], (list, tuple, np.ndarray)):
            Colors.InsertNextTuple3(*valList)
        else:
            for col in valList:
                Colors.InsertNextTuple3(*col)

        if toPoints:
            self.poly.GetPointData().SetScalars(Colors)
        elif toCells:
            self. poly.GetCellData().SetScalars(Colors)
        else:
            print("setRGBColorToPolyData ---> Wrong Cell Type")
            return None
        # gdy jest ta linie nie musimy zwracac poly,
        # bo oryginal zostanie zaktualizowany
        self.poly.Modified()


if __name__ == '__main__':
    import os
    import mklib_vtkpolydata_sources as mkpds

    from mkRenderer import mkRenderer
    from mkPolyDataIO import mkPolyDataIO

    rd = mkRenderer()
    rd.displayAxesWXYZ0()
    # rd.displayPlaneWXYZ0(xRng=[-5, 5], yRng=[-5, 5])
    rd.displayUnitSphereWXYZ(rad=0.5)

    c0 = mkpds.cubeFromSource(3, 3, 1)
    c1 = mkpds.cubeFromSource(4, 4, 1)
    c2 = mkpds.cubeFromSource(4, 3, 2)

    pd = mkPolyData(c0)
    pd.appendPolyDatas([c1, c2])
    # pd1.deleteCellFromPolyData(1)

    pd.triangulatePolyData()
    col = np.random.randint(0, 255, size=(pd.poly.GetNumberOfCells(), 3))
    pd.setRGBColorToPolyData('Cels', col, toCells=1)

    # pd.cleanPolyData()
#    col = np.random.randint(0, 255, size=(pd.poly.GetNumberOfPoints(),3))
#    pd.setRGBColorToPolyData('Points', col, toPoints=1)

    rd.ren = pd.asActor(col=(0, 0, 1))
    # rd.ren = pd1.cellEdgesActor()
    rd.ren = pd.outlineActor()
    # rd.ren = pd.labelActor()

#    io = mkPolyDataIO(pd.poly)
#    io.writeSTL('yyy.stl')
#    io.writePolyData('yyy-vtk.vtk')

    rd.renWin.Render()
    rd.iren.Start()
    del rd
    print("\nEoF: %s" % os.path.basename(__file__))

