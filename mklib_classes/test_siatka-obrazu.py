#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Test. Rysowanie krawedzi wokseli obrazu

Created on Fri Jul 12 15:46:01 2019
@author: marek


(C) MK & AM

C: 2019.07.12
M: 2019.07.12

v: 0.01
"""
import os
import numpy as np

from mkVoxel import mkVoxel
from mkVtkImageIO import mkVtkImageIO
from mkRenderer import mkRenderer
from mkSimple3DModels import mkSimple3DModels
from mkPolyDataIO import mkPolyDataIO
from mkPolyDataSources import mkPolyDataSources

fname = '../../all_data/t2_tse_sag_2mm.nii'
vt = mkVtkImageIO(name='t2_tse_sag_2mm.nii')
vt.readNIFTIImage(fname)

voxDim=[0.332, 0.332, 2.2]

xr = range(275,331)
yr = range(235, 270)
zr = range(29,31)

xm, ym, zm = np.meshgrid(xr, yr, zr)
xmf = xm.flatten() * 0.332 + 81.07
ymf = ym.flatten() * 0.332 -71.52
zmf = zm.flatten() * 2.2 + 104.5

idx = np.vstack((xmf, ymf, zmf)).T

cs = mkPolyDataSources(name='cubes')
cs.cuberFromSource(pos=idx[0], sideLen=voxDim)

csN = mkPolyDataSources()
cubesPolyList = []

for p in idx[1:]:
    print(p)
    pd = csN.cuberFromSource(p, sideLen=voxDim)
    cubesPolyList.append(pd)

cs.appendPolyDatas(cubesPolyList)
print('*********** ZAPIS *********************')
io = mkPolyDataIO(cs.poly, "io writer")
io.cleanPolyData()
io.info()
fs = '../../all_data/xxx1.vtk'
io.writePolyData(fs, toASCII=False)
# io.replaceCommasAndDots(fs, read=False)


rd = mkRenderer()
rd.ren = cs.asActor()
#rd.ren = sm.cellEdgesActor()



rd.renWin.Render()
rd.iren.Start()
del rd

print("\nEoF: %s" % os.path.basename(__file__))
