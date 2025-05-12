#!/usr/bin/env python

"""
(C) MK

Plil pod zmieniona nazwa. Nazwy pierwotna: mk_Viewer3D_ver1

C : 2015
M: 2019.06.10

ver: 0.02
"""
import os
import sys
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

#from mk_paths import MY_PYTHON_DATA_DIR
from mkReader import mkReader




class Viewer3D:

    def __init__(self, X, figName='', debug=True):
        """ """

        self.debug = debug

        zsize, ysize, xsize = X.shape
        self.slices,rows,cols = X.shape
        self.ind  = int(self.slices/2)

        self.val0 = int(self.slices/2)
        self.cmap = plt.cm.gray
        self.X = X

        self.fig = plt.figure()
        self.fig.suptitle(figName, color='blue', fontsize=16)

        self.ax = plt.axes([0.1,0.2,0.6,0.6])
        self.l = self.ax.imshow(self.X[self.val0,:,:], interpolation='nearest',cmap=self.cmap)
        plt.axis('off')
        plt.title('Current slice (dir 0) - slice %d'%self.val0)
        self.fig.add_axes(self.ax)
        self.fig.colorbar(self.l)


        self.a0 = plt.axes([0.7, 0.7,0.25,0.25])
        self.i0 = plt.imshow(self.X.max(0),interpolation='nearest',cmap=self.cmap)
        plt.axis('off')
        plt.title('MIP (dir 0)')
        self.fig.add_axes(self.a0)
        plt.colorbar()

        self.a1 = plt.axes([0.7,0.4,0.25,0.25])
        self.i1 = plt.imshow(self.X.max(1), interpolation='nearest', cmap=self.cmap)
        plt.axis('off')
        plt.title('MIP (dir 1)')
        self.fig.add_axes(self.a1)
        plt.colorbar()

        self.a2 = plt.axes([0.7,0.1,0.25,0.25])
        self.i2 = plt.imshow(self.X.max(2), interpolation='nearest', cmap=self.cmap)
        plt.axis('off')
        plt.title('MIP (dir 2)')
        self.fig.add_axes(self.a2)
        plt.colorbar()



        self.axcolor = 'lightgoldenrodyellow'
        axamp  = plt.axes([0.1,0.1,0.5, 0.03])
        self.samp = Slider(axamp, 'xpos',0, self.slices-1, valinit=self.val0)
        self.samp.on_changed(self.__update__)

        rax = plt.axes([0.005, 0.5, 0.12, 0.25])
        self.radio = RadioButtons(rax, ('gray', 'jet', 'hot','copper','hot','hsv',
                                        'winter','summer','spring','spectral',
                                        'autumn'), active=0)
        self.radio.on_clicked(self.__colorfunc__)

        resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
        self.button = Button(resetax, 'Reset', color=self.axcolor, hovercolor='0.975')

        #textstr = "ala\nma\nkota"
        #props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        #self.ax.text(0.05, 0.95, textstr, transform=self.ax.transAxes, fontsize=14,
        #verticalalignment='top', bbox=props)

        self.__update__(self.samp.val)
        self.button.on_clicked(self.__reset__)


        cid1 = self.fig.canvas.mpl_connect('button_press_event', self.__onclick__)
        cid2 = self.fig.canvas.mpl_connect('scroll_event', self.__onscroll__)
        cid3 = self.fig.canvas.mpl_connect('key_press_event', self.__toogle_images__)

        self.fig.show()
        plt.show()


    def __update__(self,val):
        self.samp.val
        #ax.imshow(data[val,:,:],interpolation='nearest',cmap=cmap)
        self.l.set_data(self.X[val,:,:])
        self.ax.set_title('Current slice (dir 0) - slice %d'%val)
        self.l.axes.figure.canvas.draw()

    def __colorfunc__(self,label):
        self.l.set_cmap(label)
        self.l.axes.figure.canvas.draw()
        self.i0.set_cmap(label)
        self.i0.axes.figure.canvas.draw()
        self.i1.set_cmap(label)
        self.i1.axes.figure.canvas.draw()
        self.i2.set_cmap(label)
        self.i2.axes.figure.canvas.draw()


    def __onclick__(self,event):
        if event.inaxes == self.ax.axes:
            img = 'ax'
        elif event.inaxes == self.a0.axes :
            img = 'a0'
        elif event.inaxes == self.a1.axes:
            img = 'a1'
        elif event.inaxes == self.a2.axes:
            img = 'a2'
        else:
            return
        if self.debug: print( '%s, button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(img,
            event.button, event.x, event.y, event.xdata, event.ydata))

    def __onscroll__(self,event):
        #print event.button, event.step
        if event.button=='up':
            self.samp.set_val(self.samp.val+1)
        else:
            self.samp.set_val(self.samp.val-1)
        self.l.axes.figure.canvas.draw()

    def __reset__(self,event):
        self.samp.reset()
        self.l.axes.figure.canvas.draw()
        if self.debug: print('reset')



    def __toogle_images__(self,event):
        """ttoogle amont images displayed on ax2,ax3,ax4: (max,mean,std,min)"""
        if event.key == '1':
            s = ' max'
            if self.debug: print('pressd key:'+event.key + s)
            self.a0.set_title('%s (dir 0)'%(s))
            self.i0.set_data(self.X.max(0))
            self.i0.axes.figure.canvas.draw()

            self.a1.set_title('%s (dir 1)'%(s))
            self.i1.set_data(self.X.max(1))
            self.i1.axes.figure.canvas.draw()

            self.a2.set_title('%s (dir 2)'%(s))
            self.i2.set_data(self.X.max(2))
            self.i2.axes.figure.canvas.draw()
        elif event.key == '2':
            s =' mean'
            if self.debug: print ('pressd key:'+event.key + s)
            self.a0.set_title('%s (dir 0)'%(s))
            self.i0.set_data(self.X.mean(0))
            self.i0.axes.figure.canvas.draw()

            self.a1.set_title('%s (dir 1)'%(s))
            self.i1.set_data(self.X.mean(1))
            self.i1.axes.figure.canvas.draw()

            self.a2.set_title('%s (dir 2)'%(s))
            self.i2.set_data(self.X.mean(2))
            self.i2.axes.figure.canvas.draw()
        elif event.key == '3':
            s = ' std'
            if self.debug: print ('pressd key:'+event.key + s)
            self.a0.set_title('%s (dir 0)'%(s))
            self.i0.set_data(self.X.std(0))
            self.i0.axes.figure.canvas.draw()

            self.a1.set_title('%s (dir 1)'%(s))
            self.i1.set_data(self.X.std(1))
            self.i1.axes.figure.canvas.draw()

            self.a2.set_title('%s (dir 2)'%(s))
            self.i2.set_data(self.X.std(2))
            self.i2.axes.figure.canvas.draw()
        elif event.key == '4':
            s = ' min'
            if self.debug: print ('pressd key:'+event.key + s)
            self.a0.set_title('%s (dir 0)'%(s))
            self.i0.set_data(self.X.min(0))
            self.i0.axes.figure.canvas.draw()

            self.a1.set_title('%s (dir 1)'%(s))
            self.i1.set_data(self.X.min(1))
            self.i1.axes.figure.canvas.draw()

            self.a2.set_title('%s (dir 2)'%(s))
            self.i2.set_data(self.X.min(2))
            self.i2.axes.figure.canvas.draw()
        else: return


