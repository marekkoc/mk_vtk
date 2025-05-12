#!/usr/bin/kate
#vim: set ff=unix:
"""
Convertion among datatypes (VTK, Numpy).

(C) MK & AM

C: 2018.04.23
M: 2025.04.26 - nie działa zapis pliku zzz.vtk
"""

import vtk

# Użyj właściwej ścieżki importu dla VTK 9.2.6
try:
    from vtkmodules.util.numpy_support import vtk_to_numpy, numpy_to_vtk
except ImportError:
    # Fallback dla starszych wersji
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
		readerVolume.SetDataByteOrderToBigEndian()
		readerVolume.SetFileName(filename)
		readerVolume.Update()
		return readerVolume

def vtkImageReader(filename):
	reader = vtk.vtkStructuredPointsReader()
	reader.SetFileName(filename)
	reader.Update()
	return reader

def niftiImageReader(filename):
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader
	
### WRITERS ###
def writeVtkImageData(image, filename='xxx.vtk'):
	writer = vtk.vtkStructuredPointsWriter()
	writer.SetInputData(image)
	writer.SetFileName(filename)
	writer.Update()
	writer.Write()
    
def niftiImageWriter(image, filename='xxx.nii.gz', readerWithHeader=None):
    writer = vtk.vtkNIFTIImageWriter()
    writer.SetInputData(image)
    writer.SetFileName(filename)
    
    if readerWithHeader:
        # copy most information directory from the header
        writer.SetNIFTIHeader(readerWithHeader.GetNIFTIHeader())
        # this information will override the reader's header
        writer.SetQFac(readerWithHeader.GetQFac())
        writer.SetTimeDimension(readerWithHeader.GetTimeDimension())
        writer.SetQFormMatrix(readerWithHeader.GetQFormMatrix())
        writer.SetSFormMatrix(readerWithHeader.GetSFormMatrix())
    writer.Update()
    writer.Write()

### CONVERTERS ###
def convertVtkImageDataToNumpy(image):
	r,c,s = image.GetDimensions()
	sc = image.GetPointData().GetScalars()

	array  = vtk_to_numpy(sc)
	array=array.reshape(r,c,s,order='F')
	return array

def convertNumpyArrayToVtkImage(array,origin=[0.0,0.0,0.0],spacing=[1.0,1.0,1.0]):
	vtkimage = numpy_to_vtk(array.flatten('F'),deep=True, array_type=vtk.VTK_UNSIGNED_SHORT)
	image1 = vtk.vtkImageData() 
	image1.GetPointData().SetScalars(vtkimage)
	image1.SetDimensions(array.shape)
	image1.SetOrigin(origin)
	image1.SetSpacing(spacing)
	return image1

### Info ###
def getVtkImageInfo(image,name='VTK image'):
	print(50*'*')
	s = "*** " + name + " ***"
	print(s)
	print(len(s)*'*')
	dataDimension = image.GetDataDimension()
	print("* dataDimensions = ", dataDimension)
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
