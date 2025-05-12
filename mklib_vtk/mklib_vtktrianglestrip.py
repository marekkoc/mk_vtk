#!/usr/bin/kate
#vim: ff=unix:

"""
A script with definition of rendering functions VTK scripts.

script name: mk_vtk_rendering.py

(C) MK & AM

C: 2018.03.24
M: 2019.04.11
"""
import vtk
import numpy as np

all = []

def displayTriangleStrip(ren, polydata, rep='wire'):
    """
    rep == 'points'/'wire'/'surface'
    C: 2019.04.11
    M: 2019.04.11
    """

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    if rep == 'points':
        actor.GetProperty().SetRepresentationToPoints()
    elif rep == 'surface':
        actor.GetProperty().SetRepresentationToSurface()
    else:
        actor.GetProperty().SetRepresentationToWireframe()
    ren.AddActor(actor)
all.append('displayTriangleStrip')

def setTriangleStripVerticles(p0,p1,vec, k=4):
    """
    Funkcja generuje wspolrzedne potrzebne do zbudowania paska trojkatow
    pomiedzy punktami p0 i p1.

    p0 - lewy dolny rog paska [x0, y0, z0]
    p1 - prawy dolny rog paska [x1, y1, z1]
    vec = wysokosc paska

    C: 2019.04.11
    M: 2019.04.11
    """
    p0 = np.array(p0)
    p1 = np.array(p1)
    vec = np.array(vec)

    p2 = p0 + vec
    p3 = p1 + vec

    x0, y0, z0 = p0
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3

    dx = np.linspace(x0, x1, k+1)
    dy = np.linspace(y0, y1, k+1)
    dz = np.linspace(z0, z1, k+1)
    d = np.c_[dx, dy, dz]

    ex = np.linspace(x2, x3, k+1)
    ey = np.linspace(y2, y3, k+1)
    ez = np.linspace(z2, z3, k+1)
    e = np.c_[ex, ey, ez]

    r, c = d.shape
    vert  = np.empty((2*r, c))
    vert[::2] = d
    vert[1::2] = e
    return vert
all.append('setTriangleStripVerticles')


def triangleStripPolyData(vert):
    """
    Funkcja przygotowuje pasek trojkatow na podstawie macierzy
    wierzholkow z funkcji getTriangleStripVerticles
    C: 2019.04.11
    M: 2019.04.11
    """
    points = vtk.vtkPoints()
    for pts in vert:
        points.InsertNextPoint(*pts)

    ptsNr = vert.shape[0]
    triangleStrip = vtk.vtkTriangleStrip()
    triangleStrip.GetPointIds().SetNumberOfIds(ptsNr)
    for pt in range(ptsNr):
        triangleStrip.GetPointIds().SetId(pt, pt)

    cells = vtk.vtkCellArray()
    cells.InsertNextCell(triangleStrip)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetStrips(cells)
    return polydata
all.append('triangleStripPolyData')



#all=['createMainVTKWindow','displayAxesWXYZ0','DisplayUnitSphereWXY0','displayPlaneWXY0',
# 'setActiveCamera','close_window']




