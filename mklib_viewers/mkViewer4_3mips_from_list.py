#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MIP viewer

Created on Tue May 28 12:32:37 2019

@author: marek

Script displays 3 mip for each eamge from a list.

C: 2019.25.28
M: 2019.06.10

ver: 0.01
"""

import sys
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from mkReader import mkReader

if len(sys.argv) < 2:
        print("\nUsage: filename.[npy/nii/nii.gz] \n")
        sys.exit(0)


fileNames = sys.argv[1:]
filesNr = len(fileNames)

fig, axs = plt.subplots(filesNr, 3)

for k, f in enumerate(fileNames):

    reader = mkReader(f)

    if f.endswith('.raw'):
        reader.setRawParams()
    img = reader.loadData()


    plt.gray()


    axs[k, 0].imshow(np.rot90(img.max(0),3), origin='lower')
    axs[k, 0].set_title(f + 'MIP 0')
    axs[k, 1].imshow(img.max(1), origin='lower')
    axs[k, 1].set_title('MIP 1')
    axs[k, 2].imshow(img.max(2), origin='lower')
    axs[k, 2].set_title('MIP 2')


plt.tight_layout()
plt.show()



