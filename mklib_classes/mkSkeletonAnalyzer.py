#!/usr/bin/env python
# -*- coding: utf-8 -*-
#vim: set ff=unix:
"""
The class to analyze a skeleton of a binary image.

Created on Fri Jun 28 18:03:03 2019
@author: marek

(C) MK & AM

C: 2019.06.28
M: 2019.07.09

v: 0.01
"""

import numpy as np

from mkReader import mkReader
from mkSurface import mkSurface


class mkSkeletonAnalyzer(object):
    """
    C: 2019.06.28
    M: 2019.07.01
    """

    def __init__(self, data):
        self.imgo = data
        sx, sy, sz = self.imgo.shape
        # extended image
        self._imge = np.zeros((sx+2, sy+2, sz+2), dtype=self.imgo.dtype)
        self._imge[1:-1, 1:-1, 1:-1] = self.imgo
        self.analyzeSkeletonCharacteristicPoints()

    @property
    def imgo(self):
        return self._imgo

    @imgo.setter
    def imgo(self, data):
        if not isinstance(data, np.ndarray):
            raise ValueError('mkSkeletonAnalyzer- data must be an numpy array!')
        assert(data.ndim == 3), "mkSekeletonAnalyzer - 3D matix needed!"
        print("Data rescaled to [0-1] values.")
        self._imgo = np.where(data > 0, 1, 0)

    @property
    def imge(self):
        return self._imge

    @property
    def voxCount_(self):
        assert(hasattr(self, '_voxCount_')), "Run _getCurentVoxelNeighborCoordinates() first."
        return self._voxCount_

    @property
    def skelVoxIdx_(self):
        assert(hasattr(self, '_skelVoxIdx_')), "Run _getCurentVoxelNeighborCoordinates() first."
        return self._skelVoxIdx_

    def _getCurentVoxelNeighborCoordinates(self, x, y, z):
            # the same convention as in mkSurface class
            front = (x, y, z+1)
            back = (x, y, z-1)
            right = (x+1, y, z)
            left = (x-1, y, z)
            frontleft = (x-1, y, z+1)
            frontright = (x+1, y, z+1)
            backleft = (x-1, y, z-1)
            backright = (x+1, y, z-1)
            curSlice = [front, back, right, left, frontleft, frontright, backleft, backright]

            # upper slice
            currentU = (x, y+1, z)
            frontU = (x, y+1, z+1)
            backU = (x, y+1, z-1)
            rightU = (x+1, y+1, z)
            leftU = (x-1, y+1, z)
            frontLU = (x-1, y+1, z+1)
            frontRU = (x+1, y+1, z+1)
            backLU = (x-1, y+1, z-1)
            backRU = (x+1, y+1, z-1)
            upperSlice = [currentU, frontU, backU, rightU, leftU, frontLU, frontRU, backLU, backRU]

            # lower slice
            currentL = (x, y-1, z)
            frontL = (x, y-1, z+1)
            backL = (x, y-1, z-1)
            rightL = (x+1, y-1, z)
            leftL = (x-1, y-1, z)
            frontLL = (x-1, y-1, z+1)
            frontRL = (x+1, y-1, z+1)
            backLL = (x-1, y-1, z-1)
            backRL = (x+1, y-1, z-1)
            lowerSlice = [currentL, frontL, backL, rightL, leftL, frontLL, frontRL, backLL, backRL]

            neighbours = []
            neighbours.extend(curSlice)
            neighbours.extend(upperSlice)
            neighbours.extend(lowerSlice)
            return neighbours

    def analyzeSkeletonCharacteristicPoints(self):
        """
        C: 2019.06.28
        M: 2019.07.01
        """

        # a dictionary for voxel coordinates with specified neghbor number
        self._skelVoxIdx_ = {}
        for i in range(27):
            self._skelVoxIdx_[i] = list()

        # convert an object voxesl into matrix (coxCnt x 3)
        x, y, z = np.where(self.imge > 0)
        skeletonVoxels = np.vstack((x, y, z)).T

        #  store an object voxel count in the image
        self._voxCount_ = skeletonVoxels.shape[0]

        for k, l, m in skeletonVoxels:
            neigs = self._getCurentVoxelNeighborCoordinates(k, l, m)

            nbCounter = 0
            for cell in neigs:
                if self.imge[cell] == 1:
                    nbCounter += 1
            # Go back to original image coordinates
            self._skelVoxIdx_[nbCounter].append((k-1, l-1, m-1))

    def __str__(self):
        s = 'Nbrs ---> voxNr\n'
        for k, v in self.skelVoxIdx_.items():
            s += '{} ---> {}\n'.format(k, len(v))
        return s

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':

    import os

    from mkRenderer import mkRenderer
    from mkSimple3DModels import mkSimple3DModels

    # ## Wywolanie programu
    # f = 'bg01cm_x1_vef_0o50_1o75q_tho14.nii'
    f = '../../all_data/BG03_x_vef_1o00_3o00q_tho08-sk.nii'
    reader = mkReader(f)
    data = reader.loadData()
    sx, sy, sz = data.shape

    # #skrypt z programem
    rd = mkRenderer()
    rd.displayAxesWXYZ0(scale=(30, 30, 30))
    rd.displayPlaneWXYZ0(delXY=[50, 50], xRng=[0, sx], yRng=[0, sy])
    rd.displayUnitSphereWXYZ(opa=0.4, rad=2)

    # Analiza szkieletu
    sa = mkSkeletonAnalyzer(data)
    # obraz do analizy sasiadow poszczegolnych wokseli
    sf = mkSurface(data)

    # budujemy modele poszczegolnych galezi
    ###########################################
    # ###brak sasiadow - pojedyncze woksele ###
    ###########################################
    # lista wokseli bez sasiadow
    sa0 = sa.skelVoxIdx_[0]
    # lista obiektow typu mkVoxel (z opisem ktore scianki wlaczyc a ktore nie)
    vox0 = sf.processVoxels(voxMatrix=sa0)
    # opis geometryczny woskeli (klasa dziedziczy po mkPolyData)
    sm0 = mkSimple3DModels(cubesPntsLst=vox0)
    #rd.ren = sm0.asActor(col=(0.1, 0.1, 0.9))

    # ##################################
    # ### 1 sasiad - koncowki galezi ###
    # ##################################
    sa1 = sa.skelVoxIdx_[1]
    vox1 = sf.processVoxels(voxMatrix=sa1)
    sm1 = mkSimple3DModels(cubesPntsLst=vox1)
    rd.ren = sm1.asActor(col=(0.1, 0.9, 0.1))

    # #####################################
    # ### 2 sasiadow - voksele z glaezi ###
    # #####################################
    sa2 = sa.skelVoxIdx_[2]
    vox2 = sf.processVoxels(voxMatrix=sa2)
    sm2 = mkSimple3DModels(cubesPntsLst=vox2)
    rd.ren = sm2.asActor(col=(0.5, 0.5, 0.5))

    # ###############################
    # ### 3 sasiadow - bifurkacje ###
    # ###############################
    sa3 = sa.skelVoxIdx_[3]
    vox3 = sf.processVoxels(voxMatrix=sa3)
    sm3 = mkSimple3DModels(cubesPntsLst=vox3)
    rd.ren = sm3.asActor(col=(0.9, 0.1, 0.1))

    # #######################
    # ### wiecej sasiadow ###
    # #######################
    # tutaj wpisuje recznie dla danego drzewa: 7 wokseli ma 4 sasiadow i 1 woksel ma 6 sasiadow
    sa4 = sa.skelVoxIdx_[4]
    vox4 = sf.processVoxels(voxMatrix=sa4)
    sm4 = mkSimple3DModels(cubesPntsLst=vox4)
    rd.ren = sm4.asActor(col=(0.9, 0.9, 0.9))

    sa6 = sa.skelVoxIdx_[6]
    vox6 = sf.processVoxels(voxMatrix=sa6)
    sm6 = mkSimple3DModels(cubesPntsLst=vox6)
    rd.ren = sm6.asActor(col=(0.9, 0.9, 0.9))

    rd.renWin.Render()
    rd.iren.Start()
    del rd
    print("\nEoF: %s" % os.path.basename(__file__))
