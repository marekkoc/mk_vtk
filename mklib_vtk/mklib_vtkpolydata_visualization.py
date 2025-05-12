#!/usr/bin/kate
#vim: set ff=unix:
"""
A module with definition of some functions to deal polydata in a VTK scene.


Some of functions, in witch any objects are build, were moved to a newly created file mklib_vtkpolydata_sources.py on 2019.06.14


script name: mk_vtkpolydata.py

(C) MK & AM

C: 2018.04.13
M: 2018.06.14
"""

import vtk
all = []

def displayPolyData( ren, polydata, scalarVisibility=False, color=(.9,.1,.1), opa=1, withedges= False, lineWidth=False, backCulling=False):
    mapper = vtk.vtkPolyDataMapper()
    if scalarVisibility:
        mapper.ScalarVisibilityOn()
        mapper.SetScalarRange(0,polydata.GetPointData().GetNumberOfTuples())
    else:
        mapper.ScalarVisibilityOff()

    mapper.SetInputData( polydata )

    actor = vtk.vtkActor()
    actor.GetProperty().SetColor( *color ) # ( 0.5, 0.5, 0.5 )
    actor.GetProperty().SetOpacity( opa )
    if backCulling:
        actor.GetProperty().BackfaceCullingOn()
    if lineWidth:
        actor.GetProperty().SetLineWidth(lineWidth)
    actor.SetMapper( mapper )
    if withedges:
        actor.GetProperty().SetEdgeColor(1.0, 1.0, 1.0) # (0.0, 0.0, 0.0)
        actor.GetProperty().EdgeVisibilityOn()
    ren.AddActor( actor )
all.append('displayPolyData')


def sphereGlyphPoints(polydata, sphereRadius ):
	"""
		previous name: cubeGlyphPoints
	"""
	sphere = vtk.vtkSphereSource()
	sphere.SetRadius(sphereRadius)
	sphere.Update()
	glyph = vtk.vtkGlyph3D()
	glyph.SetInputData(polydata)
	glyph.SetSourceConnection(sphere.GetOutputPort())
	glyph.GeneratePointIdsOn()
	glyph.ScalingOff()
	glyph.Update()

    #mapper = vtk.vtkPolyDataMapper()
    #mapper.SetInputData( glyph.GetOutput() )
    #actor = vtk.vtkActor()
    #actor.GetProperty().SetColor( 0.1,0.1,0.9 ) # (R,G,B)
    #actor.SetMapper( mapper )
    #ren.AddActor( actor )
	return glyph.GetOutput()
all.append('sphereGlyphPoints')

def linesBetweenPointSet(coord_list):
	"""
	previous name: lineMidPoints
	"""
	pts = vtk.vtkPoints()
	pts.SetNumberOfPoints(len(coord_list))

	polyLine = vtk.vtkCellArray()
	#polyLine.InsertNextCell(len(coord_list))

	for i in range(len(coord_list)):
		pts.SetPoint(i, *coord_list[i])
		#polyLine.InsertCellPoint(i)

	for i in range(len(coord_list)-1):
		line = vtk.vtkLine()
		line.GetPointIds().SetId(0,i)
		line.GetPointIds().SetId(1,i+1)
		polyLine.InsertNextCell(line)


	linesPolyData = vtk.vtkPolyData()
	linesPolyData.SetPoints(pts)
	linesPolyData.SetLines(polyLine)

	#mapper = vtk.vtkPolyDataMapper()
	#mapper.SetInputData(linesPolyData)
	#actor = vtk.vtkActor()
	#actor.GetProperty().SetColor(*color)
	#actor.SetMapper(mapper)
	#ren.AddActor(actor)

	return linesPolyData
all.append('linesBetweenPointSet')


def marchingCubes1(ren, vtkimage,iso,color=[1,0,0]):
	marching = vtk.vtkMarchingCubes()
	marching.SetInputData(vtkimage)
	marching.ComputeNormalsOn()
	marching.SetValue(0,iso)
	marching.Update()

	mapper = vtk.vtkPolyDataMapper()
	mapper.SetInputData(marching.GetOutput())
	mapper.ScalarVisibilityOff()

	actor = vtk.vtkLODActor()
	actor.SetNumberOfCloudPoints(1000000)
	actor.SetMapper(mapper)
	actor.GetProperty().SetColor(color)
	ren.AddActor(actor)
all.append('marchingCubes1')


def planeWidget(ren, vtkimage, dir='x'):
    """
    Tuz za ta funkcja trzeba podlaczyc interaktor:
    for plane in [planeX, planeY, planeZ]:
        plane.SetInteractor(iren)
        plane.On()
    """
    dimensions = vtkimage.GetDimensions()

    if dir == 'x':
        planeWidgetX = vtk.vtkImagePlaneWidget()
        planeWidgetX.DisplayTextOn()
        planeWidgetX.SetInputData(vtkimage)
        planeWidgetX.SetPlaneOrientationToXAxes()
        planeWidgetX.SetSliceIndex(dimensions[0]//2)
        planeWidgetX.RestrictPlaneToVolumeOn()
        planeWidgetX.SetKeyPressActivationValue('x')
        planeWidgetX.GetPlaneProperty().SetColor(1, 0, 0)
        planeWidgetX.SetResliceInterpolateToNearestNeighbour()
        # planeWidgetX.SetInteractor(iren)
        # planeWidgetX.On()
        return planeWidgetX
    if dir == 'y':
        planeWidgetY = vtk.vtkImagePlaneWidget()
        planeWidgetY.DisplayTextOn()
        planeWidgetY.SetInputData(vtkimage)
        planeWidgetY.SetPlaneOrientationToYAxes()
        planeWidgetY.SetSliceIndex(dimensions[1]//2)
        planeWidgetY.RestrictPlaneToVolumeOn()
        planeWidgetY.SetKeyPressActivationValue('y')
        planeWidgetY.GetPlaneProperty().SetColor(0, 1, 0)
        planeWidgetY.SetResliceInterpolateToLinear()
        return planeWidgetY
        # planeWidgetY.SetInteractor(iren)
        # planeWidgetY.On()
    if dir == 'z':
        planeWidgetZ = vtk.vtkImagePlaneWidget()
        planeWidgetZ.DisplayTextOn()
        planeWidgetZ.SetInputData(vtkimage)
        planeWidgetZ.SetPlaneOrientationToZAxes()
        planeWidgetZ.SetSliceIndex(dimensions[2]//2)
        planeWidgetZ.RestrictPlaneToVolumeOn()
        planeWidgetZ.SetKeyPressActivationValue('z')
        planeWidgetZ.GetPlaneProperty().SetColor(0, 0, 1)
        planeWidgetZ.SetResliceInterpolateToCubic()
        # planeWidgetZ.SetInteractor(iren)
        # planeWidgetZ.On()
        return planeWidgetZ


all.append('planeWidget')
