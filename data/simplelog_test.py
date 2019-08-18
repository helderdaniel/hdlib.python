#Simple logger
#
#v0.1 jul 2019
#hdaniel@ualg.pt
#
from hdlib.data.simplelog import SimpleLog

##############
# Unit tests #
##############
import unittest
from typing import ClassVar #, Any, Tuple, Type, List
from datetime import datetime

class TestSimpleLog(unittest.TestCase):
    """Unit tests"""

    logFN : ClassVar[str] = "logexample.log"
    
    @classmethod
    def setUpClass(cls) -> None:
        #code to be executed only once before all tests start
        #Create and save log
        log = SimpleLog()
        log.add(("SimpleLog first entry ", 0))
        log.add(("SimpleLog second entry ", 1))
        log.save(TestSimpleLog.logFN)
    
    def testLoad0(self) -> None:
        log = SimpleLog.load(TestSimpleLog.logFN)
        logentries = log.getAll()
        #print(logentries)
        self.assertEqual(logentries[0][1], ('SimpleLog first entry ', 0))
        self.assertEqual(logentries[1][1], ('SimpleLog second entry ', 1))

    def testFirstLastClear0(self) -> None:
        log = SimpleLog.load(TestSimpleLog.logFN)
        log.add(('SimpleLog third entry ', 2))
        logfirst = log.getFirst()
        loglast  = log.getLast()
        self.assertEqual(log.len(), 3)
        self.assertEqual(logfirst[1], ('SimpleLog first entry ', 0))  #type: ignore
        self.assertEqual(loglast[1],  ('SimpleLog third entry ', 2))  #type: ignore
        log.clear()
        self.assertEqual(log.len(), 0)  

    def testCopy0(self) -> None:
        log = SimpleLog.load(TestSimpleLog.logFN)
        lognew = log.copy()
        logentries = lognew.getAll()
        self.assertEqual(logentries[0][1], ('SimpleLog first entry ', 0))
        self.assertEqual(logentries[1][1], ('SimpleLog second entry ', 1))

    def testDel0(self) -> None:
        log = SimpleLog.load(TestSimpleLog.logFN)
        log.add(("SimpleLog third entry ", 2))
        log.remove(1)
        logentries = log.getAll()
        self.assertEqual(log.len(), 2)  
        self.assertEqual(logentries[0][1], ('SimpleLog first entry ', 0))
        self.assertEqual(logentries[1][1], ('SimpleLog third entry ', 2))

    def testGetTime0(self) -> None:
        log = SimpleLog.load(TestSimpleLog.logFN)
        logentries = log.getAll()
        logentriestime = log.getTime()
        #print(logentriestime)
        self.assertEqual(logentries[0][0], logentriestime[0])
        self.assertEqual(logentries[1][0], logentriestime[1])

    def testGetInfo0(self) -> None:
        log = SimpleLog.load(TestSimpleLog.logFN)
        logentries = log.getAll()
        logentriesinfo = log.getInfo()
        #print(logentriestime)
        self.assertEqual(logentries[0][1], logentriesinfo[0])
        self.assertEqual(logentries[1][1], logentriesinfo[1])

    def testCopyEqual0(self) -> None:
        log0 = SimpleLog.load(TestSimpleLog.logFN)
        log1 = log0.copy()

        #equal logs
        self.assertTrue(log0==log1)
        
        #diff log entries
        log1._SimpleLog__log[0] = None  #type: ignore
        self.assertFalse(log0==log1)

        #diff number of log entries
        log1 = log0.copy()
        self.assertTrue(log0==log1)
        log1.add('test')
        self.assertFalse(log0==log1)

        #diff log time entries
        log1 = log0.copy()
        self.assertTrue(log0==log1)
        e0 = log1._SimpleLog__log[0]                     #type: ignore
        log1._SimpleLog__log[0] =  (e0[0], ('test', 2))  #type: ignore
        self.assertFalse(log0==log1)

        #diff log info entries
        log1 = log0.copy()
        self.assertTrue(log0==log1)
        e0 = log1._SimpleLog__log[0]                     #type: ignore
        log1._SimpleLog__log[0] =  (datetime.now(), e0[1])  #type: ignore
        self.assertFalse(log0==log1)

    def testHeadTail0(self) -> None:
        log0 = SimpleLog.load(TestSimpleLog.logFN)
        log0.add(("SimpleLog third entry ", 2))
        log0.add(("SimpleLog fourth entry ", 3))
        #log 0 has 4 entries
        log1 = log0.copy()
        log1.remove(3)      #has first 3 entries
        log2 = log0.copy()
        log2.remove(0)      #has last 3 entries
        self.assertTrue(log0.head(3) == log1)
        self.assertTrue(log0.tail(3) == log2)
        self.assertTrue(log0.tail(3) != log1)


#This way only runs if NOT imported!
if __name__ == "__main__":
    try:
        unittest.main()
    #avoid exception inside vscode when exiting unittest
    except SystemExit as e: 
        pass
