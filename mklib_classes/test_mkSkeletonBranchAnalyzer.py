#!/usr/bin/env python
# -*- coding: utf-8 -*-
#vim: set ff=unix:
"""
Test algorytmu do analizy galezi w szkielecie:
    mkSkeletonBranchAnalyzer

Created on Sun Jul 14 20:58:15 2019
@author: mk

C: 2019.07.14
M: 2019.07.22
"""

import numpy as np

from mkReader import mkReader
from mkSkeletonAnalyzer import mkSkeletonAnalyzer


def inc1(p):
    """
    C: 2019.07.15
    M: 2019.07.15
    """
    return (p[0]+1, p[1]+1, p[2]+1)


def dec1(p):
    """
    C: 2019.07.15
    M: 2019.07.15
    """
    return (p[0]-1, p[1]-1, p[2]-1)


def inc1Dct(dct, k=False):
    """
    C: 2019.07.16
    M: 2019.07.16
    """
    if k:
        d = dct[k]
        print("\n%d:" % k)
        print('bn:', d['bn'])
        print('b:', inc1(d['b']))
        print('e:', inc1(d['e']))
        print('v:', [inc1(f) for f in d['v']])
        print('l:', d['l'])
    else:
        for k in dct.keys():
            d = dct[k]
            print("\n%d:" % k)
            print('bn:', d['bn'])
            print('b:', inc1(d['b']))
            print('e:', inc1(d['e']))
            print('v:', [inc1(f) for f in d['v']])
            print('l:', d['l'])

def lst2idx(idxList, inc1=False, dec1=False):
    """
    C: 2019.07.20
    M: 2019.07.20
    """
    if isinstance(idxList, list):
        idxNP = np.array(idxList)
        if inc1:
            idxNP += 1
        if dec1:
            idxNP -= 1
        x, y, z = idxNP[:, 0], idxNP[:, 1], idxNP[:, 2]
        return x, y, z

def _getCurentVoxelNeighborLst(pc, imge):
        # aktualny punkt
        x, y, z = pc

        # tutaj operujemy na indeksach obrazu rozszerzonegoe imge!
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

        # lista ze wszystkimi 26 sasiadami
        neighbours = []
        neighbours.extend(curSlice)
        neighbours.extend(upperSlice)
        neighbours.extend(lowerSlice)

        nbrLst = []
        for cell in neighbours:
            if imge[cell] == 1:
                nbrLst.append(cell)
        return nbrLst


def pnt2BifOneBranch(bn, cp, imge):
    """
    Zalozenie:
            Funkcja uruchamiana po odnalezieniu wszystkich luznych galezi.

    C: 2019.07.19
    M: 2019.07.21
    """

    # slownik opisujacu currentBranch
    cB = {}
    cB['bn'] = bn
    # beg - zapisujemy wart. wsp. w obrazie oryginalnyem
    cB['b'] = cp
    vox = []  # lista z voxelami w galezi

    # ###############################
    # ###  ZWIEKSZONE INDEKSY O 1 ###
    # ###############################
    # current point -> list
    # ### PRZECHODZIMY DO WSPOLRZEDNYCH OBRAZU ROZSZERZONEGO imgE
    cp = inc1(cp)

    # lista z voxelami do sprawdzenia
    brVoxels = [cp]
    # previous point
    pp = (0, 0, 0)
    while len(brVoxels):
        cp = brVoxels.pop()

        vox.append(cp)
        nbrLst = _getCurentVoxelNeighborLst(cp, imge)
        # usuwamy z listy sasiadow woxel poprzedni (z ktorego przyszlismy)
        if pp in nbrLst:
            nbrLst.remove(pp)

        # Bifurkacja
        if len(nbrLst) == 2:
            vox = vox[:-1] # usuwamy cp z listy, bo cp jest zakwalifikowny jako bifurkacja
            cB['e'] = dec1(pp)
            vox1 = [dec1(v) for v in vox]
            cB['v'] = vox1
            cB['l'] = len(vox1)
            cB['bf'] = dec1(cp)  # punkt bifurkacji na koncu
            cB['bch'] = [dec1(c) for c in nbrLst]  # indeksy poczatkowe dzieci
            return cB

        # N-furkacja
        if len(nbrLst) > 2:
            vox = vox[:-1] # usuwamy cp z listy, bo cp jest zakwalifikowny jako n-furkacja
            cB['e'] = dec1(pp)
            vox1 = [dec1(v) for v in vox]
            cB['v'] = vox1
            cB['l'] = len(vox1)
            cB['nf'] = dec1(cp)  # punkt n-furkacji na koncu
            cB['nch'] = [dec1(c) for c in nbrLst]  # indeksy poczatkowe dzieci
            return cB

        # GDY: len(nbrList) == 1 : to normalny woksel srodkowy galezi
        # GDY: len(nbrList) == 0 : to woksel koncowy galezi -END (bez dzieci)

        # dodajemy do listy znalezionego sasiada
        brVoxels.extend(nbrLst)
        # print(cp, pp, brVoxels)
        pp = cp
    # ########################################
    # ###  ZWIEKSZONE INDEKSY O 1 - KONIEC ###
    # ########################################
    # KONCOWKA GALEZI - BEZ IF, NORMALNE ZAKONCZENIE FUNKCJI
    # uzupelniamy slownik
    # end
    cB['e'] = dec1(cp)
    vox1 = [dec1(v) for v in vox]
    cB['v'] = vox1
    cB['l'] = len(vox1)
