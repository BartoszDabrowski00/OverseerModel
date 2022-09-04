import logging

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from overseer.vader_emotion_recognition.audio_converter import AudioToTextConverter


log = logging.getLogger(__name__)


class TextNotConverterException(Exception):
    pass


class VaderClassifier:

    def __init__(self):
        self.sa = SentimentIntensityAnalyzer()
        self.audio_converter = AudioToTextConverter()

    def get_emotions_distribution(self, audio):
        text = self.audio_converter.convert_audio_to_text(audio)
        if text is None:
            raise TextNotConverterException()

        emotions_distribution = self.sa.polarity_scores(text)

        return emotions_distribution