def main():
    if len(sys.argv)<2:
        print ("Usage:\nVeiwer3D_ver1.1 fileToDispaly.npy")
        pth = os.path.join('/', 'media', 'marek', 'p1ext4', 'work', '00', 'all_data')
        data = np.load(os.path.join(pth, 'normal01.npy'))

        print ("*** Loaded...default image ***")

    else:
        file, ext = os.path.splitext(sys.argv[1])
        if ext == ".raw":
            if len(sys.argv)<4:
                print ("*** Zla liczba parametrow! ***\n\n*** Usage:\n*** Veiwer3D_ver1.1 fileToDispaly.raw size dtype")
                return
            else:
                data = np.fromfile(sys.argv[1] ,dtype=str(sys.argv[3]))
                res = int(sys.argv[2])
                data.shape = res,res,res
        elif ext == ".npy" and os.path.exists(sys.argv[1]):
            data = np.load(sys.argv[1])
        elif ext == ".nii" or ".nii.gz":
            data = nib.load(sys.argv[1]).get_data()
            data = data.reshape(data.shape, order='C')
        else:
            print( '\n*** Cos nie tak:\n-nieobslugiwany format plikow,\n-plik o podanej nazwie nieistenieje,\n-zla liczba parametrow ***\n')
            return

    print (data.shape, type(data))
    Viewer3D(data, "Numerical phantom :-)" )


#############################################
############ STAND ALONE PROGRAM ############
#############################################

if __name__ == '__main__':

    main()
#else:
#    print 'Class Viewer3D imported successfully from Viewer3D_ver1.1.py'
