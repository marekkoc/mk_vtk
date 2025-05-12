#!/usr/bin/env python
"""
===================
Image Slices Viewer
===================

Scroll through 2D image slices of a 3D array.

https://matplotlib.org/gallery/event_handling/image_slices_viewer.html


C: 2018.12.01
M: 2019.06.10

ver: 0.02
"""
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt


class IndexTracker(object):
    def __init__(self, ax, X, cmap):

        if not isinstance(X, np.ndarray):
            print('mkp-Viewer2 --->>> X matrix is not a NUMPY object type!!!')
            return

        self.ax = ax
        self.cmap = cmap
        ax.set_title('use scroll wheel to navigate images')
        ax.axis('off')


        self.X = X
        rows, cols, self.slices = X.shape
        self.ind = self.slices//2

        self.im = ax.imshow(self.X[:, :, self.ind])
        self.im.set_cmap(self.cmap)
        self.update()

    def onscroll(self, event):
        #print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()


if __name__ =='__main__':

    import sys
    import nibabel as nib

    


    if len(sys.argv) < 2:
        X = np.random.randint(0, 100, size=(100, 100, 100))
        print("\nUsage: filename.[npy/nii/nii.gz] [cmap]\n")

    else:
        from mkReader import mkReader
        filename = str(sys.argv[1])
        reader = mkReader(filename)
        #reader.setRawParams()
        X = reader.loadData()

    # CMAP (jako drugi argument)
    if len(sys.argv) == 3:
        cmap = str(sys.argv[2])
        #print(cmap)
    else:
        cmap = 'gray'



    fig, ax = plt.subplots(1, 1)
    tracker = IndexTracker(ax, X, cmap)

    fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    plt.show()
