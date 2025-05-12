#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The module to deal with I/O operations on poyl datas.

Created on Sat Jul  6 14:01:17 2019
@author: mk

(C) MK & AM

C: 2019.07.06
M: 2019.07.07

v: 0.01
"""
import os
import vtk
from mkPolyData import mkPolyData

class mkPolyDataIO(mkPolyData):
    """
    C: 2019.07.06
    M: 2019.07.07
    """
    def __init__(self, poly=False, name="Poly Data"):
        super(mkPolyDataIO, self).__init__(poly, name)

    def writeSTL(self, filename, toASCII=True):
        """
        C: 2019.07.06
        M: 2019.07.06
        """
        stlWriter = vtk.vtkSTLWriter()
        stlWriter.SetFileName(filename)
        stlWriter.SetInputData(self.poly)
        if toASCII:
            stlWriter.SetFileTypeToASCII()
        else:
            stlWriter.SetFileTypeToBinary()
        stlWriter.Update()
        stlWriter.Write()

    def writePolyData(self, filename, toASCII=True):
        """
        formaty: VTK

        C: 2019.07.06
        M: 2019.07.06
        """
        writer = vtk.vtkPolyDataWriter()
        writer.SetInputData(self.poly)
        writer.SetFileName(filename)
        if toASCII:
            writer.SetFileTypeToASCII()
        else:
            writer.SetFileTypeToBinary()
        writer.Update()
        writer.Write()

    def readSTL(self, filename, asPolyData=True, name="PD from STL"):
        """
        asPolyData = True (returns poly data) / False (returns vtkActor)

        C: 2019.07.06
        M: 2019.07.07
        """
        reader = vtk.vtkSTLReader()
        reader.SetFileName(filename)
        reader.Update()
        self.poly = reader.GetOutput()
        self.name = name
        if asPolyData:
            return self.poly
        else:
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(reader.GetOutput())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            return actor

    def readVTKGeometry(self, filename, asPolyData=True, name="PD from VTK"):
        """
        Reads VTK file format
        asPolyData = True (returns poly data) / False (returns vtkActor)

        Input: filename.vtk
        Output: actor

        C: 2019.07.06
        M: 2019.07.07
        """
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(filename)
        reader.Update()  # Needed because of GetScalarRange
        output = reader.GetOutput()

        usg = vtk.vtkGeometryFilter()
        usg.SetInputData(output)
        usg.Update()
        self.poly = usg.GetOutput()
        self.name = name

        if asPolyData:
            return self.poly
        else:
            scalar_range = output.GetScalarRange()
            mapper = vtk.vtkDataSetMapper()
            mapper.SetInputData(output)
            mapper.SetScalarRange(scalar_range)
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            return actor

    @staticmethod
    def replaceCommasAndDots(fname, read):
        """
        if not Read than Write!
        - Read - needs commas
        - Write - needs dots

        C: 2019.07.07
        M: 2019.07.07
        """
        fn, ext = os.path.splitext(fname)

        f = open(fname, 'r')
        f2 = open('tmp.stl', 'w')
        lines = f.readlines()
        for line in lines:
            if read:
                if '.' in line and line[0] is not '#':
                    line = line.replace('.', ',')
            # write
            else:
                if ',' in line:
                    line = line.replace(',', '.')
            f2.write(line)
        f.close()
        f2.close()
        os.rename('tmp.stl', fname)



if __name__ == '__main__':

    from mkPolyData import mkPolyData
    from mkRenderer import mkRenderer

    rd = mkRenderer()
    rd.displayAxesWXYZ0()

    if 0:
        io = mkPolyDataIO()
        fname = '../../all_data/tof_2_22_34_37_58_66-COM.stl'
        fname = '../../all_data/voxesl3-ascii.stl'

        #io.replaceCommasAndDots(fname, read=True)
        pdstl = io.readSTL(fname, True)
        pdact = io.readSTL(fname, False)

        io.writeSTL(fname)
        io.replaceCommasAndDots(fname, read=False)

        io.info()
        rd.ren = pdact

    if 0:
        fname = '../../all_data/bg01-bin.stl'

        io = mkPolyDataIO()
        pdstl = io.readSTL(fname, True)
        pdact = io.readSTL(fname, False)
        #io.writeSTL('bg01-bin22.stl', toASCII=False)

        io.info()
        rd.ren = pdact

    if 0:
        fname = '../../all_data/voxels3-ascii.vtk'

        io = mkPolyDataIO()
        # UWAGA format VTK nie musimy zamieniac na przecinki
        # przy wczytywaniu
        pdvtk = io.readVTKGeometry(fname, True)
        io.info()

        pdvtkact = io.readVTKGeometry(fname, False)
        rd.ren = pdvtkact

        io.writePolyData(fname, toASCII=True)
        io.replaceCommasAndDots(fname, read=False)

    if 1:
        fname = '../../all_data/voxels3-bin.vtk'
        io = mkPolyDataIO()
        pdvtk = io.readVTKGeometry(fname, True)
        io.info()

        pdvtkact = io.readVTKGeometry(fname, False)
        rd.ren = pdvtkact

        io.writePolyData('output/yyy-bin.vtk', toASCII=False)



    rd.renWin.Render()
    rd.iren.Start()
    del rd
    print("\nEoF: %s" % os.path.basename(__file__))
