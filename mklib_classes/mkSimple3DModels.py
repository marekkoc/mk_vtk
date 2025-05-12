#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Rysujemy modele na podstawie listy punktow. Modele sa niezalezne od obrazu (nie trzeba miec obrazu zeby narysowac modele).

Created on Tue Jul  9 12:26:30 2019
@author: marek

(C) MK & AM

C: 2019.07.09
M: 2019.07.10

v: 0.01
"""
import vtk
import numpy as np
from mkPolyData import mkPolyData
from mkVoxel import mkVoxel


class mkSimple3DModels(mkPolyData):
    """

    C: 2019.07.09
    M: 2019.07.10

    """

    def __init__(self, linePntsLst=[], cubesPntsLst = [], name="Some 3D model"):
        """
        C: 2019.07.09
        M: 2019.07.10
        """

        if len(linePntsLst):
            poly = self._drawLinesBetweenPoints(linePntsLst)
        elif len(cubesPntsLst):
            poly = self._drawCubesFromVoxels(cubesPntsLst)
        else:
            print("zla flaga! -nic nie robimy")
            poly = None
        # inicjalizujemy klase rodzica
        super(mkSimple3DModels, self).__init__(poly, name)

    def _drawLinesBetweenPoints(self, coord_list):
        """
        C: 2019.07.10
        M: 2019.07.10
        """
        pntsNr = len(coord_list)

        pts = vtk.vtkPoints()
        pts.SetNumberOfPoints(pntsNr)

        polyLine = vtk.vtkCellArray()
        # polyLine.InsertNextCell(len(coord_list))

        for i in range(pntsNr):
            pts.SetPoint(i, *coord_list[i])
            # polyLine.InsertCellPoint(i)

        for i in range(pntsNr-1):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, i)
            line.GetPointIds().SetId(1, i+1)
            polyLine.InsertNextCell(line)

        linesPolyData = vtk.vtkPolyData()
        linesPolyData.SetPoints(pts)
        linesPolyData.SetLines(polyLine)
        return linesPolyData

    def drawSphereGlyphs(self, sphereRadius, color=[.1, .1, .9], opa=1):
        """
        C: 2019.07.10
        M: 2019.07.10
        """
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(sphereRadius)
        sphere.Update()
        glyph = vtk.vtkGlyph3D()
        glyph.SetInputData(self._poly)
        glyph.SetSourceConnection(sphere.GetOutputPort())
        glyph.GeneratePointIdsOn()
        glyph.ScalingOff()
        glyph.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(glyph.GetOutput())
        actor = vtk.vtkActor()
        actor.GetProperty().SetColor(*color) # (R,G,B)
        actor.GetProperty().SetOpacity(opa)
        actor.SetMapper(mapper)
        return actor

    def drawCubicGlyphs(self, side=[.1,.1,.1], col=(1.,1, 0), opa=1):
        # create cube
        cube = vtk.vtkCubeSource()
        cube.SetXLength(side[0])
        cube.SetYLength(side[1])
        cube.SetZLength(side[2])
        cube.Update()

        glyph = vtk.vtkGlyph3D()
        glyph.SetInputData(self._poly)
        glyph.SetSourceConnection(cube.GetOutputPort())
        glyph.GeneratePointIdsOn()
        glyph.ScalingOff()
        glyph.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(glyph.GetOutput())
        actor = vtk.vtkActor()
        actor.GetProperty().SetColor(*col)  # (R,G,B)
        actor.GetProperty().SetOpacity(opa)
        actor.SetMapper(mapper)
        return actor

    def _drawCubesFromVoxels(self, pntsList):
        """
        C: 2019.07.10
        M: 2019.07.10
        """
        # gdy podajemy liste indeksow (w liscie lub macierzy np.array)
        if isinstance(pntsList[0], (list, np.ndarray, tuple)):
            voxels = []
            for p in pntsList:
                p = list(p)
                voxels.append(mkVoxel(p))
        else:
            # gdy podajemy liste obiektow typu mkVoxel
            voxels = pntsList

        allVoxelsPDList = []
        for v in voxels:
            pdVoxelTriangles = []
            pts = v.triangles
            for k in range(len(pts)):
                pdVoxelTriangles.append(self._drawTriangleFromPoints(*pts[k]))

            oneVoxelPD = self.appendPolyDatas(pdVoxelTriangles)
            oneVoxelCleanPD = self.cleanPolyData(oneVoxelPD)
            allVoxelsPDList.append(oneVoxelCleanPD)

        allVoxelsPD = self.appendPolyDatas(allVoxelsPDList)
        return allVoxelsPD

    def _drawTriangleFromPoints(self, p1, p2, p3):
        """
        p1, p2 and p3 are lists of coordinates.

        C: 2019.07.10
        M: 2019.07.10
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

    @staticmethod
    def appendPolyDatas(polyDataList):
        """
        Appends a few poly datas into one data set.

        C: 2019.06.14
        M: 2019.07.10
        """
        nr = len(polyDataList)
        append = vtk.vtkAppendPolyData()
        append.UserManagedInputsOn()
        append.SetNumberOfInputs(nr)
        for k in range(nr):
            append.SetInputDataByNumber(k, polyDataList[k])
        append.Update()
        return append.GetOutput()

    @staticmethod
    def cleanPolyData(poly, tolerance=0.01):
        clean2 = vtk.vtkCleanPolyData()
        clean2.SetInputData(poly)
        clean2.SetTolerance(tolerance)
        clean2.PointMergingOn()
        clean2.Update()
        return clean2.GetOutput()







