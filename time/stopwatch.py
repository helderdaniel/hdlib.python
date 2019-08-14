"""
Stopwatch
v0.1 jan 2019
hdaniel@ualg.pt
"""
#perf_count only available in 3.7
#but tensoflow only supports 3.6 by the end of 2018.
#got to checkit later

from time import sleep
from time import perf_counter as timer
from hdlib.base import Base

class Stopwatch(Base):
    """Implements a stopwatch, that can store multiple time lapses"""

    def __init__(self):
        """Create and reset clock."""
        self.reset()
 
    def reset(self):
        """
        Reset clock:
        sets startTime to current time
        clear lap list
        """
        self._startTime = timer()
        self._laps = []
        self._laps.append(0)

    def lap(self):
        """Add time elapsed since last reset in seconds to lap list."""
        self._laps.append(self.watch())

    def watch(self):
        """Return time elapsed since last reset in seconds."""
        # current time-startTime
        return timer()-self._startTime
    
    def read(self, idx):
        """
        Read a registered elapsed time from the lap list, at position idx.
        read(0) returns always 0.
        """
        return self._laps[idx]


##############
# Unit tests #
##############
import unittest

chrono = Stopwatch()

class TestStopWatch(unittest.TestCase):
    """Unit tests."""
    def test0(self): 
        chrono.reset()
        sleep(1)
        chrono.lap()
        sleep(2)
        chrono.lap()
        self.assertEqual("0", str(chrono.read(0)).split(".")[0])
        self.assertEqual("1", str(chrono.read(1)).split(".")[0])
        self.assertEqual("3", str(chrono.read(2)).split(".")[0])


#This way only runs if NOT imported!
if __name__ == "__main__":
    unittest.main()



