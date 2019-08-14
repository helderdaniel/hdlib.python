#id hardware avaiable to tensorflow
#
#v0.1 jan 2019
#hdaniel@ualg.py
#
import tensorflow as tf
from tensorflow.python.client import device_lib 

def localDevices():
	return device_lib.list_local_devices()

def sessionDevices():
	return tf.Session(config=tf.ConfigProto(log_device_placement=True))

def sessionDevicesList():
    return tf.Session().list_devices()

#Example: is not ran if imported!
if __name__ == "__main__":
	pass



