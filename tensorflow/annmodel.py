''' 
Define ANN models and algorithms base class
Defines also some common network topologies

jan 2019 hdaniel@ualg.pt
'''

import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import pandas as pd
from hdlib.time.stopwatch import Stopwatch
import hdlib.tensorflow.plot as tfplt


class ANNModel():
    ''' 
    Define ANN models and algorithms base class
    Default constructor calls self.define() method on descedant class,
    with default arguments

    self.define() method must be defined in each subclass
    '''

#define the network model
    def __init__(self, *args, **kwargs):
        '''
        Base class constructor calls define() in each sub class with any arguments.
        Sets also callbacks to None.
        Callbacks can be used to autosave model during trainning. See autosave()

        If called with no arguments from the subclass, calls define() on the subclass
        with default arguments.
        '''
        self._callbacks = []
        self.define(*args, **kwargs)

    #Define the net
    def define(self, save=None):
        '''
        Must be redefined in each subclass to define the network topology.
        See MLP subclass example
        '''
        # module ABC introduces decorator @abstractmethod
        # but has problems with multiple inheritance if a descendan inherites from metaclass
        # ABCmeta (because base abstact class must) and form a descendadnt of other metacalss
        #
        # raising an exception have also issues with multiple inheritance, because
        # the use of super() is not possible (raises exception=), making multiple inheritance 
        # impossible to choose upper class
        #raise NotImplementedError('Should be implemented by concrete sub class')
        #
        #better just pass
        pass

    # compile the model
    # Define training optimizer function and learning rate,
    # eg.: sgd: Stochastic Gradient Descent
    #['accuracy', 'mean_absolute_error', 'mean_squared_error']
    #or: acc , mae,  mse
    def compile(self, optimizer='sgd', loss='mse', metrics='acc', *args, **kwargs):
        self.model.compile(optimizer=optimizer, loss=loss, metrics=metrics, *args, **kwargs)

    def save(self, filename):
        self.model.save(filename)
    
    def load(self, filename):
        self.model = tf.keras.models.load_model(filename)

    #https://machinelearningmastery.com/how-to-stop-training-deep-neural-networks-at-the-right-time-using-early-stopping/
    def earlyStop(self, filename, monitor='val_loss', minDelta=0.0001, patience=10, epochPeriod=1, verbose=1):
        estop = tf.keras.callbacks.EarlyStopping(
                        monitor=monitor, min_delta=minDelta, patience=patience, 
                        verbose=verbose)
        self._callbacks.append(estop)
        self.autosave(self, filename, epochPeriod=epochPeriod, verbose=verbose)

    #https://keras.io/callbacks/#reducelronplateau
    #if minLR == 0 it keeps reducing 
    #cooldown: wait before resuming normal operation (i.e. beginning to monitor if there is any improvement in the monitored metric over a patience epochs).
    #if cooldown=5 after the learning rate is reduced, the algorithm waits 5 epochs before starting to monitor the metrics again. 
    #So if there is no improvement in the metric and patience=10, the learning rate will be reduced again after 15 epochs.
    def adaptLR(self, monitor='val_loss', factor=0.1, minDelta=0.0001, minLR=0, cooldown=0, patience=5):
        reducef = tf.keras.callbacks.ReduceLROnPlateau(
                        monitor='val_loss', factor=factor, min_delta=minDelta, 
                        min_lr=minLR, cooldown=cooldown, patience=patience, verbose=verbose)
        self._callbacks.append(reducef)
        
    def autosave(self, filename, epochPeriod=1, verbose=1):
        '''
        verbose = 0 do not save anything
        verbose = 1 save the last best model only
        verbose = 2 save each best model as is obtained
        verbose = 3 save at each epoch period

        Note: by default save_weights_only==False, so save allways whole model
              also by default monitors loss function to infer models (monitor='val_loss') 
              and mode='auto' to infer direction (mode can be 'min' or 'max')
        '''
        if verbose == 1:
            save = tf.keras.callbacks.ModelCheckpoint(filepath=filename, verbose=verbose, period=epochPeriod, save_best_only=True)
        if verbose == 2:
            filename += '-{epoch:04d}-{val_loss:.6f}.h5'
            save = tf.keras.callbacks.ModelCheckpoint(filepath=filename, verbose=verbose, period=epochPeriod, save_best_only=True)
        if verbose == 3:
            filename += '-{epoch:04d}-{val_loss:.6f}.h5'
            save = tf.keras.callbacks.ModelCheckpoint(filepath=filename, verbose=verbose, period=epochPeriod)
        self._callbacks.append(save)

    #Train the model
    def train(self, trainXs, trainYs, epochs=10, validationSplit=0.2, batchSize=128, 
              verbose=0, debug=False):
        chrono = Stopwatch()
        chrono.reset() 

        #Note: If batchSize, after split in train and validate, train data is smaller than batch
        #gives error at fit():
        ##AttributeError: 'ProgbarLogger' object has no attribute 'log_values
        #https://github.com/keras-team/keras/issues/3657#issuecomment-360522232
        response = self.model.fit(trainXs, trainYs, batch_size=batchSize, 
                                validation_split=validationSplit,
                                epochs=epochs, callbacks=self._callbacks, verbose=verbose)
        chrono.lap()
        loss = response.history['loss'][0]
        print('Train Loss:', loss, 'compute time: ' + str(chrono.read(1)))
        print(response.history.keys())
        if debug:
            tfplt.plotTrainHistory(response)              

    #Predict
    def predict(self, testXs):
        #predict
        predict = self.model.predict(testXs)
        #set time index
        predict = pd.DataFrame(predict, columns=['predict'], index=testXs.index)
        return predict

    def __str__(self):
        rows = []
        self.model.summary(print_fn=lambda x: rows.append(x))
        output = "\n".join(rows)
        return output


class MLP1h(ANNModel):
    '''
    Define a Multi Layer Perceptron with one hidden kayer
    '''
    def define(self, numInputs=1, numOutputs=1, numNeurons=1, activation=tf.nn.relu, save=None):
        super().define(save)
        self.model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(numNeurons, activation=activation, input_shape=(numInputs,)),  # input shape required
        tf.keras.layers.Dense(numNeurons, activation=activation),
        tf.keras.layers.Dense(numOutputs)
        ])

class MLP(ANNModel):
    '''
    Define a Multi Layer Perceptron with n hidden layers
    '''
    def define(self, numInputs=1, numOutputs=1, numNeurons=[1], activation=tf.nn.relu, save=None):
        super().define(save)
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Dense(numNeurons[0], activation=activation, input_shape=(numInputs,)))  # input shape required
        for n in numNeurons:
            self.model.add(tf.keras.layers.Dense(n, activation=activation))
        self.model.add(tf.keras.layers.Dense(numOutputs))