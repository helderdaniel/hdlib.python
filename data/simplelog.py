#Simple logger
#
#v0.1 jul 2019
#hdaniel@ualg.pt
#
import pytz, pickle
from datetime import datetime
from typing import Tuple, List, Any, Optional, AnyStr

class SimpleLog:   
    def __init__(self, tz='Europe/Lisbon') -> None:
        self.clear()
        self.__tz = pytz.timezone(tz)
    
    def copy(self) -> 'SimpleLog':
        copyLog = SimpleLog()
        copyLog._SimpleLog__tz = self.__tz          #type: ignore
        copyLog._SimpleLog__log = self.__log.copy() #type: ignore
        return copyLog

    def __eq__(self, other) -> bool:  #Super defines other as Object
        '''Overrides the default implementation'''
        if isinstance(other, SimpleLog):
            if self.len() != other.len(): return False
            for l0,l1 in zip(self.getAll(), other.getAll()):
                if l0 != l1: return False
            return True
        return NotImplemented

    def len(self) -> int:
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
        return self.__log
      
    def getFirst(self) -> Optional[Tuple[datetime, Any]]: #Optional allow also None
        if len(self.__log) <= 0: return None
        return self.__log[0]
      
    def getLast(self) -> Optional[Tuple]:
        if len(self.__log) <= 0: return None
        return self.__log[len(self.__log)-1]
    
    def getTime(self) -> List:
        return [e[0] for e in self.__log]
    
    def getInfo(self) -> List[Any]:
        return [e[1] for e in self.__log]
    
    def clear(self) -> None:
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
        self.__log.extend(log._SimpleLog__log)      #type: ignore
        
    #Returns new Log with head(n) entries of receptor
    def head(self, howMany:int=1) -> 'SimpleLog':
        nLog = self.copy()  #Could just create new an copy __tz
        nLog._SimpleLog__log = self.__log[:howMany] #type: ignore
        return nLog

    #Returns new Log with tail(n) entries of receptor
    def tail(self, howMany:int=1) -> 'SimpleLog':
        nLog = self.copy()  #Could just create new an copy __tz
        nLog._SimpleLog__log = self.__log[-howMany:] #type: ignore
        return nLog
