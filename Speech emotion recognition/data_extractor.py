import os
import time
import librosa
import librosa.display
import matplotlib.pyplot as plt
import json
import numpy as np

FILES_PATH = 'Emotions'
OUTPUT_FILE_NAME = 'conv_data3'
N_MFCC = 40

def display_mffcs(mffcs):
    librosa.display.specshow(mffcs)
    plt.colorbar()
    plt.show()


def extract_mffc(file_path):
    signal, sample_rate = librosa.load(file_path)
    #mffc = np.mean(librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=N_MFCC).T, axis=0)
    mffc = librosa.feature.mfcc(y=signal, sr=sample_rate, n_mfcc=N_MFCC)
    return mffc


def load_data(path):
    data = {
        "labels": [],
        "features": []
    }

    for root, _, files in os.walk(path):
        counter = 0
        for file in files:
            emotion_category = root.split("\\")[-1]
            mffcs = extract_mffc(os.path.join(root, file))
            data["labels"].append(emotion_category)
            data["features"].append(mffcs.tolist())
            counter += 1
            if counter == 2:
                break

    return data


def save_data(path, data):
    with open(path, "w") as fp:
        json.dump(data, fp, indent=4)


def main():
    data = load_data(FILES_PATH)
    save_data(OUTPUT_FILE_NAME, data)


if __name__ == '__main__':
    main()

