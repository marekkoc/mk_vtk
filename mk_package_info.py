#!/usr/bin/env python
#vim: set ff=unix:
#-*- coding: utf-8 -*-
"""
Created on Wed Nov  1 13:00:07 2017
@author: Marek

C: 2017.11.01
M: 2019.07.14
"""
import platform as pl
print("\n")
print("Komputer: {}".format(pl.node()))
print("System operacyjny: {}, {}".format(pl.architecture()[1], pl.architecture()[0]))
try:
    import sys
    print ("\nWersja jezyka Python: {}\n".format(sys.version))
except ImportError:
    print('sys - not installed')
try:
    import numpy
    print("Numpy: {}".format(numpy.__version__))
except ImportError:
    print('numpy - not installed')
try:
    import scipy
    print("Scipy: {}".format(scipy.__version__))
except ImportError:
    print('scipy - not installed')
try:
    import matplotlib
    print("matplotlib: {}".format(matplotlib.__version__))
except ImportError:
    print('scipy - not installed')
try:
    import sklearn
    print("sklearn: {}".format(sklearn.__version__))
except ImportError:
    print('sklearn - not installed')
try:
    import skimage
    print("skimage: {}".format(skimage.__version__))
except ImportError:
    print('skimage - not installed')
try:
    import OpenGL
    print("OpenGL: {}".format(OpenGL.__version__))
except ImportError:
    print('OpenGL - not installed')
try:
    import nibabel
    print("nibabel: {}".format(nibabel.__version__))
except ImportError:
    print('nibabel - not installed')
try:
    import dicom
    print("dicom: {}".format(dicom.__version__))
except ImportError:
    print('dicom - not installed')
try:
    import tkinter
    print("tkinter: {}".format(tkinter.TkVersion))
except ImportError:
    print('tkiner - not installed')
try:
    import PyQt5
    from PyQt5 import QtCore
    print("PyQt5: {}".format(QtCore.QT_VERSION_STR))
except ImportError:
    print('PyQt5 - not installed')
try:
    import vtk
    print ("VTK: {}".format(vtk.vtkVersion.GetVTKSourceVersion()))
except ImportError:
    print("VTK - not installed")
try:
    import itk
    print ("ITK: {}".format(itk.Version.GetITKSourceVersion()))
except ImportError:
    print("ITK - not installed")
try:
    import PyInstaller
    print ("PyInstaller: {}".format(PyInstaller.__version__))
except ImportError:
    print("PyInstaller - not installed")
try:
    import PIL
    print ("PIL: {}".format(PIL.__version__))
except ImportError:
    print("PIL - not installed")
try:
    import imageio
    print ("imageio: {}".format(imageio.__version__))
except ImportError:
    print("imageio - not installed")
try:
	import cython
	print('cython: {}'.format(cython.__version__))
except ImportError:
	print("cython - not installed")
try:
    import csv
    print('csv: {}'.format(csv.__version__))
except ImportError:
    print("csv - not installed")
try:
    import json
    print('json: {}'.format(json.__version__))
except ImportError:
    print("json - not installed")

