#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 22:43:21 2018

@author: Marek

C: 2018.06.20
M: 2025.04.26
"""


import scipy.io as io
import os
from mk_add_path_dropbox import MK_DROPBOX_DANE


import mklib_vtkrendering as mkr
import mklib_vtkimage as mki
import mklib_vtkpolydata_sources as mks
import mklib_vtkpolydata_visualization as mkv
import mklib_vtkpolydata_utils as mku
import mklib_vtkpolydata_io as mkio



if __name__ == '__main__':
    from mkReader import mkReader
    print(100*'-')
    print(os.getcwd())
    

    fd = os.path.join(MK_DROPBOX_DANE, "tof-58-tof-66")
    rd66 = mkReader(os.path.join(fd, 'tof_66.mat'))
    rd66.setMatDcitName('xList')
    data66 = rd66.loadData()

    rd58 = mkReader(os.path.join(fd, 'tof_58.mat'))
    rd58.setMatDcitName('xList')
    data58 = rd58.loadData()

    renderer, renWin, iren = mkr.createMainVTKWindow()

    # punkty szkieletu
    sk58 = data58[:, :3]
    spd58_1 = mks.cubesFromPointsList(sk58, scale=1)
    spd58_01 = mks.cubesFromPointsList(sk58, scale=.2)
    lpd58 = mkv.linesBetweenPointSet(sk58)

    mkv.displayPolyData(renderer, spd58_1, color=(.1, .9, .1), opa=0.5)
    mkv.displayPolyData(renderer, spd58_01, color=(.7, .1, .1), opa=1)
    mkv.displayPolyData(renderer, lpd58)

    sk66 = data66[:, :3]
    spd66_1 = mks.cubesFromPointsList(sk66, scale=1)
    spd66_01 = mks.cubesFromPointsList(sk66, scale=.2)
    lpd66 = mkv.linesBetweenPointSet(sk66)
    mkv.displayPolyData(renderer, spd66_1, color=(.1, .1, .9), opa=0.5)
    mkv.displayPolyData(renderer, spd66_01, color=(.7, .1, .1), opa=1)
    mkv.displayPolyData(renderer, lpd66)

    # linia laczaca srodki punktow
    int58 = data58[:, 3:6]
    int66 = data66[:, 3:6]
    # ilpd58 = mkv.linesBetweenPointSet(int58)

    renWin.Render()
    iren.Start()

    print("EOF: %s" % os.path.basename(__file__))

    del renderer
    del renWin
    del iren

