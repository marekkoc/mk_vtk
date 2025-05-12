#!/usr/bin/env python
"""

C: 2014.06
M: 2019.06.16
"""
from mklib_stl import stlConvert3DPointsToVerticlesAndFaces
from mklib_stl import stlSaveSTLFileFromVertclesAndFaces

import os
import numpy as np
import nibabel as nib

# fname2 = 'normal01_4000_036_3_256_skel'
fname = 'test_stl/t2_nowy_lepszy'
im = nib.load(fname+'.nii').get_fdata()
# pobieramy 3 macierze 1D z indeksami
x, y, z = np.where(im)
# układamy wertykanie macierze indeskow- otrzymujemy np: (3x100)
# transponumemy macierz C do rozmiaru np: (100x3)
C = np.vstack((x, y, z)).T
# budujemy macierze wierzcholkow (vertex)
# i scianek (faces) dla kazdego woksela
vc, fc = stlConvert3DPointsToVerticlesAndFaces(C)
stlSaveSTLFileFromVertclesAndFaces(vc,fc, fname, VOX=0.5, sh=True)


print("EoF: %s" % os.path.basename(__file__))
