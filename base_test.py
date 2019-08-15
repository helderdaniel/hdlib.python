#base class for hdlib
#
#v0.1 jan 2019
#hdaniel@ualg.pt
#
from hdlib.base import *

##############
# Unit tests #
##############
import unittest

b = Base()

class TestBaseHDlibClass(unittest.TestCase):
    def testSTR0(self): 
        self.assertEqual(str(b), "<class 'hdlib.base.Base'>({})")

    #def testREPR0(self): #repr(b)  #Should raise an exception
    #    with self.assertRaises(NotImplementedError) as context:
    #        repr(b)
    #    self.assertTrue('Subclass must implement "__repr__(self)" method' in str(context.exception))

    def testIsNumber(self):
        self.assertTrue(Base.isNumber(9))
        self.assertTrue(Base.isNumber(9.0))
        self.assertFalse(Base.isNumber('9'))


#This way only runs if NOT imported!
if __name__ == "__main__":
	try:
		unittest.main()
	#avoid exception inside vscode when exiting unittest
	except SystemExit as e: 
		pass

