#Abstract class to give default behaviour to subclasses that
# manipulate multiple data series together
#
#v0.1 feb 2019
#hdaniel@ualg.pt
#
from abc import ABC, abstractmethod
from hdlib.data.dataseries.idataseries import IDataSeries
from hdlib.base import Base
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import ClassVar, Any, Tuple, Type

class DataSeries(IDataSeries, Base):
	'''
	Data series manipulation abstract super class
	subclass of the interface IDataSeries
	'''

	'''
	class variables
	'''
	_comment    : ClassVar[str] = '#'
	_rawDataRef : ClassVar[str] = '_rawData'
	
	'''
	Nested classes for indexing:

	Need to reference an object, which containd an element indexed by _rawData.
	If passed just the reference to _rawData at the moment of initialiazation,
	which is None, this reference cannot ever change
	Have to reference the object that contains a reference for what ever _rawData is,
	which is __dict__ and access the place where this reference is: __dict__[DataSeries._rawDataRef].
	Now if the contents of this place, the reference stored at __dict__[DataSeries._rawDataRef], changes
	it accesses the changed contents always.

	For this is needed to store __dict__[DataSeries._rawDataRef] in the instace variable _objDict
	calling the _Indexer superclass constructor from the DataSeries constructor

	def __init(self):
		self.loc  = self._Loc (self.__dict__, type(self))

	It is also needed to store the concrete subclass that initialized the constructor,
	like SimpleSeries or TimeSeries, to create objects of that class when returning with __getitem_.
	So it is passed type(self) in the constructor above.
	If passing __class__ it will always be the name of the class in which the indexer classes
	are declared, the ab stract super class DataSeries. However self from __init(self), is
	always an object of the class that it is being created, even if calling DataSeries.__init__()
	from a subclass like TimeSeries with: super.__init().
	So it must be passed "type(self)" or "self.__class__"

	This way  it is needed to call this abstract class constructor from all subclasses
	constructors:

	def __init__(self) -> None: 
		super().__init__() #Init _rawData and index nested classes
	

	Note: Can not verify tipe with mypy because if we set -> 'DataSeries'
   		  mypy find that:
		  self._cls has no attribute fromDatFrame()

		  it is a static type checker and self._cls only takes values at runtime
	'''
	class _Indexer:
		def __init__(self, objDict:dict, cls:type) -> None:
			#Note: Cannot just get ref to _rawData now:
			#
			#	self._objDict = objDict[DataSeries._rawDataRef]
			#
			#cause it can change in the future. Must get it in each index
			self._objDict = objDict
			self._cls = cls

	class _Loc(_Indexer):
		def __getitem__(self, slice): 
			'''returns a Dataseries with a view since fromDataFrame copy == False'''
			#Avoid mypy bug: Unexpected "error: Slice index must be an integer or None"
			return self._cls.fromDataFrame(self._objDict[DataSeries._rawDataRef].loc[slice], copy=False) 

		def __setitem__(self, slice, value: Any) -> None:
			self._objDict[DataSeries._rawDataRef].loc[slice] = value

	class _ILoc(_Indexer):
		def __getitem__(self, slice): # ->  'DataSeries': Gives more errors Try also Type['DataSeries']
			'''returns a Dataseries with a view since fromDataFrame copy == False'''
			return self._cls.fromDataFrame(self._objDict[DataSeries._rawDataRef].iloc[slice], copy=False)

		def __setitem__(self, slice, value: Any) -> None:
			self._objDict[DataSeries._rawDataRef].iloc[slice] = value

	class _AT(_Indexer):
		def __getitem__(self, slice) -> Any:
			'''returns an element'''
			return self._objDict[DataSeries._rawDataRef].at[slice]

		def __setitem__(self, slice, value: Any) -> None:
			self._objDict[DataSeries._rawDataRef].at[slice] = value

	class _IAT(_Indexer):
		def __getitem__(self, slice) -> Any:
			'''returns an element'''
			return self._objDict[DataSeries._rawDataRef].iat[slice]

		def __setitem__(self, slice, value: Any) -> None:
			self._objDict[DataSeries._rawDataRef].iat[slice] = value

	'''
	End nested classes for indexing
	'''

	'''
	indexing and accessing
	'''	
	'''
	Deprecated: Use [], loc and iloc
	The below discussion tells how to create a slice literal to pass to a function
	However it can be done with nested classes as iloc and loc in this class

	filters slice of _rawData as specified in argument slice
	eliminating everything else

	Note: since there are no slice literals in python, argument slice must be 
	passed as a slice object crated with:
	
		slice(start,stop,step) #to omit one use None as ':' in a slice literal
	
	or use numpy s_ to generate a slice objet with the usual syntax:
	
		numpy.s_[start,stop[,step]]
		
		aDataSeries.filter(np.s_[:,3:])
	
	This can be implemented using __getitem__ as suggested in:

	https://stackoverflow.com/questions/13706258/passing-python-slice-syntax-around-to-functions

	class SliceMaker(object):
		def __getitem__(self, item):
			return item

	l = [0,1,2,3,4,5]
	s_ = SliceMaker()
	print (s_[3:4]) #slice (3,4,None)
	print (s_[:,1]) #(slice(None, None, None), 1)

	def filter(self, slice):
		self._rawData = self._rawData.iloc[slice]
	'''

	#Does not make sense to implement __reversed__ because
	#DataSeries is not an Iterable Sequence
	def reversed(self) -> 'DataSeries':
		return type(self).fromDataFrame(self._rawData[::-1]) #type: ignore

	def __getitem__(self, slice) -> 'DataSeries':
		'''return a Dataseries with a view since fromDataFrame copy == False'''
		return type(self).fromDataFrame(self.__dict__[DataSeries._rawDataRef][slice], copy=False) #type: ignore

	def __setitem__(self, slice, value) -> None:
		self._rawData[slice] = value

	def __len__(self) -> int:
		return len(self._rawData)

	@property
	#Use decorator property so that
	#shape() can be accessed as <DataSeries>.shape
	#without parenteses
	def shape(self) -> Tuple[int, int]:
		return self._rawData.shape

	def beginEndIndex(self) -> Tuple [Any, Any]:
		'''
		If index sorted ascending returns [min, max] index
		'''
		begin = self._rawData.index[0] 
		end   = self._rawData.index[-1] 
		return begin, end

	def sortIndex(self) -> None:
		''' Sort ascending index in place '''
		self._rawData : pd.DataFrame = self._rawData.sort_index()

	def findMissing(self, resolution:float) -> Tuple[int, int]:
		'''
		Count missing samples considering index have constant spaced 
		period, at given resolution.
		The meaning of parameter resolution depends on the concrete class implementation, 
		it can be interpreted as the distance between points on the iondex axis, 
		as in SimpleSeries or a time period in seconds, as in TimeSeries
	
		returns expected samples, existing samples
		'''
		#begin, end = self.beginEndIndex()
		#get expected samples from concrete subclass
		expectedSamples = self.findExpectedSamples(resolution)
		existingSamples = len(self._rawData)
		return (expectedSamples, existingSamples)

	def hasMissing(self, resolution:float) -> bool:
		expectedSamples, existingSamples = self.findMissing(resolution) 
		return  expectedSamples != existingSamples


	'''
	Constructor, copy, converters, and factory methods
	'''
	def __init__(self) -> None:
		self._rawData = pd.DataFrame([])
		#type(self) get the class of a subclass, if self is subclass
		#or this class, whether __class__ is always the name of this superclass
		self.loc  = self._Loc (self.__dict__, type(self))
		self.iloc = self._ILoc(self.__dict__, type(self))
		self.at   = self._AT  (self.__dict__, type(self))
		self.iat  = self._IAT (self.__dict__, type(self))
		self._scaler = None
	
	#If user defined class must express between '' or it will not find the type
	def copy(self) -> 'DataSeries':
		'''Deep copy object'''
		
		#From scratch
		#type(self)(), or self.__class__(), to get subclass constructor
		'''
		obj = type(self)()	
		obj._rawData = self._rawData.copy()
		return obj
		'''
		#using _rawFromDataFrame() factory method
		#fromDataFrame already copies
		#type(self) to get subclass Class and thus subclass object
		obj = type(self)._rawFromDataFrame(self._rawData, copy=True)
		return obj
	
	@classmethod
	#dataframe: Any to allow scalars to
	def _rawFromDataFrame(cls, dataframe: Any, copy=True) -> 'DataSeries':
		'''
		Factory method to create DataSeries, or its subclasses' objects, with values
		from a pandas DataFrame.
		Note: External 'dataframe' object is copied by default.
			  If parameter copy is False is created a new DataSeries
			  with a reference to it.
		'''
		
		#if it is passed a scalar, puts it in a DataFrame
		if np.isscalar(dataframe):
			dataframe = pd.DataFrame([dataframe])

		obj = cls()
		if copy: obj._rawData = dataframe.copy()
		else:    obj._rawData = dataframe
		return obj

	@classmethod
	def _rawRandom(cls, min:float, max:float, samples:int, columns) -> 'DataSeries':
		'''
		Factory method to create DataSeries object with sample random values
		between [min, max] in every column
		'''
		#Note by default random generator gets seed from timer
		arr = np.random.rand(samples, len(columns))
		arr = arr * (max - min) + min
		df = pd.DataFrame(arr, columns=columns)
		obj = cls._rawFromDataFrame(df)
		return obj

	#Note:pandas has no support yet feb 2019
	#pd.DataFrame behaves as Any
	def toDataFrame(self) -> pd.DataFrame: 
		'''
		returns a copy of the underlying pandas Dataframe
		this way _rawData can not be modified externally
		'''
		df = self._rawData
		return df.copy()

	def __str__(self):
		'''called by print'''
		return str(self._rawData)


	
	'''
	Info 
	'''
	def columnNames(self): 
		'''return all column names'''
		return self._rawData.columns #Not needed: .tolist(), cause is an Index

	def numericColumnNames(self):
		'''return numeric column names'''
		return self._rawData._get_numeric_data().columns #Not needed: .tolist(), cause is an Index
		
	'''
	Compare, test, check
	'''
	def __eq__(self, other) -> bool:
		'''
		returns True if self._rawData  == other._rawData
		'''
		if not isinstance(other, DataSeries):
			raise TypeError("DataSeries subclass expected")
		#Note: pandas.testing.assert_frame_equal() gives more control on how equal are
		return self._rawData.equals(other.toDataFrame())
	
	def bounded(self, min:float, max:float) -> bool:
		'''
		returns True if all numeric columns fave values between min and max (included)

		PRE: min > max
		'''
		cols = self.numericColumnNames() #Not needed: .tolist(), cause is an Index
		b = self._rawData[cols].applymap(lambda x: (x>=min) & (x<=max))
		return all(b.values.flatten())

	
	'''
	Operations
	'''
	def minmaxScale(self, range:tuple = (0,1)) -> None:
		'''
		Scale data between [0, 1] (minmax scaling), 
		only on numeric columns
		in place
		'''
		#get numeric column names
		cols = self._rawData._get_numeric_data().columns #Not needed: .tolist()
		#scale
		self._scaler = MinMaxScaler(feature_range=range)
		# mypy does not knows self._scaler was initialized above
		# so assert requires that the object has been initialized
		# and shut up mypy
		assert self._scaler is not None
		self._rawData[cols] = self._scaler.fit_transform(self._rawData[cols])

	def unMinmaxScale(self) -> None:
		'''
		Inverse minmaxScale according to specified range in minmaxScale()
		only on numeric columns
		in place
		'''
		#unscale
		if self._scaler is not None:
			#get numeric column names
			cols = self._rawData._get_numeric_data().columns #Not needed: .tolist()
			self._rawData[cols] = self._scaler.inverse_transform(self._rawData[cols])
		else:
			raise TypeError ('Object not previously scaled with minmaxScale()')
	
	def _rawInterpolate(self, rng) -> None:
		'''
		reindexed and interpolated to add missing samples, or supress samples,
		over given rng
		
		Index must be sorted with <DataSeries>.sortIndex()
		Works in place
		
		Note: Dataframe.interpolate() just interpolates numeric columns
		'''
		self._rawData = self._rawData.reindex(rng)
		self._rawData = self._rawData.interpolate()  #default: method='linear' interpolation



