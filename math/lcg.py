from __future__ import annotations #must be at the beginning of file
import random
import math

'''
 Simple Linear congruential generator:
 https://en.wikipedia.org/wiki/Linear_congruential_generator#Sample_Python_code
 
 @author hdaniel@ualg.pt
 @version 202108301159
 based on java @version 202104191059
'''
class LCG:
    #As defined in Numerical Recipes
    #https://en.wikipedia.org/wiki/Numerical_Recipes
    defaultSeed       : int = 0
    defaultMultiplier : int = 1664525
    defaultIncrement  : int = 1013904223
    defaultModulus    : int = 0x100000000

    def __init__(self, seed : int, a : int, c : int, m : int) -> None:
        self._x0 : int = seed  #seed
        self._a  : int = a     #multiplier
        self._c  : int = c     #increment
        self._m  : int = m     #modulus
    

    @classmethod
    def lcg(cls, seed : int = 0) -> LCG:
        return LCG(cls.defaultSeed, cls.defaultMultiplier, 
                   cls.defaultIncrement, cls.defaultModulus)

    # allow setting seed at any time
    def seed(self, seed : int) -> None:
        self._x0 = seed

    # update generator
    def _update(self) -> int:
        self._x0 = (self._a * self._x0 + self._c) % self._m
        return self._x0

    '''
     @pre bound > 0
     
     @return pseudo random long integer in [0, bound[
    '''
    def nextInt(self, bound : int) -> int:
        #return (int) Math.abs(update() % bound)
        return int(abs(self._update() % bound))
