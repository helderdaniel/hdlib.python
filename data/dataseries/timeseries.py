'''
Manipulate multiple data series together

v0.1 feb 2019
hdaniel@ualg.pt
'''
from typing import ClassVar, Any, Tuple, List
import csv
import pandas as pd
import numpy as np
from hdlib.data.dataseries.dataseries import DataSeries

#Use static method for util functions and class method to create objects of the class(factory)
#https://www.geeksforgeeks.org/class-method-vs-static-method-python/

class TimeSeries (DataSeries):
	'''
	Time series manipulation
	'''

	'''
	Constructor, copy, converters, and factory methods
	'''
	def __init__(self) -> None: 
		super().__init__() #Init _rawData and index nested classes

	@classmethod
	#dataframe: Any to allow scalars to
	def fromDataFrame(cls, dataframe: Any, timeRange=None, copy=True) -> 'TimeSeries':
		'''
		Factory method to create TimeSeries object with values
		from a pandas DataFrame and time indexes in timeRange
		Note: External 'dataframe' object is copied by default.
			  If parameter copy is False is created a new TimeSeries
			  with a reference to it.

		time range format:
			- None (if dataframe have already a time index)
			- as string list formatted as YYYY-MM-DD HH:MM:SS.mmm
			- unix time stamp integer list
			- datetime64 list
		'''
		#Use DataSeries to check if it is a DataFrame
		#this way it is only tested in the upper class
		ds  = super()._rawFromDataFrame(dataframe, copy)

		#create TimeSeries and add time index
		obj = cls()
		obj._rawData = ds.toDataFrame() 
		if timeRange is not None:
			obj._rawData = obj._rawData.set_index(pd.to_datetime(timeRange))
		return obj

	@classmethod
	def fromCSV(cls, datafile:str, columns, timeRange) -> 'TimeSeries':
		'''
		Factory method to create TimeSeries object with values
		read csv file with time indexes in specified in timeRange

		columns:    List with the names of columns

		time range format:
			- sole string is a column name where time series is
			(series)		
			- as string list formatted as YYYY-MM-DD HH:MM:SS.mmm
			- unix time stamp integer list
			- datetime64 list
		'''
		#create TimeSeries and add time index
		obj = cls()
		obj._rawData = pd.read_csv(datafile, names=columns, comment=cls._comment)

		if isinstance(timeRange, str): #is Name of column with date
			obj._rawData[timeRange] = pd.to_datetime(obj._rawData[timeRange]) #need to be first 
			obj._rawData = obj._rawData.set_index(timeRange)				  #after being index it is no longer a column
		else:	#is numeric list
			obj._rawData = obj._rawData.set_index(pd.to_datetime(timeRange))
	
		return obj
	

	@classmethod
	def random(cls, min:float, max:float, columns, dateBegin, dateEnd, resolution:float) -> 'TimeSeries':
		'''
		Factory method to create TimeSeries object with sample random values
		between [min, max] in every column between dateBegin and dateEnd,
		with resolutin expressed in seconds or fractions of seconds:
											60 is a minute, 0.001 is a ms

		Note: swaps (dateBegin, dateEnd) if dateBegin > dateEnd
		'''
		begin = pd.to_datetime(dateBegin)
		end   = pd.to_datetime(dateEnd)
		if begin > end: 	#(swap)
			end, begin = begin, end 	

		timeRange = TimeSeries.createDateTimeIndex(begin, end, resolution)
		samples = len(timeRange)

		#create TimeSeries and add time index
		obj = super()._rawRandom(min, max, samples, columns)
		obj._rawData = obj.toDataFrame().set_index(timeRange)
		return obj #type:ignore


	'''
	Utilities
	'''
	@staticmethod
	def createDateTimeIndex(begin: np.datetime64,
							end:   np.datetime64,
							resolution: float) -> pd.DatetimeIndex:
		'''
		Generates a DateTimeIndex with fixed period (resolution)
		'''
		freq  = '{}S'.format(resolution) #resolution in seconds (float suppported)
		timeRange = pd.date_range(begin, end, freq=freq)
		return timeRange

	'''
	Indexing
	'''
	def shifTimeIndex(self, delta: float) -> None:
		'''
        Shifts time index by delta seconds or fractions of seconds:
        	60 is a minute, 0.001 is a ms
        '''
		self._rawData.index = (self._rawData.index + pd.Timedelta(seconds=delta))


	def findExpectedSamples(self, resolution: float) -> int:
		'''
		returns the number of samples for a time series sarting at begin
		and ending on end, for the given resolution in seconds or fractions of seconds:
			60 is a minute, 0.001 is a ms

		Note that last samples may not be considered if end 
		is not a multiple of resolution:
		Eg1.: [0, 5] with resolution 2
			  int(5-0)/2+1 = int(2,5)+1 = 3, samples: {0, 2, 4}
		Eg2.: [0, 5] with resolution 3
			  int(5-0)/3+1 = int(1.66)+1 = 2 samples: {0, 3}
		
		'''
		begin, end = self.beginEndIndex()
		return int(abs(end-begin).total_seconds()/resolution)+1


	'''
	Operations
	'''
	def interpolate(self, resolution:float) -> None:
		'''
		reindexed and interpolated to add missing samples at given resolution in seconds,
		or suppress samples.
		
		Index must be sorted with <DataSeries>.sortIndex()
		Works in place
		
		Note: Dataframe.interpolate() just interpolates numeric columns
		'''
		begin, end = self.beginEndIndex()
		timeRange = TimeSeries.createDateTimeIndex(begin, end, resolution)

		super()._rawInterpolate(timeRange)
