'''
Compare predicted series
v0.1 nov 2020
hdaniel@ualg.pt
'''

from hdlib.base import Base
import numpy as np

class Tools(Base):
    """Implements several tools to compare time series predictions"""
    "It assumes a series are unidimensional vectors"

    @staticmethod
    def predictedCommon(actual:np.array, predict:np.array, horizon:int) -> (np.array,np.array):
        """
        :param actual:  the actual series
        :param predict: the predicted series (of actual)
        :param horizon: horizon defines how steps in future is the first prediction
                        cannot be larger than series length
        :return:

        ?? BUT that is NOT what we want?!? we want to predict from now n future steps.... right?"
        horizon defines how many steps in future is the first prediction

        both series should have same length but
        predict should be skewed horizon points from actual, so:

        predict starts at point horizon (referring to actual)
        and will predict more horizon points after end of actual
        Eg.:
        If:
        actual = [0, 1, 2, 3, 4, 5, 6]
        horizon = 3
        then:
        predict = [3, 4, 5, 6, 7, 8, 9]
        """

        #force np.array
        __actual  = np.array(actual)
        __predict = np.array(predict)
        nsamples = __actual.shape[0]

        #series should have same length
        if __actual.shape != __predict.shape:
            raise RuntimeError('actual and predicted should have same length')

        #horizon must be in [0, __nsamples]
        if horizon > nsamples or horizon < 0:
            raise RuntimeError('horizon must be in range: [0, series length]')

        """
        These views have horizon samples less than the originals: actual and predict

            Common points view:
            __actualCommon removes not predicted horizon samples from beginning of actual
            __predictCommon removes horizon predicted points from the end of predict

            This way if prediction is 100% accurate __actualCommon == __predictCommon

            Note: If predict is the same as actual (naive forecasting): actual == predict
        """
        return  (__actual[horizon:], __predict[:nsamples-horizon])
