#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The module to read, save and convert vtkImage to/from Numpy N-D array.

Created on Sat Jul  6 21:51:13 2019
@author: mk

(C) MK & AM

C: 2019.07.06
M: 2019.07.10

v: 0.01
"""
import vtk
from mkVtkImage import mkVtkImage

class mkVtkImageIO(mkVtkImage):
    """
    C: 2019.07.06
    M: 2019.07.07
    """
    def __init__(self, img=None, name='A vtk image'):
        super(mkVtkImageIO, self).__init__(img, name)

        self._NIFTI_header_ = None

    @property
    def NIFTI_header_(self):
        """
        C: 2019.07.08
        M: 2019.07.08
        """
        if self._NIFTI_header_ is not None:
            return self._NIFTI_header_
        else:
            print('There is NO NIFTI header!')
            return None

    @NIFTI_header_.setter
    def NIFTI_header_(self, hdr):
        """
        C: 2019.07.08
        M: 2019.07.08
        """
        self._NIFTI_header_ = hdr

    def print_NIFTI_header(self):
        if hasattr(self, '_NIFTI_header_'):
            print(self._NIFTI_header_)

    def readDicomImage(self, folderName):
        """
        C: 2019.07.06
        M: 2019.07.06
        """
        reader = vtk.vtkDICOMImageReader()
        reader.SetDirectoryName(folderName)
        reader.Update()
        self.img = reader.GetOutput()

    def readRawImage(self, filename,**kw):
        """
        C: 2019.07.06
        M: 2019.07.06
        """
        origin = kw.get('origin', [0, 0, 0])
        spacing = kw.get('spacing', [1.0, 1.0, 1.0])
        dim = kw.get('dim', 3)
        dtype = kw.get('dtype', vtk.VTK_UNSIGNED_CHAR)
        extent = kw.get('extent', [0, 255, 0, 255, 0, 255])

        readerVolume = vtk.vtkImageReader()
        readerVolume.SetDataScalarType(dtype)
        readerVolume.SetFileDimensionality(dim)
        readerVolume.SetDataExtent(*extent)
        readerVolume.SetDataSpacing(*spacing)
        readerVolume.SetDataOrigin(*origin)
        readerVolume.SetNumberOfScalarComponents(1)
        # readerVolume.SetDataByteOrderToBigEndian()
        readerVolume.SetFileName(filename)
        readerVolume.Update()
        self.img = readerVolume.GetOutput()

    def readVTKImage(self, filename):
        """
        C: 2019.07.06
        M: 2019.07.06
        """
        reader = vtk.vtkStructuredPointsReader()
        reader.SetFileName(filename)
        reader.Update()
        self.img = reader.GetOutput()

    def readNIFTIImage(self, filename):
        """
        C: 2019.07.06
        M: 2019.07.08
        """
        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileName(filename)
        reader.Update()
        self.img = reader.GetOutput()
        self.NIFTI_header_ = reader.GetNIFTIHeader()
        return reader

    def writeAsVTKImage(self, filename='xxx.vtk'):
        """
        C: 2019.07.06
        M: 2019.07.06
        """
        writer = vtk.vtkStructuredPointsWriter()
        writer.SetInputData(self.img)
        writer.SetFileName(filename)
        writer.Update()
        writer.Write()

    def writeAsNIFTIImage(self, filename='xxx.nii.gz', withHeader=False):
        """
        C: 2019.07.06
        M: 2019.07.10
        """
        writer = vtk.vtkNIFTIImageWriter()
        writer.SetInputData(self.img)
        writer.SetFileName(filename)

        if withHeader:
            # copy most information directory from the header
            writer.SetNIFTIHeader(self.NIFTI_header_)
            # this information will override the reader's header
#            writer.SetQFac(readerWithHeader.GetQFac())
#            writer.SetTimeDimension(readerWithHeader.GetTimeDimension())
#            writer.SetQFormMatrix(readerWithHeader.GetQFormMatrix())
#            writer.SetSFormMatrix(readerWithHeader.GetSFormMatrix())
        writer.Update()
        writer.Write()




if __name__ == '__main__':
    import os

    from mkVtkImage import mkVtkImage

    if 0:
        im = mkVtkImageIO()
        fname = '../../all_data/1.3.12.2.1107.5.2.30.27640.2017070314003110363513030.0.0.0'
        im.readDicomImage(fname)

        vim = mkVtkImage(im.img, 'dicom')
        vim.info()
    if 0:
        im = mkVtkImageIO()
        fname = '../../all_data/normal01_4000_036_5_256_N00.raw'
        im.readRawImage(fname)

        vim = mkVtkImage(im.img, 'raw')
        vim.setSpacing([2, 2, 2.5])
        vim.setOrigin([-80, -77, 100])
        vim.info()
    if 0:
        im = mkVtkImageIO()
        fname = '../../all_data/T1_ad.vtk'
        im.readVTKImage(fname)
        vim = mkVtkImage(im.img, 'T1_ad - vtk')
        vim.info()
    if 0:
        im = mkVtkImageIO()
        fname = '../../all_data/t2_tse_sag_2mm.nii'
        red = im.readNIFTIImage(fname)
        vim = mkVtkImage(im.img, 't2_tse_sag_2mm - NIFTI')
        vim.info()
    if 0:
        im = mkVtkImageIO()
        fname = '../../all_data/t2_tse_sag_2mm.vtk'
        im.readVTKImage(fname)
        im.writeAsVTKImage()
    if 0:
        im = mkVtkImageIO()
        fname = '../../all_data/t2_tse_tra_2mm.nii'
        reader = im.readNIFTIImage(fname)
        # im.setSpacing([2, 2, 2.5])
        # im.setOrigin([-80, -77, 100])
        im.writeAsNIFTIImage('output/nii2nii2.nii.gz', reader)

    print("\nEoF: %s" % os.path.basename(__file__))
