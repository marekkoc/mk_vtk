#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Created on Fri Jan 18 11:23:15 2019
@author: marek

Zamykaie okna:
https://stackoverflow.com/questions/15639762/close-vtk-window-python
Linie:
https://vtk.org/Wiki/VTK/Examples/Python/GeometricObjects/Display/ColoredLines

C: 2019.01.18
M: 2019.01.19


UWAGA:
TO JEST KOPIA PLIKU!
ORYGINAL ZNAJDUJE SIE W KATALOGU:
    /home/marek/Dropbox/To_synchro/work/all_python/test_vtk

TEN PLIK ZLE DZIALA
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

import os
import vtk
import numpy as np
import mklib_vtkrendering as mkr
#import mklib_vtkpolydata as mkp
import mklib_vtkpolydata_io as mkio
import mklib_vtkpolydata_visualization as mkv

print(__doc__)

if __name__ == "__main__":

    renderer, renWin, iren = mkr.createMainVTKWindow()

    vesname = 'test_vtk/normal01_4000_036_Rth-2-vox-con.npy'
    #vesname = 'vtree_tra.npy'
    ves = np.load(vesname)

    # wczytujemy wspolrzedne kolejnych punkow i zamieniamy wsp. x i z
    points = ves[:, 12:9:-1] + 0.5
    r = ves[:, -1]
    #del ves, vesname

    # liczba punktow wezlowych - 12, zatem mamy 11 galezi
    Kseg = points.shape[0]

    # tablica na losowo wybrane kolory
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName('Colors')
    for k in range(Kseg):
        colors.InsertNextTuple(np.random.randint(0, 255, 3))

    # tbalica na wartosci promieni dla poszczegolnych segmentow
    tubeRadius = vtk.vtkDoubleArray()
    tubeRadius.SetName('TubeRadius')
    tubeRadius.SetNumberOfTuples(12)
    for i in range(len(r)):
        tubeRadius.SetTuple1(i, r[i])

    # wywolujemy funkcje ktora rysuje linie pomiedzy punktami
    # wezlowymi i zwraca obiekt polyData
    linesPolyData = mkv.linesBetweenPointSet(points)

    # wartosci promienii wstawiamy do PUNKTOW wezlowych
    linesPolyData.GetPointData().AddArray(tubeRadius)
    linesPolyData.GetPointData().SetActiveScalars('TubeRadius')

    # kolory przypisujemy komorkom
    linesPolyData.GetCellData().SetScalars(colors)

    # filtr ktory rysuje cylindry dookola linii
    tube = vtk.vtkTubeFilter()
    tube.SetInputData(linesPolyData)
    tube.SetNumberOfSides(20)
    #tube.SetRadius(5)

    #tube.SetVaryRadius(1)
    tube.SetVaryRadiusToVaryRadiusByAbsoluteScalar()
    #tube.SetVaryRadiusToVaryRadiusByScalar()
    tube.Update()

    # Zapis do pliku STL
    if 0: mkio.writeSTL('tree.stl', tube.GetOutput())
    if 0: mkio.writePolyData('tree.vtk', tube.GetOutput())

    # Mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(tube.GetOutput())
    mapper.ScalarVisibilityOn()
    mapper.SetScalarModeToUseCellFieldData()
    #mapper.SetScalarModeToUsePointFieldData()
    mapper.SelectColorArray('Colors')

    actor = vtk.vtkActor()
    actor.GetProperty().SetColor(1,0,0)
    actor.SetMapper(mapper)
    renderer.AddActor(actor)

    iren.Start()
    del renderer
    del renWin
    del iren

print('EOF: %s' % os.path.basename(__file__))