#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A module with definition and testing mkVoxel class.

Created on Sat Jun 22 13:21:11 2019
@author: mk

(C) MK & AM

C: 2019.06.22
M: 2019.07.10

v: 0.02
"""
import numpy as np
from numpy import r_


class mkVoxel(object):
    """
    A 3D image voxel representation class.

    The class defines all voxel properties. Each class instance has the following attributes:
        - center - a list [x, y, z]
        - vert - an np.array, (8x3), asses the 8 vertex coordinates (x,y,z) of the center
        - faces - an np.array(), (up to12x3), in each row there are 3 indexes of three vertices for a single triangle.
        - triangles - a list - up to 12 elements. In each line there are three point coordinates (x,y,z) of each triangle.
        - ngbr - a boolean list. Each element is True if there is a voxel's neighbor. Order of wals: [front(+z), back(-z), right(+x), left(-x), top(+y), bottom(-y)].

    2019.07.12  - dodano dlugosc boku woksela (_sideLen)
                - poprawiono nawijanie trojkatow (oba trojkaty w sciance lewej byly odwrotnie nawiniete).

    C: 2019.06.22
    M: 2019.07.12

    v: 0.02
    """

    def __init__(self, center=[0, 0, 0], nb=np.ones((6), dtype=bool), sideLen=[1, 1, 1]):
        """
        C: 2019.06.22
        M: 2019.07.12
        """
        self.center = center
        self._sideLen = np.array(sideLen)
        self.vert = center
        #  front (+z), back (-z), right(+x), left (-x), top(+y), bottom(-y)
        self.ngbr = nb  # sasiadujace sicanki (voksele)

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, center):
        if not isinstance(center, np.ndarray):
            self._center = np.array(center)
        else:
            self._center = center

    @property
    def ngbr(self):
        return self._ngbr

    @ngbr.setter
    def ngbr(self, ngbr):
        self._ngbr = ngbr
        self._set_faces()
        self._set_triangles()

    @property
    def vert(self):
        return self._vert

    @vert.setter
    def vert(self, v):
        """
        C: 2019.07.12
        M: 2019.07.12
        """
        x, y, z = v
        x2, y2, z2 = self._sideLen / 2
        V0 = r_[x+x2, y-y2, z+z2]
        V1 = r_[x-x2, y-y2, z+z2]
        V2 = r_[x-x2, y+y2, z+z2]
        V3 = r_[x+x2, y+y2, z+z2]
        V4 = r_[x+x2, y-y2, z-z2]
        V5 = r_[x-x2, y-y2, z-z2]
        V6 = r_[x-x2, y+y2, z-z2]
        V7 = r_[x+x2, y+y2, z-z2]
        self._vert = np.vstack((V0, V1, V2, V3, V4, V5, V6, V7))

    @property
    def faces(self):
        return self._faces

    @property
    def triangles(self):
        return self._triangles

    def _set_triangles(self):
        """
        Triangle coordinates.
        """
        tria = []
        if len(self._faces):
            for k in range(self._faces.shape[0]):
                i1, i2, i3 = self._faces[k]
                t1 = list(self._vert[i1])
                t2 = list(self._vert[i2])
                t3 = list(self._vert[i3])
                tria.append([t1, t2, t3])
            self._triangles = tria
        else:
            self._triangles = []

    def _set_faces(self):
        fr, ba, ri, le, to, bo = self._ngbr
        faces = []
        # przod: t0, t1 - FRONT
        if fr:
            t0 = r_[0, 2, 1]
            t1 = r_[0, 3, 2]
            faces.append(t0)
            faces.append(t1)
        # tyl: t2, t3 - BACK
        if ba:
            t2 = r_[4, 5, 6]
            t3 = r_[4, 6, 7]
            faces.append(t2)
            faces.append(t3)
        # prawy: t4, t5 - RIGHT
        if ri:
            t4 = r_[0, 4, 3]
            t5 = r_[4, 7, 3]
            faces.append(t4)
            faces.append(t5)
        # lewy: t6, t7 - LEFT
        if le:
            t6 = r_[5, 1, 2]
            t7 = r_[2, 6, 5]
            faces.append(t6)
            faces.append(t7)
        # gora t8, t9 - TOP
        if to:
            t8 = r_[3, 7, 6]
            t9 = r_[3, 6, 2]
            faces.append(t8)
            faces.append(t9)
        # dol: t10, t11 - BOTTOM
        if bo:
            t10 = r_[0, 1, 5]
            t11 = r_[0, 5, 4]
            faces.append(t10)
            faces.append(t11)
        if faces:
            self._faces = np.vstack(faces)
        # nie ma żadnych ścianek, woksel jest otoczony innymi
        else:
            self._faces = []

    def __str__(self):
        fac = self.faces
        if len(fac):
            faces = fac.shape[0] // 2
        else:
            faces = 0
        tr = sum(self.ngbr) * 2
        return('C:{},  FA:{},  TR:{:02},  NBs:{}\t(F, BA, R, L, T, BO)'.format(self.center, faces, tr, self.ngbr))

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    from mkSimple3DModels import mkSimple3DModels
    import os

    from mkRenderer import mkRenderer

    rd = mkRenderer()
    rd.displayAxesWXYZ0(scale=(2, 2, 2))
    rd.displayPlaneWXYZ0(xRng=[-2, 2], yRng=[-2, 2], delXY=[4, 4])
    # rd.displayUnitSphereWXYZ(opa=0.4)

    # model z obiektow mkVoxel
    if 1:
        v1 = mkVoxel([0, 0, 0], [True, True, True, True, True, True], sideLen=[2, 1, 1])
        v2 = mkVoxel([0, 2, 0], [True, True, True, True, True, True], sideLen=[1, 2, 1])
        v3 = mkVoxel([2, 1, 0], [True, True, True, True, True, True], sideLen=[1, 1, 2])
        print(v1)
        voxList = [v1, v2, v3]
        sm = mkSimple3DModels(cubesPntsLst=voxList)
        rd.ren = sm.asActor(backCulling=1)
        rd.ren = sm.labelActor()

    # model z listy i np.array
    if 0:
        v1 = [1, 0, 0]
        v2 = np.array([1, 1, 1])

        voxList = [v1, v2]
        sm = mkSimple3DModels(cubesPntsLst=voxList)
        rd.ren = sm.asActor(col=[0, 1, 0])



    rd.renWin.Render()
    rd.iren.Start()
    del rd
    print("\nEoF: %s" % os.path.basename(__file__))
