#Numpy arrays extensions
#
#Deprecated: Can also be done with Pandas
#
#v0.1 jan 2019
#hdaniel@ualg.pt
#
import numpy as np
import math

#scale between 0 and 1
#normalization or min-max scaling
def normalize(data):
    return scale(data)
def scale(data, minimum=None, maximum=None):
    if minimum is None: minimum = np.amin (data)
    if maximum is None: maximum = np.amax (data)
    den = maximum-minimum
    return np.vectorize(lambda val: (val-minimum)/den)(data)

#returns a list of arrays with specified size
def splitSize(data, size):
    idxs = np.arange(size, data.shape[0], size)
    # Does NOT work, since it divides in equal arrays
    # not in arrays with a given size
    # nSections = math.ceil(data.shape[0] / size)
    return np.array_split(data, idxs)
    '''
    #From scratch (did not take care about efficiency):
    allSections = []
    count = 0
    section = []
    
    for row in data:
        section.append(row)
        count += 1
        if count >= size:
            allSections.append(np.array(section))
            count = 0
            section = []
    if count>0:
        allSections.append(np.array(section))
    return allSections
    '''    

#Joins a list of arrays with specified size and returns it
#Note: numpy array.flatten() can not be used, since this is a list of array
#      not an array of arrays
#
#This is just a wrapper for numpy concatenate
def join(data):
    return np.concatenate(data)

#splitAt vector (or array by row) at threshold: [0:threshold], [threshold:]
#if threshold is undefined then compute it from ratio
#if ratio and threshold are undefine returns None
def splitAt(data, threshold=None, ratio=None):
    datalen = len(data)
    if threshold is None:
        if ratio is None: return None
        threshold = round(datalen * ratio)
	#or: (both returns.views)
    return [data[0:threshold], data[threshold:]]
    #return np.split(data, [threshold])


##############
# Unit tests #
##############
import unittest

a = np.array([0, 1, 2, 3, 4, 5, 6, 7])
b = np.array([[0, 1], [2, 3], [4, 5], [6, 7]])
u = np.array([[1, 11], [2, 3], [4, 5], [6, 7]])

class TestScale(unittest.TestCase):
    def test0(self):
        self.assertTrue(np.array_equal(scale(u),    [[0, 1], \
                                                    [0.1, 0.2], \
                                                    [0.3, 0.4], \
                                                    [0.5, 0.6]]))
    def test1(self):
        self.assertTrue(np.array_equal(scale(u),    [[0, 1], \
                                                    [0.1, 0.2], \
                                                    [0.3, 0.4], \
                                                    [0.5, 0.6]]))
    def test2(self):
        self.assertTrue(np.array_equal(scale(u,1,3),[[0, 5], \
                                                    [0.5, 1], \
                                                    [1.5, 2], \
                                                    [2.5, 3]]))

class TestsplitSize(unittest.TestCase):
    def testVector0(self):
        self.assertTrue(np.array_equal(splitSize(a,1), [[0],[1],[2],[3],[4],[5],[6],[7]]))
    def testVector1(self):
        r = [[0,1],[2,3],[4,5],[6,7]]
        c = splitSize(a,2)
        for i in range(4):  
            self.assertTrue(np.array_equal(c[i], r[i]))
    def testVector2(self):
        #or: self.assertTrue(np.array_equal(splitSize(a,3), [[0,1,2],[3,4,5],[6,7]]))        
        r = [[0,1,2],[3,4,5],[6,7]]
        c = splitSize(a,3)
        for i in range(3):  
            self.assertTrue(np.array_equal(c[i], r[i]))
    def test2Darray0(self):
        c = splitSize(b,3)
        self.assertTrue(np.array_equal(c[0], [[0,1],[2,3],[4,5]]))
        self.assertTrue(np.array_equal(c[1], [[6,7]]))
 
class TestSplitAt(unittest.TestCase):
    def testNone(self):
        self.assertEqual(splitAt(a), None)
    def testVector0(self):
        c, d = splitAt(a, threshold=2)
        self.assertTrue(np.array_equal(c, [0,1]))
        self.assertTrue(np.array_equal(d, [2,3,4,5,6,7]))
    def testVector1(self):
        c, d = splitAt(a, ratio=0.8)
        self.assertTrue(np.array_equal(c, [0,1,2,3,4,5]))
        self.assertTrue(np.array_equal(d, [6,7]))
    def test2Darray0(self):
        c, d = splitAt(b, threshold=2)
        self.assertTrue(np.array_equal(c, [[0,1],[2,3]]))
        self.assertTrue(np.array_equal(d, [[4,5],[6,7]]))
    def test2Darray1(self):
        c, d = splitAt(b, ratio=0.8)
        self.assertTrue(np.array_equal(c, [[0,1],[2,3],[4,5]]))
        self.assertTrue(np.array_equal(d, [[6,7]]))

class TestJoin(unittest.TestCase):
    def test0(self):
        self.assertTrue(np.array_equal(join(b), a))

#This way only runs if NOT imported!
if __name__ == "__main__":
    unittest.main()

