#!/usr/bin/env python
# -*- coding: utf-8 -*-
#vim: set ff=unix:
"""
Plik testowy: analiza szkieletu skSkeletonAnalyzer.py
 dla obrazu bg01cm_x1_vef_0o50_1o75q_tho12-sk.nii

Created on Tue Jul  2 12:19:17 2019
@author: marek

Plik znajduje sie w katalogach:
    .../work19/nitric_2019/bg01_x1_analiza_20190517/SKEL/
    .../work/all_python/mklib_classes/

C: 2019.07.02
M: 2019.07.19

"""
from mkReader import mkReader
from mkSkeletonAnalyzer import mkSkeletonAnalyzer, mkSurface


if __name__ == '__main__':
    import os

    from mkRenderer import mkRenderer
    from mkSimple3DModels import mkSimple3DModels

    # ## Wywolanie programu
    # f = 'bg01cm_x1_vef_0o50_1o75q_tho14.nii'
    # f = '../../all_data/bg01cm_x1_vef_0o50_1o75q_tho06-sk-lin.nii'
    f = '../../../all_data/bg01cm_x1_vef_0o50_1o75q_tho12_g10_sk.nii.gz'
    # f = '../../all_data/bg01cm_x1_vef_0o50_1o75q_tho14-sk-lin.nii'

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
    # rd.ren = sm0.asActor(col=(0.1, 0.1, 0.9))

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
    # tutaj woksele ktore maja wiecej sasiadow niz 3
    for k in range(4, 27):
        sak = sa.skelVoxIdx_[k]
        if len(sak):
            print('{} --> {}'.format(k, len(sa.skelVoxIdx_[k])))
            # sfk = mkSurface(data)
            voxk = sf.processVoxels(voxMatrix=sak)
            smk = mkSimple3DModels(cubesPntsLst=voxk)
            rd.ren = smk.asActor(col=(0.1, 0.1, 0.1))

    rd.renWin.Render()
    rd.iren.Start()
    del rd
    print("\nEoF: %s" % os.path.basename(__file__))
