#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

A module to create and test VTK library rendering process.

Created on Wed Jul  3 16:31:02 2019
@author: marek

(C) MK & AM

C: 2019.07.03
M: 2019.08.22

v: 0.01
"""

import vtk

class mkRenderer(object):
    """
    C: 2019.07.03
    M: 2019.08.22
    """
    def __init__(self, bgCol=[0.329412, 0.34902, 0.427451]):
        # Renderer
        self._bgColor = bgCol # Paraview blue
        self._ren = vtk.vtkRenderer()
        self._ren.SetBackground(*self._bgColor)

        # Renderer window
        self._renWinSize = (700, 500)
        self._renWin = vtk.vtkRenderWindow()
        self._renWin.AddRenderer(self._ren)
        self._renWin.SetSize(*self._renWinSize)

        # Renderer Window Interactor
        self._iren = vtk.vtkRenderWindowInteractor()
        self._iren.SetRenderWindow(self._renWin)

    def __del__(self):
        # self._iren.GetRenderWindow().Finalize()
        # self._iren.TerminateApp()
        del self._ren
        del self._renWin
        del self._iren

    def displayAxesWXYZ0(self, pos=(0,0,0), scale=(1,1,1)):
        transform = vtk.vtkTransform()
        transform.Translate(pos)
        transform.Scale(scale)

        axesActor = vtk.vtkAxesActor()
        axesActor.SetUserTransform(transform)
        self.ren = axesActor

    def displayPlaneWXYZ0(self, delXY=(10,10), xRng=[-5,5], yRng=[-10,10], zPos=-0.0001, opa=0.5):
        planeSource = vtk.vtkPlaneSource()
        xmin, xmax = xRng
        ymin, ymax = yRng
        planeSource.SetXResolution(delXY[0])
        planeSource.SetYResolution(delXY[1])
        planeSource.SetOrigin(xmin, ymin, zPos)
        planeSource.SetPoint1(xmax, ymin, zPos)
        planeSource.SetPoint2(xmin, ymax, zPos)
        planeSource.Update()

        # poly data, mapper & actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(planeSource.GetOutput())
        actor = vtk.vtkActor()
        actor.GetProperty().EdgeVisibilityOn()
        actor.GetProperty().SetEdgeColor(0.75, 0.75, 0.75)
        actor.GetProperty().SetOpacity(opa)
        actor.SetMapper(mapper)
        self.ren = actor

    def displayUnitSphereWXYZ(self, rad=1, col=(.8,.8,.8), opa=1, edgeVisibility=False, pos=(0,0,0)):

        transform = vtk.vtkTransform()
        transform.Translate(pos)

        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetRadius(rad)
        sphereSource.SetThetaResolution(18)
        sphereSource.SetPhiResolution(18)
        sphereSource.Update()

        # poly data, mapper & actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(sphereSource.GetOutput())
        actor = vtk.vtkActor()
        actor.SetUserTransform(transform)
        actor.GetProperty().SetColor(*col)
        actor.GetProperty().SetOpacity(opa)
        if edgeVisibility:
            actor.GetProperty().EdgeVisibilityOn()
            actor.GetProperty().SetEdgeColor(0.75, 0.75, 0.75)
        actor.SetMapper(mapper)
        self.ren = actor

    def setActiveCamera(self, pos=(0,0,5), foc=(0,0,0)):
        camera = vtk.vtkCamera()
        camera.SetPosition(*pos)
        camera.SetFocalPoint(*foc)
        self.ren.SetActiveCamera(camera)
        #self.ren.ResetCamera()

    def getActiveCamera(self):
        """
        C: 2019.08.22
        M: 2019.08.22
        """
        return self.ren.GetActiveCamera()

    def setActiveCamera2(self, camera):
        """
        C: 2019.08.22
        M: 2019.08.22
        """
        self.ren.SetActiveCamera(camera)

    def sceneScreenShoot(self, saveFileName):
        """
        C: 2019.08.22
        M: 2019.08.22
        """
        # screenshot code:
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(self.renWin)
        w2if.Update()

        if not saveFileName.endswith(".png"):
            saveFileName += '.png'
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(saveFileName)
        writer.SetInputData(w2if.GetOutput())
        writer.Write()



    @property
    def ren(self):
        return self._ren

    @ren.setter
    def ren(self, actor):
        self.ren.AddActor(actor)

    @property
    def renWin(self):
        return self._renWin

    @property
    def iren(self):
        return self._iren

    @property
    def actors(self):
        return self._actors




if __name__ == '__main__':
    import os

    import mklib_vtkpolydata_sources as mkpds
    import mklib_vtkpolydata_utils as mkpdu
    import mklib_vtkpolydata_visualization as mkpdv

    from mkVoxel import mkVoxel

    rd = mkRenderer()
    rd.displayAxesWXYZ0(scale=(2,2,2))
    rd.displayPlaneWXYZ0(yRng=[-1,2])
    rd.displayUnitSphereWXYZ(opa=0.5)

    v1 = mkVoxel([0, 0, 0], [True, True, True, True, True, True])
    print(v1)

    for v in [v1]:
        pts = v.triangles
        pdlst = []
        for k in range(len(pts)):
            pdlst.append(mkpds.triangleFromPoints(*pts[k]))
        allpd = mkpdu.appendPolyDatas(pdlst)
        cln = mkpdu.cleanPolyData(allpd.GetOutput())
        mkpdv.displayPolyData(rd.ren, cln)

#    rd.ren.SetBackground([0.1, 0.1, 0.1])
#    rd.renWin.SetSize(640, 480)
    rd.renWin.Render()
    if 0:
        rd.sceneScreenShoot('screen2')
    rd.iren.Start()
    del rd
    print("\nEoF: %s" % os.path.basename(__file__))