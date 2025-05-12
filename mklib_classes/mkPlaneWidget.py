#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


Created on Mon Jul  8 17:52:34 2019
@author: marek

(C) MK & AM

C: 2019.07.08
M: 2019.07.08

v: 0.01
"""
import vtk
import numpy as np
from vtk.util.numpy_support import numpy_to_vtk


class mkPlaneWidget(object):
    """
    UWAGA:
        Obiekty trzeba skasowac recznie na koncu skryptu!

    C: 2019.07.08
    M: 2019.07.22
    """
    def __init__(self, ren, iren, data, dr,
                 dataOrder='C', origin=[0, 0, 0], spacing=[1, 1, 1],
                 atype=vtk.VTK_UNSIGNED_SHORT, name='Some Plane Widget'):
        """
        2019.07.22 - parametry dataOrder, spacing, origin, atype dodano do konstruktora
                    i zapisano jako parametry obiektu, aby wykorzystac w funkcji
                    _np2vtk(). Konieczna była możliwość zmiany kierunku odczytu danych w
                    macierzy pomiędzy "C" i "F".

        C: 2019.07.08
        M: 2019.07.22
        """
        self._origin = origin
        self._spacing = spacing
        self._dataOrder = dataOrder
        self._atype = atype
        self.img = data
        self._name = name
        self._ren = ren
        self._iren = iren
        self._dir = dr
        self.crossSection()

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, data):
        if isinstance(data,  vtk.vtkImageData):
            self._img = data
            self._x, self._y, self._z = data.GetDimensions()
        elif isinstance(data, np.ndarray):
            self._img = self._np2vtk(data)
            self._x, self._y, self._z = data.shape
        else:
            self._img = None
            self._x, self._y, self._z = 0, 0, 0

    def _np2vtk(self, array):
        """
        C: 2019.07.08
        M: 2019.07.22
        """
        origin = self._origin
        spacing = self._spacing
        atype = self._atype
        dataOrder = self._dataOrder

        vtkimage = numpy_to_vtk(array.flatten(dataOrder), deep=1, array_type=atype)
        image1 = vtk.vtkImageData()
        image1.GetPointData().SetScalars(vtkimage)
        image1.SetDimensions(array.shape)
        image1.SetOrigin(origin)
        image1.SetSpacing(spacing)
        return image1


    def crossSection(self):
        self.planeWidget_ = vtk.vtkImagePlaneWidget()
        self.planeWidget_.DisplayTextOn()
        self.planeWidget_.SetInputData(self._img)

        if self._dir.lower() == 'x':
            dim = self._x
            col = (1, 0, 0)
            self.planeWidget_.SetPlaneOrientationToXAxes()
        if self._dir.lower() == 'y':
            dim = self._y
            col = (0, 1, 0)
            self.planeWidget_.SetPlaneOrientationToYAxes()
        if self._dir.lower() == 'z':
            dim = self._z
            col = (0, 0, 1)
            self.planeWidget_.SetPlaneOrientationToZAxes()

        self.planeWidget_.SetSliceIndex(dim//2)
        self.planeWidget_.RestrictPlaneToVolumeOn()
        self.planeWidget_.SetKeyPressActivationValue(self._dir)
        self.planeWidget_.GetPlaneProperty().SetColor(*col)
        self.planeWidget_.SetResliceInterpolateToNearestNeighbour()
        self.planeWidget_.SetInteractor(self._iren)
        self.planeWidget_.On()
        #return self.planeWidget_


if __name__ == '__main__':
    import os
    from mkReader import mkReader
    from mkRenderer import mkRenderer
    from mkVtkImageIO import mkVtkImageIO

    rd = mkRenderer()
    rd.displayAxesWXYZ0(scale=(25,25,25))
    rd.displayUnitSphereWXYZ(rad=5)

    if 1:
            fname = '../../all_data/bg01cm_x1.nii'
            #fname = '../../all_data/t2_tse_tra_2mm.nii'
            vt = mkVtkImageIO(name='t2_tse_tra_2mm.nii')
            vt.readNIFTIImage(fname)
            vt.info()
            sx ,sy, sz = vt.img.GetDimensions()
            spx, spy, spz = vt.img.GetSpacing()
            rd.displayPlaneWXYZ0(delXY=[10, 10], xRng=[0, sx*spx], yRng=[0, sy*spy])

            pw1 = mkPlaneWidget(rd.ren, rd.iren, vt.img, dr='X')
            pw2 = mkPlaneWidget(rd.ren, rd.iren, vt.img, dr='y')
            pw3 = mkPlaneWidget(rd.ren, rd.iren, vt.img, dr='z')

            rd.renWin.Render()
            rd.iren.Start()
            del pw1
            del pw2
            del pw3
    if 0:
        npimg = np.random.randint(0, 256, size=(100, 150, 180))
        pw1 = mkPlaneWidget(rd.ren, rd.iren, npimg, dr='X')
        pw2 = mkPlaneWidget(rd.ren, rd.iren, npimg, dr='Y')

        rd.renWin.Render()
        rd.iren.Start()
        del pw1, pw2

    if 0:
        fname = '../../all_data/bg01cm_x1.nii'
        i1 = mkReader(fname)
        im1 = i1.loadData()
        print(type(im1), im1.dtype, im1.shape)

        im1pw = mkPlaneWidget(rd.ren, rd.iren, im1 , dr='X', dataOrder='F')

        rd.renWin.Render()
        rd.iren.Start()
        del im1pw

    del rd
    print("\nEoF: %s" % os.path.basename(__file__))
