#!/usr/bin/env python
# -*- coding: utf-8 -*-
#vim: set ff=unix:
"""


Created on Sat Jul  6 22:37:11 2019
@author: mk

(C) MK & AM

C: 2019.07.06
M: 2019.07.10

v: 0.01
"""
import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk


class mkVtkImage(object):
    """
    C: 2019.07.06
    M: 2019.07.06

    v: 0.01
    """
    def __init__(self, data=None, name='Vtk image'):
        self.img = data
        self._name = name

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, data):
        if isinstance(data,  vtk.vtkImageData):
            self._img = data
        else:
            self._img = None

    @property
    def name(self):
        return self._name

    def info(self):
        if self.img is None:
            print('There is NO vtkImage!')
            return
        print(50*'*')
        s = "*** " + self.name + " ***"
        print(s)
        print(len(s)*'*')
        dataDimension = self.img.GetDataDimension()
        print("* dataDimension = ", dataDimension)
        voxelType = self.img.GetScalarTypeAsString()
        print('* voxelType = ', voxelType)
        origin = self.img.GetOrigin()
        print('* origin = ', origin)
        spacing = self.img.GetSpacing()
        print('* spacing = ', spacing)
        dimensions = self.img.GetDimensions()
        print('* dimensions = ', dimensions)
        extent = self.img.GetExtent()
        print('* extent = ', extent)
        bounds = self.img.GetBounds()
        print('* bounds = ', bounds)
        numberOfPoints = self.img.GetNumberOfPoints()
        print('* numberOfPoints =', numberOfPoints)
        length = self.img.GetLength()
        print('* length = ', length)
        print(50*'*')

    def setSpacing(self, sp=[1, 1, 1]):
        if self.img is not None:
            self.img.SetSpacing(*sp)

    def setOrigin(self, orig=[0, 0, 0]):
        if self.img is not None:
            self.img.SetOrigin(*orig)

    def convertVtkImageToNumpy(self):
        """
        C: 2019.07.06
        M: 2019.07.10
        """
        r, c, s = self.img.GetDimensions()
        sc = self.img.GetPointData().GetScalars()

        array = vtk_to_numpy(sc)
        array = array.reshape(r, c, s, order='F')
        return array

    def convertNumpyArrayToVtkImage(self, array,
                                    origin=[0, 0, 0], spacing=[1, 1, 1],
                                    atype=vtk.VTK_UNSIGNED_SHORT):
        """
        C: 2019.07.06
        M: 2019.07.10
        """

        vtkimage = numpy_to_vtk(array.flatten('F'), deep=1, array_type=atype)
        image1 = vtk.vtkImageData()
        image1.GetPointData().SetScalars(vtkimage)
        image1.SetDimensions(array.shape)
        image1.SetOrigin(origin)
        image1.SetSpacing(spacing)
        self.img = image1

    @staticmethod
    def npInfo(im, name="Numpy array"):
        print((len(name) + 8)*'*')
        s = "*** " + name + " ***"
        print(s)
        print(len(s)*'*')
        print("max={}, min={}, aver={:.2f}, dtype={}, shape={}".format(im.max(), im.min(), im.mean(), im.dtype, im.shape))

    ### Extract ROI - Nie dziala
    def extractVoi(self, region=[0,50,0,50,0,35], sampleRate=[1,1,1]):
        voi = vtk.vtkExtractVOI()
        voi.SetInputData(self.img)
        voi.SetVOI(*region)
        voi.SetSampleRate(*sampleRate)
        voi.Update()
        return voi.GetOutput()

    def resampleVtkImage(self, spacing=[1,1,1], method='cubic'):
        """
        method = 'cubic' / 'linear' / 'nearest'

        https://coderwall.com/p/gij2va/resample-3d-image-data-in-a-vtkimagedata-object-using-the-vtkimagereslice-class
        """
        resliceFilter = vtk.vtkImageReslice()
        resliceFilter.SetInputData(self.img)
        resliceFilter.SetOutputSpacing(*spacing)
        resliceFilter.SetOutputOrigin(self.img.GetOrigin())
        if method == 'cubic':
            resliceFilter.SetInterpolationModeToCubic()
            print("Interpolation method: Cubic")
        elif method == 'linear':
            resliceFilter.SetInterpolationModeToLinear()
            print("Interpolation method: Linear")
        elif method == 'nearest':
            resliceFilter.SetInterpolationModeToNearestNeighbor()
            print("Interpolation method: Nearest Neighbor")
        else:
            print("Wrong interpolation method name!!!")
        resliceFilter.Update()
        return resliceFilter.GetOutput()

    @staticmethod
    def stringPattern(someString, pattern='x'):
        ln = len(someString)
        p0 = pattern
        p1 = p0 * (10+ln)
        print(p1)
        print("{} {} {}".format(4*p0, someString, 4*p0))
        print(p1)


