#Manipulate multiple data series together
#
#v0.1 feb 2019
#hdaniel@ualg.pt
#
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
		or supress samples.
		
		Index must be sorted with <DataSeries>.sortIndex()
		Works in place
		
		Note: Dataframe.interpolate() just interpolates numeric columns
		'''
		begin, end = self.beginEndIndex()
		timeRange = TimeSeries.createDateTimeIndex(begin, end, resolution)

		super()._rawInterpolate(timeRange)
		

##############
# Unit tests #
##############
import unittest
import matplotlib.pyplot as plt

plot     : bool = False
seriesFN : str  = "unittest1.csv"

#Dates are set at the beggining and end of time series
#seriesDates : Tuple [str, str] = ("2018-8-1 00:00:00", "2018-8-31 23:59:00") 
#Dates are set before/after time series
seriesDates : Tuple [str, str] = ("2018-7-25 00:00:00", "2018-9-5 23:59:00")
#Missing samples in August (3830)

marketValuesColumns : List[str] = ['Open','High','Low','Close','Volume']
allColumNames : List[str] = ['UnixTimeStamp','Date','Symbol']+marketValuesColumns

class TestTimeSeries(unittest.TestCase):
	"""Unit tests."""

	marketDataTS : ClassVar[TimeSeries]
	rndts0       : ClassVar[TimeSeries]
	rndts1       : ClassVar[TimeSeries]
	min			 : ClassVar[float]
	max			 : ClassVar[float]
	'''
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#code to be executed before each test
	
	def setUp(self):
		#code to be executed before each test
	'''
	
	@classmethod
	def setUpClass(cls) -> None:
		#code to be executed only once before tests start
		#Get market data
		cls.marketDataTS = TimeSeries.fromCSV(seriesFN, allColumNames, 'Date')
		#Sort ascending time index
		cls.marketDataTS.sortIndex()
		cls.marketDataTS = cls.marketDataTS.loc[seriesDates[0]:seriesDates[1]] # type: ignore
		
		#Generate random TimeSeries
		cls.min = 0.000001
		cls.max = 0.000005
		cls.rndts0 = TimeSeries.random(cls.min, cls.max, ['A', 'B', 'Cr'], "2018-1-1 00:00:00", "2018-1-1 00:30:00", 60)
		cls.rndts1 = TimeSeries.random(cls.min, cls.max, ['A', 'B', 'Cr'], "2018-1-1 00:30:00", "2018-1-1 00:00:00", 60)

	''' Indexing & accessing '''
	def testIndexes0(self) -> None:
		'''
		Note: Gives deprecated warning on .ix when using loc with DateTimeIndex
			  and a String. Biut only if breakpoint set
		'''
		#ok
		type(self).marketDataTS['2018-08-01 02:00:00':'2018-08-02 04:00:00'] #type:ignore
		#ok
		type(self).marketDataTS.loc['2018-08-01 02:00:00':'2018-08-02 04:00:00'] #type:ignore
		#ok
		#To get a value with an exact match Pandas needs a DateTime. 
		#If it finds a label with time it assumes it is a column name and gives a KeyError
		#When assigning a value it does ok
		#But its safer to use DateTime objects
		buf = type(self).marketDataTS.at[pd.to_datetime('2018-08-01 00:00:00'), 'Open'] #type:ignore
		type(self).marketDataTS.loc['2018-08-01 00:00:00','Open'] = 1     
		type(self).marketDataTS.loc['2018-08-01 00:00:00', 'Open'] = buf  
		#ok
		type(self).marketDataTS.iloc[1,4]
		#gets just the number
		self.assertEqual(type(self).marketDataTS.iat[1,4], 7731.18)
		#ok
		type(self).marketDataTS.iloc[1,1]
		#gets just the string: 'BTCUSD'
		self.assertEqual(type(self).marketDataTS.iat[1,1], 'BTCUSD')
		#test raise 
		#Error cannot iloc by string, use loc
		with self.assertRaises(TypeError) as context:
 			type(self).marketDataTS.iloc['2018-08-01 02:00:00':'2018-08-02 04:00:00'] #type:ignore
		self.assertTrue("cannot do slice indexing on <class 'pandas.core.indexes.datetimes.DatetimeIndex'> with these indexers [2018-08-01 02:00:00] of <class 'str'>" \
			            in str(context.exception))

	def testReversed0(self) -> None:
		ts0 = type(self).marketDataTS.reversed()
		ts1 = ts0.reversed()
		self.assertNotEqual(ts0, type(self).marketDataTS)
		self.assertEqual(ts1, type(self).marketDataTS)
		self.assertEqual(type(ts1), TimeSeries)

	def testReturnType(self) -> None:
		#returns TimeSeries
		self.assertEqual(type(type(self).marketDataTS[:]), type(type(self).marketDataTS))
		self.assertEqual(type(type(self).marketDataTS.iloc[0,:]), TimeSeries)
		#returns DataFrame
		self.assertTrue(type(type(self).marketDataTS.toDataFrame()) is pd.DataFrame) 

	def testFindExpectedSamples0(self) -> Any:
		df0 = pd.DataFrame([[0,1],[2,3],[4,5]], columns=['A', 'B'])
		ts0 = TimeSeries.fromDataFrame(df0, pd.date_range(start='2018-1-1', periods=3, freq='T'))
		
		self.assertEqual(ts0.findExpectedSamples(0.1), 1201)
		self.assertEqual(ts0.findExpectedSamples(1),   121)
		self.assertEqual(ts0.findExpectedSamples(60),  3)
		self.assertEqual(ts0.findExpectedSamples(360), 1)
		ts1 = ts0.reversed()
		self.assertEqual(ts1.findExpectedSamples(0.1), 1201)

	''' Copy and creation '''
	def testDeepCopy0(self) -> None:
		ts0 = type(self).marketDataTS
		ts1 = ts0.copy()
	
		#Test different storage for data
		#buf = ts1.loc['2018-08-01 00:00:00','Open'].toDataFrame().values[0,0]
		buf = ts1.at[pd.to_datetime('2018-08-01 00:00:00'),'Open']
		ts1.at['2018-08-01 00:00:00','Open'] = buf+1
		
		b0 = (ts0.toDataFrame() == ts1.toDataFrame())
		t  = b0.at[pd.to_datetime('2018-08-01 00:00:00'), 'Open']
		self.assertFalse(t)
		ts1.at['2018-08-01 00:00:00','Open'] = buf #restore to make equal again for next test
		
		#Test same data and index
		self.assertTrue(ts0==ts1)
	
	def testRandom0values(self) -> None:
		buf = type(self).rndts0.iat[1,1]
		type(self).rndts0.iat[1,1] = 1   	#set value outside to force error
		b0 = type(self).rndts0.bounded(type(self).min, type(self).max)
		
		type(self).rndts0.iat[1,1] = buf	#restore Object for next tests
		b1 = type(self).rndts0.bounded(type(self).min, type(self).max)
		
		self.assertFalse(b0)
		self.assertTrue(b1)

	def testRandom0timeRange(self) -> None:
		rindx0 = type(self).rndts0.toDataFrame().index
		rindx1 = type(self).rndts1.toDataFrame().index
		self.assertLessEqual(rindx0.values[0],  rindx0.values[-1])
		self.assertLessEqual(rindx1.values[0],  rindx1.values[-1])
		self.assertEqual(len(type(self).rndts0), 31)
		self.assertEqual(len(type(self).rndts1), 31)
		self.assertEqual(rindx0.values[0], rindx1.values[0])
		self.assertEqual(rindx0.values[30], rindx1.values[30])
	
	def testFromDataFrame0(self) -> None:
		df0 = pd.DataFrame([[0,1],[2,3],[4,5]], columns=['A', 'B'])
		ts = TimeSeries.fromDataFrame(df0, pd.date_range(start='2018-1-1', periods=3, freq='T'))
		df1 = df0.copy()
		df1 = df1.set_index(pd.date_range(start='2018-1-1', periods=3, freq='T'))
		b0 = ts.toDataFrame() == df1
		b1 = ts.toDataFrame().index.values == df1.index.values
		self.assertTrue(all(b0.values.flatten()))
		self.assertTrue(all(b1))
	
	def testFromDataFrame1(self) -> None:
		df0 = pd.DataFrame([[0,1, 0],[2,3, 60],[4,5, 120]], columns=['A', 'B', 't'])
		ts = TimeSeries.fromDataFrame(df0, pd.to_datetime(df0.iloc[:,2]))
		ts = ts.iloc[:,:2]
		df1 = pd.DataFrame([[0,1],[2,3],[4,5]], columns=['A', 'B'])
		df1 = df1.set_index(pd.to_datetime([0, 60, 120]))
		b0 = ts.toDataFrame() == df1
		b1 = ts.toDataFrame().index.values == df1.index.values
		self.assertTrue(all(b0.values.flatten()))
		self.assertTrue(all(b1))	

	''' Operators '''
	def testEqual0(self) -> None:
		ts = type(self).marketDataTS.copy()
		b = (ts == type(self).marketDataTS)
		self.assertTrue(b)
		#test raise 
		with self.assertRaises(TypeError) as context:
			ts == 1
		self.assertTrue("DataSeries subclass expected" in str(context.exception))

	def testEqual1(self) -> None:
		df0 = pd.DataFrame([[0,1,0],[2,3,60],[4,5,120]], columns=['A', 'B', 't'])
		ts0 = TimeSeries.fromDataFrame(df0, pd.to_datetime(df0.iloc[:,2]))
		ts1 = TimeSeries.fromDataFrame(df0, pd.to_datetime(df0.iloc[:,2]))
		self.assertTrue(ts0 == ts1)
		buf = ts1.iat[0,0]
		ts1.iat[0,0] = -1
		self.assertFalse(ts0 == ts1)
		ts1.iat[0,0] = buf
		self.assertFalse(ts0 != ts1)
		df0 = pd.DataFrame([[0,1,1],[2,3,60],[4,5,120]], columns=['A', 'B', 't'])
		ts1 = TimeSeries.fromDataFrame(df0, pd.to_datetime(df0.iloc[:,2]))
		self.assertFalse(ts0 == ts1)

	''' Utilities '''
	def testCreateDateTimeIndex0(self) -> None:
		tr0 = TimeSeries.createDateTimeIndex('2018-1-1 00:00:00', '2018-1-1 00:00:30', 1)
		tr1 = TimeSeries.createDateTimeIndex('2018-1-1 00:00:00', '2018-1-1 00:10:30', 60)
		tr2 = TimeSeries.createDateTimeIndex('2018-1-1 00:00:00', '2018-1-1 00:00:01', 0.1)
		tr3 = TimeSeries.createDateTimeIndex('2018-1-1 00:00:00', '2018-1-1 00:00:01', 360)
		self.assertEqual(len(tr0), 31)
		self.assertEqual(tr0[2], pd.to_datetime('2018-1-1 00:00:02'))
		self.assertEqual(len(tr1), 11)
		self.assertEqual(tr1[2], pd.to_datetime('2018-1-1 00:02:00'))
		self.assertEqual(len(tr2), 11)
		self.assertEqual(tr2[2], pd.to_datetime('2018-1-1 00:00:00.2'))
		self.assertEqual(len(tr3), 1)
		self.assertEqual(tr3[0], pd.to_datetime('2018-1-1 00:00:00'))
	
	''' Operations '''
	#Tests also samples functions
	def testInterpolate0(self) -> None:
		resolution = 60
		ts0 : TimeSeries = type(self).marketDataTS
		expectedSamples, existingSamples = ts0.findMissing(resolution) 
		self.assertTrue(ts0.hasMissing(resolution))
		self.assertEqual(existingSamples, 40810)
		self.assertEqual(expectedSamples, 44640)
		self.assertEqual(expectedSamples-existingSamples, 3830)
	
		ts1 = ts0.copy() 
		ts1.interpolate(resolution)  
		expectedSamples, existingSamples = ts1.findMissing(resolution) 
		self.assertFalse(ts1.hasMissing(resolution))
		self.assertEqual(existingSamples, 44640)
		self.assertEqual(expectedSamples, 44640)

		#get only market data meaningful in this data set
		if plot: 
			plt.subplot(1,2,1); plt.plot(ts0.iloc[:,2:].toDataFrame())
			plt.subplot(1,2,2); plt.plot(ts1.iloc[:,2:].toDataFrame())
			plt.show()

#This way only runs if NOT imported!
if __name__ == "__main__":
	try:
		unittest.main()
	#avoid exception inside vscode when exiting unittest
	except SystemExit as e: 
		pass

