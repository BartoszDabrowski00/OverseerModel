import os
import logging
from emotoins_printer import print_all_emotions_distribution
from overseer.vader_emotion_recognition.vader_classifier import VaderClassifier

TEST_RECORDINGS = os.environ.get('TEST_RECORDINGS', '../../recordings')
log = logging.getLogger(__name__)


def test(path: str) -> None:
    if not os.path.exists(path):
        log.error('Given directory deos not exist.')

    vader_classifier = VaderClassifier()
    file_paths = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for file in file_paths:
        emotions_distribution = vader_classifier.get_emotions_distribution(file)
        print_all_emotions_distribution(file, emotions_distribution)


if __name__ == '__main__':
    test(TEST_RECORDINGS)
