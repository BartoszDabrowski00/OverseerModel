import json
import numpy as np
import os
from models import NetworksFactory
from skimage import transform
from sklearn.model_selection import train_test_split
from helper import to_one_hot_encoding, to_label_encoding
TRAINING_DATA_PATH = os.environ.get("TRAINING_DATA", "training_data")
CNN_TRAINING_DATA_PATH = os.environ.get("CNN_TRAINING_DATA", "cnn_training_data")
CNN_TRANSFORM_SIZE = [40, 130]


def load_data(file_path):
    with open(file_path, "r") as fp:
        data = json.load(fp)

    X = np.array(data["features"])
    X = np.expand_dims(X, -1)
    y = data["labels"]
    return X, y


def load_data_for_cnn(file_path):
    with open(file_path, "r") as fp:
        data = json.load(fp)

    X = data["features"]
    for i in range(len(X)):
        X[i] = transform.resize(np.array(X[i]), CNN_TRANSFORM_SIZE)

    X = np.array(X)
    X = np.expand_dims(X, -1)
    y = data["labels"]
    return X, y


def main():
    X, y = load_data(TRAINING_DATA_PATH)
    X, X_test, y, y_test = train_test_split(X, y, test_size=0.05, random_state=42)
    network_factory = NetworksFactory(X, y)
    y_test = to_label_encoding(y_test)

    network = network_factory.get_network("Feedforward")
    network.fit(200, 64, 0.1)

    #network = network_factory.get_network("Lstm")
    #network.fit(20, 64, 0.1)

    #network = network_factory.get_network("Lstm2")
    #network.fit(20, 64, 0.1)

    #network = network_factory.get_network("Lstm3")
    #network.fit(20,64,0.1)

    X, y = load_data_for_cnn(CNN_TRAINING_DATA_PATH)
    X, X_test, y, y_test = train_test_split(X, y, test_size=0.05, random_state=42)
    network_factory = NetworksFactory(X, y)
    y_test = to_label_encoding(y_test)
    network = network_factory.get_network("Cnn")
    network.fit(30, 64, 0.1)

    score = network.model.evaluate(X_test, y_test, batch_size=60, verbose=0)
    print('Accuracy: {0:.0%}'.format(score[1] / 1))
    print("Loss: %.4f\n" % score[0])


if __name__ == '__main__':
    main()
