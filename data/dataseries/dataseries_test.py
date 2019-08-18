'''
Abstract class to give default behaviour to subclasses that
manipulate multiple data series together

v0.1 feb 2019
hdaniel@ualg.pt
'''
from hdlib.data.dataseries.dataseries import DataSeries

##############
# Unit tests #
##############
import unittest


class TestIDataSeries(unittest.TestCase):
	"""Unit tests"""

	def testInstantiation(self) -> None:
		#test raise exception on instantiation
		with self.assertRaises(TypeError) as context:
			x = DataSeries() #type:ignore
		self.assertTrue("Can't instantiate abstract class DataSeries with abstract methods" \
			            in str(context.exception))


#This way only runs if NOT imported!
if __name__ == "__main__":
	try:
		unittest.main()
	#avoid exception inside vscode when exiting unittest
	except SystemExit as e: 
		pass
