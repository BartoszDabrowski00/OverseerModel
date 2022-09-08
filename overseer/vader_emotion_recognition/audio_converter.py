from typing import Optional

import speech_recognition as sr
import logging

log = logging.getLogger(__name__)


class AudioToTextConverter:

    def convert_audio_to_text(self, data: str) -> Optional[str]:
        log.info('Converting audio to text')
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 1
        with sr.AudioFile(data) as source:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                log.error("The speech is unintelligible")
            except sr.RequestError:
                log.error(
                    "Speech recognition operation failed. The key isn't valid, or there is no internet connection")

        return None