#    cB['bf'] = ()
#    cB['nf'] = ()
#    cB['ch'] = []
    return cB


def pnt2BifAllBranches(k, e2b, imgE):
    """
    C: 2019.07.19
    M: 2019.07.21
    """
    #  poczatki ktore prowadza do bifurkacj
    e2bCopy = [e for e in e2b]

    bfLst = []  # bifurcation point list
    nfLst = []  # n-furcation point list
    bChList = []  # bifurcation children list
    nChList = []  # n-furcation children list
    p2bDct = {}  # dictionary with all found branch description

    while len(e2bCopy):
        p1 = e2bCopy.pop()
        cb = pnt2BifOneBranch(k, p1, imgE)
        p2bDct[k] = cb
        # zerujemy galaz
        if len(cb['v']):
            x, y, z = lst2idx(cb['v'], inc1=True)
            imgE[x, y, z] = 0

        # koncowka -nie robimy nic dodatkowego
        if 'bf' not in cb.keys():
            pass
            # print('k={}, END'.format(k))

        # bifurkacja, zerowanie
        if 'bf' in cb.keys():
            # print('k={}, BF'.format(k))
            bfLst.append(cb['bf'])
            xb, yb, zb = inc1(cb['bf'])
            imgE[xb, yb, zb] = 0
            bChList.extend(cb['bch'])

        # n-furkacja, zerowanie
        if 'nf' in cb.keys():
            # print('k={}, NF'.format(k))
            nfLst.append(cb['nf'])
            xn, yn, zn = inc1(cb['nf'])
            imgE[xn, yn, zn] = 0
            nChList.extend(cb['nch'])
        k += 1

    bfLst = list(set(bfLst))
    nfLst = list(set(nfLst))
    bChList = list(set(bChList))
    nChList = list(set(nChList))
    return bfLst, nfLst, bChList, nChList, p2bDct, k


def automaticAnalyzeTheWholeTree(sa1, imgE, sh=False):
    """
    sa1 - lista z wspolrzednymi punktow poczatkowych galezi
    C: 2019.07.21
    M: 2019.07.21
    """

    stPnts = list(set(sa1))
    k = 0
    bfLst = []
    nfLst = []
    bChLst = []
    nChLst = []

    brDct = {}

    loopCounter = 0
    while len(stPnts) and loopCounter < 50:
        bfL, nfL, bChL, nChL, brDc, k = pnt2BifAllBranches(k, stPnts, imgE)
        bfLst.extend(bfL)
        nfLst.extend(nfL)
        bChLst.extend(bChL)
        nChLst.extend(nChL)
        bfLst = list(set(bfLst))
        nfLst = list(set(nfLst))
        bChLst = list(set(bChLst))
        nChLst = list(set(nChLst))

        brDct.update(brDc)

        stPnts.clear()
        stPnts.extend(bChL)
        stPnts.extend(nChL)

        if sh:
            print('bfLst=', len(bfLst))
            print('nfLst=', len(nfLst))
            print('bChLst=', len(bChLst))
            print('nChLst=', len(nChLst))
            print('bChL =', len(bChL))
            print('nChL =', len(nChL))
            print('brDct=', len(brDct))
            print('k =', k, '; loopCounter =', loopCounter, '; OnVoxels=', imgE.sum())
            print(45*'x')
        loopCounter += 1
    return brDct

def findBranchWithVoxel(dct, vox):
    """
    C: 2019.09.02
    M: 2019.09.02
    """
    dc = {}
    vox = tuple(vox)
    for k,v in dct.items():
        if vox in v['v']:
            dc[k] = v
    return dc


def getBrLongerThan(dct, thLen):
    dc = {}
    bfLst = []
    for k, v in dct.items():
        ln1 = v['l']
        if ln1 > thLen:
            if 'bf' in v.keys():
                bf = v['bf']
                bfLst.append(bf)
            else:
                bf = (0, 0, 0)
            # print('k={}, len={}, bif={}'.format(k, ln1, bf), flush=True)
            dc[k] = dct[k]
    return dc, bfLst