if __name__ == "__main__":
    import os
    from mkRenderer import mkRenderer

    rd = mkRenderer()
    # rd.displayAxesWXYZ0()
    # rd.displayUnitSphereWXYZ(rad=0.5)
    # rd.displayUnitSphereWXYZ()

    if 0:

        a = (0, 0, 0)
        b = (1, 1, 1)
        c = (2, 3, 4)
        d = (1, 4, 0)
        lst = [a, b, c, d]

        bm1 = mkSimple3DModels(linePntsLst=lst, name="First Line")
        rd.ren = bm1.labelActor()
        rd.ren = bm1.drawSphereGlyphs(0.2, opa=0.1)
        rd.ren = bm1.asActor(lineWidth=1)
        rd.displayPlaneWXYZ0(xRng=[-5, 5], yRng=[-5, 5])

    if 0:
        a = (0, 0, 0)
        b = (1, 1, 1)
        c = (2, 3, 4)
        d = (1, 4, 0)
        lst = [a, b, c, d]
        sm2 = mkSimple3DModels(cubesPntsLst=lst, name='First cubes')
        rd.ren = sm2.asActor(col=(0., 1, 0), opa=0.3)
        rd.displayPlaneWXYZ0(xRng=[-5, 5], yRng=[-5, 5])

    if 1:
        from mkReader import mkReader
        fname66 = '../../all_data/tof_66.mat'
        mt66 = mkReader(fname66)
        mt66.getMatDictKeys()
        mt66.setMatDcitName('xList')
        data66 = mt66.loadData()

        cInt66 = data66[:, 0:3]

        # szesciany 66
        sm66Cubes = mkSimple3DModels(cubesPntsLst=cInt66, name='tof66-int')
        rd.ren = sm66Cubes.asActor(opa=0.35)

        # Linie laczaca srodki (int) 66
        sm66Lines = mkSimple3DModels(linePntsLst=cInt66)
        rd.ren = sm66Lines.asActor()
        rd.ren = sm66Lines.drawCubicGlyphs(col=[1, 1, 0])

        # spline 66
        cFl66 = data66[:, 3:6]
        sm66f = mkSimple3DModels(linePntsLst=cFl66)
        rd.ren = sm66f.asActor(col=(0, 0, 1))
        rd.ren = sm66f.drawSphereGlyphs(0.1, opa=1)

        fname58 = '../../all_data/tof_58.mat'
        mt58 = mkReader(fname58)
        mt58.setMatDcitName('xList')
        data58 = mt58.loadData()

        cInt58 = data58[:, 0:3]
        cFl58 = data58[:, 3:6]

        sm58 = mkSimple3DModels(cubesPntsLst=cInt58, name='tof58-int')
        rd.ren = sm58.asActor(opa=0.35, col=(0, 0, 1))

        sm58f = mkSimple3DModels(linePntsLst=cFl58)
        rd.ren = sm58f.asActor()
        rd.ren = sm58f.drawSphereGlyphs(0.1, opa=1)



    rd.renWin.Render()
    rd.iren.Start()
    del rd
    print("\nEoF: %s" % os.path.basename(__file__))
