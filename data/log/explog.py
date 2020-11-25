#Experiment logger
#
#v0.1 aug 2019
#hdaniel@ualg.pt
#
#import pytz, pickle
#from datetime import datetime
from typing import Tuple, AnyStr #List, Any, Optional, AnyStr
from hdlib.data.log.simplelog import SimpleLog


class ExpLog(SimpleLog):  
    
    def __init__(self, tz="Europe/Lisbon", full=False) -> None:
        super().__init__(tz)
        self.__full = full

    def isFullLog(self) -> bool:
        return self.__full

    def copy(self) -> "SimpleLog":
        copyLogsuper = super().copy()
        copyLog = ExpLog(full=self.__full)
        copyLog.append(copyLogsuper)
        return copyLog

    def __eq__(self, other) -> bool:  #Super defines other as Object
        """Overrides the default implementation"""
        if isinstance(other, SimpleLog):
            if len(self) != len(other): return False
            if self.getTimeZone() != other.getTimeZone():     return False
            #Cannot be used here since it is defined in the base class:
            #if self.__tz != other.__tz: return False
            if self.__full != other.__full:   return False
            for l0,l1 in zip(self.getAll(), other.getAll()):
                if l0 != l1: return False
            return True
        return NotImplemented
    
    #log.add((exp, run, numEpochs, bestAcc, bestLoss, trainTime, trainResponse.history))
    def add(self, exp:AnyStr, run:int, etime:float, history:dict) -> None:
        numEpochs = len(history["val_acc"])
        bestAcc   = max(history["val_acc"])
        bestLoss  = min(history["val_loss"])

        if self.__full:
            super().add((exp, run, numEpochs, bestAcc, bestLoss, etime, history))
        else:
            super().add((exp, run, numEpochs, bestAcc, bestLoss, etime))

    #print log formated
    def show(self, time:bool=True) -> str:
        outstr = ""
        outstr += "Log entries = {}\n".format(len(self))
        outstr += "Log:\n"
        for e in self.getAll():
            if time: outstr += str(e[0]) + ": "
            outstr += str(e[1]) + "\n"

        last = self.getLast()
        outstr += "\nLast log entry:\n"
        outstr += str(last[0]) + "\n"
        outstr += str(last[1])

        return outstr

