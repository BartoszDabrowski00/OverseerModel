import soundfile
import os, glob, pickle
import numpy as np
import librosa
from keras import regularizers
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping
from keras.callbacks import History, ReduceLROnPlateau, CSVLogger
import warnings
warnings.filterwarnings('ignore')


TRAINING_DATA_PATH = "D:/Studia/Inzynierka/emotion_recognition_cnn-master/data/Ravdess/audio_speech_actors_01-24"#Works only with RAVDESS dataset
TEST_RECORDINGS_PATH = "D:/Studia/Inzynierka/emotion_recognition_cnn-master/data/sample_wav"#Test recording are in wav format

#Extract features (mfcc, chroma, mel) from a sound file
def extract_feature(file_name, mfcc, chroma, mel):
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        if X[1].size == 2:
            X = X[:,0]
        sample_rate=sound_file.samplerate
        if chroma:
            stft=np.abs(librosa.stft(X))
        result=np.array([])
        if mfcc:
            mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            if mfccs.size == 40:
                result=np.hstack((result, mfccs))
            else:
                return result
        if chroma:
            chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result=np.hstack((result, chroma))
        if mel:
            mel=np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
            result=np.hstack((result, mel))
    return result


# Emotions in the RAVDESS dataset
emotions={
  '01':'neutral',
  '02':'neutral',
  '03':'neutral',
  '04':'negative',
  '05':'negative',
  '06':'ignored',
  '07':'negative',
  '08':'neutral'
}
#emotions={
#  '01':'neutral',
#  '02':'calm',
#  '03':'happy',
#  '04':'sad',
#  '05':'angry',
#  '06':'fearful',
#  '07':'disgust',
#  '08':'surprised'
#}

# Emotions in the test recordings
emotions2={
  'ANGRY':'negative',
  'DISGUSTED':'negative',
  'HAPPY':'neutral',
  'NEUTRAL':'neutral',
  'SAD':'negative',
  'SURPRISED':'neutral',
}

#Emotions to observe
observed_emotions=['neutral', 'negative']
#observed_emotions=['neutral', 'positive', 'negative']
#observed_emotions=['neutral', 'calm', 'happy', 'sad', 'angry', 'disgust']


#Load the test data and extract features for each sound file
def load_sample_data():
    x,y=[],[] 
    for file in glob.glob(f"{TEST_RECORDINGS_PATH}/*/*.wav"):
        dir_name = os.path.dirname(file)
        emotion=emotions2[dir_name.split("\\")[1]]
        if emotion not in observed_emotions:
            continue
        feature=extract_feature(file, mfcc=True, chroma=True, mel=False)
        if feature.size != 0:
            x.append(feature)
            y.append(emotion)
    return (np.array(x), y)

x_sample_test,y_sample_test = load_sample_data();

#Load the data and extract features for each sound file
def load_data(test_size=0.2):
    x,y=[],[]
    for file in glob.glob(f"{TRAINING_DATA_PATH}/Actor_*/*.wav"):
        file_name=os.path.basename(file)
        emotion=emotions[file_name.split("-")[2]]
        if emotion not in observed_emotions:
            continue
        feature=extract_feature(file, mfcc=True, chroma=True, mel=False)
        if feature.size != 0:
            x.append(feature)
            y.append(emotion)
    return train_test_split(np.array(x), y, test_size=test_size, random_state=9)

print("Start data loading")
#Split the dataset
x_train,x_test,y_train,y_test=load_data(test_size=0.1)
print("Data loaded")

#Get the shape of the training and testing datasets
print(f"Training dataset: {x_train.shape[0]}")
print(f"Internal testing dataset: {x_test.shape[0]}")
print(f"Test recordings testing dataset: {x_sample_test.shape[0]}")

#Get the number of features extracted
print(f'Features extracted: {x_train.shape[1]}')


#Initialize the Multi Layer Perceptron Classifier

for i in range(1, 10):
    model=MLPClassifier(alpha=0.01, batch_size=64, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=700)#, early_stopping=True
    print("Start training " + str(i))
    model.fit(x_train,y_train)

    #Predict for the test set
    y_pred=model.predict(x_test)

    #Calculate the accuracy of our model
    accuracy=accuracy_score(y_true=y_test, y_pred=y_pred)

    #Print the accuracy
    print("Accuracy for test: {:.2f}%".format(accuracy*100))

    #Predict for the test set
    y_pred=model.predict(x_sample_test)

    #Calculate the accuracy of our model
    accuracy=accuracy_score(y_true=y_sample_test, y_pred=y_pred)

    #Print the accuracy
    print("Accuracy in sample: {:.2f}%".format(accuracy*100))


#import pickle
# Writing different model files to file
#with open( '../../model/modelForPrediction12.sav', 'wb') as f:
    #pickle.dump(model,f)



#filename = '../model/modelForPrediction1.sav'
#loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage

#feature=extract_feature("/content/drive/MyDrive/Colab_Notebooks/RAVDESS_Emotional_speech_audio/speech-emotion-recognition-ravdess-data/Actor_01/03-01-01-01-01-01-01.wav", mfcc=True, chroma=True, mel=True)

#feature=feature.reshape(1,-1)

#prediction=loaded_model.predict(feature)