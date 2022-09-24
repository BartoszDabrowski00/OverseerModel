import logging

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from overseer.vader_emotion_recognition.audio_converter import AudioToTextConverter

log = logging.getLogger(__name__)


class TextNotConvertedException(Exception):
    pass


class VaderClassifier:

    def __init__(self):
        self.sa = SentimentIntensityAnalyzer()
        self.audio_converter = AudioToTextConverter()
        log.info('Initialized vader classifier')

    def get_emotions_distribution(self, audio):
        try:
            text = self.audio_converter.convert_audio_to_text(audio)
            if text is None:
                raise TextNotConvertedException()
        except Exception as e:
            raise TextNotConvertedException(e)

        emotions_distribution = self.sa.polarity_scores(text)
        log.info('Successfully extracted emotions from audio')

        return emotions_distribution
