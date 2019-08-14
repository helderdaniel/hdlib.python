#Manipulate multiple series 
#
#v0.1 feb 2019
#hdaniel@ualg.pt
#
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
		


	


##############
# Unit tests #
##############
import unittest
import matplotlib.pyplot as plt

plot     : bool = False
seriesFN : str  = "unittest0.csv"
marketValuesColumns : List[str] = ['Open','High','Low','Close','Volume']
allColumNames : List[str] = ['UnixTimeStamp','Date','Symbol']+marketValuesColumns

class TestSimpleSeries(unittest.TestCase):
	"""Unit tests"""
	
	marketDataSS : ClassVar[SimpleSeries]
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
		cls.marketDataSS = SimpleSeries.fromCSV(seriesFN, allColumNames)

	''' Indexing & accessing '''
	def testIndex0(self) -> None:
		ds = type(self).marketDataSS.copy()
		self.assertEqual(type(self).marketDataSS[:], type(self).marketDataSS)
		self.assertEqual(ds[0:1].toDataFrame().loc[0, 'Open'], 4025.54)
		self.assertEqual(ds.loc[0,'Open'].toDataFrame().iloc[0,0], 4025.54)
		self.assertEqual(ds.iloc[1,1].toDataFrame().values[0,0], '2019-01-07 15:00:00')
		self.assertEqual(ds.iat[1,1], '2019-01-07 15:00:00')

	def testReversed0(self) -> None:
		ds0 = type(self).marketDataSS.reversed()
		ds1 = ds0.reversed()
		self.assertNotEqual(ds0, type(self).marketDataSS)
		self.assertEqual(ds1, type(self).marketDataSS)
		self.assertEqual(type(ds1), SimpleSeries)
	
	def testLen0(self) -> None:
		self.assertEqual(len(type(self).marketDataSS), 10)

	def testShape0(self) -> None:
		self.assertEqual(type(self).marketDataSS.shape, (10,8))

	def testReturnType(self) -> None:
		#returns SimpleSeries
		self.assertEqual(type(type(self).marketDataSS[:]), type(type(self).marketDataSS))
		self.assertEqual(type(type(self).marketDataSS.iloc[0,:]), SimpleSeries)
		#returns DataFrame
		self.assertTrue(type(type(self).marketDataSS.toDataFrame()) is pd.DataFrame) 

	def testFindExpectedSamples0(self) -> Any:
		df0 = pd.DataFrame([[10,1,0],[20,3,60],[30,5,120],[40,8,20],[50,5,10]], columns=['i', 'A', 'B'])
		df0 = df0.set_index('i')
		ds0 = SimpleSeries.fromDataFrame(df0)
		self.assertEqual(ds0.findExpectedSamples(0.1), 401)
		self.assertEqual(ds0.findExpectedSamples(1),   41)
		self.assertEqual(ds0.findExpectedSamples(10),  5)
		self.assertEqual(ds0.findExpectedSamples(100), 1)
		ds1 = ds0.reversed()
		self.assertEqual(ds1.findExpectedSamples(0.1), 401)

	''' Copy and creation '''
	def testDeepCopy0(self) -> None:
		ds0 = type(self).marketDataSS
		ds1 = ds0.copy()
		
		#Test different storage for data
		buf = ds1.at[0,'Open'] #or: buf = ds1.iat[0, 3]
		ds1.loc[0,'Open'] = buf+1
		b0 = (ds0.toDataFrame() == ds1.toDataFrame())
		t  = b0.loc[0,'Open']
		self.assertFalse(t)
		ds1.loc[0,'Open'] = buf #restore to make equal again for next test
		
		#Test same data and index
		self.assertTrue(ds0==ds1)

	def testRandom0(self) -> None:
		#tests also __setitem__
		min = 0.000001
		max = 0.000005
		ds = SimpleSeries.random(min, max, 10, ['A', 'B', 'Cr'])
		ds[1,1] = 1
		self.assertFalse(ds.bounded(min, max))

	def testRandom1(self) -> None:
		min = -10.000001
		max = 0.000005
		ds = SimpleSeries.random(min, max, 10, ['A', 'B', 'Cr'])
		self.assertTrue(ds.bounded(min, max))

	''' Operators '''
	def testEqual0(self) -> None:
		ds = type(self).marketDataSS.copy()
		b = (ds == type(self).marketDataSS)
		self.assertTrue(b)
		#test raise 
		with self.assertRaises(TypeError) as context:
			ds == 1
		self.assertTrue("DataSeries subclass expected" in str(context.exception))

	def testEqual1(self) -> None:
		df0 = pd.DataFrame([[0,1,0],[2,3,60],[4,5,120]], columns=['A', 'B', 'C'])
		ds0 = SimpleSeries.fromDataFrame(df0)
		ds1 = SimpleSeries.fromDataFrame(df0)
		self.assertTrue(ds0 == ds1)
		buf = ds1.iat[0,0]
		ds1.iat[0,0] = -1
		self.assertFalse(ds0 == ds1)
		ds1.iat[0,0] = buf
		self.assertFalse(ds0 != ds1)

	def testBounded0(self) -> None:
		df0 = pd.DataFrame([[0,1,10.23],[2,3,-23.1],[4,5,9]], columns=['A', 'B', 'C'])
		ds0 = SimpleSeries.fromDataFrame(df0)
		self.assertTrue(ds0.bounded(-23.1, 10.23))
		self.assertFalse(ds0.bounded(-23.0, 10.23))
		self.assertFalse(ds0.bounded(-23.2, 10.0))
		self.assertFalse(ds0.bounded(-22, 10.0))

	''' Info '''
	def testColumnNames0(self) -> None:
		columnsNames=['A', 'B', 'C']
		numColumnsNames=['A']
		df0 = pd.DataFrame([[0,1,'A'],[2,3,'B'],[4,'x','C']], columns=columnsNames)
		ds0 = SimpleSeries.fromDataFrame(df0)
		self.assertTrue(all(ds0.columnNames() == columnsNames))
		self.assertTrue(all(ds0.numericColumnNames() == numColumnsNames))
	
	''' Utilities '''
	def testCreateNumericIndex0(self) -> None:
		r0 = SimpleSeries.createNumericIndex(0.9, 40, 0.1)
		r1 = SimpleSeries.createNumericIndex(10, 40, 1)
		r2 = SimpleSeries.createNumericIndex(10, 40, 10)
		r3 = SimpleSeries.createNumericIndex(10, 40, 100)
		self.assertEqual(len(r0), 392)
		self.assertAlmostEqual(r0[-2], 39.9, 1)
		self.assertEqual(len(r1), 31)
		self.assertEqual(r1[-2], 39)
		self.assertEqual(len(r2), 4)
		self.assertEqual(r2[-2], 30)
		self.assertEqual(len(r3), 1)
		self.assertEqual(r3[0], 10)
	
	''' Operations '''
	#Tests also samples functions
	def testInterpolate0(self) -> None:
		resolution = 0.1
		ds0 = SimpleSeries.random(0.1, 0.3, 5, ['A', 'B'])
		expectedSamples, existingSamples = ds0.findMissing(resolution) 
		self.assertTrue(ds0.hasMissing(resolution))
		self.assertEqual(existingSamples, 5)
		self.assertEqual(expectedSamples, 41)
		self.assertEqual(expectedSamples-existingSamples, 36)
		
		ds1 = ds0.copy() 
		ds1.interpolate(resolution)  
		expectedSamples, existingSamples = ds1.findMissing(resolution) 
		self.assertFalse(ds1.hasMissing(resolution))
		self.assertEqual(existingSamples, 41)
		self.assertEqual(expectedSamples, 41)

		if plot: 
			plt.subplot(1,2,1); plt.plot(ds0.toDataFrame())
			plt.subplot(1,2,2); plt.plot(ds1.toDataFrame())
			plt.show()
		

	def testMimmaxScale0(self) -> None:
		ds0 = type(self).marketDataSS
		ds1 = ds0.copy()
		
		#test raise 
		with self.assertRaises(TypeError) as context:
			ds1.unMinmaxScale()
		self.assertTrue("Object not previously scaled with minmaxScale()" \
			            in str(context.exception))

		#minmaxScale operates only on numeric columns
		ds1.minmaxScale()

		#check numeric values between 0 and 1
		self.assertTrue(ds1.bounded(0,1))

		if plot: 
			plt.plot(ds1.iloc[:, 3:7].toDataFrame())
			plt.show()

		#unscale
		ds1.unMinmaxScale()

		#Compare if it is almost equal
		#to the 2nd decimal place
		#cannot use == due to round errors
		cols = ds0.toDataFrame()._get_numeric_data().columns
		dsn0 = ds0.toDataFrame()[cols]
		dsn1 = ds1.toDataFrame()[cols]
		diff = dsn0 - dsn1
		diff = diff.round(2)
		max=diff.values.max()
		self.assertEqual (max, 0.0)


#This way only runs if NOT imported!
if __name__ == "__main__":
	try:
		unittest.main()
	#avoid exception inside vscode when exiting unittest
	except SystemExit as e: 
		pass
