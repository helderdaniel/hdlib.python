#Simple logger
#
#v0.1 jul 2019
#hdaniel@ualg.pt
#
import pytz, pickle
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Tuple, List, Any, Optional, AnyStr

class SimpleLog:   
    def __init__(self, tz='Europe/Lisbon') -> None:
        self.clear()
        self.__tz = pytz.timezone(tz)
    
    def getTimeZone(self):
        return self.__tz
        
    def getInfoAt(self, idx):
        return self.__log[idx][1]

    def setInfoAt(self, idx, val):
        entry = list(self.__log[idx])
        entry[1] = val
        self.__log[idx] = tuple(entry)

    def copy(self) -> 'SimpleLog':
        copyLog = SimpleLog()
        copyLog.__tz = self.__tz          #type: ignore
        copyLog.__log = self.__log.copy() #type: ignore
        return copyLog

    def __eq__(self, other) -> bool:  #Super defines other as Object
        '''Overrides the default implementation'''
        if isinstance(other, SimpleLog):
            if len(self) != len(other): return False
            if self.getTimeZone() != other.getTimeZone():     return False
            #or, since it is defined in this base class:
            #if self.__tz != other.__tz: return False
            for l0,l1 in zip(self.getAll(), other.getAll()):
                if l0 != l1: return False
            return True
        return NotImplemented

    def __len__(self) -> int:
        return len(self.__log)
        
    def add(self, data:Any) -> None:
        now = datetime.now(self.__tz)
        self.__log.append((now, data))
    
    def remove(self, index:int) -> None:
        '''
        removes log entry specified by index
        PRE: index >= 0 && index < self.len()
        '''
        del self.__log[index]
    
    def getAll(self) -> List[Tuple[datetime, Any]]:
        """returns a copy of log list"""
        return self.__log.copy()
    
    def getFirst(self) -> Optional[Tuple[datetime, Any]]: #Optional allow also None
        """returns a copy of log first entry"""
        if len(self.__log) <= 0: return None
        #need to copy all log, cause log entrie can be any type
        #that might not support .copy()
        return self.__log.copy()[0]
      
    def getLast(self) -> Optional[Tuple]:
        """returns a copy of log last entry"""
        if len(self.__log) <= 0: return None
        #need to copy all log, cause log entrie can be any type
        #that might not support .copy()
        return self.__log.copy()[len(self.__log)-1]
    
    def getTime(self) -> List:
        """returns a copy of log time entries"""
        return [e[0] for e in self.__log.copy()]
    
    def getInfo(self) -> List[Any]:
        """returns a copy of log info entries"""
        return [e[1] for e in self.__log.copy()]
    
    def clear(self) -> None:
        """clears all log entries"""
        self.__log : List[Tuple[datetime, Any]] = [] 
    
    def save(self, fn:AnyStr) -> None:
        with open(fn, 'wb') as fp:
            pickle.dump(self, fp)
    
    @classmethod 
    def load(cls, fn:AnyStr) -> 'SimpleLog':
        with open(fn, 'rb') as fp:
            return pickle.load(fp)

    #Appends to receptor
    def append(self, log:'SimpleLog') -> None:
        self.__log.extend(log.__log)      #type: ignore
        
    #Returns new Log with head(n) entries of receptor
    def head(self, howMany:int=1) -> 'SimpleLog':
        nLog = self.copy()  #Could just create new an copy __tz
        nLog.__log = self.__log[:howMany] #type: ignore
        return nLog

    #Returns new Log with tail(n) entries of receptor
    def tail(self, howMany:int=1) -> 'SimpleLog':
        nLog = self.copy()  #Could just create new an copy __tz
        nLog.__log = self.__log[-howMany:] #type: ignore
        return nLog

    def __str__(self):
        out = ""
        for e in self.getAll():
            out += str(e[0]) + ": " + str(e[1]) + "\n"
        return out

    def timeplot(self):
        plt.plot(range(len(self)), self.getTime())
        plt.ylabel("time")
        plt.xlabel("entries")
        plt.show()

