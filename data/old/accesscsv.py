#CSV utils
#
#Deprecated: Can also be done with Pandas
#
#v0.1 jan 2019
#hdaniel@ualg.pt
#
import csv
import numpy as np

#read from CSV file
#invert row order if invTime = True
#returns numpy.array
def readNParray(csvfilename, delimiter=',', invTime=False):
    #arr = np.genfromtxt(csvfilename, delimiter=delimiter)
    arr = np.loadtxt(csvfilename, delimiter=delimiter)
    if invTime:
        return np.flipud(arr)
    return arr

#read from CSV file
#invert row order if invTime = True
#returns python list
def readList(csvfilename, delimiter=',', invTime=False):
    l = []
    with open(csvfilename, 'r', newline='') as csvfilein:
        reader = csv.reader(csvfilein, delimiter=delimiter)
        for row in reader:
            #map: Only works in Python 2.x. Why?
            #row = map(float, row)
            #row = map(lambda x: float(x), row)
            row = [float(i) for i in row]
            if invTime:
                l.insert(0, row)
            else:
                l.append(row)
    csvfilein.close()
    return l

#write numpy.array to CSV file
def writeNParray(csvfilename, x,  delimiter=',', **args):
    np.savetxt(csvfilename, x, delimiter=delimiter, **args)

#write python list to CSV file
def writeList(csvfilename, x,  delimiter=','):
    with open(csvfilename, 'w', newline='') as csvfileout:
        writer = csv.writer(csvfileout, delimiter=delimiter)
        writer.writerows(x)
    csvfileout.close()

##############
# Unit tests #
##############
import unittest
import os # to remove testfile

class TestCSV(unittest.TestCase):
    testfn = "testfile.csv"
    a = np.array([[0, 1], [2, 3], [4, 5], [6, 7]])
    b = [[0, 1], [2, 3], [4, 5], [6, 7]]
    br= [[6, 7], [4, 5], [2, 3], [0, 1]]

    
    def testReadWriteNumpy0(self):
        if os.path.exists(self.testfn):
            raise Exception("File with the same name as Test Filename exists. Cannot perfrom test")
        writeNParray(self.testfn, self.a,  delimiter=' ')
        r = readNParray(self.testfn, delimiter=' ', invTime=False)
        self.assertTrue(np.array_equal(self.a, r))
        os.remove(self.testfn)

    def testReadWriteNumpy1(self):
        if os.path.exists(self.testfn):
            raise Exception("File with the same name as Test Filename exists. Cannot perfrom test")
        writeNParray(self.testfn, self.a,  delimiter=' ')
        r = readNParray(self.testfn, delimiter=' ', invTime=True)
        self.assertTrue(np.array_equal(np.flipud(self.a), r))
        os.remove(self.testfn)

    def testReadWriteList0(self):
        if os.path.exists(self.testfn):
            raise Exception("File with the same name as Test Filename exists. Cannot perfrom test")
        writeList(self.testfn, self.b,  delimiter=' ')
        r = readList(self.testfn, delimiter=' ', invTime=False)
        self.assertTrue(np.array_equal(self.b, r))
        os.remove(self.testfn)

    def testReadWriteList1(self):
        if os.path.exists(self.testfn):
            raise Exception("File with the same name as Test Filename exists. Cannot perfrom test")
        writeList(self.testfn, self.b,  delimiter=' ')
        r = readList(self.testfn, delimiter=' ', invTime=True)
        self.assertTrue(np.array_equal(self.br, r))
        os.remove(self.testfn)

#This way only runs if NOT imported!
# #Note: this example cannot be executed from this module since 
#it imports a module (csv) with the same  name of this,
#so the name of the module was defined as: accesscsv
if __name__ == "__main__":
    unittest.main()
 
