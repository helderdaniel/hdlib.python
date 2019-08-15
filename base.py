#base class for hdlib
#
#v0.1 jan 2019
#hdaniel@ualg.pt
#
class Base:
    #def __repr__(self):
    #   raise NotImplementedError('Subclass must implement "__repr__(self)" method')
 
    #May have problem is recursion if objets are composed recursively?
    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    @staticmethod
    def isNumber(obj):
        '''
        Check if an object is integer.
        Multiply the object by zero.
        Any number times zero is zero. 
        Any other result means that the object is not a number (including exceptions)

        https://stackoverflow.com/questions/3441358/what-is-the-most-pythonic-way-to-check-if-an-object-is-a-number/44418960#44418960

        "There probably are some non-number objects in the world that define __mul__ to return zero when multiplied by zero but that is an extreme exception. This solution should cover all normal and sane code that you generate/encouter."
        '''
        try:
            return 0 == obj*0
        except:
            return False
