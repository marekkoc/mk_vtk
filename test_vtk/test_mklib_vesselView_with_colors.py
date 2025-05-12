#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
******************************************************************************************

Angio3D
(C) MK & AM

VesselView - soft to 3D visualization of numerical vascular tree described in *.ves file.

C: 2019.01.19
M: 2019.02.06
******************************************************************************************
"""

import os
import vtk
import numpy as np
import mklib_vtkrendering as mkr
import mklib_vtkpolydata_io as mkpdio

print(__doc__)


def get_MRICube_params_from_ves_file(fname):
    """
    Plik wyznacza parametry wykorzysane do zapisania drzewa w trojwymiarowym obrazie rastrowym w        programi MRISiulator (z 2008 roku). Procedura zostala powtórzona z poprzedniej wersji programu. Na podstawie maksymalnego i minimalnego wychylenia w osiach x,y,z wyznaczane jest najwieksze wychylenie jednej z 3 wspolrzednych (x,y,z), potem dla "bezpieczenstawa" dodajemy podwojona wartosc maksymalnego promienia w drzewie i mnozymy 2x. Tak zdefiniowana wartos uznajemy za rozmiar sceny i wyznaczamy rozmiar malego woksela (5 lub 3), rozmiar duzego wokslea oraz wektor przesuniecia punktow galezi odczytanych z pliku ves.

    wejscie: nazwa pliku ves opisujacego PELNE drzewo.
    wyjscie: vektor przesuniecia i rozmiar duzego woksela
    """

    # Load ves file to get maximum dimensions of vessel branches
    ves = np.loadtxt(fname, dtype=np.float64, delimiter=' ', skiprows=1)

    mx = ves[:,:-1].max()
    mn = ves[:,:-1].min()
    maxVal = np.max([np.abs(mn), np.abs(mx)])

    maxRadius = ves[:,-1].max()
    # rozmiar sceny w metrach
    realSizeMRICube = 2 * (maxVal + 2 * maxRadius)
    # rozmiar sceny w 3D (w metrach)
    realDim = np.array([realSizeMRICube, realSizeMRICube, realSizeMRICube])

    # wektor przesuniecia wspolrzednych (w malych wokselach) do srodka sceny aby pozbyc sie wspolrzednych o ujemnych wartosciach
    vesTrans = realDim / 2.0

    _voxelDim = 5 # liczba malych wokseli w duzym wokselu
    x, y, z = 256, 256, 256 # rozdzielczosc obrazu w skali duzych wokseli

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
    bigVoxelLen = _bigVoxelLen[0] # zakladam izotropowosc

    return vesTrans, bigVoxelLen


if __name__ == "__main__":

    randomColors = False

    vesname = 'test_vtk/normal01_4000_036.ves'
    #vesname = 'vtree_tra.ves'
    transVec, bigVoxelLen = get_MRICube_params_from_ves_file(vesname)
    ves = np.loadtxt(vesname, skiprows=1)

    # wyznaczam indeksy w obrazie rastrowym punktow bifurjacji odczytanych z zredukowanego (po usunieciu grubych galezi) pliku ves
    ves_tr = ves[:,:-1] + transVec[0]
    ves_tr = ves_tr / bigVoxelLen

    # TO DO:
    # wczytujemy wspolrzedne kolejnych punkow i zamieniamy wsp. x i z
    # MUSIMY DODAJ JESZCZE JEDEN PUNKT Z KONCA OSTATNIEJ GALEZI
    points = ves_tr
    #points = np.vstack((points, ves[-1, 15:12:-1]))
    #points += 0.5

   # odczytujemy wartosci promienia dla poszczegolnych galezi
    r = ves[:,-1]
    # zamieniamy wektor wierszowy w wektor kolumnowy
    r = r[:,np.newaxis]
    # wyliczamy dlugosc promienia w odniesieniu do dlugosci "duzych wokseli"
    # czyli to jest ta wartosc ktora wyliczamy nasza metoda segmentacji
    r_vox = r / bigVoxelLen
    del vesname

    # liczba punktow wezlowych
    Kpoints = points.shape[0]
    Kseg = len(r)  # 12

    appendedpolys = vtk.vtkAppendPolyData()
    appendedpolys.UserManagedInputsOn()
    appendedpolys.SetNumberOfInputs(Kseg)

    for k in range(Kseg):
        pts = vtk.vtkPoints()
        pts.SetNumberOfPoints(2)
        # Tutaj można zamienic kolejnosc wspolrzednych x i z!!!
        pts.SetPoint(0, *points[k,:3])
        pts.SetPoint(1, *points[k,3:])

        # CELKI / Komorki / linie
        polyLine = vtk.vtkCellArray()

        line = vtk.vtkLine()
        line.GetPointIds().SetId(0,0)
        line.GetPointIds().SetId(1,1)
        polyLine.InsertNextCell(line)

        # POLY DATA
        linesPolyData = vtk.vtkPolyData()
        linesPolyData.SetPoints(pts)
        linesPolyData.SetLines(polyLine)

        if randomColors:
            # kolory przypisujemy komorkom
            colors = vtk.vtkUnsignedCharArray()
            colors.SetNumberOfComponents(3)
            colors.SetName('Colors')
            colors.InsertNextTuple3(*np.random.randint(0, 255, 3))
            linesPolyData.GetCellData().AddArray(colors)
            linesPolyData.GetCellData().SetScalars(colors)
        else:
            tubeRadius = vtk.vtkDoubleArray()
            tubeRadius.SetName('TubeRadius')
            tubeRadius.SetNumberOfTuples(1)
            tubeRadius.SetTuple1(0, r_vox[k])
            # wartosci promienii wstawiamy do PUNKTOW wezlowych
            linesPolyData.GetCellData().AddArray(tubeRadius)
            linesPolyData.GetCellData().SetScalars(tubeRadius)


        tube = vtk.vtkTubeFilter()
        tube.SetInputData(linesPolyData)
        tube.SetNumberOfSides(80)
        tube.SetRadius(r_vox[k])
        tube.Update()

        # Zapis do pliku STL
        s = '-s{:02}'.format(k)
        fn = 'vtree_tra_br37-48' + s
        if 0: mkpdio.writeSTL( fn + '.stl', tube.GetOutput())
        if 0: mkpdio.writePolyData(fn + '.vtk', tube.GetOutput())

        appendedpolys.SetInputDataByNumber(k, tube.GetOutput())

    appendedpolys.Update()
    polydata = appendedpolys.GetOutput()

    fn = 'vtree_tra_all'
    if 1: mkpdio.writeSTL(fn + '.stl', polydata)
    if 1: mkpdio.writePolyData(fn + '.vtk', polydata)

    # Mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    mapper.ScalarVisibilityOn()
    mapper.SetScalarModeToUseCellFieldData()

    if randomColors:
        mapper.SelectColorArray('Colors')
    else:
        mapper.SelectColorArray('TubeRadius')

    renderer, renWin, iren = mkr.createMainVTKWindow()

    actor = vtk.vtkActor()
    actor.GetProperty().SetColor(1,0,0)
    actor.SetMapper(mapper)
    renderer.AddActor(actor)

    iren.Start()



    del renderer
    del renWin
    del iren

print('\nEOF: %s' % os.path.basename(__file__))