"""
Plots for tensorflow

in development

v0.01 jan 2019
hdaniel@ualg.pt
"""
import matplotlib.pyplot as plt


def plotTrainHistory(response):
	hist = response.history
	
	plt.subplot(2,1,1)
	plt.xlabel("Epoch")
	plt.ylabel("Accuracy [%]")
	plt.plot([x*100 for x in hist["acc"]], label="Train accuracy")
	plt.plot([x*100 for x in hist["val_acc"]], label = "Validation accuracy")
	plt.legend()
	#plt.ylim([0,2])

	plt.subplot(2,1,2)
	plt.xlabel("Epoch")
	plt.ylabel("Loss [mse]")
	plt.plot(hist["loss"], label="Train loss")
	plt.plot(hist["val_loss"], label = "Validation loss")
	plt.legend()
	#plt.ylim([0,2])
	print(min(hist["val_loss"]))
	plt.show()


'''
def plotTrainHistory(response):
	hist = response.history
	plt.subplot(2,2,1)
	plt.xlabel("Epoch")
	plt.ylabel("Mean Abs Error [MPG]")
	#plt.plot(response.epoch, hist["mean_absolute_error"], label="Train abs Error")
	#plt.plot(response.epoch, hist["val_mean_absolute_error"], label = "Validation abs Error")
	plt.plot(hist["mean_absolute_error"], label="Train abs Error")
	plt.plot(hist["val_mean_absolute_error"], label = "Validation abs Error")
	plt.legend()
	#plt.ylim([0,1])

	plt.subplot(2,2,2)
	plt.xlabel("Epoch")
	plt.ylabel("Mean Square Error [$MPG^2$]")
	plt.plot(hist["mean_squared_error"], label="Train sqd Error")
	plt.plot(hist["val_mean_squared_error"], label = "Validation sqd Error")
	plt.legend()
	#plt.ylim([0,1])

	plt.subplot(2,2,3)
	plt.xlabel("Epoch")
	plt.ylabel("Accuracy [Accuracy]")
	plt.plot(hist["acc"], label="Train accuracy")
	plt.plot(hist["val_acc"], label = "Validation accuracy")
	plt.legend()
	#plt.ylim([0,2])

	plt.subplot(2,2,4)
	plt.xlabel("Epoch")
	plt.ylabel("Loss [Loss]")
	plt.plot(hist["loss"], label="Train loss")
	plt.plot(hist["val_loss"], label = "Validation loss")
	plt.legend()
	#plt.ylim([0,2])

	plt.show()
'''