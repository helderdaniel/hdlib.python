'''
Stopwatch unit tests
v0.1 jan 2019
hdaniel@ualg.pt
'''
from hdlib.time.stopwatch import Stopwatch
import time

##############
# Unit tests #
##############
import unittest

chrono = Stopwatch()

class TestStopWatch(unittest.TestCase):
    """Unit tests."""
    def test0(self): 
        chrono.reset()
        time.sleep(1)
        chrono.lap()
        time.sleep(2)
        chrono.lap()
        self.assertEqual("0", str(chrono.read(0)).split(".")[0])
        self.assertEqual("1", str(chrono.read(1)).split(".")[0])
        self.assertEqual("3", str(chrono.read(2)).split(".")[0])


#This way only runs if NOT imported!
if __name__ == "__main__":
    unittest.main()



