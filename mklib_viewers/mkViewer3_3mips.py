#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MIP viewer

Created on Tue May 28 12:32:37 2019

@author: marek

Script to display 3 mips of one image.

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
else:
    fileName = sys.argv[1]
    reader = mkReader(fileName)

    if fileName.endswith('.raw'):
        reader.setRawParams()
    img = reader.loadData()

    if not isinstance(img, np.ndarray):
        print('mkp-Viewer3 --->>> img matrix is not a NUMPY object type!!!')
        sys.exit(0)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    plt.gray()
    plt.suptitle(fileName)

    ax1.imshow(np.rot90(img.max(0),3), origin='lower')
    ax1.set_title('MIP 0')
    ax2.imshow(img.max(1), origin='lower')
    ax2.set_title('MIP 1')
    ax3.imshow(img.max(2), origin='lower')
    ax3.set_title('MIP 2')

    plt.tight_layout()
    plt.show()



