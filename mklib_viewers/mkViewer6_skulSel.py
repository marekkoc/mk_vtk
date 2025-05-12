#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
(C) MMIV-ML
    MK & SK & ASL & AL

    Program napisany dla Sathiesha, w celu akceptacji lub odrzucenia wybranych plikow.
    Dlatego wyswietlane sa dwa obrazy, aby program dzialal potrzebny jest podkatalog z danymi.

    Kody do programu znajduja sie w katalogach:
        /media/marek/p1ext4/no19/skullstrip_viewer
        /media/marek/p1ext4/work/00/all_python/mklib_viewers

    Pierwotna nazwa pliku to: skulSel.py


    C: 2020.01.17
    M: 2020.01.20
    v: 0.01
"""
import os
import numpy as np
# import nibabel as nib
#import matplotlib
#matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.widgets import Slider, Button, MultiCursor


def prepareFilesDictionary(pathToDataDir='./data', filesNr=0):
    files = os.listdir(pathToDataDir)
    if filesNr == 0:
        filesNr = len(files)
    files = [f for f in files if f.endswith('.npy')][:filesNr]

    data_dict = {'o': [], 'n': [], 'f': []}
    for f in files:
        pathToFile = os.path.join(pathToDataDir, f)
        oryg = np.load(pathToFile)
        neg = oryg.max() - oryg
        data_dict['o'].append(oryg)
        data_dict['n'].append(neg)
        data_dict['f'].append(f)

    [print(f) for f in files]
    return data_dict


def dictionaryInfo(dct):
    for k, v in dct.items():
        print(k, '--->', len(v))


####################################################
class ImageSelector(object):
    def __init__(self, dc,  cm='gray', intrp='None'):

        self.Idx = 0
        self.IdxMax = len(dc['o'])
        self.dc = dc

        self.acceptNr = 0
        self.rejectNr = 0
        self.accList = []
        self.rejList = []



        self.fig, self.ax = plt.subplots(2, 3, sharex=True,
                                         sharey=True, figsize=(12, 8))
        self.fig.subplots_adjust(bottom=0.2)
        # an iterator to ax array
        axF = self.ax.flat[:]
        [a.set_autoscale_on(True) for a in axF]

        titles = ['o1', 'o2', 'o3', 'n1', 'n2', 'n3']
        [a.set_title(titles[k]) for k, a in enumerate(axF)]  # set titles
        # [a.set_frame_on(False) for a in axF] # frames around an image
        # [a.set_axis_off() for a in axF] # axis label

        self.i1 = np.random.rand(100,100,100)
        self.i2 = np.random.rand(100,100,100)
        self.i1mx = self.i2mx = 1
        self.i1mn = self.i2mn = 0
        self.xCur = self.yCur = self.zCur = 50
        self.x = self.y = self.z = 99

        self.viewsO = []
        self.vo1 = axF[0].imshow(self.i1[self.xCur, :, :], cmap=cm, interpolation=intrp)
        self.vo2 = axF[1].imshow(self.i1[:, self.yCur, :], cmap=cm, interpolation=intrp)
        self.vo3 = axF[2].imshow(self.i1[:, :, self.zCur], cmap=cm, interpolation=intrp)
        self.viewsO.extend([self.vo1, self.vo2, self.vo3])

        self.viewsN = []
        self.vn1 = axF[3].imshow(self.i2[self.xCur, :, :], cmap=cm, interpolation=intrp)
        self.vn2 = axF[4].imshow(self.i2[:, self.yCur, :], cmap=cm, interpolation=intrp)
        self.vn3 = axF[5].imshow(self.i2[:, :, self.zCur], cmap=cm, interpolation=intrp)
        self.viewsN.extend([self.vn1, self.vn2, self.vn3])

        slcolor = 'lightgoldenrodyellow'
        p1 = self.ax[1, 0].get_position()
        p2 = self.ax[1, 1].get_position()
        p3 = self.ax[1, 2].get_position()

        # ### SLIDER 1
        self.slax1 = self.fig.add_axes([p1.x0, p1.y0-0.06,
                                   p1.width, 0.02], facecolor=slcolor)
        self.sl1 = Slider(self.slax1, 'x:', 0, self.x-1, valinit=self.xCur,
                          valfmt='%i', valstep=1)
        self.sl1.on_changed(self.updateSl1)
        # ### SLIDER 2
        self.slax2 = self.fig.add_axes([p2.x0, p2.y0-0.06,
                                   p2.width, 0.02], facecolor=slcolor)
        self.sl2 = Slider(self.slax2, 'y:', 0, self.y-1, valinit=self.yCur,
                          valfmt='%i', valstep=1)
        self.sl2.on_changed(self.updateSl2)
        # ### SLIDER 3
        self.slax3 = self.fig.add_axes([p3.x0, p3.y0-0.06,
                                   p3.width, 0.02], facecolor=slcolor)
        self.sl3 = Slider(self.slax3, 'z', 0, self.z-1, valinit=self.zCur,
                          valfmt='%i', valstep=1)
        self.sl3.on_changed(self.updateSl3)

        # ### BUTTONS


        # MultiCursor
        self.cursor1 = MultiCursor(self.fig.canvas, (axF[0], axF[3]),
                                  horizOn=True, vertOn=True, color='r', lw=1)
        self.cursor2 = MultiCursor(self.fig.canvas, (axF[1], axF[4]),
                                  horizOn=True, vertOn=True, color='g', lw=1)
        self.cursor3 = MultiCursor(self.fig.canvas, (axF[2], axF[5]),
                                  horizOn=True, vertOn=True, color='b', lw=1)
        self.cursor1.visible = False
        self.cursor2.visible = False
        self.cursor3.visible = False

        # Widget connections with the main window
        self.fig.canvas.mpl_connect('key_press_event', self.onKeyButtonClick)
        self.fig.canvas.mpl_connect('button_press_event', self.onMouseButtonClick)

        plt.suptitle('Random images')
        # plt.tight_layout()
        plt.show()


    def setNewImages(self, idx):
        im1 = self.dc['o'][idx]
        im2 = self.dc['n'][idx]
        fileName = self.dc['f'][idx]
        #print(fileName, idx)

        self.i1 = im1
        self.i2 = im2
        self.i1mx, self.i1mn = im1.max(), im1.min()
        self.i2mx, self.i2mn = im2.max(), im2.min()
        self.fileName = fileName

        self.x, self.y, self.z = im1.shape
        self.xCur = int(self.x // 2)
        self.yCur = int(self.y // 2)
        self.zCur = int(self.z // 2)
        plt.suptitle(self.fileName)

    def updateSliderRanges(self):
        self.sl1.valmax = self.x-1
        self.sl2.valmax = self.y-1
        self.sl3.valmax = self.z-1

        self.slax1.set_xlim(0, self.x-1)
        self.slax2.set_xlim(0, self.y-1)
        self.slax3.set_xlim(0, self.z-1)

        self.sl1.set_val(self.xCur)
        self.sl2.set_val(self.yCur)
        self.sl3.set_val(self.zCur)


    def accept(self):
        if hasattr(self, 'fileName'):
            if self.fileName not in self.accList and self.fileName not in self.rejList:
                self.accList.append(self.fileName)
                self.acceptNr += 1
                print ('{} --- accepted ({})'.format(self.fileName, self.acceptNr))
            else:
                print('Image "%s" is on the list already' % self.fileName)

    def reject(self):
        if hasattr(self, 'fileName'):
            if self.fileName not in self.rejList and self.fileName not in self.accList:
                self.rejList.append(self.fileName)
                self.rejectNr += 1
                print ('{} --- rejected ({})'.format(self.fileName, self.rejectNr))
            else:
                print('Image "%s" is on the list already' % self.fileName)

    def goToNextImage(self):
        if self.Idx < self.IdxMax:
            print('{}/{}'.format(self.Idx+1, self.IdxMax), end=': ')
            self.setNewImages(self.Idx)
            self.updateSliderRanges()
            self.updateSliceViews()
            self.fig.canvas.draw()
            self.Idx +=1
        else:
            print("That's all")

    def onKeyButtonClick(self, event):
        if event.key == 'n':
            # print('Key --- > goToNextImage function')
            self.goToNextImage()
        if event.key == 'a':
            # print('Key --- > Accept function')
            self.accept()
        if event.key == 'd':
            # print('Key --- >  delete/reject function')
            self.reject()
        if event.key == 'ctrl+a':
            print('\n\nA list of accepted images:\n')
            [print(f) for f in self.accList]
        if event.key == 'ctrl+d':
            print('\n\nA list of rejected images:\n')
            [print(f) for f in self.rejList]
        if event.key == 'alt+a':
            with open('accepted_list.txt', 'w') as f:
                [f.write('{}\n'.format(i)) for i in self.accList]
            print('accepted list saved to a file')
        if event.key == 'alt+d':
            with open('rejected_list.txt', 'w') as f:
                [f.write('{}\n'.format(i)) for i in self.rejList]
            print('rejected list saved to a file')

        if event.key == 'm':
            self.prepareMIPImages(k='M')
        if event.key == 'ctrl+m':
            self.prepareMIPImages(k='m')
        if event.key == 'i':
            self.info()


        if event.key == '1':
            self.cursor1.visible = not self.cursor1.visible
            self.cursor2.visible = self.cursor3.visible = False
        if event.key == '2':
            self.cursor2.visible = not self.cursor2.visible
            self.cursor1.visible = self.cursor3.visible = False
        if event.key == '3':
            self.cursor3.visible = not self.cursor3.visible
            self.cursor1.visible = self.cursor2.visible = False
        self.fig.canvas.draw()

    def prepareMIPImages(self, k='M'):
        if k == 'M':
            self.vo1.set_data(self.i1.max(0))
            self.vn1.set_data(self.i2.max(0))
            self.vo2.set_data(self.i1.max(1))
            self.vn2.set_data(self.i2.max(1))
            self.vo3.set_data(self.i1.max(2))
            self.vn3.set_data(self.i2.max(2))
        if k == 'm':
            self.vo1.set_data(self.i1.min(0))
            self.vn1.set_data(self.i2.min(0))
            self.vo2.set_data(self.i1.min(1))
            self.vn2.set_data(self.i2.min(1))
            self.vo3.set_data(self.i1.min(2))
            self.vn3.set_data(self.i2.min(2))

    def onMouseButtonClick(self, event):
        windowNr = -1
        for k, v in enumerate(self.ax.flat[:]):
            if event.inaxes == v.axes:
                windowNr = k
                break
        if windowNr < 0: return
        if windowNr in [0, 3]:
            # print(1, event.xdata, event.ydata)
            xx = self.sl1.val
            yy = event.ydata
            zz = event.xdata
            self.sl2.set_val(yy)
            self.sl3.set_val(zz)
        if windowNr in [1, 4]:
            # print(2, event.xdata, event.ydata)
            xx = event.ydata
            yy = self.sl2.val
            zz = event.xdata
            self.sl1.set_val(xx)
            self.sl3.set_val(zz)
        if windowNr in [2, 5]:
            # print(3, event.xdata, event.ydata)
            xx = event.ydata
            yy = event.xdata
            zz = self.sl3.val
            self.sl1.set_val(xx)
            self.sl2.set_val(yy)
        self.fig.canvas.draw()

    def updateSl1(self, val):
        self.xCur = int(val)
        self.updateSliceViews()

    def updateSl2(self, val):
        self.yCur = int(val)
        self.updateSliceViews()

    def updateSl3(self, val):
        self.zCur = int(val)
        self.updateSliceViews()

    def updateSliceViews(self):
        # X
        xCur = self.xCur
        i1mx, i1mn = self.i1mx, self.i1mn
        i2mx, i2mn = self.i2mx, self.i2mn

        self.vo1.set_clim(i1mn, i1mx)
        self.vn1.set_clim(i2mn, i2mx)
        [v.set_clim(i1mn, i1mx) for v in self.viewsO]
        [v.set_clim(i2mn, i2mx) for v in self.viewsN]

        self.vo1.set_data(self.i1[xCur, :, :])
        self.vn1.set_data(self.i2[xCur, :, :])
        # Y
        yCur = self.yCur
        self.vo2.set_data(self.i1[:, yCur, :])
        self.vn2.set_data(self.i2[:, yCur, :])
        # Z
        zCur = self.zCur
        self.vo3.set_data(self.i1[:, :, zCur])
        self.vn3.set_data(self.i2[:, :, zCur])

        [a.relim() for a in self.ax.flat[:]]
        [a.autoscale_view(True,True, True) for a in self.ax.flat[:]]
        self.fig.canvas.draw()

    def info(self):
        print("Usage:")
        print("""1/2/3 --- turn on/off a cursor on images:\n\t1-(o1, n1),\n\t2-(o2, n2),\n\t3-(o3, n3),""")
        print("n --- select next image,")
        print('a/ctrl+a/alt+a --- accept an image/print accepted list/save accepted list to a file "accepted_list.txt",')
        print('d/ctrl+d/alt+d --- reject(delete) an image/print rejected list/save rejected list to a file "rejected_list.txt",')
        print("m/ctr+m --- display Maximim/minimum Intensity Projections,")
        print("i --- print help.")



if __name__ == '__main__':

    dc = prepareFilesDictionary(filesNr=0)
    dictionaryInfo(dc)
    print(30*'c')

    sel = ImageSelector(dc)

