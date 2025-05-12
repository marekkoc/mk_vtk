#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MIP viewer

Created on Tue May 28 12:32:37 2019

@author: marek

Script shows mip image from number of files.

C: 2019.25.28
M: 2019.06.10

ver: 0.01
"""

import sys
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor

from mkReader import mkReader

if len(sys.argv) < 2:
        print("\nUsage: filename.[npy/nii/nii.gz] \n")
        sys.exit("Brak nazwy pliku!")


fileNames = sys.argv[1:]
filesNr = len(fileNames)

cmp = 'gray'
dr = 0
multiCursor = True

if filesNr == 1:
    name = sys.argv[1]
    reader = mkReader(name)
    if name.endswith('.raw'):
        reader.setRawParams()
    img = reader.loadData()

    fig, ax = plt.subplots()
    ax.imshow(np.rot90(img.max(dr), 1), cmap=cmp)
    ax.set_title(name)

elif filesNr > 1 and filesNr <= 4:
    fig, axs = plt.subplots(1, filesNr, True, True)
    if multiCursor:
        multi = MultiCursor(fig.canvas, list(axs), color='r', lw=1, horizOn=True, vertOn=True)
    for k, f in enumerate(fileNames):

        name = fileNames[k]
        reader = mkReader(name)
        if name.endswith('.raw'):
            reader.setRawParams()
        img = reader.loadData()
        axs[k].imshow(np.rot90(img.max(dr), 3), origin='lower')
        axs[k].set_title(name)

else:
    c, m = divmod(filesNr, 4)
    fig, axs = plt.subplots(c+1, 4, True, True)
    for ax in axs.flatten() : ax.axis('off')
    axlist = []
    for k, name in enumerate(fileNames):
        c, m = divmod(k, 4)


        name = fileNames[k]
        reader = mkReader(name)
        if name.endswith('.raw'):
            reader.setRawParams()
        img = reader.loadData()

        axs[c, m].imshow(np.rot90(img.max(dr), 3), origin='lower')
        axs[c, m].set_title(name)
        axs[c, m].axis('on')
        axlist.append(axs[c, m])

    if multiCursor:
        multi = MultiCursor(fig.canvas, axlist, color='r', lw=1, horizOn=True, vertOn=True)

#
plt.show()
