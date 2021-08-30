from __future__ import annotations #must be at the beginning of file
from typing import List
import unittest
from lcg import LCG


'''
@author hdaniel@ualg.pt
@version 202108301159
'''
class TestLCG(unittest.TestCase):
    
    def test_nextInt00(self) -> None:   #Method Must start with test_, File must have test in its name
        upBound  : int = 35
        seed     : int = 0
        rnd      : LCG = LCG(seed, 134775813, 1, 0x100000000)  #Turbo Pascal

        expected : List[int] = [ 1, 19, 2, 5, 12, 22, 32, 27, 17, 20 ]
        count    : int       = len(expected)
        actual   : List[int] = [0]*count
        for i in range(count):
            actual[i] = rnd.nextInt(upBound)

        #assertArrayEquals(expected, actual);
        self.assertEqual(expected, actual)


    def testRNDdefault(self):
        rnd      : LCG = LCG.lcg()
        upBound  : int = 35
        expected : List [int] =[3,32,7,9,12,22,29,18,23,24,12,14,27,5,30,4,28,9,7,5,25,29,6,8,20,
                                9,5,13,24,5,10,34,31,18,9,13,4,3,23,28,3,9,33,5,19,20,25,7,26,20,
                                15,13,30,13,3,30,3,21,25,9,7,26,32,10,5,31,11,17,0,0,26,33,1,27,4, 
                                11,28,10,11,15,0,26,12,13,2,29,26,30,14,25,12,24,21,23,17,9,18,33,5,17,
                                7,11,21,20,6,7,29,2,11,20,18,11,20,24,1,17,25,14,7,7,11,25,5,27,0]

        actual : List[int] = [] 
        for i in range (0, len(expected)):
            actual.append(rnd.nextInt(upBound))

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()