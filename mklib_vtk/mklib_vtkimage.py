#!/usr/bin/kate
#vim: set ff=unix:
"""
Convertion among datatypes (VTK, Numpy).

(C) MK & AM

C: 2018.04.23
M: 2018.06.20
"""

import vtk
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk


### READERS ###
def dicomImageReader(folder):
	reader = vtk.vtkDICOMImageReader()
	reader.SetDirectoryName(folder)
	reader.Update()
	return reader

def rawImageReader(filename,**kw):
		origin = kw.get('origin',[0,0,0])
		spacing = kw.get('spacing',[1.0,1.0,1.0])
		dim = kw.get('dim',3)
		dtype = kw.get('dtype',vtk.VTK_UNSIGNED_CHAR)
		extent = kw.get('extent',[0,255,0,255,0,255])
		
		readerVolume = vtk.vtkImageReader()
		readerVolume.SetDataScalarType(dtype)
		readerVolume.SetFileDimensionality(3)
		readerVolume.SetDataExtent(*extent)
		readerVolume.SetDataSpacing(*spacing)
		readerVolume.SetDataOrigin(*origin)
		readerVolume.SetNumberOfScalarComponents(1)
		#readerVolume.SetDataByteOrderToBigEndian()
		readerVolume.SetFileName(filename)
		readerVolume.Update()
		return readerVolume

def vtkImageReader(filename):
	reader = vtk.vtkStructuredPointsReader()
	reader.SetFileName(filename)
	reader.Update()
	return reader

def vtkNIFTIReader(filename):
	"""
	to implement:
	vtk.org/doc/nightly/html/classvtkNIFTIImageReader.html
	https://vtk.org/doc/nightly/html/c2_vtk_t_13.html#c2_vtk_t_vtkNIFTIImageReader
	
	"""
	pass
	
### WRITERS ###
def writeVtkImageData(image, filename='xxx.vtk'):
	writer = vtk.vtkStructuredPointsWriter()
	writer.SetInputData(image)
	writer.SetFileName(filename)
	writer.Update()
	writer.Write()
	
def vtkNIFTIWriter(image, filename):
	"""
	to implement
	https://vtk.org/doc/nightly/html/c2_vtk_t_13.html#c2_vtk_t_vtkNIFTIImageReader
	"""
	pass

### CONVERTERS ###
def convertVtkImageDataToNumpy(image):
	r,c,s = image.GetDimensions()
	sc = image.GetPointData().GetScalars()

	array  = vtk_to_numpy(sc)
	array=array.reshape(r,c,s,order='F')
	return array

def convertNumpyArrayToVtkImage(array, origin=(0,0,0), spacing=(1,1,1)):
    """
    Convert a numpy 3D array to a vtkImageData
    """
    from vtk.util.numpy_support import numpy_to_vtk
    
    # Spłaszcz tablicę używając prawidłowej składni
    flat_array = array.flatten('C')  # 'C' oznacza row-major order (domyślny w NumPy)
    
    vtkimage = numpy_to_vtk(flat_array, deep=True, array_type=vtk.VTK_UNSIGNED_SHORT)
    
    # Reszta funkcji pozostaje bez zmian
    img = vtk.vtkImageData()
    img.SetDimensions(array.shape[0], array.shape[1], array.shape[2])
    img.SetSpacing(spacing)
    img.SetOrigin(origin)
    img.GetPointData().SetScalars(vtkimage)
    
    return img

### Info ###
def getVtkImageInfo(image,name='VTK image'):
	print(50*'*')
	s = "*** " + name + " ***"
	print(s)
	print(len(s)*'*')
	dataDimension = image.GetDataDimension()
	print("* dataDimension = ", dataDimension)
	voxelType = image.GetScalarTypeAsString()
	print('* voxelType = ', voxelType)
	origin = image.GetOrigin()
	print('* origin = ', origin)
	spacing = image.GetSpacing()
	print('* spacing = ', spacing)
	dimensions = image.GetDimensions()
	print('* dimensions = ', dimensions)	
	extent = image.GetExtent()
	print('* extent = ', extent)
	bounds = image.GetBounds()
	print('* bounds = ', bounds)
	numberOfPoints = image.GetNumberOfPoints()
	print('* numberOfPoints =', numberOfPoints)
	length = image.GetLength()
	print('* length = ', length)
	print(50*'*')
	
def getNumpyArrayInfo(im, name="Numpy array"):
	print(50*'*')
	s = "*** " + name + " ***"
	print(s)
	print(len(s)*'*')
	print("max={}, min={}, aver={:.2f}, dtype={}, shape={}".format(im.max(),im.min(),im.mean(),im.dtype,im.shape))

### Extract ROI
def vtkVoiExtractor(img, region=[0,100,0,80,0,70], sampleRate=[1,1,1]):
	voi = vtk.vtkExtractVOI()
	voi.SetInputData(img)
	voi.SetVOI(*region)
	voi.SetSampleRate(*sampleRate)
	voi.Update()
	return voi

### Resample image (Reslice)
def resampleVtkImage(vtkImage,spacing=[1,1,1]):
	"""
	https://coderwall.com/p/gij2va/resample-3d-image-data-in-a-vtkimagedata-object-using-the-vtkimagereslice-class
	"""
	resliceFilter = vtk.vtkImageReslice()
	resliceFilter.SetInputData(vtkImage)
	resliceFilter.SetOutputSpacing(*spacing)
	resliceFilter.SetInterpolationModeToCubic()
	resliceFilter.Update()
	return resliceFilter.GetOutput()

### Threshold image
def thresholdVtkImageByUpper(vtkImage, upperVal = 115, InVal=255, OutVal=0):
	th = vtk.vtkImageThreshold()
	th.SetInputData(vtkImage)
	th.ThresholdByUpper(upperVal)
	th.SetInValue(InVal)
	th.SetOutValue(OutVal)
	th.Update()
	return th

all=['dicomImageReader','rawImageReader','vtkImageReader','writeVtkImageData',
'convertVtkImageDataToNumpy',	 
'convertNumpyArrayToVtkImage','getVtkImageInfo','getNumpyArrayInfo','vtkVoiExtractor',
'vtkVoiExtractor','thresholdVtkImageByUpper']
