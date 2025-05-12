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

C: 2019.01.19
M: 2019.01.19


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

import os
import vtk
import numpy as np
import mklib_vtkrendering as mkr
import mklib_vtk as mkp

print(__doc__)


def get_MRICube_params_from_ves_file(fname):
    """
    Plik wyznacza parametry wykorzysane do zapisania drzewa w trojwymiarowym obrazie rastrowym w        programi MRISiulator (z 2008 roku). Procedura zostala powtórzona z poprzedniej wersji programu. Na podstawie maksymalnego i minimalnego wychylenia w osiach x,y,z wyznaczane jest najwieksze wychylenie jednej z 3 wspolrzednych (x,y,z), potem dla "bezpieczenstawa" dodajemy podwojona wartosc maksymalnego promienia w drzewie i mnozymy 2x. Tak zdefiniowana wartos uznajemy za rozmiar sceny i wyznaczamy rozmiar malego woksela (5 lub 3), rozmiar duzego wokslea oraz wektor przesuniecia punktow galezi odczytanych z pliku ves.

    wejscie: nazwa pliku ves opisujacego PELNE drzewo.
    wyjscie: vektor przesuniecia i rozmiar duzego woksela
    """

    # Load ves file to get maximum dimensions of vessel branches
    ves = np.loadtxt(fname, dtype=np.float, delimiter=' ', skiprows=1)

    mx = ves[:, :-1].max()
    mn = ves[:, :-1].min()
    maxVal = np.max([np.abs(mn), np.abs(mx)])

    maxRadius = ves[:, -1].max()
    # rozmiar sceny w metrach
    realSizeMRICube = 2 * (maxVal + 2 * maxRadius)
    # rozmiar sceny w 3D (w metrach)
    realDim = np.array([realSizeMRICube, realSizeMRICube, realSizeMRICube])

    # wektor przesuniecia wspolrzednych (w malych wokselach) do srodka sceny aby pozbyc sie wspolrzednych o ujemnych wartosciach
    vesTrans = realDim / 2.0

    _voxelDim = 5  # liczba malych wokseli w duzym wokselu
    x, y, z = 256, 256, 256  # rozdzielczosc obrazu w skali duzych wokseli

    # rozdzielczosc obrazu w skali malych wokseli dla x,y,z
    _xRes = x * _voxelDim
    _yRes = y * _voxelDim
    _zRes = z * _voxelDim
    # rozdzielczosc macierz 3D w ktorej bedzie odzworowana scena
    voxRealRes = np.array([_xRes, _yRes, _zRes])

    # dlugosc malego woksela
    _voxelLen = realDim / voxRealRes

    # dlugosc duzego woksela
    _bigVoxelLen = _voxelLen * _voxelDim
    # zmienna dodatkowa przy zalozenia ze woksel jest izotropowy, aby uproscic obliczenia
    bigVoxelLen = _bigVoxelLen[0]  # zakladam izotropowosc

    return vesTrans, bigVoxelLen


if __name__ == "__main__":

    # vesname = 'normal01_4000_036_Rth-2-vox-con.npy'
    vesname = 'test_vtk/vtree_tra_con-br37-48.npy'
    ves = np.load(vesname)

    # wczytujemy wspolrzedne kolejnych punkow i zamieniamy wsp. x i z
    # MUSIMY DODAJ JESZCZE JEDEN PUNKT Z KONCA OSTATNIEJ GALEZI
    points = ves[:, 12:9:-1]
    points = np.vstack((points, ves[-1, 15:12:-1]))
    points += 0.5

    r = ves[:, -1]
    del vesname

    # liczba punktow wezlowych - 13, zatem mamy 12 galezi
    Kpoints = points.shape[0]  # 13
    Kseg = len(r)  # 12

    appendedpolys = vtk.vtkAppendPolyData()
    appendedpolys.UserManagedInputsOn()
    appendedpolys.SetNumberOfInputs(12)

    for k in range(Kseg):

        pts = vtk.vtkPoints()
        pts.SetNumberOfPoints(2)
        pts.SetPoint(0, *points[k])
        pts.SetPoint(1, *points[k+1])

        # CELKI / Komorki / linie
        polyLine = vtk.vtkCellArray()

        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 0)
        line.GetPointIds().SetId(1, 1)
        polyLine.InsertNextCell(line)

        # POLY DATA
        linesPolyData = vtk.vtkPolyData()
        linesPolyData.SetPoints(pts)
        linesPolyData.SetLines(polyLine)

        # kolory przypisujemy komorkom
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName('Colors')
        colors.InsertNextTuple3(*np.random.randint(0, 255, 3))

        linesPolyData.GetCellData().AddArray(colors)
        linesPolyData.GetCellData().SetScalars(colors)

        tube = vtk.vtkTubeFilter()
        tube.SetInputData(linesPolyData)
        tube.SetNumberOfSides(80)
        tube.SetRadius(r[k])
        tube.Update()

        # Zapis do pliku STL
        s = '-s{:02}'.format(k)
        fn = 'vtree_tra_br37-48' + s
        if 0 : mkp.writeSTL( fn + '.stl', tube.GetOutput())
        if 0 : mkp.writePolyData(fn + '.vtk', tube.GetOutput())

        appendedpolys.SetInputDataByNumber(k, tube.GetOutput())

    appendedpolys.Update()
    polydata = appendedpolys.GetOutput()

    fn = 'vtree_tra_br37-48'
    if 0: mkp.writeSTL(fn + '.stl', polydata)
    if 0: mkp.writePolyData(fn + '.vtk', polydata)

    # Mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    mapper.ScalarVisibilityOn()
    mapper.SetScalarModeToUseCellFieldData()
    mapper.SelectColorArray('Colors')

    renderer, renWin, iren = mkr.createMainVTKWindow()

    actor = vtk.vtkActor()
    actor.GetProperty().SetColor(1, 0, 0)
    actor.SetMapper(mapper)
    renderer.AddActor(actor)

    iren.Start()

    del renderer
    del renWin
    del iren

print('\nEOF: %s' % os.path.basename(__file__))
