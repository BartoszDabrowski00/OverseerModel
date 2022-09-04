from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization
from keras.regularizers import l2
from helper import to_one_hot_encoding, to_label_encoding
from sklearn.model_selection import train_test_split


class Network:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.model = None

    def fit(self, epochs, batch_size, validation_size):
        X_train, X_validation, y_train, y_validation = train_test_split(self.X, self.y,
                                                                        test_size=validation_size, random_state=42)
        history = self.model.fit(X_train, y_train, validation_data=(X_validation, y_validation), verbose=2,
                                 epochs=epochs, batch_size=batch_size)
        return history


class FeedforwardNetwork(Network):
    def __init__(self, X, y, optimizer, input_shape, loss_func):
        super().__init__(X, y)
        self.y = to_label_encoding(y)
        self.model = Sequential([
            Flatten(input_shape=input_shape),

            Dense(256, activation='relu', kernel_regularizer=l2(0.1)),
            Dropout(0.5),

            Dense(256, activation='relu', kernel_regularizer=l2(0.01)),
            Dropout(0.5),

            Dense(128, activation='relu', kernel_regularizer=l2(0.001)),
            Dropout(0.3),

            Dense(7, activation='softmax')
        ])
        self.model.compile(optimizer=optimizer, loss=loss_func, metrics=['accuracy'])


class LstmNetwork(Network):
    def __init__(self, X, y, optimizer, input_shape, loss_func):
        super().__init__(X, y)
        self.y = to_label_encoding(y)
        self.model = Sequential([
            LSTM(256, return_sequences=False, input_shape=input_shape),
            Dropout(0.2),
            Dense(128, activation='relu'),
            Dropout(0.2),
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(7, activation='softmax')
        ])
        self.model.compile(optimizer=optimizer, loss=loss_func, metrics=['accuracy'])


class LstmNetwork2(Network):
    def __init__(self, X, y, optimizer, input_shape, loss_func):
        super().__init__(X, y)
        self.y = to_one_hot_encoding(y)
        self.model = Sequential([
            LSTM(256, return_sequences=True, input_shape=(40, 1)),
            LSTM(64),
            Dense(7, activation='softmax')
        ])
        self.model.compile(optimizer=optimizer, loss=loss_func, metrics=['accuracy'])


class LstmNetwork3(Network):
    def __init__(self, X, y, optimizer, input_shape, loss_func):
        super().__init__(X, y)
        self.y = to_one_hot_encoding(y)
        self.model = Sequential([
            LSTM(256, return_sequences=True, input_shape=(40, 1)),
            Dropout(0.3),
            LSTM(64),
            Dropout(0.3),
            Dense(7, activation='softmax')
        ])
        self.model.compile(optimizer=optimizer, loss=loss_func, metrics=['accuracy'])


class CnnNetwork(Network):
    def __init__(self, X, y, optimizer, input_shape, loss_func):
        super().__init__(X, y)
        self.y = to_label_encoding(y)
        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            MaxPooling2D((3, 3), strides=(2, 2), padding='same'),
            BatchNormalization(),
            Conv2D(32, (3, 3), activation='relu'),
            MaxPooling2D((3, 3), strides=(2, 2), padding='same'),
            BatchNormalization(),
            Conv2D(32, (2, 2), activation='relu'),
            MaxPooling2D((2, 2), strides=(2, 2), padding='same'),
            BatchNormalization(),
            Flatten(),
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(7, activation='softmax')
        ])
        self.model.compile(optimizer=optimizer, loss=loss_func, metrics=['accuracy'])


class NetworksFactory:
    def __init__(self, X, y):
        self.networks = {
            "Feedforward": FeedforwardNetwork(X, y, keras.optimizers.Adam(learning_rate=0.00001),
                                              (40, 1), 'sparse_categorical_crossentropy'),
            "Lstm": LstmNetwork(X, y, 'adam', (40, 1), 'sparse_categorical_crossentropy'),
            "Lstm2": LstmNetwork2(X, y, 'adam', (40, 1), 'sparse_categorical_crossentropy'),
            "Lstm3": LstmNetwork3(X, y, 'adam', (40, 1), 'sparse_categorical_crossentropy'),
            "Cnn": CnnNetwork(X, y, keras.optimizers.Adam(learning_rate=0.001), (40, 130, 1),
                              'sparse_categorical_crossentropy')
        }

    def get_network(self, network_name):
        return self.networks[network_name]
