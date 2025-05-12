#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A module with util function class.

Created on Thu Jul 11 22:46:15 2019
@author: mk

(C) MK & AM

C: 2019.07.11
M: 2019.07.11

v: 0.01
"""
import vtk
import numpy as np

from mkSurface import mkSurface
from mkRenderer import mkRenderer
from mkSimple3DModels import mkSimple3DModels


class mkUtils(object):
    """
    C: 2019.07.11
    M: 2019.07.11
    """
    def __init__(self):
        print('Util object created :)')

    @staticmethod
    def npImageFromVoxelCoordinates(voxMatrix):
        if isinstance(voxMatrix, (list, np.ndarray)):
            if isinstance(voxMatrix, list):
                voxMatrix = np.array(voxMatrix)
            mx, my, mz = voxMatrix.max(0)
            data = np.zeros((mx+1, my+1, mz+1), dtype=np.uint16)
            x, y, z = voxMatrix[:, 0], voxMatrix[:, 1], voxMatrix[:, 2]
            data[x,y,z] = 1
            return data

    @staticmethod
    def textWrap(fname = ''):
        """
        C: 2019.06.18
        M: 2019.06.22
        """
        if not len(fname):
            fname=os.path.basename(__file__)
        print()
        p = len(fname) + 8
        print(p * '#')
        print("### %s ###" % fname)
        print(p * '#')




if __name__ == '__main__':
    import os

    if 1:
        a = (0, 0, 2)
        b = (0, 0, 3)
        c = (0, 1, 3)
        d = (1, 1, 3)
        e = (1, 2, 3)
        lst = [a, b, c, d, e]

        u = mkUtils()
        data = u.npImageFromVoxelCoordinates(lst)

        # sprawdzenie indeksow w macierzy
        x,y,z = np.where(data > 0)
        idx = np.vstack((x, y, z)).T
        print(idx)


        s = mkSurface(data)
        vox = s.processVoxels()

        sm = mkSimple3DModels(cubesPntsLst=vox)

        rd = mkRenderer()
        # rd.displayAxesWXYZ0(scale=(1,1,1))
        # rd.displayPlaneWXYZ0(yRng=[-1,2])
        # rd.displayUnitSphereWXYZ(rad=0.5, opa=0.4)

        rd.ren = sm.asActor(opa=0.8)

        rd.renWin.Render()
        rd.iren.Start()
        del rd
        print("\nEoF: %s" % os.path.basename(__file__))



