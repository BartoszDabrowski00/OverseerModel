import os
import time
import librosa
import librosa.display
import matplotlib.pyplot as plt
import json
import numpy as np

FILES_PATH = os.environ.get('RECORDINGS_PATH', 'Emotions')
TRAINING_DATA_FILE_NAME = 'training_data'
CNN_TRAINING_DATA_FILE_NAME = 'cnn_training_data'
N_MFCC = 40


def display_mffcs(mffcs):
    librosa.display.specshow(mffcs)
    plt.colorbar()
    plt.show()


def extract_mffc(file_path, two_dimensional):
    signal, sample_rate = librosa.load(file_path)
    if two_dimensional:
        mffc = librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=N_MFCC)
    else:
        mffc = np.mean(librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=N_MFCC).T, axis=0)
    return mffc


def load_data(path, two_dimensional=False):
    data = {
        "labels": [],
        "features": []
    }

    for root, _, files in os.walk(path):
        for file in files:
            emotion_category = root.split(os.sep)[-1]
            mffcs = extract_mffc(os.path.join(root, file), two_dimensional)
            data["labels"].append(emotion_category)
            data["features"].append(mffcs.tolist())

    return data


def save_data(path, data):
    with open(path, "w") as fp:
        json.dump(data, fp, indent=4)


def main():
    data = load_data(FILES_PATH)
    cnn_data = load_data(FILES_PATH, two_dimensional=True)
    save_data(TRAINING_DATA_FILE_NAME, data)
    save_data(CNN_TRAINING_DATA_FILE_NAME, cnn_data)


if __name__ == '__main__':
    main()

