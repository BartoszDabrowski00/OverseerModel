from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
import numpy as np


def to_label_encoding(y):
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)
    return y


def to_one_hot_encoding(y):
    one_hot_encoder = OneHotEncoder()
    y = one_hot_encoder.fit_transform(np.array(y).reshape(-1, 1)).toarray()
    return y
