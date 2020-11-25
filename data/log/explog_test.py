#Experiment logger
#
#v0.1 aug 2019
#hdaniel@ualg.pt
#
from hdlib.data.log.simplelog import SimpleLog
from hdlib.data.log.explog    import ExpLog

##############
# Unit tests #
##############
import unittest
import pickle
from typing import ClassVar, AnyStr, Any, Tuple, List
from datetime import datetime

class TestExpLog(unittest.TestCase):
    """Unit tests"""

    log   : ClassVar[ExpLog]
    logFN     : ClassVar[str] = "logexpexample.log"
    historyFN : ClassVar[str] = "trainhistory.pickle"
    history   : ClassVar[dict]
    logExpectedEntries : ClassVar[List[Tuple[str, int, float, float, float, float]]] = [
    ("10", 0, 103, 0.9921428571428571, 0.002061287123396923, 3.33),
    ("10", 1, 103, 0.9921428571428571, 0.002061287123396923, 3.21)
    ]
    logTestTimeFmt   : ClassVar[str] = "%Y-%m-%d %H:%M:%S"
    logExpectedTimes : ClassVar[List[str]] = [
    "2019-08-22 12:33:19", "2019-08-22 12:43:00"
    ]
    
    @classmethod
    def setUpClass(cls) -> None:
        #code to be executed only once before all tests start
        #Create and save log
        with open(cls.historyFN, "rb") as fp:
            cls.history = pickle.load(fp)
        cls.log = ExpLog(full=False)
        cls.log.add("10", 0, 3.33, cls.history)
        cls.log.add("10", 1, 3.21, cls.history)

        #Force log to have fixed times, not the ones when created here
        #to compare __str__ 
        e = list(cls.log._SimpleLog__log[0])
        e[0] = datetime.strptime(cls.logExpectedTimes[0], cls.logTestTimeFmt)
        cls.log._SimpleLog__log[0] = tuple(e)
        e = list(cls.log._SimpleLog__log[1])
        e[0] = datetime.strptime(cls.logExpectedTimes[1], cls.logTestTimeFmt)
        cls.log._SimpleLog__log[1] = tuple(e)

        cls.log.save(TestExpLog.logFN)

    def testLoad0(self) -> None:
        log = ExpLog.load(TestExpLog.logFN)
        logentries = log.getAll()
        #print(logentries)
        self.assertEqual(logentries[0][1], TestExpLog.logExpectedEntries[0])
        self.assertEqual(logentries[1][1], TestExpLog.logExpectedEntries[1])
    
    def testCopy0(self) -> None:
        log = TestExpLog.log.copy()
        lognew = log.copy()
        logentries = lognew.getAll()
        self.assertFalse(lognew.isFullLog())
        self.assertEqual(len(log), len(lognew))
        self.assertEqual(log.getTimeZone(), lognew.getTimeZone())
        self.assertEqual(logentries[0][1], TestExpLog.logExpectedEntries[0])
        self.assertEqual(logentries[1][1], TestExpLog.logExpectedEntries[1])
    
    def testCopyEqual0(self) -> None:
        log0 = TestExpLog.log.copy()
        log1 = log0.copy()
        
        #equal logs
        self.assertTrue(log0==log1)
        
        #diff log entries
        log1 = ExpLog()
        log1.add("101", 1, 3.21, TestExpLog.history)
        log1.add("10",  1, 3.21, TestExpLog.history)
        self.assertFalse(log0==log1)

        #diff number of log entries
        log1 = log0.copy()
        self.assertTrue(log0==log1)
        log1.add("20", 0, 2.11, TestExpLog.history)
        self.assertFalse(log0==log1)

        #diff log time entries
        log1 = ExpLog()
        log1.add("10", 0, 3.33, TestExpLog.history)
        log1.add("10", 1, 3.21, TestExpLog.history)
        self.assertFalse(log0==log1)
        
        #diff log info entries
        log1 = log0.copy()
        self.assertTrue(log0==log1)
        log1.setInfoAt(1, ("101", 1, 103, 0.9921428571428571, 0.002061287123396923, 3.21))
        self.assertFalse(log0==log1)
        
        #diff full
        log1 = log0.copy()
        self.assertTrue(log0==log1)
        log1._ExpLog__full = True
        self.assertFalse(log0==log1)

    def testFullLog0(self) -> None:
        log0 = ExpLog(full=True)
        log0.add("10", 0, 3.33, TestExpLog.history)
        lastHistory = log0.getInfoAt(0)[6]
        self.assertDictEqual(lastHistory,TestExpLog.history)

    def testShow0(self) -> None:
        log = TestExpLog.log.copy()
        strcmp  = "Log entries = 2\n"
        strcmp += "Log:\n"
        strcmp += "2019-08-22 12:33:19: ('10', 0, 103, 0.9921428571428571, 0.002061287123396923, 3.33)\n"
        strcmp += "2019-08-22 12:43:00: ('10', 1, 103, 0.9921428571428571, 0.002061287123396923, 3.21)\n"
        strcmp += "\nLast log entry:\n"
        strcmp += "2019-08-22 12:43:00\n"
        strcmp += "('10', 1, 103, 0.9921428571428571, 0.002061287123396923, 3.21)"
        self.assertEqual(log.show(), strcmp) #time=true, default

    def testShow1(self) -> None:
        log = TestExpLog.log.copy()
        strcmp  = "Log entries = 2\n"
        strcmp += "Log:\n"
        strcmp += "('10', 0, 103, 0.9921428571428571, 0.002061287123396923, 3.33)\n"
        strcmp += "('10', 1, 103, 0.9921428571428571, 0.002061287123396923, 3.21)\n"
        strcmp += "\nLast log entry:\n"
        strcmp += "2019-08-22 12:43:00\n"
        strcmp += "('10', 1, 103, 0.9921428571428571, 0.002061287123396923, 3.21)"
        self.assertEqual(log.show(time=False), strcmp)
   

#This way only runs if NOT imported!
if __name__ == "__main__":
    try:
        unittest.main()
    #avoid exception inside vscode when exiting unittest
    except SystemExit as e: 
        pass
