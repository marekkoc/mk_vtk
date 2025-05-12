#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A module with definition and testing of mkSurface class.

Created on Tue Jun 25 15:43:39 2019
@author: marek

(C) MK & AM

C: 2019.06.25
M: 2019.07.11

v: 0.02
"""

import numpy as np

from mkReader import mkReader
from mkVoxel import mkVoxel


class mkSurface(object):
    """
    The class to define the boundary voxels of an binary 3D object. Ones can separate an outer voxels from inner voxels of an image object.

    _allVoxels_ - the list of mkVoxel objects (centers are in agreement with oryginal image, not extended one!)
    - innerVoxels_ - the list of mkVoxel objects that are inside the objects (are surrounded by other voxels.)
    - outerVoxels_ -the list of mkVoxlel objects that are external object voxels. They contain at least one fvoxel face.

    C: 2019.06.25
    M: 2019.07.03
    """
    _imge = None

    def __init__(self, data):
        if isinstance(data, np.ndarray):
            self._objVoxelCount_ = -1
            sx, sy, sz = data.shape
            # extended image
            mkSurface._imge = np.zeros((sx+2, sy+2, sz+2), dtype=data.dtype)
            mkSurface._imge[1:-1, 1:-1, 1:-1] = data.copy()
        else:
            print()

    @classmethod
    def get_imge(cls):
        return cls._imge

    @property
    def voxCount_(self):
        return self._objVoxelCount_

    # lista wszystkich wokseli (obietky klasy mkVoxel)
    @property
    def allVoxels_(self):
        return self._allVoxels_

    @property
    def innerVoxels_(self):
        return self._innerVoxels_

    @property
    def outerVoxels_(self):
        return self._outerVoxels_

    def _checkVoxelNeighbours(self, v):
        """
        The function checks if 6 wall neighbors of current voxel exists. If any exists, the appropriate face is not modeled with triangles - a False flag is set in voxel's ngbr list.
        The voxesl is created with the use of oryginal image spatial coordinates - not with the extended image - so, there is why the 1 is subtracted from each x, y, z coordinate.

        C: 2019.06.26
        M: 2019.07.03
        """
        x, y, z = v
        ie = self.get_imge()
        front = back = right = left = top = bottom = True
        if ie[x, y, z+1] == 1:
            front = False
        if ie[x, y, z-1] == 1:
            back = False
        if ie[x+1, y, z] == 1:
            right = False
        if ie[x-1, y, z] == 1:
            left = False
        if ie[x, y+1, z] == 1:
            top = False
        if ie[x, y-1, z] == 1:
            bottom = False
        ngbrs = [front, back, right, left, top, bottom]
        # Voxels are stored with accordance with oryginal image! Not extended image.
        vx = mkVoxel([x-1, y-1, z-1], nb=ngbrs)
        return vx

    def processVoxels(self, voxMatrix=None, inc1=True):
        """
        Function analyzes neighborhod of each voxele under consideration. If voxMatrix is equalled to None all foreground voxels in extended image are analyzied. If voxMatrix is a numpy matrix, this is a source of voxel spatial coordinates. In such a case there is a need to be consistent with an extedned image (self._imge) spatial coordinates, as a concequance to each coordinate (x, y, z) an one is added.

        There is a need to call this function to process voxel inside an image or in a np.array matrix.

        Output: a list with mkVoxel objects (both: inner and outer).

        C: 2019.06.26
        M: 2019.07.03
        """
        if voxMatrix is not None:
            # przeczhodzimy do wspolrzednych obrazu powiekszonego
            if inc1:
                objectVoxels = voxMatrix + np.array([1, 1, 1])
            else:
                objectVoxels = np.array(voxMatrix)
        else:
            x, y, z = np.where(self.get_imge())
            objectVoxels = np.vstack((x, y, z)).T

        voxels = []
        #  save object voxel count in the image
        self._objVoxelCount_ = objectVoxels.shape[0]
        for c in objectVoxels:
            v = self._checkVoxelNeighbours(c)
            voxels.append(v)
        self._allVoxels_ = voxels
        # List of objects of type mkVoxel
        # All voxel centers are in accordance with oryginal image indices!
        return self.allVoxels_

    def separateVoxels(self):
        """
        A function to separate inner object voxels from outer object voxels. As a result ones receives two lists of mkVoxel objects.

        C: 2019.06.26
        M: 2019.07.03
        """
        vox = self.allVoxels_

        outer = []
        inner = []
        for v in vox:
            if sum(v.ngbr) > 0:
                outer.append(v)
            else:
                inner.append(v)
        self._innerVoxels_ = inner
        self._outerVoxels_ = outer
        return inner, outer


if __name__ == '__main__':

    import os
    from mkSimple3DModels import mkSimple3DModels
    from mkRenderer import mkRenderer

    # ## Wywolanie programu
    #f = '../../all_data/bg01cm_x1_vef_0o50_1o75q_tho14.nii'
    f = '/media/marek/p1ext4/work/19/midas_database_20191002/SKEL_SEL_BRS/n009i0_vjo99x1_2t15_sk-br#1.nii'

    reader = mkReader(f)
    data = reader.loadData()
    # data[:,:,:] = data[::-1,:,:]
    sx, sy, sz = data.shape

    sf = mkSurface(data)
    vox = sf.processVoxels(voxMatrix=None)
    inner, outer = sf.separateVoxels()

    rd = mkRenderer()
    rd.displayAxesWXYZ0(scale=(30, 30, 30))
    rd.displayPlaneWXYZ0(delXY=[50, 50], xRng=[0, sx], yRng=[0, sy])
    rd.displayUnitSphereWXYZ(opa=0.4, rad=2)

    sm = mkSimple3DModels(cubesPntsLst=outer)
    rd.ren = sm.asActor()

    rd.renWin.Render()
    rd.iren.Start()
    del rd

    print("\nEoF: %s" % os.path.basename(__file__))
