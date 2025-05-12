#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Skrypt do zamiany wokseli zawartych w obrazie nii (macierzy)
na obiekty trojkatne zapisane w pliku tekstowym STL.

Uwaga:
	1. Plik zamienia kazdy woksel na szescian, nie usuwa scianek sasiadujacych przy sasiednich
wokselach. Te scianki sie dubluja!

Oryginalna nazwa pliku:
    00_mk_lib_nii2stl.py
Pliki podobne:
    mk_lib_nii2stl.py


C: 2014.06
M: 2019.06.19
"""
import os
import numpy as np
from numpy import r_
import nibabel as nib

all = []


def stlConvert3DPointsToVerticlesAndFaces(C):
    """
    Funkcja otrzymuje tablice z indeksami wokseli (nrWokselix3).
    Kazdy srodek woskela jest otaczant 6 sciankami (z 12 trojkatow) ktore
    stanowia powierzchnie boczna woksela. Nie sa usuwane scianki ktore
    sie dubluja w sasiednich wokselach.

    Funkcja zwraca dwie macierze:
        1. macierz z 8 wierzcholkami dla kazdego woksela (8*nrWokselix3)
        2. macierz z 12 trojkatami dla 6 scianek kazdego woksela (12*nrWokselix3)

    Poprzednia nazwa funkcji:
        stlAddCubeObjects

    C: 2016.04
    M: 2019.06.14
    """
    for k in range(C.shape[0]):

       V1 = r_[C[k,0]+0.5, C[k,1]-0.5, C[k,2]+0.5]
       V2 = r_[C[k,0]-0.5, C[k,1]-0.5, C[k,2]+0.5]
       V3 = r_[C[k,0]-0.5, C[k,1]+0.5, C[k,2]+0.5]
       V4 = r_[C[k,0]+0.5, C[k,1]+0.5, C[k,2]+0.5]
       V5 = r_[C[k,0]+0.5, C[k,1]-0.5, C[k,2]-0.5]
       V6 = r_[C[k,0]-0.5, C[k,1]-0.5, C[k,2]-0.5]
       V7 = r_[C[k,0]-0.5, C[k,1]+0.5, C[k,2]-0.5]
       V8 = r_[C[k,0]+0.5, C[k,1]+0.5, C[k,2]-0.5]
       vert = np.vstack((V1,V2,V3,V4,V5,V6,V7,V8))

       t0=r_[0,2,1]; t1=r_[0,3,2]; t2=r_[4,5,6]
       t3=r_[4,6,7]; t4=r_[0,4,3]; t5=r_[4,7,3]
       t6=r_[1,5,2]; t7=r_[5,6,2]; t8=r_[0,1,5]
       t9=r_[0,5,4]; t10=r_[3,7,6];t11=r_[3,6,2]
       F = np.vstack((t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11))

       if k == 0:
          #print("k===0")
          vC = vert
          fC = F
       else:
           # indeksy F (trojkatow) sa uzaleznioe od liczby przetworzonych
           # wierzholkow, np. dla k zanalizowanych wirzcholkow
           # aktualne indeksy w tablicy z trojkatami beda
           # mialy wartosci: curIdx + k *8 gdzie curIdx=<0-8>.
           G = F + vC.shape[0]
           vC = np.vstack((vC, vert))
           fC = np.vstack((fC, G))
    return vC, fC


all.append('stlConvert3DPointsToVerticlesAndFaces')


def _stlAddTriangleToSTLFile(VOX, A, B, C, fid):
    """

    A,B,C - wspolrzedne wierzcholka trojkata ktory ma byc dodany do pliku STL,
        A = [ax, ay, az]
        B = [bx, by, bz]
        C = [cx, cy, cz]
    fid - uchwyt do pliku tekstowego (STL),
    VOX - rozmiar woksela.

    Pierwotna nazwa funkcji:
        stl_add_triangle

    C: 2014.06
    M: 2019.06.14
    """
    # liczymy wektory na ktorych oparty jest trojkat
    a = B - A
    b = C - A
    n = np.cross(a, b)
    n = n / np.sqrt(sum(n * n))
    av = A * VOX
    bv = B * VOX
    cv = C * VOX

    print('  facet normal %.6f %.6f %.6f' % (n[0], n[1], n[2]), file=fid)
    print('   outer loop', file=fid)
    print('    vertex %.6f %.6f %.6f' % (av[0], av[1], av[2]), file=fid)
    print('    vertex %.6f %.6f %.6f' % (bv[0], bv[1], bv[2]), file=fid)
    print('    vertex %.6f %.6f %.6f' % (cv[0], cv[1], cv[2]), file=fid)
    print('   endloop', file=fid)
    print('  endfacet', file=fid)


def stlSaveSTLFileFromVertclesAndFaces(vc,fc, fname, VOX=1, sh=False):
    """
    Funkcja zamienia opis veirzcholkow (verticles, v) i scianek (faces, f) na opis teksoty stosowany w pliku STL. Wynikiem jest tekstowy plik STL.

    v - macierz ze wspolrzednymi wierzcholkow (nrWierzcholkow x 3),
    f- macierz z indeksami wierzcholkow, ktore opisuja trojkatne scianki. W kazdym wierszu znajduja 3 indeksy z (macierzy wierzcholkow) ktore opisuja kazdy trojkat,
    VOX - rozmiar woksela,
    sh - wypisywanie postepu zapisu do pliku STL.
    
    (C) MK & AM

    C: 2019.06.16
    M: 2019.06.14
    """
    if not fname.endswith('.stl'):
        fname += '.stl'
        print(fname)
    if os.path.exists(fname):
        print("\n**** Nadpisjujemy plik o nazwie: {} ****".format(fname))

    fid = open(fname, 'w')
    fid.write('solid Vessel branches: {}\n'.format(fname))

    # fc.shape[0] - liczba trojkatow do narysowania
    nrFaces = fc.shape[0]
    for k in range(nrFaces):
        _stlAddTriangleToSTLFile(VOX, vc[fc[k, 0], :], vc[fc[k, 1], :], vc[fc[k, 2], :], fid);
        if sh and not k % 10000:
            print("{}/{}".format(k, nrFaces))
    fid.write('endsolid')
    fid.close()


all.append('stlSaveSTLFileFromVertclesAndFaces')


def prepareBinary3DImageToBuild3DSTLModel(im):
    """
    Funkcja pobiera macierz 3D, wyszukuje woksele obietku i zwaraca macierz ze wspolrzednymi woskeli.

    C: 2019.06.19
    M: 2019.06.19
    """
    # pobieramy 3 macierze 1D z indeksami
    x, y, z = np.where(im)
    # układamy wertykanie macierze indeskow- otrzymujemy np: (3x100)
    # transponumemy macierz C do rozmiaru np: (100x3)
    C = np.vstack((x, y, z)).T
    return C
all.append('prepareBinary3DImageToBuild3DSTLModel')



if __name__ == '__main__':

    # fname2 = 'normal01_4000_036_3_256_skel'
    # fname = 't2_nowy_lepszy'
    fname = 'bg01cm_x1_vef_0o50_1o75q_tho14-lb-o1'
    im = nib.load(fname+'.nii').get_fdata()
    # zamieniamy macierz obrazu na macierz ze wspolrzednymi wokseli
    C = prepareBinary3DImageToBuild3DSTLModel(im)
    # budujemy macierze wierzcholkow (vertex)
    # i scianek (faces) dla kazdego woksela
    vc, fc = stlConvert3DPointsToVerticlesAndFaces(C)
    stlSaveSTLFileFromVertclesAndFaces(vc,fc, fname, VOX=0.5, sh=True)


    print("EoF: %s" % os.path.basename(__file__))
