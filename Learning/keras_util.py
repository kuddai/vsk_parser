import numpy as np
import json
import cPickle
import sys

def to_learn(name, xtr, ttr, model, optimizer, loss):
    cPickle.dump((name, xtr, ttr, model.to_json(), optimizer, loss),
                 open("./Learning/tmp/cur_learning_model.pkl", "w"))
    print "saving " + name

def learn_from(nb_epoch=45, batch_size=32):
    from keras.models import model_from_json
    name, xtr, ttr, model_json, optimizer, loss = cPickle.load(open("./Learning/tmp/cur_learning_model.pkl"))
    model = model_from_json(model_json)
    model.compile(optimizer=optimizer, loss=loss)

    print name, xtr.shape, ttr.shape
    hist = model.fit(xtr, ttr, validation_split=0.1, nb_epoch=nb_epoch, batch_size=batch_size)
    cPickle.dump((hist, model), open("./Learning/tmp/cur_trained_model.pkl", "w"))
    print "saved to ./Learning/tmp/cur_trained_model.pkl"

def get_learnt():
    hist, model = cPickle.load( open("./Learning/tmp/cur_trained_model.pkl"))
    return hist, model

def create_dense_layer(dense_layer_index, keras_weights):
    result = {}
    weights_index = 2*dense_layer_index
    bias_index    = 2*dense_layer_index + 1

    weights_values = keras_weights[weights_index].tolist()
    bias_values = keras_weights[bias_index].tolist()

    weights = {}
    weights["$type"] = "System.Double[,], mscorlib"
    weights["$values"] = weights_values

    bias = {}
    bias["$type"] = "System.Double[], mscorlib"
    bias["$values"] = bias_values

    result["$type"] = "ASKI.Learning.LinearLayer, Assembly-CSharp"
    result["Weights"] = weights
    result["Bias"] = bias
    return result

def keras2unity(keras_model_json, keras_weights):
    """
    converts keras model into unity feedforward neural network via Json.
    Assumptions:
    * keras model is Sequential
    * it has only Dense, Relu, Sigmoid layers.
    * Model is MLP
    return:  Json string of keras model with weights compatible with Unity.
    """
    net_spec = {}
    net_spec["$type"] = "ASKI.Learning.NeuralNet, Assembly-CSharp"
    layers_spec = {}
    layers_spec["$type"] = "System.Collections.Generic.List`1[[ASKI.Learning.ILayer, Assembly-CSharp]], mscorlib"

    layers_values = []
    dense_layer_index = 0

    for r in json.loads(keras_model_json)["config"]:
        layer = {}
        if   r["class_name"] == "Activation" and r["config"]["activation"] == "relu":
            layer["$type"] = "ASKI.Learning.ReluLayer, Assembly-CSharp"
        elif r["class_name"] == "Activation" and r["config"]["activation"] == "sigmoid":
            layer["$type"] = "ASKI.Learning.SigmoidLayer, Assembly-CSharp"
        elif r["class_name"] == "Dense":
            layer = create_dense_layer(dense_layer_index, keras_weights)
            dense_layer_index += 1
        else:
            raise KeyError("Unknown layer type: " + r["class_name"] + r["config"]["activation"])

        layers_values.append(layer)

    layers_spec["$values"] = layers_values
    net_spec["Layers"] = layers_spec

    return json.dumps(net_spec)

if __name__ == "__main__":
    hist, model = cPickle.load(open("./tmp/cur_trained_model.pkl"))
    print keras2unity(model.to_json(), model.get_weights())