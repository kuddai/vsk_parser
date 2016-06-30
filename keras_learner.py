import cPickle
from keras.regularizers import l2
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD, Adam
from keras.models import model_from_json
import numpy as np

name, xtr, ttr, model_tmp = cPickle.load(open("./Learning/tmp/cur_learning_model.pkl"))
model_json = open("./Learning/tmp/cur_learning_model.json").read()
model = model_from_json(model_json)
model.compile('adam', 'mse')

print name, xtr.shape, ttr.shape
hist = model.fit(xtr, ttr, validation_split=0.1, nb_epoch=45, batch_size=32)
cPickle.dump((hist, model), open("./Learning/tmp/cur_trained_model.pkl", "w"))
print "saved to ./Learning/tmp/cur_trained_model.pkl"

