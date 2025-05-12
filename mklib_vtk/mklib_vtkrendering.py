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

all = []


def createMainVTKWindow():
    ren = vtk.vtkRenderer()
    ren.SetBackground(0.329412, 0.34902, 0.427451)   # Paraview blue

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(700, 700)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    return ren, renWin, iren


all.append('createMainVTKWindow')


def displayAxesWXYZ0(ren, pos=(0, 0, 0), scale=(1, 1, 1)):
    transform = vtk.vtkTransform()
    transform.Translate(pos)
    transform.Scale(scale)

    axesActor = vtk.vtkAxesActor()
    axesActor.SetUserTransform(transform)
    ren.AddActor(axesActor)


all.append('displayAxesWXYZ0')


def displayUnitSphereWXY0(ren, rad=1, col=(.8,.8,.8), opa=1, edgeVisibility=False):
	sphereSource = vtk.vtkSphereSource()
	sphereSource.SetRadius(rad)
	sphereSource.SetThetaResolution(36)
	sphereSource.SetPhiResolution(18)
	sphereSource.Update()

	#sphere = vtk.vtkPolyData()
	sphere = sphereSource.GetOutput()

	mapper = vtk.vtkPolyDataMapper()
	mapper.SetInputData(sphere)

	actor = vtk.vtkActor()
	actor.GetProperty().SetColor(*col) # (R,G,B)
	if edgeVisibility:
		actor.GetProperty().EdgeVisibilityOn()
		actor.GetProperty().SetEdgeColor( 0.75, 0.75, 0.75)
	actor.GetProperty().SetOpacity(opa)
	#    actor.SetTexture( texture )
	actor.SetMapper( mapper )
	ren.AddActor( actor )
all.append('displayUnitSphereWXY0')

def displayPlaneWXY0(ren,deltaXY=(10,10), xRange=[-5, 5], yRange=[-10,10]):
    planeSource = vtk.vtkPlaneSource()
    lon_min = xRange[0]
    lon_max = xRange[1]
    lat_min = yRange[0]
    lat_max = yRange[1]
    planeSource.SetXResolution(deltaXY[0])
    planeSource.SetYResolution(deltaXY[1])
    planeSource.SetOrigin( lon_min, lat_min, -0.0001)
    planeSource.SetPoint1( lon_max, lat_min, -0.0001)
    planeSource.SetPoint2( lon_min, lat_max, -0.0001)
    planeSource.Update()

    #geogrid = vtk.vtkPolyData()
    geogrid = planeSource.GetOutput()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(geogrid)

    actor = vtk.vtkActor()
#    actor.SetTexture( texture )
#    actor.GetProperty().SetColor( color ) # (R,G,B)
#    actor.GetProperty().EdgeVisibilityOff()
    actor.GetProperty().EdgeVisibilityOn()
#    actor.GetProperty().SetEdgeColor( 1, 1, 1)
    actor.GetProperty().SetEdgeColor( 0.75, 0.75, 0.75)
    actor.GetProperty().SetOpacity( 0.5 )

    actor.SetMapper( mapper )
    ren.AddActor( actor )
all.append('displayUnitSphereWXY0')

def setActiveCamera(ren,pos=(0,0,5), foc=(0,0,0)):
	camera = vtk.vtkCamera()
	camera.SetPosition(*pos)
	camera.SetFocalPoint(*foc)

	ren.SetActiveCamera(camera)
	#ren.ResetCamera()
all.append('setActiveCamera')

def close_window(iren, render_window):
    """Ta funkcja jest wywolywana na koncu programu!
    A potem jeszcze kasujemy recznie obiekty:
    del renWin, iren
    """
    render_window = iren.GetRenderWindow()
    render_window.Finalize()
    iren.TerminateApp()
all.append('close_window')


#all=['createMainVTKWindow','displayAxesWXYZ0','DisplayUnitSphereWXY0','displayPlaneWXY0',
# 'setActiveCamera','close_window']