if __name__ == '__main__':
    import os

    from mkVtkImageIO import mkVtkImageIO

    if 0:
        fname = '../../all_data/t2_tse_sag_2mm.vtk'
        viio = mkVtkImageIO()
        viio.readVTKImage(fname)

        vi = mkVtkImage(viio.img, 'Wczytany VTK')
        vi.info()
        a = vi.convertVtkImageToNumpy()
        vi.npInfo(a)

    if 0:
        a = np.random.randint(0, 255, (100, 100, 100), dtype=np.uint16)
        vi = mkVtkImage()
        vi.convertNumpyArrayToVtkImage(a, origin=[19,15,20], spacing=[.7, .8, .9])
        vi.npInfo(a)
        vi.info()

        viio = mkVtkImageIO(vi.img, 'From a NUMPY')
        viio.writeAsVTKImage()

    if 0:  #  nie dziala!!! - chyba trzeba przepisac QFormMatrix, SFormMatrix
#        fname = 't2_tse_sag_2mm.vtk'
#        viio = mkVtkImageIO(name='ORYG')
#        viio.readVTKImage(fname)
#        viio.info()

        fname = '../../all_data/normal01_4000_036_5_256_N00.raw'
        ex = mkVtkImageIO(name='ORYG')
        ex.readRawImage(fname)
        ex.info()

        voi = ex.extractVoi([0, 50, 0, 60, 0, 40])
        voiio = mkVtkImageIO(voi, 'VOI')
        voiio.info()
        voiio.writeAsVTKImage('voi-vtk.vtk')
        voiio.writeAsNIFTIImage('voi-nii.nii')

    if 0:
        fname = '../../all_data/t2_tse_sag_2mm.vtk'
        viio = mkVtkImageIO(name='ORYG')
        viio.readVTKImage(fname)
        viio.info()

        res = viio.resampleVtkImage([0.32, 0.32, 0.32])
        resio = mkVtkImageIO(res, "RESAMPLED")
        resio.info()
        resio.writeAsVTKImage('resampled.vtk')

    if 0:  # roiExtractor jeszcze raz - tym razem dziala!!!
        """
        Niby wszystko dziala, zapis i odczyt. Jednak ITKSNAP
        obrazy vtk wyswietla jako liczby zmienno przecinkowe w zakresie 0-1
        zatem tracimy informacje o rzeczywistych wartosciach. Jednak
        zapis i odczyt zachowuja oryginalny typ danych.
        """
        fname = '../../all_data/normal01_4000_036_5_256_N00.raw'
        rd = mkVtkImageIO(name="Oryg")
        rd.readRawImage(fname)
        rd.info()

        ex = mkVtkImageIO(rd.img, 'EXT')
        ex.info()
        voi = ex.extractVoi(region=[100, 150, 100, 160, 100, 180])
        v = mkVtkImageIO(voi, "ROI")
        v.info()
        v.writeAsVTKImage('voi3.vtk')

    if 1:
        fname = '../../all_data/normal01_4000_036_5_256_N00.vtk'
        org = mkVtkImageIO(name='Oryg -vtk')
        org.readVTKImage(fname)
        org.info()
        npim = org.convertVtkImageToNumpy()
        org.npInfo(npim)
        npim = npim.astype(np.uint16)
        npim = npim * 2
        org.npInfo(npim)
        oryg = org.img.GetOrigin()
        sp = org.img.GetSpacing()
        org.convertNumpyArrayToVtkImage(npim,
                                    origin=oryg, spacing=sp,
                                    atype=vtk.VTK_UNSIGNED_SHORT)
        org.info()
        org.writeAsVTKImage('normal01-float.vtk')


    print("\nEoF: %s" % os.path.basename(__file__))
