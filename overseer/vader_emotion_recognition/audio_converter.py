from typing import Optional

import speech_recognition as sr
import logging

log = logging.getLogger(__name__)


class AudioToTextConverter:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 1

    def convert_audio_to_text(self, data: str) -> Optional[str]:
        log.info('Converting audio to text')
        with sr.AudioFile(data) as source:
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                log.error("The speech is unintelligible")
            except sr.RequestError:
                log.error(
                    "Speech recognition operation failed. The key isn't valid, or there is no internet connection")

        return None
