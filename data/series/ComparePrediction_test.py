'''
Compare predicted series unit tests
v0.1 nov 2020
hdaniel@ualg.pt
'''

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

#Naive prediction
predict1 = actual0
mse1 = 9

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
        cp = ComparePrediction(actual0, predict0, horizon0)
        ap = cp.commonPoints()
        self.assertTrue((ap[0] == ap[1]).all)
        self.assertTrue((ap[0] == common0).all)

    def testExactPredictionMSE0(self):
        cp = ComparePrediction(actual0, predict0, horizon0)
        ap = cp.commonPoints()
        self.assertEqual(mse(ap[0],ap[1]), mse0)

    def testNaivePredictionMSE0(self):
        cp = ComparePrediction(actual0, predict1, horizon0)
        ap = cp.commonPoints()
        self.assertEqual(mse(ap[0],ap[1]), mse1)


#This way only runs if NOT imported!
if __name__ == "__main__":
    print("ok")
    try:
        unittest.main()
    #avoid exception inside vscode when exiting unittest
    except SystemExit as e:
        pass