def saveDictToTXT(dct, fname, folder='../../all_data'):
    """
    C: 2019.07.22
    M: 2019.07.22
    """
    fs = os.path.join(folder, fname + '.txt')
    f = open(fs, 'w')
    for v in dct.values():
        k = v['bn']
        vox = v['v']
        for kk in range(len(vox)):
            x, y, z = vox[kk]
            f.write("%d %d %d %d\n" % (k, x, y, z))
    f.close()


def saveDictToNPY(dct, fname, folder='../../all_data'):
    """
    C: 2019.07.22
    M: 2019.07.22
    """
    import numpy as np
    fs = os.path.join(folder, fname)
    mat = np.zeros((len(dct), 4), dtype=np.uint16)

    lst = []
    for v in dct.values():
        k = v['bn']
        vox = v['v']
        for kk in range(len(vox)):
            x, y, z = vox[kk]
            lst.append([k, x, y, z])

        mat = np.array(lst)
        np.save(fs + '.npy', mat)
        np.savetxt(fs + '1.txt', mat, fmt='%d')


if __name__ == '__main__':

    import os
    from mkVtkImage import mkVtkImage
    from mkVtkImageIO import mkVtkImageIO
    from mkPlaneWidget import mkPlaneWidget
    from mkSurface import mkSurface
    from mkRenderer import mkRenderer
    from mkSimple3DModels import mkSimple3DModels

    f1 = '../../all_data/bg01cm_x1.nii'
    # f = '../../all_data/bg01cm_x1_vef_0o50_1o75q_tho06-sk-lin.nii'
    f = '../../all_data/bg01cm_x1_vef_0o50_1o75q_tho12-sk.nii'
    # f = '../../all_data/bg01cm_x1_vef_0o50_1o75q_tho14-sk-lin.nii'
    reader = mkReader(f)
    data = reader.loadData()
    sx, sy, sz = data.shape

    reader1 = mkReader(f1)
    data1 = reader1.loadData()

    # #skrypt z programem
    rd = mkRenderer()
    rd.displayAxesWXYZ0(scale=(30, 30, 30))
    rd.displayPlaneWXYZ0(delXY=[50, 50], xRng=[0, sx], yRng=[0, sy])
    rd.displayUnitSphereWXYZ(opa=0.4, rad=2)

    # Analiza szkieletu
    sa = mkSkeletonAnalyzer(data)
    imgo = sa.imgo.copy()
    imge = sa.imge.copy()
    imgE = sa.imge.copy()

    sa0 = sa.skelVoxIdx_[0]  # indeksy w obrazie oryginalnym
    sa1 = sa.skelVoxIdx_[1]  # indeksy w obrazie oryginalnym

    # zerujemy pojedyncze voksele
    x, y, z = lst2idx(sa0, inc1=True)
    imgE[x, y, z] = 0
    del x, y, z

    brDc = automaticAnalyzeTheWholeTree(sa1, imgE)
    dc, bfLst = getBrLongerThan(brDc, 5)
    # saveDictToTXT(dc, "slownik")
    # saveDictToNPY(dc, 'slownik')

    if 1:
        # obraz do analizy sasiadow poszczegolnych wokseli
        sf = mkSurface(data)
        for k, v in dc.items():
            voxk = sf.processVoxels(voxMatrix=dc[k]['v'])
            # opis geometryczny woskeli (klasa dziedziczy po mkPolyData)
            brk = mkSimple3DModels(cubesPntsLst=voxk)
            rd.ren = brk.asActor(col=(np.random.rand(3)), opa=1)
        voxbf = sf.processVoxels(voxMatrix=bfLst)
        modbf = mkSimple3DModels(cubesPntsLst=voxbf)
        rd.ren = modbf.asActor(col=(1, 0, 0))

    if 1:
        # pw1 = mkPlaneWidget(rd.ren, rd.iren, data, dr='x', dataOrder='F')
        pw2 = mkPlaneWidget(rd.ren, rd.iren, data1, dr='x', dataOrder='F')
        pw3 = mkPlaneWidget(rd.ren, rd.iren, data1, dr='y', dataOrder='F')

    if 0:
        vtkimg = mkVtkImageIO('vtk - pw3')
        vtkimg.readNIFTIImage(f1)
        pw4 = mkPlaneWidget(rd.ren, rd.iren, vtkimg.img, dr='y')

    # obraz sprogowany - przed szkieletyzacja
    if 1:
        f = '../../all_data/bg01cm_x1_vef_0o50_1o75q_tho14.nii'
        reader2 = mkReader(f)
        data2 = reader2.loadData()

        sf = mkSurface(data2)
        vox = sf.processVoxels(voxMatrix=None)
        inner, outer = sf.separateVoxels()

        sm = mkSimple3DModels(cubesPntsLst=outer)
        rd.ren = sm.asActor(opa=0.3)

    rd.renWin.Render()
    rd.iren.Start()
    # del pw1
    del pw2
    del pw3
    # del pw4
    del rd
    print("\nEoF: %s" % os.path.basename(__file__))
