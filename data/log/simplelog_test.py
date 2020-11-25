#Simple logger
#
#v0.1 jul 2019
#hdaniel@ualg.pt
#
from hdlib.data.log.simplelog import SimpleLog

##############
# Unit tests #
##############
import unittest
from typing import ClassVar, Tuple, List, Any
from datetime import datetime

class TestSimpleLog(unittest.TestCase):
    """Unit tests"""

    log   : ClassVar[SimpleLog]
    logFN : ClassVar[str] = "logexample.log"
    logExpectedEntries : ClassVar[List[Tuple[str, int]]] = [
    ("SimpleLog first entry", 0),
    ("SimpleLog second entry", 1),
    ("SimpleLog third entry", 2),
    ("SimpleLog fourth entry", 3)
    ]
    logTestTimeFmt   : ClassVar[str] = "%Y-%m-%d %H:%M:%S"
    logExpectedTimes : ClassVar[List[str]] = [
    "2019-08-22 12:33:19", "2019-08-22 12:43:00"
    ]

    @classmethod
    def setUpClass(cls) -> None:
        #code to be executed only once before all tests start
        #Create and save log
        cls.log = SimpleLog()
        cls.log.add(cls.logExpectedEntries[0])
        cls.log.add(cls.logExpectedEntries[1])

        #Force log to have fixed times, not the ones when created here
        #to compare __str__ 
        e = list(cls.log._SimpleLog__log[0])
        e[0] = datetime.strptime(cls.logExpectedTimes[0], cls.logTestTimeFmt)
        cls.log._SimpleLog__log[0] = tuple(e)
        e = list(cls.log._SimpleLog__log[1])
        e[0] = datetime.strptime(cls.logExpectedTimes[1], cls.logTestTimeFmt)
        cls.log._SimpleLog__log[1] = tuple(e)

        cls.log.save(TestSimpleLog.logFN)
    
    def __logTestStr(self):
        logstr =  TestSimpleLog.logExpectedTimes[0] + ": " + str(
                    TestSimpleLog.logExpectedEntries[0]) + "\n"
        logstr += TestSimpleLog.logExpectedTimes[1] + ": " + str(
                    TestSimpleLog.logExpectedEntries[1]) + "\n"
        return logstr

    def testLoad0(self) -> None:
        log = SimpleLog.load(TestSimpleLog.logFN)
        logentries = log.getAll()
        #print(logentries)
        self.assertEqual(logentries[0][1], TestSimpleLog.logExpectedEntries[0])
        self.assertEqual(logentries[1][1], TestSimpleLog.logExpectedEntries[1])

    def testGetSetInfo(self) -> None:
        log = TestSimpleLog.log.copy()
        self.assertCountEqual(log.getInfoAt(1), TestSimpleLog.logExpectedEntries[1])
        log.setInfoAt(1, "New")
        self.assertCountEqual(log.getInfoAt(1), "New")

    def testGetAllDeepCopy0(self) -> None:
        log = TestSimpleLog.log.copy()
        length = len(log)
        l = log.getAll()
        del l[0]
        self.assertEqual(len(log), length)

    def testGetInfo0(self) -> None:
        log = TestSimpleLog.log.copy()
        logentries = log.getAll()
        logentriesinfo = log.getInfo()
        #print(logentriestime)
        self.assertEqual(logentries[0][1], logentriesinfo[0])
        self.assertEqual(logentries[1][1], logentriesinfo[1])

    def testGetInfoDeepCopy0(self) -> None:
        log = TestSimpleLog.log.copy()
        i = log.getTime()
        i[0] = "New"
        #Compare if remains constant using str 
        cmpstr = self.__logTestStr()
        self.assertEqual(str(log), cmpstr)

    def testGetTime0(self) -> None:
        log = TestSimpleLog.log.copy()
        logentries = log.getAll()
        logentriestime = log.getTime()
        #print(logentriestime)
        self.assertEqual(logentries[0][0], logentriestime[0])
        self.assertEqual(logentries[1][0], logentriestime[1])

    def testGetTimeDeepCopy0(self) -> None:
        log = TestSimpleLog.log.copy()
        t = log.getTime()
        t[0] = 0
        #Compare if remains constant using str 
        cmpstr = self.__logTestStr()
        self.assertEqual(str(log), cmpstr)

    def testFirstLastClear0(self) -> None:
        log = TestSimpleLog.log.copy()
        log.add(TestSimpleLog.logExpectedEntries[2])
        logfirst = log.getFirst()
        loglast  = log.getLast()
        self.assertEqual(len(log), 3)
        self.assertEqual(logfirst[1], TestSimpleLog.logExpectedEntries[0])  
        self.assertEqual(loglast[1],  TestSimpleLog.logExpectedEntries[2])  
        log.clear()
        self.assertEqual(len(log), 0)  

    def testGetFirstDeepCopy0(self) -> None:
        log = TestSimpleLog.log.copy()
        e = log.getFirst()
        e = "New"
        #Compare if remains constant using str 
        cmpstr = self.__logTestStr()
        self.assertEqual(str(log), cmpstr)

    def testGetLastDeepCopy0(self) -> None:
        log = TestSimpleLog.log.copy()
        e = log.getLast()
        e = "New"
        #Compare if remains constant using str 
        cmpstr = self.__logTestStr()
        self.assertEqual(str(log), cmpstr)

    def testCopy0(self) -> None:
        log = TestSimpleLog.log.copy()
        lognew = log.copy()
        logentries = lognew.getAll()
        self.assertEqual(len(log), len(lognew))
        self.assertEqual(log.getTimeZone(), lognew.getTimeZone())
        self.assertEqual(logentries[0][1], TestSimpleLog.logExpectedEntries[0])
        self.assertEqual(logentries[1][1], TestSimpleLog.logExpectedEntries[1])

    def testDeepCopy0(self) -> None:
        log = TestSimpleLog.log.copy()
        lognew = log.copy()
        self.assertEqual(log, lognew)
        log.remove(0)
        self.assertNotEqual(log, lognew)

    def testCopyEqual0(self) -> None:
        log0 = TestSimpleLog.log.copy()
        log1 = log0.copy()
        
        #equal logs
        self.assertTrue(log0==log1)
        
        #diff log entries
        log1 = SimpleLog()
        log1.add(None)
        log1.add(TestSimpleLog.logExpectedEntries[1])
        self.assertFalse(log0==log1)

        #diff number of log entries
        log1 = log0.copy()
        self.assertTrue(log0==log1)
        log1.add("New")
        self.assertFalse(log0==log1)

        #diff log time entries
        log1 = SimpleLog()
        log1.add(TestSimpleLog.logExpectedEntries[0])
        log1.add(TestSimpleLog.logExpectedEntries[1])
        self.assertFalse(log0==log1)

        #diff log info entries
        log1 = log0.copy()
        self.assertTrue(log0==log1)
        log1.setInfoAt(1, "New")
        self.assertFalse(log0==log1)

    def testDel0(self) -> None:
        log = TestSimpleLog.log.copy()
        log.add(TestSimpleLog.logExpectedEntries[2])
        log.remove(1)
        logentries = log.getAll()
        self.assertEqual(len(log), 2)  
        self.assertEqual(logentries[0][1], TestSimpleLog.logExpectedEntries[0])
        self.assertEqual(logentries[1][1], TestSimpleLog.logExpectedEntries[2])

    def testHeadTail0(self) -> None:
        log0 = TestSimpleLog.log.copy()
        log0.add(TestSimpleLog.logExpectedEntries[2])
        log0.add(TestSimpleLog.logExpectedEntries[3])
        #log 0 has 4 entries
        log1 = log0.copy()
        log1.remove(3)      #has first 3 entries
        log2 = log0.copy()
        log2.remove(0)      #has last 3 entries
        self.assertTrue(log0.head(3) == log1)
        self.assertTrue(log0.tail(3) == log2)
        self.assertTrue(log0.tail(3) != log1)

        #Just to make sure logo was not changed
        #simple test deepcopy of Head() and Tail()
        self.assertTrue(len(log0)==4)


    def testPrint0(self) -> None:
        log = TestSimpleLog.log.copy()
        cmpstr = self.__logTestStr()
        self.assertEqual(str(log), cmpstr)


    def testPlot0(self) -> None:
        log = TestSimpleLog.log.copy()
        log.timeplot()


#This way only runs if NOT imported!
if __name__ == "__main__":
    try:
        unittest.main()
    #avoid exception inside vscode when exiting unittest
    except SystemExit as e: 
        pass
