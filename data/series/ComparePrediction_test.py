'''
Compare predicted series unit tests
v0.1 nov 2020
hdaniel@ualg.pt
'''

'''
Tests must be ran from module dir to find figures to compare
in folder: testdata
'''

import io
import numpy as np
from sklearn.metrics import mean_squared_error as mse
from hdlib.data.series.ComparePrediction import ComparePrediction

##############
# Unit tests #
##############
import unittest

spawn = 20
horizon0 = 3

#Exact prediction
actual0  = np.arange(spawn)
predict0 = np.arange(horizon0,spawn+horizon0)
common0  = np.arange(horizon0,spawn)
mse0 = 0
cpexact = ComparePrediction(actual0, predict0, horizon0)


#Naive prediction
predict1 = actual0
mse1 = 9
cpnaive = ComparePrediction(actual0, predict1, horizon0)


class TestComparePredicition(unittest.TestCase):
    """Unit tests."""
    def testDiffLengths0(self):
        with self.assertRaises(RuntimeError) as context:
            ComparePrediction([0, 1], [0, 2, 3, 4], 1)
            self.assertTrue('actual and predicted should have same length' in str(context.exception))

    def testInvalidHorizon0(self):
        with self.assertRaises(RuntimeError) as context:
            ComparePrediction([0, 1], [0, 2], -33)
            self.assertEqual('0 <= horizon <= series length', str(context.exception))

    def testInvalidHorizon1(self):
        with self.assertRaises(RuntimeError) as context:
            ComparePrediction([0, 1], [0, 2], -1)
            self.assertEqual('0 <= horizon <= series length', str(context.exception))

    def testInvalidHorizon2(self):
        with self.assertRaises(RuntimeError) as context:
            ComparePrediction([0, 1], [0, 2], 3)
            self.assertEqual('0 <= horizon <= series length', str(context.exception))

    def testExactPredictionElements(self):
        ap = cpexact.commonPoints()
        self.assertTrue((ap[0] == ap[1]).all)
        self.assertTrue((ap[0] == common0).all)

    def testExactPredictionMSE0(self):
        ap = cpexact.commonPoints()
        self.assertEqual(mse(ap[0],ap[1]), mse0)

    def testNaivePredictionMSE0(self):
        ap = cpnaive.commonPoints()
        self.assertEqual(mse(ap[0],ap[1]), mse1)

    #DOES NOT test, just to show
    #could save the file and compare it
    def testPlotCMP0(self):
        fig, axs = cpnaive.plot(xtatitle=" (MSE = " + str(mse1) +")")
        buffer = io.BytesIO()
        fig.savefig(buffer) #fig.savefig('figcmp.png')
        file = open('testdata/figcmp.png','rb')
        self.assertEqual(buffer.getvalue(), file.read())
        buffer.close()
        file.close()
        

    def testPlotNAIVE0(self):
        fig, axs = cpnaive.plot(overlap=True, xtatitle=" (overlapping is bad)")
        buffer = io.BytesIO()
        fig.savefig(buffer) #fig.savefig('fignaive.png')
        file = open('testdata/fignaive.png','rb')
        self.assertEqual(buffer.getvalue(), file.read())
        buffer.close()
        file.close()


#This way only runs if NOT imported!
if __name__ == "__main__":
    print("ok")
    try:
        unittest.main()
    #avoid exception inside vscode when exiting unittest
    except SystemExit as e:
        pass
