'''
Manipulate multiple series 

v0.1 feb 2019
hdaniel@ualg.pt
'''
from typing import ClassVar, Any, Tuple, Type, List
import csv
import numpy as np
import pandas as pd
from hdlib.data.dataseries.dataseries import DataSeries

#Use static method for util functions and class method to create objects of the class(factory)
#https://www.geeksforgeeks.org/class-method-vs-static-method-python/

class SimpleSeries(DataSeries):
	'''
	Simple data series manipulation
	'''

	'''
	Constructor, copy, converters, and factory methods
	'''
	def __init__(self) -> None: 
		super().__init__() #Init _rawData and index nested classes

	@classmethod
	def fromDataFrame(cls, dataframe: Any, copy=True) -> 'SimpleSeries':
		'''
		Factory method to create SimpleSeries, or its subclasses' objects, with values
		from a pandas DataFrame.
		Note: External 'dataframe' object is copied by default.
		 	  If parameter copy is False is created a new SimpleSeries
			  with a reference to it.
		'''
		return super()._rawFromDataFrame(dataframe, copy) #type: ignore 
		
	
	@classmethod
	def fromCSV(cls, datafile:str, columns) -> 'SimpleSeries':
		'''
		Factory method to create SimpleSeries object with values
		read from csv file with data series

		columns:    List with the names of columns
		'''
		obj = cls()
		obj._rawData = pd.read_csv(datafile, names=columns, comment=cls._comment)
		return obj


	@classmethod
	#Not needed in the present implementation since just call super._rawRandom()
	def random(cls, min:float, max:float, samples:int, columns) -> 'SimpleSeries':
		'''
		Factory method to create SimpleSeries object with sample random values
		between [min, max] in every column
		'''
		return super()._rawRandom(min, max, samples, columns) #type: ignore 

	'''
	Utilities
	'''
	@staticmethod
	def createNumericIndex(begin: float,
						   end:   float,
						   resolution: float) -> np.ndarray:
		'''
		Generates a DateTimeIndex with fixed period (resolution)
		'''
		#since arange do not include upper limit,  use linspace
		samples = int(abs(end-begin)/resolution)+1
		return np.linspace(begin, end, samples)

	'''
	Indexing
	'''
	def findExpectedSamples(self, resolution: float) -> int:
		'''
		returns the number of samples for a simple series sarting at begin
		and ending on end, for the given resolution,  which means the distance
		between to points in the index
			
		Note that last samples may not be considered if end 
		is not a multiple of resolution:
		Eg1.: [0, 5] with resolution 2
			  int(5-0)/2+1 = int(2,5)+1 = 3, samples: {0, 2, 4}
		Eg2.: [0, 5] with resolution 3
			  int(5-0)/3+1 = int(1.66)+1 = 2 samples: {0, 3}
		
		'''
		begin, end = self.beginEndIndex()
		return int(abs(end-begin)/resolution)+1

	'''
	Operations
	'''
	def interpolate(self, resolution:float):
		'''
		reindexed and interpolated to add missing samples at given resolution in seconds,
		or supress samples.
		
		Index must be sorted with <DataSeries>.sortIndex()
		Works in place
		
		Note: Dataframe.interpolate() just interpolates numeric columns
		'''
		begin, end = self.beginEndIndex()
		rng = SimpleSeries.createNumericIndex(begin, end, resolution)
		
		super()._rawInterpolate(rng)
