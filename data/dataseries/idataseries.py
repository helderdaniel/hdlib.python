#Interface to define methods to classes that manipulate multiple data series together
#
#v0.1 feb 2019
#hdaniel@ualg.pt
#
from abc import ABC, abstractmethod
from typing import Any

class IDataSeries(ABC):
	'''
	Data series manipulation interface
	'''

	#Need to have at least an abstract method to prevent instantiation
	@abstractmethod
	def findExpectedSamples(self, resolution: float) -> int:
		'''
		returns the number of samples for a DataSeries sarting at begin
		and ending on end, for the given resolution.
		The meaning of parameter resolution depends on the concrete class implementation, 
		it can be interpreted as the distance between points on the iondex axis, 
		as in SimpleSeries or a time period in seconds, as in TimeSeries
		'''
		pass
	
	@abstractmethod
	def interpolate(self, resolution:float) -> None:
		'''
		reindex and interpolated along the index to add missing samples, or supress samples, 
		at the given resolution.
		The meaning of parameter resolution depends on the concrete class implementation, 
		it can be interpreted as the distance between points on the iondex axis, 
		as in SimpleSeries or a time period in seconds, as in TimeSeries
		'''
		pass

	@abstractmethod
	def minmaxScale(self, range:tuple = (0,1)) -> None:
		'''
		Scale data between [0, 1] (minmax scaling), 
		only on numeric columns
		in place
		'''
		pass

	@abstractmethod
	def unMinmaxScale(self) -> None:
		'''
		Inverse minmaxScale according to specified range in minmaxScale()
		only on numeric columns
		in place
		'''
		pass

##############
# Unit tests #
##############
import unittest


class TestIDataSeries(unittest.TestCase):
	"""Unit tests"""

	def testInstantiation(self) -> None:
		#test raise exception on instantiation
		with self.assertRaises(TypeError) as context:
			x = IDataSeries() #type:ignore
		self.assertTrue("Can't instantiate abstract class IDataSeries with abstract methods" \
			            in str(context.exception))


#This way only runs if NOT imported!
if __name__ == "__main__":
	try:
		unittest.main()
	#avoid exception inside vscode when exiting unittest
	except SystemExit as e: 
		pass
